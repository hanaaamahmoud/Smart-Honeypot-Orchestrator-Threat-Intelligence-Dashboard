
# SNARE & Tanner Honeypot Evaluation

## Overview

As part of the Smart Honeypot Orchestrator & Threat Intelligence Dashboard project, SNARE and Tanner were evaluated as low-interaction HTTP honeypot solutions. The primary objective was to assess their deployment workflows, interaction capabilities, logging behavior, and overall suitability for capturing adversary activities.

The goal of this evaluation extends beyond deploying a deceptive web service to analyzing the depth of telemetry collected from attacker interactions and how these logs will feed into downstream threat intelligence and machine learning pipelines.

---

## SNARE Overview

SNARE (Surface Nasty Attack Receptor) is a web application honeypot designed to emulate web services by cloning existing targets or serving predefined templates. It intercepts incoming HTTP requests and records detailed visitor telemetry.

Testing Scenario:  
A fake banking login page was deployed to simulate real-world attack vectors. This setup enabled testing and capturing common adversary behaviors:

* **Reconnaissance:** Browsing specific endpoints and crawling site structure.
* **Credential Harvesting:** Submitting forms and authentication payloads.
* **HTTP Request Manipulation:** Sending crafted headers and non-standard HTTP methods.

SNARE successfully captured all simulated interaction sequences and stored them in its log files.

---

## Deployment Architecture

SNARE and Tanner were containerized and deployed using Docker for environment isolation and rapid orchestration.

### Architectural Layout

```text
               +-----------------------+
               |   Attacker / Visitor  |
               +-----------+-----------+
                           |
                     HTTP (Port 80)
                           |
                           v
+-----------------------------------------------------+
|                  Docker Host                        |
|                                                     |
|  +-----------------------------------------------+  |
|  |           SNARE Honeypot Container            |  |
|  |             (Frontend Emulator)               |  |
|  +-----------------------+-----------------------+  |
|                          |                          |
|                    Internal API                     |
|                          v                          |
|  +-----------------------------------------------+  |
|  |           Tanner Analysis Engine              |  |
|  |  +-----------------+   +-------------------+  |  |
|  |  | API (Port 8090) |   | WebUI (Port 8091) |  |  |
|  |  +-----------------+   +-------------------+  |  |
|  +-----------------------+-----------------------+  |
|                          |                          |
|                          v                          |
|            Logs & Structured JSON Reports           |
+-----------------------------------------------------+

```

### Port Exposure & Services

| Component | Port / Service | Description |
| --- | --- | --- |
| **SNARE** | Port 80 (HTTP) | Publicly exposed web trap serving fake application pages |
| **Tanner API** | Port 8090 | Internal communications backend between SNARE and Tanner |
| **Tanner Web UI** | Port 8091 | Management and visualization interface for Tanner analysis |

---

## Testing Scenario

A fake banking portal login interface was served to evaluate the honeypot's response to unauthorized access attempts.

### Execution Workflow

1. Establish HTTP connection to the honeypot.
2. Navigate to the login route (`/doLogin`).
3. Inject simulated adversary credentials:
```yaml
Username: admin
Password: 123456

```


4. Transmit POST payload via form submission.
5. Extract and analyze generated logs across SNARE and Tanner containers.

---

## Telemetry & Logging Capabilities

### 1. SNARE Logs

SNARE writes raw HTTP interaction telemetry to:
`/opt/snare/snare.log`

Key attributes captured include requested URI paths, HTTP verbs, source IP addresses, User-Agent strings, and raw POST form parameters.

#### Captured Payload Sample

```http
Request path: /doLogin
POST data:
  uid: admin
  passw: 123456
  btnSubmit: Login

```

---

### 2. Tanner Engine & Analysis Output

While SNARE handles frontend communication, Tanner operates as the cognitive intelligence engine. It evaluates incoming events, detects signatures, manages sessions, and produces structured analytical outputs.

Structured reports are stored at:
`/tmp/tanner/tanner_report.json`

#### Report JSON Snippet

```json
{
  "method": "GET",
  "path": "/",
  "status": 200,
  "peer": {
    "ip": "172.19.0.1"
  }
}

```

---

## Interaction Level Classification

SNARE and Tanner function strictly as low-interaction honeypots. They mimic web services to observe baseline adversary behavior without hosting actual backend databases or vulnerable operating systems.

| Observed Capabilities | Non-Supported Actions |
| --- | --- |
| Endpoint enumeration & URL crawling | Native OS command execution |
| Login form submissions & credential sniffing | Interactive shell access |
| HTTP request header profiling | Active malware detonation environments |
| Session tracking & basic signature analysis | Post-exploitation lateral movement observation |

---

## Identified Technical Limitations

1. **Static Workflows:** The system logs credential submissions but cannot emulate full authentication state transitions (e.g., redirecting to a fake post-login dashboard).
2. **Asset Dependencies:** Realistic emulation requires complete HTML, CSS, JavaScript, and image assets. Missing static resources yield standard 404 status codes, signaling artificiality to sophisticated scanners.
3. **Shallow Post-Exploitation Scope:** Adversary actions beyond the initial HTTP transport layer cannot be tracked due to the absence of underlying OS primitives.

---

## Strategic Evaluation & Integration

SNARE and Tanner demonstrate strong capabilities for capturing web-layer reconnaissance and credential brute-force telemetry.

For the Smart Honeypot Orchestrator framework:

* **SNARE & Tanner** will serve as the dedicated HTTP/S Deception Layer.
* Complementary honeypots (such as **Cowrie** for SSH/Telnet and **Dionaea** for network protocol exploits) will be paired alongside them to achieve deep visibility into malware propagation and terminal command execution.

```

```
