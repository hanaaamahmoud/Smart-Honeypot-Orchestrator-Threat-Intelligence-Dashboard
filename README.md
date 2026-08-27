# Smart Honeypot Orchestrator & Threat Intelligence Dashboard

A proactive security platform designed to automatically deploy containerized honeypots, collect attack telemetry, and analyze threat behavior in real time.


## Overview

Traditional defense mechanisms often detect threats only after they breach production environments. This project deploys isolated decoy services including SSH, HTTP, and FTP to safely capture early stage attacker interactions, enrich log data with context, and display actionable threat insights on a real-time monitoring dashboard.


## Key Capabilities

* **Automated Orchestration:** Deploys Cowrie (SSH), Dionaea (FTP), and SNARE/TANNER (HTTP) container environments using Docker Compose.
* **Real-Time Telemetry Capture:** Records authentication attempts, executed terminal commands, and web application attack payloads.
* **Log Enrichment:** Parses raw telemetry logs and enriches events with GeoIP context.
* **Behavioral Analytics:** Analyzes session patterns to group similar attack vectors for threat intelligence processing.
* **Live Dashboard Visualization:** Streams real-time event updates, top attacking IP addresses, targeted protocols, and interactive threat maps via WebSockets.

## Quick Start

### Prerequisites
* Docker (v20.10+)
* Docker Compose (v2.0+)

### Deployment Steps

1. Clone the repository:
   ```bash
   git clone [https://github.com/hanaaasmahmoud/Smart-Honeypot-Orchestrator-Threat-Intelligence-Dashboard.git](https://github.com/hanaaasmahmoud/Smart-Honeypot-Orchestrator-Threat-Intelligence-Dashboard.git)
   cd Smart-Honeypot-Orchestrator-Threat-Intelligence-Dashboard
