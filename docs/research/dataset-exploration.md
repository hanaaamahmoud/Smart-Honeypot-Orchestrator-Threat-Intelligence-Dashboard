# Dataset Exploration Report

## Objective

The objective of this research is to evaluate publicly available cybersecurity datasets and identify the most suitable dataset(s) for the Smart Honeypot Orchestrator & Threat Intelligence Dashboard project. The evaluation focuses on attacker behavior analysis, network traffic analysis, GeoIP support, and machine learning suitability.

---

# Evaluation Criteria

Each dataset was evaluated based on the following criteria:

- What data it contains
- Available columns/features
- Suitability for machine learning
- Suitability for project objectives
- Advantages
- Limitations

---

# 1. AWS Honeypot Attack Data

## Overview

The AWS Honeypot Attack Data dataset contains real network traffic collected from AWS-hosted honeypot servers. It records network connection events together with geographical information derived from attackers' public IP addresses.

---

## What Data Does It Contain?

The dataset contains:

- Network traffic events
- Source IP addresses
- Network protocols (TCP/UDP)
- Source and destination ports
- Event timestamps
- Honeypot host information
- GeoIP information (Country, Region, Latitude, Longitude) derived from public source IP addresses

---

## Available Columns

| Column | Description |
|---------|-------------|
| etime | Event timestamp |
| host | Honeypot server |
| srcstr | Source IP address |
| proto | Network protocol |
| spt | Source port |
| dpt | Destination port |
| country | Source country |
| locale | Region |
| latitude | Latitude |
| longitude | Longitude |

---

## Suitable for Machine Learning?

**Partially.**

The dataset contains useful network-level features such as timestamps, protocols, ports, and geographic information. These features are suitable for clustering and traffic analysis. However, it lacks detailed attacker interaction information required for behavioral analysis.

---

## Suitable for Our Project?

**Yes (Supplementary Dataset).**

The dataset is valuable for enriching the project's threat intelligence capabilities by providing GeoIP information, attack origin statistics, and geographic visualization. It complements datasets that contain attacker behavior by supplying location-based intelligence derived from public source IP addresses.

**Project Role:** GeoIP enrichment and attack origin visualization.

---

## Advantages

- Real honeypot traffic
- Public source IP addresses
- Built-in GeoIP information
- Suitable for dashboard visualization
- Useful for traffic analysis
- Supports attack origin mapping

---

## Limitations

- No username information
- No password attempts
- No command execution logs
- No session-level attacker behavior

---

# 2. UNSW-NB15

## Overview

UNSW-NB15 is a labeled network intrusion detection dataset developed by the Australian Centre for Cyber Security (ACCS). It contains both normal and malicious network traffic and is widely used for cybersecurity machine learning research.

---

## What Data Does It Contain?

The dataset contains:

- Network flows
- Source and destination IP addresses
- Source and destination ports
- Network protocols
- Traffic statistics
- Attack categories
- Binary attack labels

---

## Available Features

Examples include:

- srcip
- dstip
- sport
- dsport
- proto
- service
- state
- attack_cat
- label

---

## Suitable for Machine Learning?

**Yes.**

The dataset contains rich labeled features that are widely used for machine learning tasks such as classification, clustering, anomaly detection, and network intrusion detection.

---

## Suitable for Our Project?

**Partially.**

The dataset is useful for training and evaluating machine learning models using labeled network traffic. However, it captures network flows rather than real attacker interactions with honeypot services, making it less suitable for threat intelligence and attacker behavior profiling.

**Project Role:** Supplementary dataset for machine learning model evaluation.

---

## Advantages

- Rich network features
- Labeled attack categories
- Widely used in cybersecurity research
- Excellent for supervised machine learning
- Suitable for intrusion detection research

---

## Limitations

- Not collected from honeypots
- No attacker commands
- No login attempts
- No session interaction details
- Limited attacker behavior information

---

# 3. MACCDC2012

## Overview

MACCDC2012 is a cybersecurity dataset published through **SecRepo**, a public repository of security datasets and network captures. The dataset was collected during the Mid-Atlantic Collegiate Cyber Defense Competition (MACCDC) 2012 and contains realistic network and application logs generated from multiple attack scenarios.

For this project, MACCDC2012 serves as the primary dataset for analyzing FTP and HTTP attacker behavior.

