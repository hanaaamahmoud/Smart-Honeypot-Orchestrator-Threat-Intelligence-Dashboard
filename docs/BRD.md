
# Business Requirements Document (BRD)
# Smart Honeypot Orchestrator & Threat Intelligence Dashboard

---

## Section 1: Project Overview

### 1.1 Brief Description
The Smart Honeypot Orchestrator & Threat Intelligence Dashboard is a distributed security platform that automatically deploys and manages low-interaction honeypots (SSH, HTTP, and FTP) using Docker containers. The system captures attack activities, enriches them with GeoIP information, analyzes them using unsupervised machine learning to identify attack patterns, and displays the results through a real-time dashboard.

### 1.2 Business Context
Organizations face continuous cyber threats with limited visibility into attacker behavior. Security teams need proactive tools that go beyond prevention and enable them to study, understand, and anticipate attack methods before they impact production systems.

### 1.3 Background
Honeypots are decoy systems designed to attract attackers into a controlled and isolated environment. Unlike traditional security tools that mainly block threats, honeypots allow security teams to safely observe attacker techniques and behavior, improving the organization's threat intelligence capabilities without exposing real systems to risk.

---

## Section 2: Business Problem / Opportunity

### 2.1 Problem
Security teams often have limited visibility into attacker behavior and techniques. Many attack attempts are detected only after they have affected real systems, making organizations react to threats instead of anticipating them.

### 2.2 Opportunity
By deploying and managing honeypots in a safe and isolated environment, organizations can:
- Collect attack data early.
- Study attacker behavior safely.
- Improve threat visibility.
- Support better security decisions before production systems are affected.

### 2.3 Summary Statement
This project provides a proactive platform that automatically deploys honeypots, captures attacker activities, analyzes attack patterns, and presents the results through a real-time dashboard to support threat intelligence.

---

## Section 3: Business Objectives

### 3.1 Measurable Goals
- Deploy at least 3 honeypot services (SSH, HTTP, FTP) using Docker containers.
- Capture and store attack logs from all deployed honeypots in Elasticsearch.
- Enrich all captured logs with GeoIP information.
- Display attack data on a real-time dashboard accessible to security analysts.
- Identify similar attack patterns using unsupervised machine learning.
- Generate attack statistics including top attacking IP addresses, top source countries, most targeted services, most common commands executed when available, and attack frequency trends.

### 3.2 Expected Business Outcomes
- Improved visibility into attacker behavior and techniques.
- Early detection of attack patterns before production systems are affected.
- Actionable threat intelligence reports for security teams.
- A centralized dashboard for monitoring and analyzing honeypot events.

---

## Section 4: Scope

### 4.1 In Scope

#### Honeypots
- SSH Honeypot (Cowrie)
- HTTP Honeypot (OpenCanary)
- FTP Honeypot (OpenCanary or equivalent)

#### Orchestration & Deployment
- Automated deployment and management of honeypots using Docker and a Python Orchestrator.

#### Data Collection & Processing
- Attack log collection and centralized storage (Elasticsearch).
- GeoIP enrichment of captured logs.

#### Analytics & Visualization
- Real-time dashboard (Vue.js).
- Unsupervised ML clustering for attack pattern analysis.
- Basic attack statistics and reporting.
- Threat intelligence analytics (Dashboard, Statistics, and Clustering Results).

### 4.2 Out of Scope
- High-Interaction Honeypots.
- Email Honeypots.
- Malware Analysis.
- Automated Incident Response.
- Automated Threat Hunting.
- Full SIEM Functionality.
- SOAR Capabilities.
- Endpoint Detection and Response (EDR).
- Full MITRE ATT&CK Mapping.

### 4.3 Future Work
- MITRE ATT&CK Mapping.
- Multi-Region Cloud Deployment.
- AI-Generated Honeypot Responses.
- Support for Additional Protocols (SMTP, DNS, etc.).

---

## Section 5: Stakeholders

### 5.1 Stakeholders Table

| Stakeholder | Role |
|-------------|------|
| Project Team | Design, develop, test, and maintain the system. |
| Academic Supervisor | Guide the project and review deliverables. |
| Industry Partner (Fixed Solutions) | Industry partner providing project requirements and feedback. |
| Security Analysts | Monitor attacks and investigate security events using the dashboard. |
| Security Managers | Review threat intelligence insights and support security decisions. |

### 5.2 Stakeholder Categories

| Category | Stakeholder |
|----------|-------------|
| Project Sponsor | Industry Partner (Fixed Solutions) |
| Project Supervisor | Academic Supervisor |
| End Users | Security Analysts, Security Managers |
| Decision Makers | Security Managers, Fixed Solutions |

---

## Section 6: Business Requirements

### 6.1 High-Level Functional Requirements
- The system shall deploy and manage SSH, HTTP, and FTP honeypots automatically using Docker and a Python Orchestrator.
- The system shall capture and centrally store attack logs in Elasticsearch.
- The system shall enrich all captured logs with GeoIP information.
- The system shall stream attack events to the dashboard in real time using WebSockets.
- The system shall apply unsupervised machine learning to group similar attack sessions based on attack features.
- The system shall generate attack statistics, including top attacking IP addresses, top source countries, most targeted services, most common commands executed, and attack frequency trends.
- The system shall generate threat intelligence insights based on collected attack data.
- The dashboard shall present attack statistics and trend visualizations for security analysts.
- The dashboard shall display events from multiple honeypot services in a unified interface.
  
