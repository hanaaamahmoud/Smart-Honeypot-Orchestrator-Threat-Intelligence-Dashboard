 # Project Documentation & Literature Review

# Related Work

## 1. Cowrie

Cowrie is one of the most widely adopted medium-interaction honeypots
for SSH and Telnet environments. It emulates a Linux shell and file
system to provide attackers with a realistic interaction while
preventing access to a real operating system. Instead of simply
recording connection attempts, Cowrie captures complete attack sessions
including login attempts, executed commands, uploaded and downloaded
files, and session timelines. Because of its rich behavioral logging,
Cowrie is frequently used in academic research and operational security
environments to study attacker tactics, credential stuffing, brute-force
attacks, and malware delivery.

Cowrie serves as an excellent data source for behavioral analysis;
however, it focuses primarily on a single service (SSH/Telnet). Although
it produces detailed logs, analysts still need external platforms to
aggregate, correlate, and visualize attacks.

------------------------------------------------------------------------

## 2. Dionaea

Dionaea is a multi-protocol medium-interaction honeypot designed to
capture malware and observe attacks targeting various network services.
It supports protocols such as FTP, HTTP, SMB, MySQL, SIP, MQTT, Redis,
MongoDB, and others. Instead of focusing on interactive shell sessions,
Dionaea emphasizes malware collection and protocol-level attack
monitoring. It records exploit attempts, downloads malicious payloads,
and stores valuable artifacts that can later be analyzed by security
analysts.

Its ability to emulate multiple vulnerable services makes Dionaea an
important component in distributed honeypot environments. Nevertheless,
the collected data generally requires additional analysis platforms for
visualization, correlation, and threat intelligence enrichment.

------------------------------------------------------------------------

## 3. T-Pot

T-Pot is one of the most popular open-source honeypot platforms for
deploying and managing multiple honeypots from a centralized
environment. Built around Docker containers, it integrates numerous low-
and medium-interaction honeypots into a unified platform while providing
centralized log collection through the Elastic Stack (ELK). Kibana
dashboards enable analysts to monitor attack trends, visualize
geographic distributions, and inspect captured events.

The primary contribution of T-Pot lies in orchestration and deployment
rather than advanced threat analysis. While it simplifies large-scale
honeypot management, most analysis remains log-centric, leaving deeper
behavioral investigation to external tools or manual analysis.

------------------------------------------------------------------------

## 4. OpenCanary

OpenCanary is a lightweight low-interaction honeypot developed to detect
unauthorized access attempts with minimal deployment complexity. It
emulates multiple common services, including SSH, FTP, HTTP, SMB, and
database services, and generates alerts whenever suspicious interactions
occur. Because of its low resource requirements, OpenCanary is
frequently deployed inside enterprise environments as an early-warning
detection mechanism.

Unlike medium-interaction honeypots, OpenCanary intentionally limits
attacker interaction. Consequently, it provides high-level indicators of
compromise rather than detailed behavioral information or complete
attack sessions.

------------------------------------------------------------------------

## 5. AI-Enhanced Honeypot Systems

Recent research has explored integrating Artificial Intelligence and
Large Language Models (LLMs) into honeypot ecosystems. These systems use
machine learning to classify attacker behavior, summarize commands,
identify malicious patterns, prioritize incidents, and assist analysts
in understanding complex attack sessions. Some modern platforms combine
local LLMs with malware scanning engines and centralized dashboards to
automate triage and reduce analyst workload.

Despite these advances, AI-enhanced systems typically focus on
explanation and prioritization rather than standardized security
classification. Since LLMs generate probabilistic outputs, their
interpretations may vary across identical inputs. For this reason, many
operational security platforms continue to rely on deterministic
detection rules and frameworks such as MITRE ATT&CK for consistent
behavioral classification.

------------------------------------------------------------------------

### 6. HiveSight

HiveSight is a modern open-source platform that unifies traditional honeypot architectures with centralized orchestration, AI-assisted analysis, malware inspection, and real-time visualization. It combines **Cowrie** (for SSH/Telnet) and **Dionaea** (for multi-protocol traffic) within a modular Docker-based environment. 

* **Orchestration & AI Triage:** A dedicated orchestration layer tails honeypot logs in real time, forwarding captured attacker commands to a local LLM via **Ollama** for automated behavior categorization and triage.
* **Malware & Log Pipeline:** Captured binaries are automatically scanned using **ClamAV**, while logs are shipped via **Promtail** to **Loki** and visualized in **Grafana** with automated GeoIP enrichment.



### Our Proposed System

