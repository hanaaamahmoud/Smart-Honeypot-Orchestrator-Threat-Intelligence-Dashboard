
# Project Documentation & Literature Review

## Related Work & Literature Review

This chapter reviews existing honeypot frameworks, threat intelligence platforms, and related technologies that informed the design of the Smart Honeypot Orchestrator & Threat Intelligence Dashboard. Each section examines representative approaches, discussing their purpose, architecture, strengths, limitations, dataset characteristics, and relationship to our project.

---

## 1. Single-Protocol & Multi-Protocol Honeypots

### 1.1 Cowrie
Cowrie is one of the most widely adopted medium-interaction honeypots for SSH and Telnet environments. It emulates a Linux shell and file system to provide attackers with a realistic interaction while preventing access to a real operating system. Instead of simply recording connection attempts, Cowrie captures complete attack sessions including login attempts, executed commands, uploaded and downloaded files, and session timelines. Because of its rich behavioral logging, Cowrie is frequently used in academic research and operational security environments to study attacker tactics, credential stuffing, brute-force attacks, and malware delivery.

* **Strengths:** Detailed behavioral logging, full session capture, and interactive command-line emulation.
* **Limitations:** Focuses primarily on a single service pair (SSH/Telnet). Although it produces detailed logs, analysts still need external platforms to aggregate, correlate, and visualize attacks.
* **Dataset:** Generates structured JSON logs locally. No standardized public dataset exists; researchers generate live datasets via active deployments.

### 1.2 Dionaea
Dionaea is a multi-protocol medium-interaction honeypot designed to capture malware and observe attacks targeting various network services. It supports protocols such as FTP, HTTP, SMB, MySQL, SIP, MQTT, Redis, MongoDB, and others. Instead of focusing on interactive shell sessions, Dionaea emphasizes malware collection and protocol-level attack monitoring. It records exploit attempts, downloads malicious payloads, and stores valuable artifacts that can later be analyzed by security analysts.

* **Strengths:** Multi-protocol support, automated payload/malware capture, and low-level protocol emulation.
* **Limitations:** Lacks built-in advanced analytics or interactive shell session reconstruction; collected data requires external platforms for visualization and threat intelligence enrichment.
* **Dataset:** Live payload and exploit capture logs generated during active execution.

### 1.3 OpenCanary
OpenCanary is a lightweight low-interaction honeypot developed to detect unauthorized access attempts with minimal deployment complexity. It emulates multiple common services, including SSH, FTP, HTTP, SMB, and database services, and generates alerts whenever suspicious interactions occur. Because of its low resource requirements, OpenCanary is frequently deployed inside enterprise environments as an early-warning detection mechanism.

* **Strengths:** Minimal resource footprint, quick deployment, and instant alerting.
* **Limitations:** Intentionally limits attacker interaction; provides high-level indicators of compromise rather than detailed behavioral information or complete attack sessions.
* **Dataset:** Alert-driven event logs without deep payload captures.

---

## 2. Integrated Platforms & Orchestration Frameworks

### 2.1 T-Pot: Comprehensive Multi-Honeypot Platform
T-Pot, developed by Telekom Security in collaboration with The Honeynet Project, is an all-in-one honeypot platform that bundles more than twenty individual honeypot implementations into a single Debian-based system. Each honeypot runs within its own Docker container, providing isolation and simplified management. The platform normalizes events through Logstash, stores them in Elasticsearch, and visualizes data using pre-built Kibana dashboards.

* **Strengths:** Broad protocol coverage, containerized isolation, pre-built dashboards, and an active open-source community.
* **Limitations:** High hardware resource consumption (8–16 GB RAM requirement), rigid architecture making custom analytics difficult to insert, and lack of automated pattern correlation or machine learning integration.
* **Dataset:** Live events generated locally within its Elasticsearch engine.

### 2.2 Modern Honey Network (MHN)
The Modern Honey Network (MHN) is a centralized server framework for deploying and managing distributed honeypot sensors. An administrator selects honeypot types from a web interface and executes one-line installation scripts on target systems. Sensors transmit events via HPFeeds to a central server storing data in MongoDB, with map visualization provided by Honeymap.

* **Strengths:** Highly scalable sensor deployment and centralized geographic visualization.
* **Limitations:** Outdated codebase relying on legacy packages (Python 2), lack of active maintenance, and absence of an analytical or correlation layer.
* **Dataset:** Decentralized telemetry generated dynamically per deployed sensor network.

---

## 3. Advanced & AI-Enhanced Honeypot Systems

### 3.1 AI-Driven Triage Systems & HiveSight
Recent research explores integrating Artificial Intelligence and Large Language Models (LLMs) into honeypot ecosystems to classify attacker behavior, summarize commands, and prioritize incidents. A notable modern implementation is **HiveSight**, an open-source platform combining Cowrie and Dionaea in a Docker environment:

* **Orchestration & AI Triage:** Tails logs in real time and streams commands to a local LLM via Ollama for automated behavior categorization.
* **Malware & Pipeline:** Scans captured binaries automatically via ClamAV, ships logs via Promtail to Loki, and visualizes data in Grafana with GeoIP enrichment.
* **Limitations:** LLM-based triage introduces non-deterministic outputs where interpretations vary across identical inputs, lacking alignment with standardized classification frameworks like MITRE ATT&CK.

### 3.2 HoneyDB: Community-Driven Aggregation
HoneyDB is a hosted threat intelligence platform built around a lightweight agent that contributes captured activity to a central cloud service. It exposes bad hosts, targeted services, and payload histories via REST APIs and features a natural language chat interface (HoneyDB AI).

