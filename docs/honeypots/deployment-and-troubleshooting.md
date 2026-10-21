
# Honeypot Deployment & Technical Setup

## Overview

This document provides detailed deployment specifications, actual runtime states, and technical troubleshooting notes for the baseline honeypot environment used in the **Smart Honeypot Orchestrator & Threat Intelligence Dashboard** project.

The baseline environment comprises three core honeypot architectures:

| Honeypot Framework | Target Protocol | Deployment Purpose | Container Port |
| :--- | :--- | :--- | :--- |
| **Cowrie** | SSH (TCP/22) | Captures SSH brute-force attempts, interactive shell commands, and malware downloads. | `22/tcp` |
| **Dionaea** | FTP (TCP/21) | Captures legacy network exploit traffic, malware payloads, and FTP authentication attempts. | `21/tcp` |
| **SNARE + TANNER** | HTTP (TCP/80) | Captures web-based attack vectors, suspicious application requests, and payload execution attempts. | `80/tcp` |

---

## Deployment Architecture

The entire honeypot ecosystem is orchestrated using multi-file **Docker Compose** setups for modular control and simple execution.

```text
docker/
├── docker-compose.yml          <-- Master orchestration file
├── cowrie/
│   ├── docker-compose.yml
│   └── data/
├── dionaea/
│   ├── docker-compose.yml
│   └── data/
└── tanner/
    ├── docker-compose.yml
    ├── snare/
    ├── tanner/
    ├── redis/
    └── phpox/

```

### Master Docker Compose Configuration

```yaml
include:
  - ./cowrie/docker-compose.yml
  - ./dionaea/docker-compose.yml
  - ./tanner/docker-compose.yml

```

---

## Deployment Execution & Runtime Status

### Execution Commands

Start all containers in detached mode:

```bash
docker compose up -d

```

Verify operational runtime status:

```bash
docker ps

```

### Verified Runtime Container Output

```text
CONTAINER ID   IMAGE                                     COMMAND                  STATUS          PORTS                NAMES
97f6d8f9ab35   dtagdevsec/snare:24.04.1                 "sh -c 'exec snare -…"   Up 18 minutes   0.0.0.0:80->80/tcp   snare
5150b1538ee2   dtagdevsec/tanner:24.04.1                "tanner"                 Up 18 minutes                        tanner
57c32ff908a2   ghcr.io/telekom-security/dionaea:24.04.1  "/opt/dionaea/sbin/d…"   Up 18 minutes   0.0.0.0:21->21/tcp   dionaea
d06f25a7c530   ghcr.io/telekom-security/cowrie:24.04.1   "/usr/local/bin/star…"   Up 18 minutes   0.0.0.0:22->22/tcp   cowrie
18f35d9b933b   dtagdevsec/tanner:24.04.1                "tannerapi"              Up 18 minutes                        tanner_api
820ae8bb8ea1   dtagdevsec/redis:24.04.1                 "redis-server /etc/r…"   Up 18 minutes                        tanner_redis
e919bfd0486b   dtagdevsec/phpox:24.04.1                 "python3 sandbox.py"     Up 18 minutes                        tanner_phpox

```

---

## Verification & Interactive Testing

### 1. Cowrie (SSH Honeypot)

**Interaction Test:**

```bash
ssh root@localhost -p 22

```

**Simulated Attacker Verification:**

```bash
ls
pwd
whoami
uname -a
cat /etc/passwd

```

**Telemetry Verification:**

```bash
cat cowrie/data/log/cowrie.json

```

---

### 2. Dionaea (FTP Honeypot)

**Interaction Test:**

```bash
ftp localhost

```

**Simulated Attacker Credentials:**

```text
Username: admin
Password: admin

```

**Telemetry Verification:**

```bash
cat dionaea/data/log/dionaea.json

```

---

### 3. SNARE + TANNER (HTTP Honeypot)

**Interaction Test:**

```bash
curl -i http://localhost

```

*(Or navigate to `http://localhost` via web browser)*

**Telemetry Verification:**

```bash
cat tanner/data/tanner_report.json

```

---

## Centralized Log Telemetry Schema

Each deployed service outputs structured logs to feed downstream processing pipelines (ELK Stack / Threat Intelligence Dashboard). Extracted fields include:

* Attacker Source IP Address
* Target Service Port & Protocol
* Authentication Credentials (User/Pass)
* Interactive Attacker Execution Commands
* HTTP Request Headers & Payloads
* Binary Payload Submissions

---

## Technical Troubleshooting & System Challenges

### 1. Multi-Component Honeypot Modularization

* **Challenge:** Deploying and managing multiple heterogeneous honeypot frameworks concurrently created high complexity within a single Docker compose context.
* **Solution:** Modularized configurations into sub-directories while using a top-level `include:` directive in the master `docker-compose.yml`. This allows both individual component debugging and unified system orchestration.

---

### 2. Scope Refinement & Resource Optimization

* **Challenge:** Standard multi-honeypot suites often deploy redundant protocols outside the scope of SSH, HTTP, and FTP threat models, consuming system resources.
* **Solution:** Stripped unnecessary services and retained only Cowrie, Dionaea, SNARE, and TANNER components. This decreased memory usage and simplified container logging pipelines.

---

### 3. Build & Configuration Cleanup

* **Challenge:** Default community honeypot configurations contained unnecessary build artifacts, unused scripts, and redundant directories.
* **Solution:** Cleaned deployment trees to only store required runtime configurations, Docker Compose definitions, and persistence volume mounts.

---

## Final Operational Architecture

```text
               [ Attacker Traffic ]
                        |
        +---------------+---------------+
        |               |               |
     Port 22         Port 21         Port 80
        |               |               |
        v               v               v
  +-----------+   +-----------+   +-----------+
  |  Cowrie   |   |  Dionaea  |   |   SNARE   |
  |  (SSH)    |   |  (FTP)    |   |   (HTTP)  |
  +-----+-----+   +-----+-----+   +-----+-----+
        |               |               |
        |               |               v
        |               |         +-----------+
        |               |         |  TANNER   |
        |               |         | (Analysis)|
        |               |         +-----+-----+
        +---------------+---------------+
                        |
                        v
          [ Telemetry JSON Logs ]
