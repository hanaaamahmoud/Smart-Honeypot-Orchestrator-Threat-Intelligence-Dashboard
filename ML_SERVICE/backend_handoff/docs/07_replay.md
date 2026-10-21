# Session Replay

Per-session narratives and event timelines.

| Item | Value |
|---|---|
| Data files | session_replay_list.json + session_replay_details/<id>.json |
| Schema | 07_session_replay/schema_list.json + schema_detail.json |
| Endpoint | /api/ml/session-replay + /api/ml/session-replay/{id} |

## List Item

| Field | Type | Description |
|---|---|---|
| id | string | Session ID |
| events | int | Event count |
| duration | float | Duration in seconds |
| honeypot | string | Honeypot name |
| protocol | string | Protocol |
| country | string | Source country |
| attack | string | Attack type |
| mitre | string | MITRE technique |
| severity | string | Severity level |
| flags | object | Boolean flags |
| has_replay | bool | true if detail file exists |

## Flags

| Flag | Meaning |
|---|---|
| is_suspicious | Any strong signal |
| is_brute_force_candidate | auth > 3 or usernames > 3 |
| has_commands_executed | command_count > 0 |
| has_attack_classification | has attack_type or mitre |
| is_large_session | events > 50 |
| is_long_running | duration > 3600s |
| is_multi_ip | > 5 source IPs |
| is_high_severity | severity in (High, Critical) |
| is_medium_or_higher_severity | severity in (Medium, High, Critical) |

## Detail File

    {
      "id": "...",
      "summary": { ... },
      "narrative": {
        "steps": [ ... ],
        "phases": [ ... ],
        "total_steps": N
      },
      "events": [ ... ]
    }

## Narrative Step

| Field | Type | Description |
|---|---|---|
| index | int | Step number |
| offset_seconds | float | Time since first event |
| phase | string | connection, auth, command, activity, disconnect |
| step_type | string | Detailed type |
| icon | string | Display icon |
| title | string | Display title |
| details | array | [{label, value}] pairs |
| timestamp | string | Event timestamp |

## Notes

- Only sessions with has_replay=true have a detail file.
- Load details on demand — never bulk.
- 404 for sessions without a detail file.
