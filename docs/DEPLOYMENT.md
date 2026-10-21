# Deployment

How the honeypot sensors were deployed, how they are secured, and how their logs reach the analysis stack.

The deployment separates **data collection** from **data analysis**. Only the honeypots and the orchestrator run in the cloud, which minimizes the exposed attack surface and the cloud resources required. The analysis stack (Logstash, Elasticsearch, Kibana, backend, ML service, and dashboard) runs in the project's local environment.

---

## 1. Phase 1: local deployment with ngrok

### Objective

The honeypots were first deployed as Docker containers on a development machine behind a private network. This phase exposed them to external networks without router configuration or a public IP address, in order to validate the full data path (honeypot, Logstash, Elasticsearch, dashboard) with traffic that originates outside the local network.

### Setup

ngrok was selected because it creates outbound tunnels from the local machine to ngrok's edge servers, which relay inbound connections to local ports. It supports both TCP and HTTP, which is required because the system covers SSH, FTP, and HTTP. One endpoint was mapped to each honeypot service port, and all endpoints were started as one session.

| Honeypot | Protocol | Local port | Endpoint type |
|---|---|---|---|
| Cowrie | SSH | 22 | TCP |
| Dionaea | FTP | 21 | TCP |
| Tanner + Snare | HTTP | 80 | HTTPS |

### Test method

Connectivity was tested from a network outside the LAN: repeated authentication attempts against Cowrie, login attempts against Dionaea, and requests to the public HTTPS address served by Snare and Tanner. For each service the data path was verified at successive stages: the honeypot's own log, the directory monitored by Logstash, the Elasticsearch index, and Kibana.

### Result and limitation

The three tunnels worked and externally generated events were indexed. However, events showed `source_ip = 172.19.0.1`, `country = Local`, and `ip_reputation = private`. That address is the gateway of the Docker bridge network, not the client: the connection is relayed by the ngrok agent and then address-translated by Docker. For raw TCP tunnels (SSH and FTP) the real address is not available at all, so geographic and reputation enrichment could not be applied. Together with the dependency on a personal machine, this motivated the move to the cloud.

## 2. Phase 2: cloud deployment on Azure

### Virtual machine

| Item | Value |
|---|---|
| Provider and region | Microsoft Azure, East US (availability zone 1) |
| Deployed | 29 September 2026, in a dedicated resource group |
| Size | Standard_D2as_v7 (2 vCPU, 8 GiB RAM) |
| Operating system | Ubuntu Server 24.04 LTS (x64, Generation 2) |
| OS disk | Premium SSD (locally redundant), default size; no data disks |
| Security type | Trusted launch (Secure Boot and vTPM enabled) |
| Authentication | SSH public key (no password login) |
| Network | Dedicated virtual network and subnet, one public IP address |
| Software | Docker and Docker Compose |

Containers on the VM: Cowrie (SSH), Dionaea (FTP), Snare and Tanner (HTTP) with Tanner's supporting services (API, Redis, and PHP sandbox), and the orchestrator.

### Network configuration

The honeypots listen on their native ports with no tunneling layer. Because Cowrie uses port 22, the VM's own administrative SSH service was moved to port 2222, which separates management access from attacker-facing services.

| Priority | Rule | Port | Protocol | Source | Action |
|---|---|---|---|---|---|
| 299 | Administration (SSH) | 2222 | TCP | Administrator IP only | Allow |
| 309 | Dionaea (FTP) | 21 | TCP | Any | Allow |
| 319 | Cowrie (SSH) | 22 | TCP | Any | Allow |
| 329 | Tanner and Snare (HTTP) | 80 | TCP | Any | Allow |
| 65500 | Default | Any | Any | Any | Deny |

Only the three honeypot ports are open to the Internet, and the default rule denies everything else. Azure warns about the exposure of port 22. This is intentional, because that port is served by the Cowrie honeypot and not by the real SSH daemon. Elasticsearch, Kibana, the backend, and the ML service are not deployed on the VM, so they are not reachable from the Internet at all. This matters because Elasticsearch runs with security disabled for development.

### Log transport

A script on the local machine streams the honeypot logs from the VM in near real time:

- For each log file (Cowrie, Dionaea, and Tanner) it opens an SSH connection, authenticated with a key on the management port, and follows the remote file with `tail -F`, appending the output to the local directory monitored by Logstash.
- It resumes from the byte offset already received, and restarts from the beginning if the remote file was truncated or rotated.
- It reconnects automatically five seconds after a connection loss.
- Credentials and host details are supplied through environment variables, never stored in source files.

The logs are then processed by the ELK pipeline (see [`elk/README.md`](../elk/README.md)).

### Orchestrator on the VM

The orchestrator runs on the VM inside a dedicated Python virtual environment, next to the containers it manages. Its status API listens only on the loopback interface (`127.0.0.1:8000`). The backend reaches it through an SSH tunnel that forwards a local port to that loopback port, so no additional port is opened to the Internet:

```bash
ssh -i <key> -p 2222 -N -L 8000:127.0.0.1:8000 <user>@<vm-address>
```
The backend then uses ORCHESTRATOR_URL=http://host.docker.internal:8002 (Docker Compose setup) or http://127.0.0.1:8002 (backend run directly on the host).

## 3. Comparison of the two phases

| | ngrok phase | Cloud phase |
|---|---|---|
| `source_ip` | Docker bridge address (172.19.0.1) | Attacker's public address |
| `country` and `asn` | Local and empty | Real country, populated |
| `ip_reputation` | private / empty | high, medium, low, clean, unlisted |
| Availability | Personal machine, active session only | Continuous |
| Exposure of the development host | Direct | None |

## 4. Operating checklist

1. Move the VM's own SSH service to port 2222 and confirm the new login works before starting Cowrie.
2. Apply the network rules above, with port 2222 restricted to the administrator's address.
3. Start the honeypots: `docker compose up -d` in `honeypots/docker`.
4. Start the orchestrator and its status API.
5. Start the log transport script on the local machine.
6. Confirm the data path: `curl http://localhost:9200/honeypot-events/_count` increases.