---

## About SecRepo

**SecRepo** is a public repository that provides cybersecurity datasets, packet captures (PCAPs), system logs, honeypot data, malware traces, and network security datasets collected from academic research and cybersecurity competitions.

MACCDC2012 was obtained through SecRepo and selected because it provides protocol-specific logs that closely match the project's requirements.

---

## What Data Does It Contain?

The dataset is organized into multiple protocol-specific log files. For this evaluation, the following logs were analyzed because they are the most relevant to the Smart Honeypot Orchestrator project:

- **SSH logs** – Connection timestamps, session identifiers, source and destination IP addresses, source and destination ports, SSH authentication results, connection direction, SSH client banners, and server banners.
- **FTP logs** – User authentication, FTP commands, file upload and download operations, and FTP server responses.
- **HTTP logs** – HTTP methods, requested URLs, HTTP response status codes, and User-Agent strings.

Together, these logs provide detailed protocol-specific activities, authentication events, network communication, and attacker behavior across multiple services.

---

## Available Features

Based on the analyzed SSH, FTP, and HTTP logs, the dataset includes:

- Timestamp
- Session ID
- Source IP address
- Destination IP address
- Source port
- Destination port
- Protocol
- SSH authentication results
- Connection direction
- SSH client and server banners
- FTP usernames
- FTP commands
- File upload and download operations
- FTP server responses
- HTTP methods
- Requested URLs
- HTTP response status codes
- User-Agent strings

---

## Suitable for Machine Learning?

**Yes.**

The dataset contains rich session-level and protocol-specific features that are suitable for unsupervised machine learning tasks such as behavior clustering, anomaly detection, and attacker behavior profiling. After preprocessing and feature engineering, these behavioral features can be used to group similar attacker activities.

---

## Suitable for Our Project?

**Yes**

The analyzed SSH, FTP, and HTTP logs closely match the project's objectives by providing attacker interaction data across multiple services. The dataset captures authentication events, FTP operations, HTTP requests, and network connection information, making it highly suitable for attacker behavior analysis and protocol-specific monitoring.

Although SSH logs are available, the project primarily relies on Cowrie Real Logs for SSH analysis because they contain real honeypot interactions and richer attacker behavior.

**Project Role:** Primary dataset for HTTP and FTP attacker behavior analysis.

---

## Advantages

- Multi-protocol attack data (SSH, FTP, HTTP)
- Rich attacker interaction logs
- SSH authentication events
- FTP protocol commands
- HTTP request details
- Network connection metadata
- Suitable for attacker behavior analysis
- Supports feature extraction for unsupervised learning
- Suitable for behavior clustering

---

## Limitations

- Large dataset requiring preprocessing
- Uses private IP addresses, preventing GeoIP enrichment
- Different log formats require normalization before analysis
- Raw log data requires feature engineering before machine learning
- Collected in a controlled competition environment
- Some services may not fully represent current Internet attack trends

---

Although MACCDC2012 provides rich protocol-specific logs for SSH, FTP, and HTTP analysis, it relies on private IP addresses, making GeoIP analysis impossible. Therefore, additional datasets containing public source IP addresses were evaluated to complement this limitation and provide geographic threat intelligence.

# 4. Cowrie Real Logs

## Overview

Cowrie is an open-source medium-interaction SSH and Telnet honeypot designed to emulate vulnerable systems and capture real attacker interactions. Unlike traditional network traffic datasets, Cowrie records complete attacker sessions, including authentication attempts, SSH client information, executed commands, and session metadata, making it one of the most valuable datasets for attacker behavior analysis.

---

## What Data Does It Contain?

The analyzed dataset contains structured JSON event logs generated during real attacker interactions with the honeypot.

The logs include:

- Connection events
- SSH client information
- SSH key exchange details
- HASSH fingerprints
- Authentication attempts
- Usernames and passwords
- Executed commands
- Session identifiers
- Session duration
- Source and destination IP addresses
- Source and destination ports
- Timestamps

---

## Event Types

The analyzed dataset contains the following event types:

