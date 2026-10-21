# Smart Honeypot Orchestrator

Lifecycle manager for the honeypot containers of the **Smart Honeypot Orchestrator & Threat Intelligence Dashboard**. It starts the configured honeypots, checks their health every 30 seconds, restarts any that stopped, and exposes their state through a small read-only status API.

In the deployed system the Orchestrator runs on the cloud VM, next to the honeypots it controls.

---

## 1. Features

- Starts every enabled honeypot container that is not already running
- Health check every 30 seconds, with automatic restart of stopped containers
- Read-only status API (`GET /status`) used by the backend and the dashboard
- YAML configuration: honeypots can be enabled, disabled, or renamed without code changes
- Logging to the console and to files
- Docker SDK integration, with no changes needed in the honeypots themselves

## 2. Architecture

```text
              config/config.yaml
                     │
                     ▼
             Configuration Loader
                     │
                     ▼
               Orchestrator ─────────────► Status API (GET /status)
                     │
                     ▼
               Docker Manager
                     │
                     ▼
               Docker Engine
                     │
                     ▼
     Cowrie • Tanner • Dionaea (existing containers)
```

The Orchestrator does not build or create containers. The honeypots are deployed with Docker Compose, and the Orchestrator looks each one up **by container name**. This keeps deployment (Compose) separate from runtime control (Orchestrator).

## 3. Project structure

```text
Orchestrator/
├── app.py                  # entry point: starts honeypots, runs the monitoring loop
├── requirements.txt
├── config/
│   └── config.yaml         # honeypot list
├── core/
│   ├── orchestrator.py     # startup, health check, restart, status
│   └── docker_manager.py   # Docker SDK wrapper
├── api/
│   └── status_api.py       # FastAPI status service
├── utils/
│   ├── config_loader.py    # reads config/config.yaml
│   └── logger.py           # console and file logging
└── logs/                   # orchestrator.log, docker.log (created at runtime)
```

## 4. Components

### Orchestrator (`core/orchestrator.py`)

- Loads the configuration and creates the Docker manager
- `start()` starts every enabled honeypot, then enters the monitoring loop
- `health_check()` queries each enabled container and restarts it if it is not in the `running` state
- `get_honeypot_status()` returns the state of every enabled honeypot (used by the status API)

### Docker Manager (`core/docker_manager.py`)

An abstraction over the Docker SDK (`docker.from_env()`):

| Operation | Behavior |
|---|---|
| Start | Starts the container if it is not running, otherwise logs that it is already running |
| Stop | Stops the container |
| Restart | Restarts the container |
| Status | Returns the container state (`running`, `exited`, and so on) |

If a container does not exist, the error `<name> not found` is logged and the operation is skipped. The orchestrator keeps running.

### Status API (`api/status_api.py`)

A FastAPI service with a single endpoint:

```http
GET /status
```

```json
[
  {"name": "Cowrie", "status": "running"},
  {"name": "Tanner", "status": "running"},
  {"name": "Dionaea", "status": "running"}
]
```

Only enabled honeypots are listed. A container that cannot be found is reported with the status `unknown`.

## 5. Configuration

`config/config.yaml`:

```yaml
honeypots:
  cowrie:
    enabled: true
    container_name: "cowrie"
    max_restart_attempts: 3

  tanner:
    enabled: true
    container_name: "tanner"
    max_restart_attempts: 3

  dionaea:
    enabled: true
    container_name: "dionaea"
    max_restart_attempts: 3
```

| Key | Description |
|---|---|
| `enabled` | If `false`, the honeypot is skipped (not started, not monitored, not listed in the status) |
| `container_name` | Name of the existing Docker container (must match `container_name` in the honeypot Compose file) |
| `max_restart_attempts` | Reserved. It is present in the configuration but not yet enforced by the code (see section 9) |

The configuration is read from `config/config.yaml` relative to the directory the Orchestrator is started from, so always start it from the `Orchestrator/` directory.

## 6. Monitoring

Every **30 seconds**, for each enabled honeypot:

1. Read the container status.
2. If the container is running, log `<name> is running.`
3. Otherwise log a warning and restart the container.
4. If the container does not exist, skip it (the error is logged by the Docker manager).

## 7. Requirements

- Python 3.8 or later
- Docker Engine, with the honeypot containers already created (`docker compose up -d` in the honeypots directory)
- Python packages: `docker`, `PyYAML`, `fastapi`, `uvicorn`
- The user running the Orchestrator must be allowed to use Docker (member of the `docker` group, or root)

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 8. Running

Two processes are used: the monitoring loop and the status API. Run both from the `Orchestrator/` directory.

```bash
# 1. Lifecycle and monitoring loop
python app.py

# 2. Status API, listening on the loopback interface only
uvicorn api.status_api:app --host 127.0.0.1 --port 8000
```

On the cloud VM, the status API is not exposed to the Internet. The backend reaches it through an SSH tunnel:

```bash
ssh -i <key> -p 2222 -N -L 0.0.0.0:8002:127.0.0.1:8000 <user>@<vm-address>
```

and the backend is configured with `ORCHESTRATOR_URL=http://host.docker.internal:8002` (Docker Compose setup) or `http://127.0.0.1:8002` (backend run directly on the host).

### Example log output

```text
2026-09-13 16:37:20,968 - orchestrator - INFO - Starting Orchestrator...
2026-09-13 16:37:21,889 - docker - INFO - cowrie is already running.
2026-09-13 16:37:22,426 - orchestrator - INFO - cowrie is running.
2026-09-13 16:37:22,667 - orchestrator - INFO - tanner is running.
```

If a container stops unexpectedly:

```text
orchestrator - WARNING - cowrie stopped. Restarting...
docker - INFO - Restarting Docker Container: cowrie
docker - INFO - cowrie restarted successfully.
```

If a configured container does not exist:

```text
docker - ERROR - tanner not found
```

Logs are written to `logs/orchestrator.log` and `logs/docker.log`.

## 9. Security notes and limitations

- **Docker access.** Anything that can use the Docker socket has root-equivalent control of the host. Run the Orchestrator only on the host that runs the honeypots, and never expose the status API publicly.
- **No authentication on the status API.** It is read-only and bound to `127.0.0.1`; access control relies on the SSH tunnel.
- **Existing containers only.** The Orchestrator does not create or update containers. If a container was removed, it is reported as `unknown` and must be recreated with Docker Compose.
- **No restart limit.** `max_restart_attempts` is not enforced: a container that keeps failing is restarted every 30 seconds.
- **Any non-running state is restarted**, including `exited` and `paused`.
- **Polling.** Failures are detected within one check interval (up to 30 seconds).
- **No alerting.** Failures are only written to the logs.

## 10. Technologies

Python, Docker SDK for Python, Docker Engine, FastAPI, Uvicorn, YAML.

## 11. License

This project is part of the **Smart Honeypot Orchestrator & Threat Intelligence Dashboard** master's project and is intended for academic and research purposes.