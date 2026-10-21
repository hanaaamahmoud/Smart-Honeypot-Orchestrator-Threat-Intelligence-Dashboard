# Smart Honeypot Backend

FastAPI backend of the **Smart Honeypot Orchestrator & Threat Intelligence Dashboard**. It sits between the dashboard and the data sources: it reads normalized attack events from Elasticsearch, serves precomputed machine-learning analytics, reports honeypot health from the Orchestrator, and manages users and access in PostgreSQL.

The backend never talks to the honeypots directly and never runs the ML model.

---

## 1. Responsibilities

- **Live statistics:** read-only aggregations over the `honeypot-events` index (Elasticsearch).
- **Live feed:** a WebSocket channel that pushes new events to connected dashboards.
- **ML analytics:** serves the JSON files produced by the ML service (clusters, temporal patterns, sessions, MITRE ATT&CK, session replay).
- **Honeypot status:** proxies the Orchestrator's `/status` endpoint.
- **Authentication and administration:** JWT login, role-based access, account activation, password reset, user creation, and an audit log (PostgreSQL).

## 2. Architecture

```mermaid
flowchart LR
  F["Dashboard"] -->|"REST and WebSocket"| B["FastAPI Backend :8001"]
  B -->|"aggregations, polling"| E["Elasticsearch"]
  B -->|"users, tokens, audit logs"| P["PostgreSQL"]
  B -->|"GET /status"| O["Orchestrator status API"]
  B -->|"reads JSON files"| M["app/data/ml_analytics"]
```

## 3. Project structure

```text
Backend/
├── Dockerfile
├── requirements.txt
├── test_websocket.py             # WebSocket test client
└── app/
    ├── main.py                   # routes, auth wiring, lifespan
    ├── core/
    │   ├── config.py             # settings from environment / .env
    │   └── security.py           # password hashing, JWT, token hashing
    ├── db/
    │   ├── session.py            # SQLAlchemy engine and session
    │   └── init_db.py            # creates the tables
    ├── models/
    │   ├── schemas.py            # Pydantic request/response models
    │   └── db_models/            # Organization, User, ActivationToken,
    │                             # PasswordResetToken, AuditLog
    ├── services/
    │   ├── es_client.py          # shared Elasticsearch client
    │   ├── live_service.py       # /api/live/* aggregations
    │   ├── statistics_service.py # /statistics, recent events, top attackers
    │   ├── ml_service.py         # loads the ML analytics JSON files
    │   ├── audit_service.py      # writes audit log entries
    │   ├── seed_admin.py         # creates the initial admin
    │   ├── seed_demo_users.py    # demo users, one per role (development)
    │   └── reset_admin_password.py
    ├── websocket/
    │   ├── manager.py            # active connections and broadcast
    │   └── producer.py           # polls Elasticsearch and broadcasts
    └── data/
        └── ml_analytics/         # ML output files (must be provided, see 6)
```

## 4. Configuration

Settings are read from environment variables or a `.env` file in `Backend/`.

| Variable | Description | Default |
|---|---|---|
| `DATABASE_URL` | SQLAlchemy URL, for example `postgresql+psycopg://user:password@host:5432/honeypot_platform` | required |
| `JWT_SECRET_KEY` | Secret used to sign tokens (use a long random value) | required |
| `JWT_ALGORITHM` | Signing algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Access token lifetime | `15` |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token lifetime | `7` |
| `ORCHESTRATOR_URL` | Base URL of the Orchestrator status API | `http://127.0.0.1:8000` |
| `ES_HOST` | Elasticsearch URL | `http://localhost:9200` |
| `ES_INDEX` | Index with the unified events | `honeypot-events` |

`ES_HOST` and `ES_INDEX` are read directly from the process environment, not from the `.env` file. With Docker Compose they are set by the compose file; for a local run, export them in the shell before starting the backend. The other variables work from either source.

The driver `psycopg[binary]` (version 3) is required by the `postgresql+psycopg://` URL.

## 5. Running

### With Docker (recommended)

From the repository root, the root `docker-compose.yml` starts the backend together with PostgreSQL and Elasticsearch, creates the tables, and seeds the initial admin on startup:

```bash
docker compose up -d --build backend
```

### Locally

