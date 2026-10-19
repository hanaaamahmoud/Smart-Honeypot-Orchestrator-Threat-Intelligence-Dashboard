# Smart Honeypot Frontend integration notes

## What changed
- Dashboard overview now loads the live Elasticsearch-backed endpoints through the backend API.
- Added a dedicated `Threat Intelligence / ML` page at `/threat-intelligence`.
- Added a responsive chart/table design using CSS/SVG, so no extra chart dependency is required.
- Added named `getWebSocketUrl()` export and routed WebSocket URL resolution through it. It supports `VITE_BACKEND_WS_URL`, `VITE_WS_URL`, absolute API URLs, and the `/backend` Vite proxy.
- Honeypots & Orchestrator page is preserved and remains status-only because there are no start/stop/deploy backend routes.
- No backend, Elasticsearch, or ML service files were changed.

## Live endpoints used by the Dashboard
- `GET /api/live/kpis`
- `GET /api/live/by-honeypot`
- `GET /api/live/by-protocol`
- `GET /api/live/by-severity`
- `GET /api/live/by-country`
- `GET /api/live/top-attackers`
- `GET /api/live/by-mitre`
- `GET /api/live/timeline`
- `GET /api/live/recent`
- `GET /api/live/by-reputation`

## ML endpoints used by Threat Intelligence
- `GET /api/ml/temporal`
- `GET /api/ml/sessions/summary`
- `GET /api/ml/sessions/alerts`
- `GET /api/ml/sessions/top-attackers`
- `GET /api/ml/mitre`
- `GET /api/ml/mitre/statistics`
- `GET /api/ml/mitre/trends`
- `GET /api/ml/session-replay`
- `GET /api/ml/session-replay/{session_id}`

## Known backend contract gap
The current backend imports a `get_clusters()` service function, but does not register `GET /api/ml/clusters` or `GET /api/ml/clusters/{id}`. The ML page therefore renders cluster distribution from `distributions.by_cluster` in the session-summary response and explains that detailed cluster records cannot be fetched until the backend exposes those routes. No backend changes were made.

The handoff also mentions `GET /api/ml/sessions`, but the actual backend route is `GET /api/ml/sessions/summary`; the frontend uses the actual registered route.

## Verification
- `npm run build` passes in the working copy.
- ESLint passes for the changed files: `src/App.jsx`, `src/layouts/Sidebar.jsx`, `src/pages/Dashboard.jsx`, `src/pages/ThreatIntelligence.jsx`, and `src/services/api.js`.
- The original project has unrelated pre-existing lint issues in other files; they were not changed as requested.

## Session replay presentation
- The Sessions table is backed by `GET /api/ml/session-replay` and the Replay action fetches the selected record from `GET /api/ml/session-replay/{session_id}`.
- Replay details are presented as an analyst view: session/source context, timestamps and ordered narrative steps, captured authentication attempts, command-activity counts, severity/attack classification, MITRE mapping, and the event records returned by the API. The full payload remains available in a collapsed evidence section.
- Password values are masked by default. The analyst can reveal captured *attempted* passwords; they are not represented as valid account credentials.
- Data inspection of the 367 replay detail files in the supplied Backend archive found that `commands.sample_commands` is empty in all of them, and the event records do not include raw command strings or file/hash/payload artifacts. The UI therefore shows command activity/counts when recorded, and explicitly says when command text or artifacts were not returned instead of inventing them. This is a limitation of the supplied data, not a frontend rendering issue.
- The replay view is a chronological reconstruction from ML session records, not an interactive terminal recording and does not re-execute attacker activity.

## Session and cluster endpoint compatibility
- Session summary uses the actual backend route `GET /api/ml/sessions/summary` (the handoff's `GET /api/ml/sessions` shorthand is not the registered route in the supplied Backend archive).
- The frontend requests `GET /api/ml/clusters` and uses its returned cluster records for the distribution and cluster explorer. If the running backend does not register that route, the page falls back to the cluster distribution returned in session analytics and explains that cluster detail records are unavailable. The supplied Backend archive inspected for this update does not register `/api/ml/clusters`; the separate backend handoff code shared by the team does. No backend files were changed.

## Verification for this update
- TypeScript's JSX parser reported no syntax diagnostics for `src/pages/ThreatIntelligence.jsx`.
- A full Vite production build could not be run in this environment because `npm ci` did not complete and the Vite executable was unavailable. Docker build/runtime was not executed here; use `docker compose up --build -d` in the project directory to verify in your environment.
