# 📦 Session Replay — Backend Handoff

## 🎯 What is this?

Per-session event timelines for the Smart Honeypot dashboard.

Allows users to "replay" a session event-by-event — like a video.

## 📊 Data Snapshot

- Total sessions: 11,879
- Replay-worthy sessions: **367** (with full detail files)
- Others: **summary only** (still in the list, `has_replay=false`)

## 📁 Folder Structure
07_session_replay/
├── README.md ← this file
├── session_replay_list.json ← ~7.5 MB — full table data
├── schema_list.json ← list schema
├── schema_detail.json ← detail schema
└── details/ ← 367 files
├── <session_id>.json ← full replay for each important session
└── ...

text

## 🔗 Suggested Endpoints
1. List (recommended: server-side pagination)
GET /api/ml/sessions/replay?page=1&page_size=20
→ reads from session_replay_list.json

2. Filter: only replay-worthy
GET /api/ml/sessions/replay?only_replay_worthy=true
→ sessions where has_replay == true

3. Detail (single session — on demand)
GET /api/ml/sessions/replay/{session_id}
→ reads from details/{session_id}.json
→ returns 404 if session has no detail file

text

## 🎨 Frontend Flow

### Step 1 — Load list ONCE at startup
```javascript
// ~7.5 MB raw → ~1 MB with gzip
const list = await fetch('/api/ml/sessions/replay-list').then(r => r.json());
Step 2 — Sessions Table (20 per page)
jsx
list.sessions
  .slice((page-1)*20, page*20)
  .map(s => (
    <tr key={s.id}>
      <td>{s.id}</td>
      <td>{s.events}</td>
      <td>{s.country}</td>
      <td>{s.attack}</td>
      <td>{s.severity}</td>
      <td>
        {s.has_replay
          ? <button onClick={() => openReplay(s.id)}>🎬 Replay</button>
          : <button onClick={() => openDetails(s.id)}>📋 Details</button>
        }
      </td>
    </tr>
  ))
Step 3 — On [🎬 Replay] click
javascript
async function openReplay(sessionId) {
  const detail = await fetch(`/api/ml/sessions/replay/${sessionId}`).then(r => r.json());
  showReplayModal(detail);
}
Step 4 — Filters available
Filter	Sessions
All	11,879 (paginated)
🎬 Replay-Worthy	367
High Severity	8
Brute Force Candidates	178
📐 session_replay_list.json Schema
json
{
  "contract_name": "SESSION_REPLAY_LIST",
  "contract_version": "3.0.0",
  "generated_at": "ISO-8601",
  "total_sessions": 11879,
  "replay_worthy_count": 367,
  "sessions": [
    {
      "id": "ade88c93-30a2-4cd0-902c-9b7f99df6579",
      "events": 522,
      "duration": 77494.66,
      "honeypot": "tanner",
      "protocol": "HTTP",
      "country": "Japan",
      "attack": "HTTP Exploitation",
      "mitre": "T1190",
      "severity": "Medium",
      "flags": {
        "is_suspicious": true,
        "is_brute_force_candidate": false,
        "has_commands_executed": false,
        "has_attack_classification": true,
        "is_large_session": true,
        "is_long_running": true,
        "is_multi_ip": true,
        "is_high_severity": false,
        "is_medium_or_higher_severity": true
      },
      "has_replay": true
    }
  ]
}
Field Reference
Field	Type	Description
id	string	Session ID
events	int	Event count
duration	float	Session duration (seconds)
honeypot	string|null	cowrie / tanner / dionaea
protocol	string|null	SSH / HTTP / FTP
country	string|null	Source country
attack	string|null	Attack type
mitre	string|null	MITRE technique
severity	string|null	Low / Medium / High / Critical
flags	object	Boolean flags (see below)
has_replay	bool	true → detail file available
Flags Reference
Flag	Meaning
is_suspicious	Any strong signal (severity, size, multi-IP, commands)
is_brute_force_candidate	auth > 3 OR unique usernames > 3
has_commands_executed	command_count > 0
has_attack_classification	Has attack_type or mitre_technique
is_large_session	events > 50
is_long_running	duration > 3600s
is_multi_ip	> 5 source IPs
is_high_severity	severity in (High, Critical)
is_medium_or_higher_severity	severity in (Medium, High, Critical)
📐 details/{session_id}.json Schema
json
{
  "id": "ade88c93-30a2-4cd0-902c-9b7f99df6579",
  "summary": { /* see list entry + extra */ },
  "narrative": {
    "steps": [
      {
        "index": 1,
        "offset_seconds": 0.0,
        "phase": "connection",
        "step_type": "connection",
        "icon": "🚪",
        "title": "CONNECTION ESTABLISHED",
        "details": [
          {"label": "From", "value": "45.243.162.246:33815.0"},
          {"label": "Port", "value": 80.0},
          {"label": "Protocol", "value": "HTTP"},
          {"label": "Honeypot", "value": "tanner"}
        ],
        "timestamp": "2020-01-22T04:56:10.963441+00:00"
      }
    ],
    "phases": [
      {
        "phase": "connection",
        "started_at_seconds": 0.0,
        "ended_at_seconds": 0.0,
        "step_count": 1,
        "steps": [ /* ... */ ]
      }
    ],
    "total_steps": 522
  },
  "events": [ /* full event list */ ]
}
Narrative Step Types
step_type	Icon	Meaning
connection	🚪	Session started
auth_attempt	🔑	Login attempt (has username/password)
auth_counter	🔑	Auth counters present
command	💻	Command executed
activity	📌	Generic activity
disconnect	🔚	Session ended
🎨 UI Recommendations
Sessions Table (from list.json)
Paginate: 20 rows per page

Columns: Session ID | Events | Country | Attack | Severity | Action

Filters:

All / Replay-Worthy / High Severity / Brute Force

Country dropdown

Honeypot dropdown

Replay Modal (from detail.json)
Header: Session ID + context (honeypot · protocol · country)

Classification card: Attack / MITRE / Stage / Severity

Flags bar: Badges for each active flag

Timeline: Vertical timeline with icons + details per step

Show first 20 steps

"Load more" button

Pagination: Never load all 522 steps at once

⚠️ Critical Rules
List is 7.5 MB raw → enable gzip on backend (→ ~1 MB)

Load details only on demand — never bulk

Never fabricate: all data comes from source events

has_replay=true → detail exists, else 404

Null handling: optional fields may be null

Timestamps: ISO-8601 UTC

🔄 Refresh Cadence
Regenerated on each ML pipeline run

generated_at marks the last run

📞 Contact
ML Service Owner: (fill)

Backend Integration Lead: (fill)

Frontend Lead: (fill)
