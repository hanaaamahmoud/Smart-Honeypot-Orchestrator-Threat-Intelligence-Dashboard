# Smart Honeypot Orchestrator

## Overview

The Smart Honeypot Orchestrator is responsible for managing the lifecycle of multiple honeypot containers in a Docker environment. It provides centralized control over honeypot deployment, continuously monitors their health, and automatically recovers failed services by restarting stopped containers.

The orchestrator is designed to work with Docker containers and a YAML-based configuration file, allowing new honeypots to be added without modifying the application logic.

---

## Features

- Automatic startup of enabled honeypots
- Continuous health monitoring
- Automatic restart of stopped containers
- Docker SDK integration
- YAML-based configuration
- Centralized logging
- Modular and extensible architecture

---

## Architecture

```
                config.yaml
                     │
                     ▼
             Configuration Loader
                     │
                     ▼
               Orchestrator
          ┌──────────┴──────────┐
          ▼                     ▼
   Docker Manager         Health Monitor
          │                     │
          └──────────┬──────────┘
                     ▼
               Docker Engine
                     │
                     ▼
     Cowrie • Tanner • Dionaea
```

---

## Project Structure

```
Smart-Honeypot-Orchestrator/
│
├── app.py
├── config.yaml
│
├── core/
│   ├── orchestrator.py
│   └── docker_manager.py
│
├── utils/
│   ├── config_loader.py
│   └── logger.py
│
└── logs/
```

---

## Components

### Orchestrator

Responsible for:

- Loading configuration
- Starting enabled honeypots
- Monitoring container health
- Restarting failed containers
- Managing the monitoring loop

---

### Docker Manager

Provides an abstraction layer over the Docker SDK.

Supported operations include:

- Start container
- Stop container
- Restart container
- Retrieve container status

---

## Configuration

The orchestrator uses a YAML configuration file.

Example:

```yaml
honeypots:

  cowrie:
    enabled: true
    container_name: cowrie

  tanner:
    enabled: true
    container_name: tanner

  dionaea:
    enabled: false
    container_name: dionaea
```

Each honeypot can be enabled or disabled without modifying the source code.

---

## Monitoring

The orchestrator performs a health check every **30 seconds**.

For each enabled honeypot it:

1. Retrieves the current container status.
2. Verifies whether the container is running.
3. Automatically restarts stopped containers.
4. Records all operations in the application logs.

---

## Requirements

- Python 3.8+
- Docker Desktop
- Docker SDK for Python

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Orchestrator

```bash
python app.py
```

---

## Example Log Output

```
Initializing Orchestrator...

Starting Docker Container: cowrie
Starting Docker Container: tanner

cowrie is running.
tanner is running.

Checking status of cowrie...
Checking status of tanner...
```

If a container stops unexpectedly:

```
cowrie stopped.
Restarting Docker Container: cowrie
cowrie restarted successfully.
```

---

## Technologies

- Python
- Docker SDK for Python
- Docker Engine
- YAML
- Logging Module

---

## License

This project is part of the **Smart Honeypot Orchestrator & Threat Intelligence Dashboard** master's project and is intended for academic and research purposes.