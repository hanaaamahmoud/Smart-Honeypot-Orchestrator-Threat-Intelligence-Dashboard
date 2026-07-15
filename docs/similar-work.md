 RELATED WORK

This chapter reviews existing honeypot frameworks, threat intelligence platforms, and related technologies that informed the design of the Smart Honeypot Orchestrator and Threat Intelligence Dashboard. Each section examines a representative approach, discussing its purpose, architecture, strengths, limitations, dataset characteristics, and relationship to our own work. The chapter concludes with a synthesis that positions our contribution within the broader landscape.

## 2.1 Honeypot Platforms and Frameworks

### 2.1.1 T-Pot: Comprehensive Multi-Honeypot Platform
T-Pot, developed by Telekom Security in collaboration with The Honeynet Project, is an all-in-one honeypot platform that bundles more than twenty individual honeypot implementations into a single Debian-based system. Each honeypot runs within its own Docker container, providing isolation and simplified management. The supported protocols span SSH and Telnet, web services, databases, industrial control systems, remote desktop, Android debug bridges, and various network services.

The platform includes a complete data pipeline. Events from all honeypots are normalized through Logstash, stored in Elasticsearch, and visualized through pre-built Kibana dashboards. Additional tools for traffic fingerprinting, reconnaissance, and attack mapping are integrated directly into the deployment.

**Strengths:**
*   Breadth of coverage: Twenty or more honeypots enable simultaneous monitoring of numerous attack surfaces.
*   Isolation: Docker-based isolation ensures that compromise of one honeypot does not affect others.
*   Dashboards: Pre-built dashboards reduce the time from deployment to actionable insight.
*   Community: Benefits from active maintenance and a substantial user community with extensive documentation.

**Limitations:**
*   Resource intensive: Recommendations of eight to sixteen gigabytes of RAM and substantial disk space.
*   Rigidity: Designed as an integrated appliance rather than a modular toolkit, making customization difficult.
*   Lack of Intelligence: No built-in machine learning or automated pattern analysis; identifying meaningful attack patterns remains entirely manual.
*   Noise: High volume of low-value noise from mass internet scanning, requiring extra tuning.

**Dataset:**
T-Pot does not ship with a public dataset. It generates its own live dataset locally in Elasticsearch.

**Relation to our project:**
Our project deploys a small, targeted set of honeypots (SSH, HTTP, and FTP), reducing resource requirements. We use a custom Python orchestration implementation, add an unsupervised machine learning clustering step for automatic attack pattern grouping, and use a custom Vue.js dashboard tailored to our specific metrics.

### 2.1.2 Modern Honey Network: Distributed Sensor Management
The Modern Honey Network (MHN) is a centralized server for deploying and managing distributed honeypot sensors. An administrator selects honeypot types from a web interface and executes one-line installation commands on target systems. Sensors transmit events to the central server using HPFeeds, a lightweight publish-subscribe protocol. Events are stored via Mnemosyne into MongoDB and can be viewed on a map or exported to tools like Splunk and ArcSight.

**Strengths:**
*   Scalability: Deploying a new sensor requires minimal effort.
*   Centralization: Enables comparison of attack activity across different regions and network contexts.
*   Visualization: Geographic visualization through Honeymap provides an intuitive understanding of attack distribution.
*   Integration: Out-of-the-box integrations for forwarding data to enterprise security tools.

**Limitations:**
*   Maintenance: Little active development since approximately 2018.
*   Compatibility: Targets outdated operating system versions and depends on Python 2 packages that are difficult to install on modern systems.
*   Lack of Analytics: No analytics, correlation, or machine learning layer exists; it focuses purely on deployment and raw data collection.
*   Interface: Dated web interface and map visualization providing only basic functionality.

**Dataset:**
No standardized public dataset. Each deployment generates its own dataset from connected sensors.

**Relation to our project:**
Unlike MHN's reliance on legacy operating systems and lack of analytics, our orchestrator is purpose-built for modern infrastructure. We store and index events in Elasticsearch with GeoIP enrichment and machine learning clustering, providing a real-time, purpose-built Vue.js dashboard.

## 2.2 Threat Intelligence Platforms

### 2.2.1 HoneyDB: Community-Driven Threat Aggregation
HoneyDB is a community-driven, hosted threat intelligence platform built around a lightweight honeydb-agent. The agent contributes captured honeypot activity to a central service, which aggregates data from a global network of sensors. Aggregated data (bad hosts, IP history, sensor activity, targeted services, and payloads) is exposed through the honeydb.io website and a REST API. A newer addition, HoneyDB AI, layers a natural language chat interface over the API.

**Strengths:**
*   Low barrier to entry: Requires minimal configuration and no local log management infrastructure.
*   Crowd-sourced visibility: Visibility beyond a single organization's sensors.
*   Integration: Easy to integrate free-tier API into existing security tooling.
*   Accessibility: Natural language interface lowers the skill floor for querying threat data.

**Limitations:**
*   Limited Scope: Primarily a data consumption and light-sensor platform, not a full honeypot deployment and analytics stack.
*   No Local Control: No built-in dashboard for self-hosted honeypots.
*   Dependency: Hosted nature creates dependency on a third party's operation and policies.
*   Reliability: AI interface is in early beta and can be inaccurate.

**Dataset:**
Community-contributed feed including bad hosts, per-service bad hosts, IP history, sensor/node data, autonomous system information, and payload history.

**Relation to our project:**
HoneyDB is a shared, hosted intelligence feed. Our project is a self-contained platform that deploys and analyzes its own honeypot data. While HoneyDB could serve as a complementary data source, it cannot replace our custom orchestration and analytics layer.

## 2.3 Resource Discovery and Reference

### 2.3.1 Awesome Honeypots: Curated Tool Directory
Awesome Honeypots is a curated, community-maintained GitHub list that indexes honeypot software and related tooling by category.

**Strengths:**
*   Discovery: Enables practitioners to quickly identify honeypots for specific protocols.
*   Coverage: Broad coverage across many niches.
*   Maintenance: Community-maintained via pull requests.
*   Cost: Zero cost or infrastructure requirements.

**Limitations:**
*   No functionality: No deployment, data collection, or dashboard capabilities.
*   Vetting: Does not rank or benchmark entries; some tools may be abandoned or immature.
*   No guidance: No built-in guidance for combining multiple tools into an integrated pipeline.

**Relation to our project:**
We used this resource during our research phase to identify established, community-vetted honeypots (e.g., Cowrie). However, it played no operational role in our system design or implementation.

## 2.4 Synthesis and Positioning
The reviewed approaches represent four distinct philosophies in honeypot technology:
*   T-Pot: Comprehensive but resource-intensive and analytically shallow.
*   MHN: Valuable for distributed deployment but requires unmaintained legacy infrastructure.
*   HoneyDB: Scales through community aggregation but sacrifices individual control.
*   Awesome Honeypots: Essential for discovery but insufficient for operational deployment.

Our Smart Honeypot Orchestrator and Threat Intelligence Dashboard synthesizes these lessons: we adopt a focused, Docker-based deployment; implement modern Python orchestration; maintain full control over the data pipeline; and integrate unsupervised machine learning to automate attack pattern discovery, transforming raw logs into actionable intelligence.

## 2.5 Datasets in the Honeypot Research Community
*   **Cowrie:** Generates structured JSON logs used in research. No standardized public dataset exists; researchers must generate their own via live deployment or collaboration.
*   **HoneyDB:** Aggregated community data, query-limited.