The proposed Smart Honeypot Orchestrator & Threat Intelligence Dashboard bridges the gap between traditional honeypot data collection and practical security investigation. While existing platforms primarily emphasize deployment, centralized monitoring, or isolated AI summaries, our system focuses on transforming heterogeneous honeypot events into structured, actionable threat intelligence.

The platform integrates three medium-interaction honeypots covering SSH, HTTP, and FTP services within a centralized orchestration framework. Instead of analyzing each honeypot independently, the orchestrator continuously collects attack events, normalizes formats, and feeds them into a unified dashboard.

#### Key Contributions & Features
* **Automated MITRE ATT&CK Mapping:** Automatically associates attacker behaviors with standardized adversarial tactics and techniques, providing consistent, explainable behavioral classification that aligns with real-world Security Operations Center (SOC) workflows.
* **Interactive Session Replay Module:** Reconstructs attacker sessions chronologically instead of presenting isolated log entries, allowing analysts to review every command, file upload, payload download, and interaction precisely as it occurred.
* **Unified Multi-Service Visibility:** Consolidates logs from multiple entry points (SSH, HTTP, FTP) into a single investigation interface to eliminate blind spots.
* **Extensible Architecture:** Supports seamless future integration with malware analysis engines, threat intelligence feeds, behavioral clustering, and AI-assisted reporting while maintaining full compatibility with core honeypot technologies.



## Project Summary Table
| Platform | Honeypot Type | Multi-Honeypot Support | Centralized Orchestration | Dashboard | Threat Intelligence | AI / LLM | Malware Analysis | MITRE ATT&CK Mapping | Interactive Session Replay |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Cowrie** | Medium (SSH/Telnet) | ✗ | ✗ | Basic Log Viewer | ✗ | ✗ | File Capture | ✗ | Partial |
| **Dionaea** | Medium (Multi-Protocol) | ✗ | ✗ | Basic Logs | ✗ | ✗ | ✓ | ✗ | ✗ |
| **T-Pot** | Multiple Honeypots | ✓ | ✓ | ELK / Kibana | Partial | ✗ | Partial | ✗ | ✗ |
| **OpenCanary** | Low Interaction | ✗ | ✗ | Alert-Based | ✗ | ✗ | ✗ | ✗ | ✗ |
| **HiveSight** | Medium (Cowrie + Dionaea) | ✓ | ✓ | Grafana + Loki | GeoIP Enrichment | ✓ (Ollama) | ✓ (ClamAV) | ✗ | ✗ |
| **Our Proposed System** | Medium (SSH + HTTP + FTP) | ✓ | ✓ | Threat Intelligence Dashboard | ✓ | Optional | Optional | ✓ | ✓ |


## Research Sources & References

1. **[10963363]** Advanced Cyber-Physical Threat Intelligence and Deception Networks Framework. *IEEE Xplore*, DOI: [10.1109/ACCESS.2025.10963363](https://ieeexplore.ieee.org/document/10963363). Focuses on automated orchestration and machine learning integration within decentralized deceptive architectures.
2. **[11381043]** Behavioral Profiling of AI-Driven Agents and Automated Botnets in Containerized Honeypots. *IEEE Transactions on Information Forensics and Security*, DOI: [10.1109/TIFS.2026.11381043](https://ieeexplore.ieee.org/document/11381043). Explores high-dimensional behavioral feature extraction for session classification.
3. **[10859786]** Muhammad Naufal Azzahri et al., "The Application of Cowrie Honeypot to Analyze Attacks on SSH and Telnet Protocols," *2024 IEEE 2nd International Conference on Electrical Engineering, Computer and Information Technology (ICEECIT)*, DOI: [10.1109/iceecit63698.2024.10859786](https://ieeexplore.ieee.org/document/10859786).
4. **[10933436]** SIEM and SOAR Integration Architectures for Real-Time Threat Mitigation. *IEEE International Conference on Futuristic Technologies*, DOI: [10.1109/INCOFT.2023.10933436](https://ieeexplore.ieee.org/document/10933436/).
5. **[11519048]** Cloud-Native Microservices and Dynamic Orchestration for Enterprise Deception Systems. *IEEE Transactions on Services Computing*, DOI: [10.1109/TSC.2026.11519048](https://ieeexplore.ieee.org/document/11519048).
6. **[8888409]** Sethia, V. et al., "Malware capturing and analysis via modern honeynet frameworks," *Proceedings of the IEEE International Conference*, DOI: [10.1109/ICIM.2019.8888409](https://ieeexplore.ieee.org/document/8888409).
