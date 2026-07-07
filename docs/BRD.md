
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
- Apply unsupervised machine learning to group similar attack sessions based on attack features.
- Generate attack statistics including top attacking IP addresses, top source countries, most targeted services, most common commands executed, and attack frequency trends.

### 3.2 Expected Business Outcomes
- Improved visibility into attacker behavior and techniques.
- Early detection of attack patterns before production systems are affected.
- Actionable threat intelligence reports for security teams.
- A reusable framework for deploying and managing honeypots.

---

## Section 4: Scope

### 4.1 In Scope

#### Honeypots
- SSH Honeypot (Cowrie)
- HTTP Honeypot (OpenCanary)
- FTP Honeypot (OpenCanary)

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
- Basic MITRE ATT&CK Mapping.
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
| Fixed Solutions | Industry partner providing project requirements and feedback. |
| Security Analysts | Monitor attacks and investigate security events using the dashboard. |
| Security Managers | Review threat intelligence insights and support security decisions. |

### 5.2 Stakeholder Categories

| Category | Stakeholder |
|----------|-------------|
| Project Sponsor | Fixed Solutions |
| Project Supervisor | Academic Supervisor |
| End Users | Security Analysts, Security Managers |
| Decision Makers | Security Managers, Fixed Solutions |

---

## Section 6: Business Requirements

### 6.1 High-Level Functional Requirements
- The system shall deploy and manage SSH, HTTP, and FTP honeypots automatically using Docker and a Python Orchestrator.
- The system shall capture and store attack logs from all deployed honeypots in Elasticsearch.
- The system shall enrich all captured logs with GeoIP information.
- The system shall stream attack events to the dashboard in real time using WebSockets.
- The system shall apply unsupervised machine learning to group similar attack sessions based on attack features.
- The system shall generate attack statistics, including top attacking IP addresses, top source countries, most targeted services, most common commands executed, and attack frequency trends.
- The system shall generate threat intelligence insights from captured attack data.
- The dashboard shall present attack statistics and trend visualizations for security analysts.
- The system shall support simultaneous monitoring of multiple honeypot services through a unified dashboard.
- The Python Orchestrator shall automatically restart any honeypot service that stops unexpectedly.

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
GeoIP Enrichment & ML Analysis
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

## Section 10: Timeline & Milestones

### 10.1 High-Level Implementation Phases

| Phase | Description | Duration |
|-------|-------------|----------|
| Phase 1 | Research & Planning | Week 1-2 |
| Phase 2 | System Design & Infrastructure Setup | Week 3-4 |
| Phase 3 | Honeypot Deployment & Log Collection | Week 5-6 |
| Phase 4 | Analytics, Dashboard & Threat Intelligence | Week 7-8 |
| Phase 5 | System Integration, Testing & Refinement | Week 9-10 |
| Phase 6 | Documentation & Final Refinements | Week 11-12 |

### 10.2 Key Milestones

| Milestone | Deliverable | Target Date |
|-----------|-------------|-------------|
| Project Kick-off | Team Setup & Repository Creation | Early July 2026 |
| GP Proposal | BRD + Architecture + Timeline | Mid July 2026 |
| MVP | Working Honeypots + Log Collection + Basic Dashboard | Mid September 2026 |
| Beta Version | Threat Intelligence Dashboard + GeoIP + ML Clustering | Mid October 2026 |
| Final Code | Fully Integrated System | End October 2026 |
| Thesis | Final Documentation & Thesis | Early November 2026 |