| Event Type | Description |
|------------|-------------|
| `cowrie.session.connect` | New SSH/Telnet connection established |
| `cowrie.client.version` | SSH client version identified |
| `cowrie.client.kex` | SSH key exchange details and HASSH fingerprint |
| `cowrie.login.failed` | Failed authentication attempt |
| `cowrie.login.success` | Successful authentication |
| `cowrie.command.input` | Commands executed by the attacker |
| `cowrie.session.closed` | Session terminated with duration information |

These event types provide detailed visibility into attacker activity, from the initial connection and authentication attempts to successful logins, executed commands, and session termination.

---

## Available Features

The dataset includes:

- Timestamp
- Session ID
- Source IP address
- Destination IP address
- Source port
- Destination port
- Protocol
- SSH client version
- HASSH fingerprint
- Username
- Password
- Authentication results
- Executed commands
- Session duration
- Connection events

---

## Suitable for Machine Learning?

**Yes.**

The dataset contains rich session-level features that are highly suitable for unsupervised machine learning tasks such as attacker clustering, anomaly detection, behavior profiling, and command sequence analysis.

Behavioral features that can be extracted include:

- Connection frequency
- Failed authentication count
- Successful authentication count
- Session duration
- Time between sessions
- Username diversity
- Password diversity
- SSH client version
- HASSH fingerprint
- Executed command sequences
- Command frequency
- Source IP address

---

## Suitable for Our Project?

**Yes (Primary Dataset for SSH).**

Cowrie directly supports the SSH component of the Smart Honeypot Orchestrator project by capturing real attacker interactions rather than simulated network traffic. It records authentication attempts, SSH client fingerprints, executed commands, and complete session information, making it highly suitable for attacker behavior analysis and threat intelligence.

Since the dataset contains public source IP addresses, GeoIP enrichment can be applied to identify attacker locations and generate geographic threat intelligence.

**Project Role:** Primary dataset for SSH attacker behavior analysis and threat intelligence.

---

## Advantages

- Real attacker interactions
- Public source IP addresses
- Supports GeoIP enrichment
- Rich session-level information
- Authentication events
- Username and password attempts
- Executed attacker commands
- SSH client fingerprinting (HASSH)
- Suitable for attacker behavior analysis
- Excellent for unsupervised machine learning
- Closely aligned with the project's SSH honeypot component

---

## Limitations

- Limited to SSH and Telnet attacks
- Does not include HTTP attack data
- Does not include FTP attack data
- No malware or payload analysis
- Command execution results may not always reflect the behavior of a real operating system due to the emulated environment
- Requires feature engineering before applying machine learning algorithms
---

Cowrie was selected as the primary dataset for SSH because it provides complete attacker interactions, including authentication attempts, command execution, and session tracking. Combined with MACCDC2012 for HTTP and FTP analysis and the AWS Honeypot dataset for GeoIP enrichment, it forms a strong foundation for the Smart Honeypot Orchestrator & Threat Intelligence Dashboard.

# 5. Multi-Regional Cloud Honeynet Dataset (MURHCAD)

## Overview

The Multi-Regional Cloud Honeynet Dataset (MURHCAD) is a comprehensive, high-resolution honeynet dataset collected over a continuous 72-hour period (June 9–11, 2025) using Microsoft Azure. The dataset was generated from a distributed T-Pot honeynet deployment consisting of four geographically distributed virtual machines running three different honeypots: Cowrie, Dionaea, and SentryPeer.

The dataset contains **132,425** real attack events collected from **2,438** unique public source IP addresses originating from **95 countries**, making it one of the most comprehensive publicly available honeynet datasets for threat intelligence research.

---

## What Data Does It Contain?

The dataset contains enriched honeynet event records including:

- Attack timestamps
- Source and destination IP addresses
- Autonomous System (ASN) information
- Source organization
- Source country
- Geographic coordinates
- Destination host information
- Network protocols
- Source and destination ports
- Honeypot platform identifiers
- Temporal features

Unlike traditional network traffic datasets, MURHCAD combines network metadata with geographic enrichment and multi-honeypot telemetry collected from different cloud regions.

---

## Available Columns

