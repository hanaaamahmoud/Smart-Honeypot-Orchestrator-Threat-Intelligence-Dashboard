# Cowrie Event Reference

## Dataset Information

| Item | Value |
|------|-------|
| Honeypot | Cowrie |
| Protocol | SSH |
| Log Format | NDJSON (JSON Lines) |
| Dataset | Cowrie SSH Logs |
| Purpose | Event Reference Documentation |

---

# Overview

Cowrie records attacker interactions as a sequence of structured events.

Each event represents one stage of the attack lifecycle, from the initial connection to authentication attempts, command execution, and session termination.

Understanding each event type is essential for:

- Behavioral Analysis
- Feature Engineering
- Session Reconstruction
- Machine Learning
- Threat Intelligence

---

# Event Lifecycle

Typical SSH attacker workflow inside Cowrie:

```text
cowrie.session.connect
        │
        ▼
cowrie.client.version
        │
        ▼
cowrie.client.kex
        │
        ▼
cowrie.login.failed
        │
        ▼
cowrie.login.success
        │
        ▼
cowrie.command.input
        │
        ▼
cowrie.session.closed
```

---

# Event Reference

---

## 1. cowrie.session.connect

### Description

Represents the beginning of a new SSH session.

Generated immediately after the attacker establishes a TCP connection.

### Important Fields

| Field | Description |
|--------|-------------|
| timestamp | Event time |
| session | Session identifier |
| src_ip | Attacker IP |
| src_port | Source port |
| dest_ip | Honeypot IP |
| dest_port | SSH port |
| protocol | SSH |
| message | Connection message |

### Project Usage

- Session reconstruction
- Connection statistics
- Source IP extraction
- Attack timeline

### Used for Machine Learning

 Yes

Possible features:

- Connection frequency
- Source IP activity
- Session count

---

## 2. cowrie.client.version

### Description

Captures the SSH client version sent by the attacker.

### Important Fields

| Field | Description |
|--------|-------------|
| version | SSH client version |
| session | Session ID |
| src_ip | Attacker IP |
| timestamp | Event time |

### Project Usage

- Client fingerprinting
- SSH software identification

### Used for Machine Learning

Yes

Possible feature:

- SSH Client Version

---

## 3. cowrie.client.kex

### Description

Records the SSH Key Exchange negotiation.

This event contains the SSH fingerprint (HASSH) and cryptographic algorithms used by the attacker.

### Important Fields

| Field | Description |
|--------|-------------|
| hassh | SSH fingerprint |
| hasshAlgorithms | HASSH algorithms |
| kexAlgs | Key exchange algorithms |
| keyAlgs | Host key algorithms |
| macCS | MAC algorithms |
| encCS | Encryption algorithms |
| compCS | Compression algorithms |
| langCS | Language algorithms |
| session | Session ID |

### Project Usage

- SSH fingerprinting
- Client identification
- Behavioral clustering

### Used for Machine Learning

Yes

Possible features:

- HASSH fingerprint
- Encryption algorithms
- Key exchange algorithms

---

## 4. cowrie.login.failed

### Description

Generated whenever an authentication attempt fails.

### Important Fields

| Field | Description |
|--------|-------------|
| username | Attempted username |
| password | Attempted password |
| session | Session ID |
| src_ip | Attacker IP |
| timestamp | Event time |

### Project Usage

- Brute-force analysis
- Credential analysis
- Password dictionary analysis

### Used for Machine Learning

 Yes

Possible features:

- Failed login count
- Username diversity
- Password diversity

---

## 5. cowrie.login.success

### Description

Generated after successful authentication.

Not every session contains this event.

### Important Fields

| Field | Description |
|--------|-------------|
| username | Authenticated username |
| password | Password used |
| session | Session ID |
| timestamp | Event time |

### Project Usage

- Successful compromise detection
- Credential analysis

### Used for Machine Learning

 Yes

Possible features:

- Successful login count
- Login success ratio

---

## 6. cowrie.command.input

### Description

Records every command executed by the attacker.

This is one of the richest behavioral events in the dataset.

### Important Fields

| Field | Description |
|--------|-------------|
| input | Executed command |
| session | Session ID |
| timestamp | Event time |
| src_ip | Attacker IP |

### Project Usage

- Command analysis
- Behavioral profiling
- Attack sequence reconstruction
- Threat Intelligence

### Used for Machine Learning

 Yes

Possible features:

- Number of commands
- Command diversity
- Command sequence
- Most frequent commands

---

## 7. cowrie.session.closed

### Description

Represents the end of an SSH session.

### Important Fields

| Field | Description |
|--------|-------------|
| duration | Session duration |
| session | Session ID |
| timestamp | Event time |

### Project Usage

- Session statistics
- Session duration analysis
- Timeline reconstruction

### Used for Machine Learning

 Yes

Possible features:

- Session duration
- Average session length

---

# Rare Events

The following event types exist in the dataset but occur infrequently.

| Event | Purpose |
|--------|----------|
| cowrie.client.size | Terminal window size |
| cowrie.client.var | Environment variables |
| cowrie.session.file_upload | Uploaded files |
| cowrie.session.file_download | Downloaded files |
| cowrie.direct-tcpip.request | Direct TCP forwarding |
| cowrie.direct-tcpip.data | Forwarded TCP data |

These events were retained because they represent real attacker activities, even though they occur rarely.


# Behavioral Coverage

The Cowrie event sequence captures nearly the complete SSH attack lifecycle:

- Initial connection
- Client fingerprinting
- SSH negotiation
- Authentication attempts
- Successful compromise
- Command execution
- Session termination

This provides sufficient behavioral information for attacker profiling, behavioral clustering, and threat intelligence.

---

# Relationship with Feature Engineering

The event types documented here will later be transformed into behavioral features.

Examples include:

- Failed login count
- Successful login count
- Session duration
- Command count
- Command diversity
- Time between commands
- SSH client version
- HASSH fingerprint
- Connection frequency

These features will form the basis of the Machine Learning dataset used for attacker behavior clustering.

---

# Summary

The Cowrie event model provides complete visibility into SSH attacker behavior.

The combination of authentication events, SSH fingerprints, command execution logs, and session metadata makes Cowrie one of the richest open-source honeypot datasets for behavioral analysis and unsupervised machine learning.