* **Strengths:** Crowd-sourced global visibility and low local infrastructure requirements.
* **Limitations:** Third-party dependency, lack of local pipeline control, and limited self-hosted analytics.

### 3.3 Awesome Honeypots Directory
Awesome Honeypots is a community-maintained repository indexing honeypot software and related security tools by category. It serves as an essential reference for tool discovery during preliminary architecture research.

---

## 4. Synthesis & Our Proposed System

Existing solutions represent distinct trade-offs: T-Pot offers broad coverage but remains resource-heavy and log-centric; MHN scales well but relies on unmaintained software; AI-only platforms offer summarization but lack deterministic, standardized security frameworks.

The **Smart Honeypot Orchestrator & Threat Intelligence Dashboard** addresses these gaps. It combines low- and medium-interaction honeypots (SSH, HTTP, FTP) within a lightweight, modular Python orchestration framework. Collected logs are normalized, enriched, and processed through unsupervised machine learning clustering alongside deterministic mapping models.

```text
+-----------------------------------------------------------------------------------+
|                            Proposed System Architecture                           |
+-----------------------------------------------------------------------------------+
|  [ SSH Honeypot ]       [ HTTP Honeypot (SNARE) ]       [ FTP Honeypot ]          |
+-----------------------------------------------------------------------------------+
                                          |
                                   (Event Stream)
                                          v
+-----------------------------------------------------------------------------------+
|                         Centralized Python Orchestrator                           |
|      (Format Normalization, Unsupervised ML Clustering & MITRE Mapping)           |
+-----------------------------------------------------------------------------------+
                                          |
                                          v
+-----------------------------------------------------------------------------------+
|                       Unified Threat Intelligence Dashboard                       |
|          (Interactive Session Replay, Pattern Analytics & Incident Triage)         |
+-----------------------------------------------------------------------------------+

```

### Key Contributions & Features

* **Automated MITRE ATT&CK Mapping:** Associates attacker behaviors with standardized adversarial tactics and techniques for explainable, SOC-aligned classification.
* **Interactive Session Replay Module:** Reconstructs attacker sessions chronologically, allowing analysts to review command sequences, file uploads, and payload transmissions exactly as they occurred.
* **Unified Multi-Service Visibility:** Consolidates logs from multiple entry points into a single custom dashboard (Vue.js frontend with Elasticsearch backend).
* **Resource-Efficient ML Integration:** Applies unsupervised machine learning clustering to group attack patterns automatically without requiring heavy infrastructure.

---

## 5. Comparative Evaluation

| Platform | Honeypot Type | Centralized Orchestration | Threat Intelligence | AI / LLM Support | Malware Analysis | MITRE ATT&CK Mapping | Interactive Session Replay | Resource Footprint |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **Cowrie** | Medium (SSH/Telnet) | No | No | No | File Capture | No | Partial | Low |
| **Dionaea** | Medium (Multi-Protocol) | No | No | No | Payload Capture | No | No | Low |
| **OpenCanary** | Low Interaction | No | No | No | No | No | No | Very Low |
| **T-Pot** | Multi-Honeypot Suite | Yes | Partial | No | Partial | No | No | High (8–16 GB) |
| **MHN** | Sensor Management | Yes | Basic Map | No | No | No | No | Medium |
| **HoneyDB** | Cloud Aggregated Feed | Centralized Feed | Global Feed | Chat Interface | Payload History | No | No | Minimal (Agent) |
| **HiveSight** | Medium (Cowrie/Dionaea) | Yes | GeoIP | Local (Ollama) | ClamAV | No | No | Medium |
| **Proposed System** | **Medium (SSH/HTTP/FTP)** | **Yes** | **Advanced** | **ML Clustering** | **Extensible** | **Yes** | **Yes** | **Low–Medium** |

---

## 6. References

1. **[10963363]** Advanced Cyber-Physical Threat Intelligence and Deception Networks Framework. *IEEE Xplore*, DOI: [10.1109/ACCESS.2025.10963363](https://ieeexplore.ieee.org/document/10963363).
2. **[11381043]** Behavioral Profiling of AI-Driven Agents and Automated Botnets in Containerized Honeypots. *IEEE Transactions on Information Forensics and Security*, DOI: [10.1109/TIFS.2026.11381043](https://ieeexplore.ieee.org/document/11381043).
3. **[10859786]** M. N. Azzahri et al., "The Application of Cowrie Honeypot to Analyze Attacks on SSH and Telnet Protocols," *2024 IEEE 2nd International Conference on Electrical Engineering, Computer and Information Technology (ICEECIT)*, DOI: [10.1109/iceecit63698.2024.10859786](https://ieeexplore.ieee.org/document/10859786).
4. **[10933436]** SIEM and SOAR Integration Architectures for Real-Time Threat Mitigation. *IEEE International Conference on Futuristic Technologies*, DOI: [10.1109/INCOFT.2023.10933436](https://ieeexplore.ieee.org/document/10933436/).
5. **[11519048]** Cloud-Native Microservices and Dynamic Orchestration for Enterprise Deception Systems. *IEEE Transactions on Services Computing*, DOI: [10.1109/TSC.2026.11519048](https://ieeexplore.ieee.org/document/11519048).
6. **[8888409]** V. Sethia et al., "Malware capturing and analysis via modern honeynet frameworks," *Proceedings of the IEEE International Conference*, DOI: [10.1109/ICIM.2019.8888409](https://ieeexplore.ieee.org/document/8888409).