| Column | Description |
|---------|-------------|
| weekday | Day of the week when the event occurred |
| date | Exact date of the event (MM/DD/YY) |
| srcIp | Public IP address of the attacker |
| srcOrg | Organization associated with the source IP (ASN lookup) |
| srcCountryName | Source country |
| srcGeoIp | IP used for source geolocation |
| dstIp | Public IP address of the target system |
| dstIpInternal | Private IP address of the internal target host |
| dstHostname | Hostname of the target virtual machine |
| dstGeoIp | IP used to derive the target geolocation |
| dstCountryName | Country of the targeted system |
| protocol | Protocol used during the attack |
| attackType | Honeypot that captured the event (Cowrie, Dionaea, or SentryPeer) |
| hour | Hour of the day (0–23) |
| day | Numeric day extracted from the timestamp |
| srcPort | Source port used by the attacker |
| srcLat / srcLon | Geographic coordinates of the attack origin |
| dstPort | Targeted destination port |
| dstLat / dstLon | Geographic coordinates of the target |

---
## Protocol Coverage

The dataset captures attacks across **13 distinct network protocols**, providing broad visibility into multi-protocol attack activity observed by different honeypot platforms.

The most frequently targeted protocols include:

- **SIP (Session Initiation Protocol)** – approximately **55,060 events**, representing the dominant protocol in the dataset and primarily captured by the SentryPeer honeypot.
- **Telnet** – approximately **29,000 events**, mainly recorded by the Cowrie honeypot during credential brute-force and remote access attempts.
- **SMB (SMBD)** – approximately **36,000 events**, primarily captured by the Dionaea honeypot during malware propagation and Windows file-sharing attacks.

Additional protocols observed in the dataset include SSH, HTTP, MySQL, MSSQL, MongoDB, MQTT, TFTP, PPTP, EPMAP, and other service-specific protocols, providing comprehensive coverage of multiple attack surfaces.

## Suitable for Machine Learning?

**Yes.**

The dataset provides rich multi-dimensional features that are well suited for unsupervised machine learning tasks such as attacker clustering, anomaly detection, protocol-based behavior analysis, temporal pattern analysis, and geographic threat intelligence.

Potential features include:

- Attack frequency
- Source country
- Source organization (ASN)
- Geographic coordinates
- Protocol usage
- Targeted ports
- Attack timing
- Honeypot type
- Regional attack distribution

---

## Suitable for Our Project?

**Yes (Highly Recommended).**

MURHCAD closely aligns with the objectives of the Smart Honeypot Orchestrator project by providing real-world attack telemetry collected from multiple honeypot platforms deployed across geographically distributed cloud environments.

The dataset supports:

- GeoIP visualization
- Threat intelligence
- Geographic attack analysis
- Protocol distribution analysis
- Dashboard development
- Attack statistics
- Multi-region attack analysis
- Machine learning for attack clustering

**Project Role:** Supplementary dataset for GeoIP analysis, multi-protocol attack statistics, dashboard visualization, and threat intelligence.

---

## Advantages

- Real honeynet attack data
- 132,425 real attack events
- 2,438 unique public source IP addresses
- Attack data from 95 countries
- Public source IP addresses support GeoIP enrichment
- ASN and organization mapping
- Geographic coordinates included
- Multi-region cloud deployment
- Multiple honeypot platforms (Cowrie, Dionaea, SentryPeer)
- Suitable for threat intelligence
- Excellent for dashboard visualization
- Rich metadata for machine learning

---

## Limitations

- Data collection period limited to 72 hours
- Maintenance-induced virtual machine restarts introduce gaps in the time-series data
- Different honeypot platforms introduce platform-specific collection biases
- Protocol coverage depends on the deployed honeypot services
- Does not provide complete interactive attacker sessions across all supported protocols

---

The dataset demonstrates significant diversity in attacker origins, with **2,438** unique source IP addresses distributed across **95 countries**. However, attack activity is highly concentrated, with the most active source IP accounting for approximately **15%** of all recorded events. This characteristic makes the dataset particularly valuable for studying large-scale attack campaigns, geographic threat distribution, and attacker clustering.

MURHCAD complements the other selected datasets by providing high-quality GeoIP metadata, ASN information, geographic enrichment, and multi-region honeynet telemetry that are not available in datasets such as MACCDC2012.

# 6. CTU-13

## Overview

CTU-13 is a publicly available network traffic dataset developed by the Czech Technical University (CTU) to support botnet detection research. It contains labeled network flow records collected from real botnet scenarios combined with normal background traffic and legitimate user activity.

