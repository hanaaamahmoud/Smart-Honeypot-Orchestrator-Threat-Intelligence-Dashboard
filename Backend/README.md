# Smart Honeypot Backend

Backend API for the **Smart Honeypot Orchestrator & Threat Intelligence Dashboard**.

The backend is the main application layer between the frontend dashboard, the Honeypot Orchestrator, Elasticsearch, and the authentication/user-management system.

---

## Overview

The Smart Honeypot Backend is built using **FastAPI** and is responsible for:

- Providing REST APIs for dashboard statistics, recent events, and top attackers — backed by **real data from Elasticsearch**.
- Integrating with the Honeypot Orchestrator to retrieve honeypot status.
- Streaming live attack events through WebSockets, sourced from Elasticsearch.
- Providing a full authentication and authorization system (JWT-based, role-based access control).
- Managing users, organizations, and audit logs via PostgreSQL.

---

## Architecture

```text
                         ┌─────────────────────┐
                         │     Frontend         │
                         │     Dashboard (Vue)  │
                         └──────────┬──────────┘
                                    │
                              REST / WebSocket
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   FastAPI Backend    │
                         │                      │
                         │  REST APIs           │
                         │  WebSocket           │
                         │  Auth / RBAC         │
                         └───┬─────┬──────┬─────┘
                             │     │      │
                REST         │     │      │  SQL
                             │     │      │
                             ▼     ▼      ▼
                   ┌────────────┐ ┌──────────────┐ ┌──────────────┐
                   │Orchestrator│ │ Elasticsearch│ │ PostgreSQL   │
                   │ (status)   │ │(attack events)│ │(users/org/  │
                   └─────┬──────┘ └──────────────┘ │ audit logs) │
                         │                          └──────────────┘
                         ▼
                ┌──────────────────┐
                │ Docker Honeypots │
                │ Cowrie / Dionaea │
                └──────────────────┘
```

---

## Features

### Current Features

- FastAPI-based REST API
- Honeypot status integration with the Orchestrator (`/honeypots`)
- Dashboard statistics backed by Elasticsearch aggregations (`/statistics`)
- Recent attack events backed by Elasticsearch (`/events/recent`)
- Top attackers backed by Elasticsearch aggregations (`/attackers/top`)
- WebSocket live attack event streaming, polling Elasticsearch for new events
- Unified attack-event schema aligned with the 24-field Logstash schema
- JWT-based authentication (access + refresh tokens)
- Role-based access control (`admin`, `sub-admin`, `analyst`, `reader`)
- Account activation via email token flow
- Forgot password / reset password flow
- Login rate limiting (lockout after repeated failed attempts)
- Audit logging of key security events (login, logout, user creation, password changes)
- CORS configured for the frontend origin

### Planned / In Progress

- `country` field on top attackers
- GeoIP-enriched top attackers and richer geographic breakdowns
- Full API documentation of the auth flow in Swagger via updated `response_model`s
- Secure production values for `JWT_SECRET_KEY` and database credentials

---

## Project Structure

```text
Backend/
│
├── app/
│   │
│   ├── main.py                     # FastAPI app, routes, auth wiring
│   │
│   ├── core/
│   │   ├── config.py                # Settings loaded from .env
│   │   └── security.py              # Password hashing, JWT creation/verification
│   │
│   ├── db/
│   │   ├── session.py                # SQLAlchemy engine/session
│   │   └── init_db.py                # Creates DB tables
│   │
│   ├── models/
│   │   ├── schemas.py                 # Pydantic request/response schemas
│   │   └── db_models/
│   │       ├── organization.py
│   │       ├── user.py
│   │       ├── activation_token.py
│   │       ├── password_reset_token.py
│   │       └── audit_log.py
│   │
│   ├── services/
│   │   ├── es_client.py               # Elasticsearch connection
│   │   ├── statistics_service.py      # Aggregation queries against Elasticsearch
│   │   ├── audit_service.py           # Writes audit log entries
│   │   ├── seed_admin.py              # Creates a default admin user
│   │   ├── seed_demo_users.py         # Creates demo users for each role
│   │   └── reset_admin_password.py    # Resets the default admin's password
│   │
│   └── websocket/
│       ├── manager.py                 # Tracks active WebSocket connections
│       └── producer.py                # Polls Elasticsearch and broadcasts new events
│
├── requirements.txt
└── README.md
```

---

## Main Components

### FastAPI Application — `app/main.py`

Entry point of the backend. Wires together:
- REST routes (dashboard + auth + user management + audit logs)
- WebSocket endpoint
- Orchestrator integration
- Application lifecycle (starts/stops the Elasticsearch event producer)

### Data Models — `app/models/schemas.py`

