# Smart Honeypot Orchestrator & Threat Intelligence Dashboard

# Honeypot Technology Evaluation Report

---

# 1. Introduction

As part of the Smart Honeypot Orchestrator & Threat Intelligence Dashboard project, several honeypot technologies were evaluated to understand their deployment process, attack detection capabilities, log generation, and suitability for integration with the project's ELK Stack and Machine Learning pipeline.

The evaluation focused on validating:

* Honeypot deployment.
* Service emulation.
* Attack detection.
* Log collection.
* Integration with centralized logging.
* Suitability for attacker behavior analysis.

---

# 2. OpenCanary Evaluation

## Overview

OpenCanary is a lightweight **low-interaction honeypot** that simulates commonly targeted network services and generates structured security logs whenever an attacker interacts with those services.

The initial evaluation was performed using Docker to understand the complete honeypot workflow before integrating additional specialized honeypots.

---

# 3. Deployment Environment

Environment used during testing:

* Host OS: Linux
* Container Platform: Docker
* Honeypot Type: Low-Interaction

Deployment structure:

```
Host Machine
      |
Docker Container
      |
 OpenCanary
      |
  FTP / HTTP
```

---

# 4. Enabled Services

### FTP Honeypot

Port:

```
21/TCP
```

The FTP service simulates an FTP server and records:

* Connection attempts.
* Username.
* Password.
* Authentication failures.

Example:

```
Username: admin
Password: admin
```

---

### HTTP Honeypot

Port:

```
80/TCP
```

The HTTP service simulates a web server and records:

* HTTP requests.
* Login attempts.
* Web scanning activity.

Example:

```
GET /index.html

POST /index.html
```

---

# 5. Configuration

The main configuration file:

```
data/.opencanary.conf
```

The configuration enables or disables services and defines their listening ports.

Example:

```json
{
 "ftp.enabled": true,
 "ftp.port": 21,

 "http.enabled": true,
 "http.port": 80
}
```

---

# 6. Testing Results

Both FTP and HTTP services were successfully tested.

Testing confirmed that OpenCanary:

* Exposes fake services.
* Accepts attacker interaction.
* Generates structured JSON logs.
* Records authentication attempts and web requests.

---

# 7. Log Analysis

OpenCanary produces JSON events containing information such as:

* Source IP
* Destination Port
* Username
* Password
* Event Type
* Timestamp

These logs can later be forwarded to:

* Logstash
* Elasticsearch
* Dashboard
* Machine Learning pipeline

---

# 8. HTTP Honeypot Investigation

Since the project requires collecting detailed attacker behavior on web services, additional HTTP honeypot technologies were investigated.

The main candidate selected for evaluation was **SNARE/TANNER**.

### SNARE

SNARE acts as the web honeypot responsible for receiving attacker HTTP requests and recording web attack activity such as:

* Directory scanning.
* Login attempts.
* SQL Injection attempts.
* Web reconnaissance.

### TANNER

TANNER complements SNARE by analyzing the collected HTTP requests and identifying possible attack techniques.

Compared to OpenCanary, SNARE/TANNER provides richer web attack information, making it more suitable for attacker behavior analysis.

---

# 9. FTP Honeypot Investigation

Several FTP honeypot solutions were researched to improve visibility into FTP attacker behavior.

The primary candidate selected for further evaluation is **Honeygrove**.

Honeygrove is a modular Python-based honeypot framework capable of simulating FTP services and recording:

* Authentication attempts.
* FTP commands.
* Session activity.

Although still considered a low-interaction honeypot, it provides more flexibility and richer logging than a basic FTP service simulation.

---


# 11. Conclusion

OpenCanary successfully demonstrated the deployment process, service emulation, attack detection, and structured log generation.

However, to better satisfy the project requirements for attacker behavior analysis, additional specialized honeypots were investigated.

Based on the evaluation:

* **OpenCanary** will be used for lightweight service detection and initial event collection.
* **SNARE/TANNER** is a strong candidate for HTTP attack analysis.
* **Honeygrove** is being evaluated as the FTP honeypot to provide richer FTP interaction data.

Combining these technologies is expected to provide higher-quality data for visualization, threat intelligence generation, and machine learning-based attacker clustering.