Unlike honeypot datasets, CTU-13 focuses on network communication patterns rather than direct attacker interactions, making it suitable for flow-based machine learning and network behavior analysis.

---

## What Data Does It Contain?

The dataset contains labeled network flow records including:

- Source and destination IP addresses
- Source and destination ports
- Network protocols
- Flow duration
- Packet counts
- Byte counts
- Connection states
- Flow direction
- Start and end timestamps
- Botnet labels
- Normal traffic
- Background traffic

The dataset combines malicious botnet communications with legitimate network traffic, enabling both supervised and unsupervised machine learning experiments.

---

## Available Features

Based on the analyzed sample, the dataset includes:

- Timestamp
- Duration
- Protocol
- Source IP address
- Source port
- Destination IP address
- Destination port
- Direction
- Connection state
- Packet count
- Byte count
- Flow label (Botnet / Normal / Background)

---

## Suitable for Machine Learning?

**Yes.**

CTU-13 is one of the most widely used benchmark datasets for network intrusion detection research. Its labeled network flows support supervised and unsupervised machine learning tasks, including classification, clustering, anomaly detection, and botnet behavior analysis.

Potential features include:

- Flow duration
- Packet count
- Byte count
- Protocol usage
- Connection frequency
- Communication direction
- Connection state
- Source and destination IP addresses

---

## Suitable for Our Project?

**Partially.**

CTU-13 provides valuable labeled network flow data that can support the development and evaluation of machine learning models. However, it does not capture direct attacker interactions with honeypot services, such as authentication attempts, executed commands, or protocol-specific application logs.

Since the dataset contains public IP addresses, GeoIP enrichment can also be applied to analyze attacker locations.

**Project Role:** Supplementary dataset for flow-based machine learning, botnet detection, and network traffic analysis.

---

## Advantages

- Public source IP addresses
- Supports GeoIP enrichment
- Labeled botnet traffic
- Real network communication
- Widely used benchmark dataset
- Excellent for machine learning
- Suitable for anomaly detection
- Useful for network behavior analysis

---

## Limitations

- Not collected from honeypots
- No attacker session information
- No authentication events
- No command execution logs
- No HTTP or FTP application-level interactions
- Flow-based analysis only
- Limited behavioral context compared to honeypot datasets

---

Although CTU-13 provides high-quality labeled network flows and public IP addresses suitable for GeoIP enrichment, it does not capture the detailed attacker interactions required for honeypot behavior analysis. Therefore, it serves as a supplementary dataset for machine learning evaluation rather than a primary data source for the Smart Honeypot Orchestrator & Threat Intelligence Dashboard.

# Dataset Comparison

After evaluating the selected datasets, it became clear that each dataset provides different capabilities and addresses different aspects of the project requirements. No single dataset is capable of covering all required services, attacker behaviors, and threat intelligence features.

**AWS Honeypot Attack Data** provides real honeypot network traffic with public source IP addresses and built-in GeoIP information. It is useful for geographic visualization, attack statistics, and dashboard development, but it lacks detailed attacker interaction such as authentication attempts or command execution.

**UNSW-NB15** is a labeled network intrusion detection dataset designed primarily for machine learning research. It provides rich network flow features and attack labels but does not contain honeypot interactions or protocol-specific attacker behavior.

**MACCDC2012** provides detailed protocol-specific logs covering SSH, HTTP, and FTP activities. It contains rich authentication events, application-level interactions, and protocol metadata that make it highly valuable for attacker behavior analysis. However, since the dataset uses private IP addresses, it cannot support GeoIP enrichment.

**Cowrie Real Logs** provide the most detailed SSH attacker behavior among all evaluated datasets. The logs include connection events, authentication attempts, SSH client information, HASSH fingerprints, executed commands, and session tracking. Since the dataset contains public source IP addresses, it also supports GeoIP enrichment, making it the best choice for SSH behavior analysis.

**MURHCAD** offers a large-scale, cloud-based honeynet dataset collected from multiple geographically distributed honeypots. It includes enriched GeoIP information, ASN mapping, multiple protocols, and attack telemetry collected from different cloud regions. Although it provides excellent geographic threat intelligence and multi-protocol statistics, its primary contribution overlaps with the project's planned GeoIP enrichment pipeline.

