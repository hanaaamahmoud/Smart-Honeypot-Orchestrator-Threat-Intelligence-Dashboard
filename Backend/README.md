# Smart Honeypot Backend

Backend API for the **Smart Honeypot Orchestrator & Threat Intelligence Dashboard**.

The backend acts as the main application layer between the frontend dashboard, the Honeypot Orchestrator, and the data/analytics services.

It provides REST APIs for dashboard data, honeypot status integration, and WebSocket-based real-time attack events.

---

## Overview

The Smart Honeypot Backend is built using **FastAPI** and is responsible for:

- Providing REST APIs for the frontend dashboard.
- Integrating with the Honeypot Orchestrator.
- Retrieving honeypot status information.
- Providing attack statistics and recent events.
- Streaming live attack events through WebSockets.
- Providing a unified attack-event data model.
- Preparing the application for Elasticsearch integration.
- Supporting future authentication, authorization, and user management.

---

## Architecture

```text
                         ┌─────────────────────┐
                         │     Frontend        │
                         │     Dashboard       │
                         └──────────┬──────────┘
                                    │
                              REST / WebSocket
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │   FastAPI Backend   │
                         │                     │
                         │  REST APIs          │
                         │  WebSocket          │
                         │  Data Models        │
                         └───────┬─────┬───────┘
                                 │     │
                    REST         │     │     WebSocket
                                 │     │
                                 ▼     ▼
                       ┌────────────┐  ┌────────────────┐
                       │Orchestrator│  │ Attack Events  │
                       │            │  │ / Event Stream │
                       └─────┬──────┘  └────────────────┘
                             │
                             ▼
                    ┌──────────────────┐
                    │ Docker Honeypots │
                    │                  │
                    │ Cowrie           │
                    │ Tanner           │
                    │ Dionaea          │
                    └──────────────────┘

---

## Features

### Current Features

- FastAPI-based REST API
- Honeypot status integration with the Orchestrator
- Dashboard statistics endpoints
- Recent attack events endpoint
- Top attackers endpoint
- Attack distribution by country
- WebSocket live attack events
- Unified `AttackEvent` schema
- Mock attack-event producer for development and testing
- Pydantic response validation

### Planned Integration

- Elasticsearch
- Authentication
- Role-Based Access Control (RBAC)
- User management
- Organization/company management
- Secure WebSocket authentication
- Real attack-log ingestion
- GeoIP-enriched attack data

---

## Project Structure

```text
Backend/
│
├── app/
│   │
│   ├── main.py
│   │
│   ├── models/
│   │   └── schemas.py
│   │
│   ├── data/
│   │   └── mock_data.py
│   │
│   └── websocket/
│       ├── manager.py
│       └── producer.py
│
├── test_websocket.py
│
├── requirements.txt
│
└── README.md
---

##  Main Components

### **FastAPI Application**
**File:** `app/main.py`  
This is the main entry point of the backend application.  
It provides:
- REST API routes  
- WebSocket endpoint  
- Orchestrator integration  
- Application lifecycle management  
- Mock event producer startup  

---

### **Data Models**
**File:** `app/models/schemas.py`  
Defines the **Pydantic schemas** used by the backend.

**Main models include:**
- `HoneypotStatus`
- `StatisticsResponse`
- `RecentEvent`
- `TopAttacker`
- `CountryAttacks`
- `AttackEvent`

> The `AttackEvent` model provides a unified structure for attack events collected from different honeypots.

---

### **WebSocket Manager**
**File:** `app/websocket/manager.py`  
Manages active WebSocket connections.

**Responsibilities:**
- Accepting WebSocket connections  
- Tracking connected clients  
- Removing disconnected clients  
- Broadcasting attack events to connected clients  

---

### **Event Producer**
**File:** `app/websocket/producer.py`  
Provides a **mock attack-event producer** for development and testing.

**Generated event fields:**
- Timestamp  
- Honeypot  
- Protocol  
- Source/Destination IP & Port  
- Session ID  
- Authentication attempts  
- Country & ASN  
- Attack type  
- Severity  
- Dataset source  

> The producer broadcasts new events periodically to connected WebSocket clients.  
> It will later be replaced by real attack-event ingestion after Elasticsearch integration.

---

##  REST API

### **Health Check**
`GET /`  
**Response:**
```json
{
  "message": "Smart Honeypot Backend is running"
}

---

##  Honeypot Status
**GET** `/honeypots`  
Returns the current status of configured honeypots.

## Honeypot Status
**GET** `/honeypots`  
Returns the current status of configured honeypots.

## Dashboard Statistics
**GET** `/statistics`  
Returns dashboard-level attack statistics.

## Recent Attack Events
**GET** `/events/recent`  
Returns recent attack events for the dashboard.

## Top Attackers
**GET** `/attackers/top`  
Returns IPs generating the highest number of attacks.

## WebSocket API
**Endpoint:**  
`ws://127.0.0.1:8001/ws`

After connecting, clients receive real-time attack events in JSON format.

---

## Orchestrator Integration
**Configuration:**
```python
ORCHESTRATOR_URL = "http://127.0.0.1:8000"

## Request
`GET http://127.0.0.1:8000/status`

The Orchestrator manages Docker containers and monitors honeypot services.  
The backend only retrieves status information.

---

## Development Setup

### Requirements
- Python 3.8+
- FastAPI
- Uvicorn
- Requests
- Pydantic
- WebSockets

---

### Installation
```bash
python -m venv venv
# Windows
venv\Scripts\activate
pip install -r requirements.txt

## Run Backend
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload

## Access
`http://127.0.0.1:8001`

---

## API Documentation
- Swagger UI → [http://127.0.0.1:8001/docs](http://127.0.0.1:8001/docs)
- ReDoc → [http://127.0.0.1:8001/redoc](http://127.0.0.1:8001/redoc)

Note: WebSocket endpoint is not shown in Swagger UI.

---

## WebSocket Testing
Run:
```bash
python test_websocket.py

## Data Flow
```text
Honeypots
   │
   ▼
Honeypot Orchestrator
   │
   ▼
Log Collection & Processing
   │
   ▼
Elasticsearch
   │
   ▼
FastAPI Backend
   ├──► REST APIs ─► Dashboard
   └──► WebSocket ─► Live Attack Events

---

## Authentication & Authorization
Planned features:
- User authentication
- Role-Based Access Control (RBAC)
- User management
- Protected REST & WebSocket APIs
- Organization-level support

---

## License
This project is part of the Smart Honeypot Orchestrator & Threat Intelligence Dashboard master’s project.  
Intended for academic and research purposes only.

