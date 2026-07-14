# Cowrie Study Notes

## Goal

Before starting the implementation, I studied Cowrie using both the TryHackMe room and the official open-source project to understand how it works and how it can be integrated into our project.

---

# 1. TryHackMe - Cowrie Room

Started with the practical lab to understand the basics of Cowrie.

### Studied

- Honeypot types
- SSH attack workflow
- Brute-force attacks
- Typical bot behavior
- SSH tunnelling
- Log analysis
- Attacker identification

### Learned

- How attackers interact with an SSH honeypot.
- The typical attack lifecycle after a successful login.
- How Cowrie records attacker activities.
- Why Cowrie logs are useful for security monitoring and analysis.

---

# 2. Open Source Review

After understanding the concepts, I explored the Cowrie source code to see how these features are implemented.

---

## README

Studied the project overview and architecture.

### Learned

- How Cowrie works.
- Supported interaction modes.
- Main project components.

---

## Docker Deployment

Studied:

- Dockerfile
- docker-compose.yml

### Learned

- How Cowrie is built.
- How the container is started.
- How ports and volumes are configured.

---

## Configuration

Studied:

- cowrie.cfg

### Learned

- SSH settings.
- Authentication configuration.
- Log locations.
- Output plugins.
- Main system configuration.

---

## Authentication

Studied:

- userdb.txt

### Learned

- How Cowrie handles fake user credentials.
- How login attempts are validated.

---

## Log Structure

Studied:

- cowrie.json
- cowrie.log
- tty/
- downloads/

### Learned

- Where attack events are stored.
- How attacker sessions are recorded.
- Which files will be used later in the dashboard.

---

# Outcome

After completing the TryHackMe room and reviewing the Cowrie open-source project, I now understand:

- Cowrie architecture
- SSH attack workflow
- Configuration files
- Docker deployment
- Log structure
- Authentication mechanism

This knowledge will be used during the implementation phase of the project.