### 6.2 High-Level Non-Functional Requirements
- The system shall isolate honeypots from production systems for safety.
- The dashboard shall be usable by security analysts without specialized training.
- The system shall support continuous operation during the monitoring period.
- The system shall allow configuration through external configuration files (e.g., number of honeypots and enabled services).
- The system shall store logs in a centralized repository to simplify monitoring and analysis.

---

## Section 7: User Roles

| User Role | Responsibilities |
|-----------|-----------------|
| Security Analyst | Monitor attacks, review logs, and analyze attack patterns. |
| Security Manager | Review reports and support security decisions. |
| System Administrator | Deploy and maintain honeypot services. |

---

## Section 8: Business Process

### 8.1 Current Process (As-Is)

```
Attacker
    |
Production System
    |
Attack Detected
    |
Security Team Investigation
```

In the current approach, attacks are typically detected after reaching the production environment, limiting the organization's ability to observe attacker behavior before systems are affected.

### 8.2 Future Process (To-Be)

```
Attacker
    |
Honeypot (SSH / HTTP / FTP)
    |
Attack Logs Collection
    |
GeoIP Enrichment
      |
ML Analysis
      |
Real-Time Dashboard
    |
Security Analyst
```

The proposed system captures attacker activities through isolated honeypots, enriches and analyzes the collected logs, then presents the results in real time to support proactive threat monitoring and analysis.

---

## Section 9: Assumptions & Constraints

### 9.1 Assumptions
- Honeypots can be deployed using Docker in the target environment.
- Sufficient attack data will be available from live honeypots or public datasets.
- The required software tools and development environment are available.

### 9.2 Constraints
- Limited project timeline.
- Limited development resources.
- Live attacker traffic may not always be available.
- The project is limited to low-interaction honeypots.

---

# Section 10: Project Plan & Milestones

## Project Phase 1 (MVP)

### Phase 1 – Research & Planning (Week 1–2)

#### Activities
- Study honeypot technologies and related work.
- Analyze project requirements.
- Explore and evaluate public honeypot datasets.
- Define system scope.
- Prepare the Business Requirements Document (BRD).

#### Deliverables
- BRD Document
- Dataset Exploration Report
- Project Plan

---

### Phase 2 – Infrastructure Setup & Honeypot Deployment (Week 3–4)

#### Activities
- Prepare Docker environment.
- Configure SSH, HTTP, and FTP honeypots.
- Develop the Python Orchestrator.
- Create deployment configuration files.
- Prepare and submit the Project Proposal.
- Validate and preprocess collected data.

#### Deliverables
- Project Proposal
- Containerization Environment
- Deployed SSH, HTTP, and FTP Honeypots
- Python Orchestrator
- Configuration Files
- Data Preprocessing Pipeline

---

### Phase 3 – Log Collection & Processing (Week 5–6)

#### Activities
- Collect attack logs from honeypots.
- Centralize logs in Elasticsearch.
- Enrich logs with GeoIP information.
- Build the centralized log repository.

#### Deliverables
- Centralized Log Repository
- GeoIP-Enriched Logs
- Processed Attack Dataset

---

### Phase 4 – Dashboard & Core Analytics (Week 7–8)

#### Activities
- Develop the dashboard.
- Implement WebSocket-based real-time updates.
- Integrate honeypot log visualization.
- Display attack statistics and initial analytics.

#### Deliverables
- Functional Dashboard
- Initial Attack Visualizations
- Integrated Honeypot Environment
- **Project Phase 1 (MVP)**

---

## Project Phase 2

### Phase 5 – System Integration & Evaluation (Week 9–13)

#### Activities
- Integrate all project components.
- Implement behavioral clustering.
- Perform attack simulations.
- Evaluate system performance.
- Fix detected issues and optimize the system.

#### Deliverables
- ML Clustering Module
- Evaluation Report
- Stable Beta Version

---

### Phase 6 – Documentation & Final Delivery (Week 14–15)

#### Activities
- Prepare technical documentation.
- Finalize user documentation.
- Prepare the final presentation.
- Package the complete project.

#### Deliverables
- Final Source Code
- Technical Documentation
- User Manual
- Final Presentation
- Graduation Project Package
- **Project Phase 2 (Final Submission)**
---

## Key Milestones

| Milestone | Deliverable | Target Date |
|-----------|-------------|-------------|
| Project Kick-off | Team Setup & Repository Creation | Early July 2026 |
| GP Proposal | BRD + Architecture + Timeline | Mid July 2026 |
| MVP | Honeypots + Log Collection + Basic Dashboard | Mid September 2026 |
| Beta Version | Dashboard + GeoIP + ML Clustering | Mid October 2026 |
| Final System | Fully Integrated Platform | End October 2026 |
| Final Documentation | Thesis + Presentation | Early November 2026 |