Pydantic schemas used for request validation and response documentation. Includes dashboard schemas (`StatisticsResponse`, `RecentEvent`, `TopAttacker`, `HoneypotStatus`, `AttackEvent`) and authentication schemas (`LoginRequest`, `LoginResponse`, `CreateUserRequest`, `ActivateRequest`, `ForgotPasswordRequest`, `ResetPasswordRequest`, `UserResponse`).

### Elasticsearch Client — `app/services/es_client.py`

Single shared Elasticsearch client, configured via the `ES_HOST` and `ES_INDEX` environment variables (defaults to `http://localhost:9200` and `honeypot-events`).

### Statistics Service — `app/services/statistics_service.py`

Runs aggregation queries against the `honeypot-events` index:
- `get_statistics()` — total attack count, unique attacker count (cardinality on `source_ip`), and top countries
- `get_recent_events()` — most recent events sorted by timestamp
- `get_top_attackers()` — top source IPs by event count

### WebSocket Manager — `app/websocket/manager.py`

Manages active WebSocket connections: accepting, tracking, removing disconnected clients, and broadcasting events.

### Event Producer — `app/websocket/producer.py`

Polls Elasticsearch every 5 seconds for events newer than the last broadcast timestamp, and pushes them to all connected WebSocket clients.

### Authentication & Security — `app/core/security.py`, `app/core/config.py`

- Password hashing via `bcrypt` (through `passlib`)
- JWT access and refresh token creation/verification (`python-jose`)
- Settings (database URL, JWT secret, token lifetimes, orchestrator URL) loaded from `.env` via `pydantic-settings`

### Database Models — `app/models/db_models/`

SQLAlchemy models backing PostgreSQL:
- `Organization` — tenant/organization record
- `User` — email, hashed password, role, status, organization link
- `ActivationToken` / `PasswordResetToken` — single-use, expiring tokens
- `AuditLog` — records of security-relevant actions

---

## REST API

### Health Check
`GET /`
```json
{ "message": "Smart Honeypot Backend is running" }
```

### Honeypot Status
`GET /honeypots` — proxies the Orchestrator's `/status` endpoint.

### Dashboard Statistics
`GET /statistics` — total attacks, unique attackers, top countries (from Elasticsearch).

### Recent Attack Events
`GET /events/recent` — most recent normalized events.

### Top Attackers
`GET /attackers/top` — top source IPs by attack count.

### WebSocket — Live Attack Events
`ws://127.0.0.1:8001/ws` — streams new events as they appear in Elasticsearch.

### Authentication
- `POST /api/auth/login` — returns access + refresh tokens
- `GET /api/auth/me` — returns the current authenticated user
- `POST /api/auth/logout`
- `POST /api/auth/activate` — sets a password for a newly created account
- `POST /api/auth/resend-activation` — admin/sub-admin only
- `POST /api/auth/forgot-password`
- `POST /api/auth/reset-password`

### User Management
- `POST /api/users` — create a user (admin/sub-admin only, role-restricted)

### Audit Logs
- `GET /api/audit-logs` — admin/sub-admin only

---

## Orchestrator Integration

Configured via `ORCHESTRATOR_URL` in `.env` (default `http://127.0.0.1:8000`). The backend only reads honeypot status from the Orchestrator; it does not manage or restart containers itself.

---

## Development Setup

### Requirements
- Python 3.8+
- PostgreSQL (locally, via Docker is fine — see below)
- Elasticsearch + Logstash running (see the `elk/` directory)
- FastAPI, Uvicorn, SQLAlchemy, Pydantic, python-jose, passlib, elasticsearch-py

### Installation
```bash
python -m venv venv
# Windows
venv\Scripts\activate
pip install -r requirements.txt
```

### Run PostgreSQL (if not already running)
```bash
docker run --name hp-postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_USER=postgres -e POSTGRES_DB=honeypot_platform -p 5432:5432 -d postgres:16
```

### Create database tables
```bash
python -m app.db.init_db
```

### Seed a default admin user
```bash
python -m app.services.seed_admin
```
Creates `admin@test.com` / `Admin@12345` (change this password in any real deployment).

### Run the Backend
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
```

### Access
- API base: `http://127.0.0.1:8001`
- Swagger UI: `http://127.0.0.1:8001/docs`
- ReDoc: `http://127.0.0.1:8001/redoc`

> The WebSocket endpoint (`/ws`) is not shown in Swagger UI; test it separately, e.g. with `test_websocket.py`.

---

## Data Flow

```text
Honeypots (Cowrie, Dionaea)
   │
   ▼
Logstash (normalization + GeoIP enrichment)
   │
   ▼
Elasticsearch (honeypot-events index)
   │
   ▼
FastAPI Backend
   ├──► REST APIs ─► Dashboard
   └──► WebSocket ─► Live Attack Events
```

---

## License

This project is part of the **Smart Honeypot Orchestrator & Threat Intelligence Dashboard** master's project and is intended for academic and research purposes.