```bash
cd Backend
python -m venv venv
source venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.txt

# PostgreSQL (if not already running)
docker run --name hp-postgres -e POSTGRES_USER=<user> -e POSTGRES_PASSWORD=<password> \
  -e POSTGRES_DB=honeypot_platform -p 5432:5432 -d postgres:16

python -m app.db.init_db            # create tables
python -m app.services.seed_admin   # create the initial admin
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

| | |
|---|---|
| API | `http://127.0.0.1:8001` |
| Swagger UI | `http://127.0.0.1:8001/docs` |
| ReDoc | `http://127.0.0.1:8001/redoc` |
| WebSocket | `ws://127.0.0.1:8001/ws` (not shown in Swagger; use `test_websocket.py`) |

### Initial accounts

The seed scripts create accounts for development and demonstration. The passwords are fixed in the scripts, so change or remove these accounts before any shared deployment.

| Created by | Email | Password | Role |
|---|---|---|---|
| `seed_admin` (runs automatically with Docker Compose) | `admin@test.com` | `Admin@12345` | admin |
| `seed_demo_users` (optional, one account per role) | `admin@smarthoneypot.local` | `Admin@123456` | admin |
| | `subadmin@smarthoneypot.local` | `SubAdmin@123456` | sub-admin |
| | `analyst@smarthoneypot.local` | `Analyst@123456` | analyst |
| | `reader@smarthoneypot.local` | `Reader@123456` | reader |

To create the demo users in the Docker setup:

```bash
docker compose exec backend python -m app.services.seed_demo_users
```

There is no endpoint for changing a password while logged in. A password can be changed through the forgot-password and reset-password flow, or by running `reset_admin_password.py` (which resets `admin@test.com` to `Admin@12345`).

## 6. ML analytics files

The `/api/ml/*` endpoints read precomputed files from `app/data/ml_analytics/`. These files are generated by the ML service (`ML_SERVICE/scripts/package_handoff.sh`) and must be copied there:

```text
app/data/ml_analytics/
├── cluster_analytics.json
├── temporal_analytics.json
├── session_analytics.json
├── mitre_analytics.json
├── mitre_statistics.json
├── mitre_trends.json
├── session_replay_list.json
└── session_replay_details/<session_id>.json
```

If a file is missing, the matching endpoint returns HTTP 503. The files are cached in memory after the first read, so the backend must be restarted after they are replaced.

## 7. API reference

Interactive documentation is generated at `/docs`.

### General and dashboard

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Health check |
| GET | `/honeypots` | Honeypot status from the Orchestrator (503 if unreachable) |
| GET | `/statistics` | Total attacks, unique attackers, top countries |
| GET | `/events/recent` | Most recent events |
| GET | `/attackers/top` | Top source IPs |
| WS | `/ws` | Live event stream |

### Live events (`/api/live/*`)

Read-only Elasticsearch aggregations.

| Endpoint | Returns |
|---|---|
| `/kpis` | Total events, unique IPs, unique countries, active honeypots |
| `/by-honeypot`, `/by-protocol`, `/by-severity`, `/by-country`, `/by-mitre`, `/by-reputation` | List of `{name, value}` |
| `/top-attackers` | Top source IPs with counts |
| `/timeline` | Events per day |
| `/recent` | The 50 most recent events |

### ML analytics (`/api/ml/*`)

| Endpoint | Description |
|---|---|
| `/clusters` | Cluster analytics |
| `/temporal` | Temporal analytics |
| `/sessions/summary` | Session KPIs and distributions |
| `/sessions/alerts` | Critical alerts (`count` and `alerts`) |
| `/sessions/top-attackers` | Top source IPs from the session analytics |
| `/mitre`, `/mitre/statistics`, `/mitre/trends` | MITRE ATT&CK analytics, statistics, and trends |
| `/session-replay` | Session list |
| `/session-replay/{session_id}` | One session (404 if unknown) |

### Authentication and administration

| Method | Endpoint | Access |
|---|---|---|
| POST | `/api/auth/login` | Public |
| GET | `/api/auth/me` | Any active user |
| POST | `/api/auth/logout` | Any active user |
| POST | `/api/auth/activate` | Public, with an activation token |
| POST | `/api/auth/resend-activation` | admin, sub-admin (same organization) |
| POST | `/api/auth/forgot-password` | Public |
| POST | `/api/auth/reset-password` | Public, with a reset token |
| POST | `/api/users` | admin, sub-admin |
| GET | `/api/audit-logs` | admin (all), sub-admin (own and system entries) |
| GET | `/api/admin-only` | admin |
| GET | `/api/analysis` | admin, sub-admin, analyst |