**CTU-13** is a labeled network flow dataset designed for botnet detection research. It contains public IP addresses, allowing GeoIP enrichment, and is well suited for machine learning tasks such as anomaly detection and traffic classification. However, it is not a honeypot dataset and does not capture attacker sessions or application-level interactions.

The following table summarizes the evaluation results and the final implementation decision.

| Dataset | Honeypot Dataset | Public IPs | GeoIP Support | SSH Behavior | HTTP/FTP Behavior | Machine Learning | Final Decision |
|----------|:----------------:|:----------:|:-------------:|:------------:|:-----------------:|:----------------:|----------------|
| AWS Honeypot Attack Data | Yes | Yes | Yes | No | No | Partial | **Selected (Supplementary)** |
| UNSW-NB15 | No | Partial | No | No | No | Yes | **Evaluated – Not Selected** |
| MACCDC2012 | No | No | No | Yes | Yes | Yes | **Selected (Primary)** |
| Cowrie Real Logs | Yes | Yes | Yes | Yes | No | Yes | **Selected (Primary)** |
| MURHCAD | Yes | Yes | Yes | Partial | Partial | Yes | **Evaluated – Not Selected** |
| CTU-13 | No | Yes | Yes | No | No | Yes | **Evaluated – Not Selected** |

Overall, no individual dataset satisfies all project requirements. Therefore, a combination of complementary datasets was selected to provide comprehensive protocol coverage, attacker behavior analysis, geographic threat intelligence, and machine learning support while avoiding redundant data sources during implementation.

# Final Recommendation

After evaluating all candidate datasets, it was concluded that no single dataset satisfies all requirements of the Smart Honeypot Orchestrator & Threat Intelligence Dashboard. Therefore, multiple datasets were evaluated to identify the most suitable combination for implementation.

---

## Selected Datasets for Implementation

Based on the evaluation, the following datasets were selected for implementation.

### Primary Datasets

**Cowrie Real Logs**

Cowrie Real Logs were selected as the primary dataset for SSH attacker behavior analysis. They provide detailed session-level information, including connection events, authentication attempts, SSH client information, HASSH fingerprints, executed commands, and complete session tracking. These features closely match the project's objective of profiling attacker behavior.

**MACCDC2012**

MACCDC2012 was selected as the primary dataset for HTTP and FTP attacker behavior analysis. Its protocol-specific logs contain authentication events, FTP operations, HTTP requests, and application-level interactions that complement the SSH data collected from Cowrie.

### Supplementary Dataset

**AWS Honeypot Attack Data**

The AWS Honeypot Attack Data dataset was selected as a supplementary dataset to support GeoIP enrichment, geographic visualization, and attack origin analysis. Its public source IP addresses and built-in geographic information complement the behavioral datasets used by the project.

---

## Additional Evaluated Datasets

The following datasets were evaluated during the research phase but were not selected for implementation.

### MURHCAD

MURHCAD was evaluated because it provides large-scale cloud honeynet telemetry, ASN mappings, GeoIP enrichment, and multi-protocol attack statistics collected from geographically distributed honeypots.

However, the implementation will perform live GeoIP enrichment using the MaxMind GeoLite2 database. Since geographic intelligence will be generated dynamically during data collection, MURHCAD is not required as an implementation dataset.

### CTU-13

CTU-13 was evaluated as a high-quality dataset for flow-based machine learning and botnet detection research.

However, the project focuses on session-level attacker behavior collected from honeypots rather than network flow classification. Consequently, CTU-13 is not suitable as a primary implementation dataset.

### UNSW-NB15

UNSW-NB15 was evaluated because it is one of the most widely used benchmark datasets for supervised intrusion detection research.

However, the project's machine learning component is based on unsupervised clustering of attacker sessions rather than supervised traffic classification. Therefore, UNSW-NB15 will not be used during implementation.

---

## Final Selected Dataset Combination

The final implementation will use the following datasets:

- **Cowrie Real Logs** for SSH attacker behavior analysis.
- **MACCDC2012** for HTTP and FTP attacker behavior analysis.
- **AWS Honeypot Attack Data** for GeoIP enrichment, attack origin analysis, and dashboard visualization.

This dataset combination provides the best balance between detailed attacker behavior analysis, protocol coverage, and geographic threat intelligence while avoiding redundant datasets that duplicate functionality already provided by the project pipeline.