## 8. Authentication and roles

- **Tokens:** JWT access tokens (15 minutes) and refresh tokens (7 days). Passwords are hashed with bcrypt. Activation and reset tokens are random, stored as SHA-256 hashes, single-use, and expire after 30 minutes.
- **Roles:** `admin`, `sub-admin`, `analyst`, `reader`. An admin can create any role; a sub-admin can create analysts and readers.
- **Account lifecycle:** a new account is `pending` and has no password until it is activated through its token.
- **Rate limiting:** five failed logins for the same email within 15 minutes lock that email temporarily (HTTP 429).
- **Audit log:** login (success and failure), logout, activation, password reset or change, and user creation are recorded with the client address and user agent.

## 9. Real-time channel

A background task started with the application polls Elasticsearch every five seconds and broadcasts events to all connected WebSocket clients. Each poll returns up to 50 events, oldest first, newer than the last one sent. On startup the task has no starting point, so it first works through the events already stored (50 per poll) and then follows new ones. Clients connected during this catch-up receive older events.

If Elasticsearch or the `honeypot-events` index is not available when the backend starts, the task stops with an error. Restart the backend once Elasticsearch contains data.

## 10. Error handling

| Situation | Response |
|---|---|
| Elasticsearch or ML files unavailable | 503 with a detail message |
| Orchestrator unreachable | 503 `ORCHESTRATOR_UNAVAILABLE` |
| Unknown session replay | 404 |
| Invalid or expired token | 401 with a machine-readable `code` |
| Insufficient role or inactive account | 403 with a machine-readable `code` |
| Too many failed logins | 429 |

## 11. Security notes and limitations

- The dashboard data endpoints (`/api/live/*`, `/api/ml/*`, `/statistics`, and so on) and the WebSocket do not require authentication in the current version. Role checks apply to the authentication and administration endpoints; adding `Depends(require_roles([...]))` to the data routes is the next hardening step.
- Activation and reset tokens are returned in the API response (`*_for_testing` fields) because no email service is connected. This must be replaced with email delivery before any real deployment.
- No refresh endpoint is implemented yet: refresh tokens are issued at login but cannot be exchanged.
- Failed-login counters are kept in memory, so they are per process and reset on restart.
- CORS allows the origin `http://localhost:3000` only.
- ML analytics are served from files and refreshed manually.
- The live-feed task does not recover from an Elasticsearch error: if the index is missing or Elasticsearch is down at startup, the backend must be restarted (see section 9).
- The `/api/live/*` aggregations use the field names directly, while `/statistics` and `/attackers/top` use the `.keyword` sub-fields. Which family works depends on how Elasticsearch mapped the fields (see section 12).
- The live feed uses the event timestamp as its position marker, so several events with an identical timestamp can be missed.

## 12. Troubleshooting

| Symptom | Likely cause and fix |
|---|---|
| `/api/live/*` returns 503 mentioning `fielddata` | The fields are mapped as `text` (Elasticsearch default for an index created without a template). These endpoints need the fields mapped as `keyword`; `/statistics` and `/attackers/top` need the opposite (`.keyword` sub-fields). Create the `honeypot-events` index with the mapping used in the ELK setup before ingesting data, and check both endpoint families after a fresh install. |
| `/statistics` or `/attackers/top` returns 503 mentioning a missing field | The fields are mapped as `keyword` directly, so the `.keyword` sub-field does not exist (see the row above). |
| `/api/ml/*` returns 503 | `app/data/ml_analytics/` is missing or incomplete (see section 6). |
| `/honeypots` returns 503 | The Orchestrator status API is not reachable. Check `ORCHESTRATOR_URL` and, when it runs on a remote host, the SSH tunnel. |
| Backend exits on startup | `DATABASE_URL` or `JWT_SECRET_KEY` is missing, or PostgreSQL is not ready. |
| WebSocket connects but stays silent | There are no new events, or the live-feed task stopped because Elasticsearch had no index at startup. Check the backend log, make sure the index contains data, and restart the backend. |

## 13. Testing

- Explore and test endpoints interactively with Swagger UI.
- Test the WebSocket stream: `python test_websocket.py` (the backend must be running).