# 🎨 Frontend Handoff — Smart Honeypot Dashboard

**الهدف:** كل حاجة يحتاجها الـ Frontend team.

**مهم جدًا:** فيه **مصدرين مختلفين للبيانات**:

- 🔴 **Source A — Live Events** (من Elasticsearch مباشرة)
- 🤖 **Source B — ML Analytics** (من JSON files بتاعتنا)

**إنتِ (الـ Frontend) حر تستخدم الاتنين مع بعض، أو كل واحد في Tab/قسم منفصل.**

---

# 🔴 SOURCE A — Live Events

**المصدر:** Elasticsearch (`honeypot-events` index)
**الطريقة:** Backend يستعلم من ES مباشرة
**الملفات المرجعية:** موجودة في `BACKEND_HANDOFF/` (اللي إنتِ واخداها)

## 🎯 البيانات المتوفرة

- 58,895 events
- 26 fields per event
- 4 honeypots: cowrie / tanner / dionaea / t-pot-ftp
- GeoIP + MITRE + IP Reputation enrichment

## 📊 إيه اللي تعرضه على الـ Dashboard من Source A

### 1. KPI Cards
| Card | Value |
|---|---|
| Total Events | 58,895 |
| Unique IPs | 1,139 |
| Countries | 47 |
| Honeypots | 4 |
| Protocols | 3 (SSH/HTTP/FTP) |

### 2. Events by Honeypot (Pie Chart)
| Honeypot | Events | % |
|---|---|---|
| cowrie (SSH) | 54,934 | 93.3% |
| tanner (HTTP) | 2,544 | 4.3% |
| dionaea (FTP) | 1,342 | 2.3% |
| t-pot-ftp | 75 | 0.1% |

### 3. Events by Protocol (Pie Chart)
| Protocol | Events |
|---|---|
| SSH | 54,934 |
| HTTP | 2,544 |
| FTP | 1,417 |

### 4. Events by Severity (Bar Chart)
Low / Medium / High / Critical

### 5. Top Countries (Map + Table)
| Country | Events |
|---|---|
| Australia | 18,493 |
| United States | 11,766 |
| Hong Kong | 5,825 |
| Seychelles | 4,718 |
| China | 3,989 |
| Singapore | 1,891 |
| Latvia | 1,679 |
| The Netherlands | 1,649 |
| Russia | 1,558 |
| United Kingdom | 1,373 |

### 6. Top Attackers (Table — Top 20 IPs)
| IP | Events |
|---|---|
| 173.231.185.164 | 4,155 |
| 47.239.170.26 | 3,743 |
| 170.64.153.215 | 3,543 |
| 196.251.84.225 | 2,863 |
| 170.64.232.83 | 2,607 |
| 209.38.85.5 | 2,360 |
| 209.38.82.85 | 2,358 |
| 134.199.160.187 | 2,357 |
| 95.182.115.26 | 1,679 |
| 118.31.52.241 | 1,256 |

### 7. MITRE Techniques (Bar Chart)
| Technique | Events |
|---|---|
| T1595 | 44,989 |
| T1110 | 10,925 |
| T1190 | 2,544 |
| T1059 | 305 |
| T1046 | 94 |
| T1078 | 20 |
| T1090 | 18 |

### 8. Timeline — Events over Time (Line Chart)
- X-axis: Timestamp (daily bucket)
- Y-axis: Event Count

### 9. Recent Events (Live Feed — Last 50)
| Timestamp | Honeypot | Source IP | Country | Attack | Severity |

### 10. IP Reputation Levels (Bar Chart)
clean / low / medium / high / critical

---

## 📡 Endpoints المطلوبة من Backend (Source A)

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/live/kpis | KPI cards |
| GET | /api/live/by-honeypot | Pie chart |
| GET | /api/live/by-protocol | Pie chart |
| GET | /api/live/by-severity | Bar chart |
| GET | /api/live/by-country | Map + Table |
| GET | /api/live/top-attackers | Top 20 IPs |
| GET | /api/live/by-mitre | MITRE bar |
| GET | /api/live/timeline | Line chart |
| GET | /api/live/recent | Live feed |
| GET | /api/live/by-reputation | Reputation bar |

---
---

# 🤖 SOURCE B — ML Analytics

**المصدر:** ML Service (JSON files أو API endpoints)
**الطريقة:** ML pipeline يشتغل على نفس الـ events، ويطلع ملفات تحليلية

## 🎯 الملفات المتوفرة

| File | Content |
|---|---|
| cluster_analytics.json | Clusters + Behaviors |
| temporal_analytics.json | Timeline + Periods |
| session_analytics.json | KPI + Alerts + Distributions |
| mitre_analytics.json | Techniques + Tactics + Top IPs |
| mitre_statistics.json | Flat statistics table |
| mitre_trends.json | Time-series per technique |
| session_replay_list.json | 11,879 sessions list |
| session_replay_details/ | 367 session details |

## 📊 إيه اللي تعرضه على الـ Dashboard من Source B

### 1. KPI Cards (ML)
| Card | Value |
|---|---|
| ML Clusters | 29 |
| Sessions Analyzed | 11,879 |
| Critical Alerts | 8 |
| ML Techniques | 6 |
| Attack Periods | 2 |

### 2. Cluster Distribution (Bar Chart)
- 29 clusters — Bar chart by session count

### 3. Cluster Details Table
| Cluster | Sessions | Type | Confidence |
|---|---|---|---|
| 28 | 1,547 | Geo-temporal Username Activity | MEDIUM |
| 2 | 1,503 | Geo-temporal Activity | MEDIUM |
| 17 | 1,258 | Time-concentrated Activity | MEDIUM |
| 25 | 1,243 | Geo-temporal Username Activity | MEDIUM |
| 33 | 908 | Authentication-focused Activity | MEDIUM |

### 4. Cluster Detail Card (عند الضغط على cluster)
- ID + Session Count
- Type + Activity Profile
- Attacker Behavior
- Confidence
- Evidence Features
- Top Honeypots / Countries / Protocols / Attacks / MITRE

### 5. MITRE Techniques (ML — with Tactics)
| Technique | Sessions | Tactic |
|---|---|---|
| T1595 | 11,637 | Reconnaissance |
| T1110 | 178 | Credential Access |
| T1190 | 30 | Initial Access |
| T1046 | 26 | Discovery |
| T1078 | 5 | Defense Evasion |
| T1090 | 3 | Command and Control |

### 6. MITRE Tactics (Pie Chart)
- Reconnaissance: 97.96%
- Credential Access: 1.5%
- Initial Access: 0.25%
- Discovery: 0.22%
- Defense Evasion: 0.04%
- Command and Control: 0.03%

### 7. MITRE Statistics (Filterable Table)
- Filter by statistic_type: OVERALL / CLUSTER / MITRE_TECHNIQUE / ATTACK_TYPE / ATTACK_STAGE
- 49 rows total

### 8. MITRE Trends (Multi-Line Chart)
- Line per technique over time

### 9. Session Timeline (Line Chart)
- Daily session counts
- 2 active periods (2020 + 2025)

### 10. Peak Days (Card / Table)
- Peak: 2025-06-10 (6,812 sessions)

### 11. Sessions Table (Paginated)
- 11,879 sessions — 20 per page
- Columns: ID / Events / Country / Attack / Severity
- Filters: Replay-Worthy / High Severity / Brute Force

### 12. Critical Alerts (List)
- Only Critical + High severity sessions

### 13. Session Replay Modal
- Trigger: Click [🎬 Replay] في Sessions Table
- Content: Timeline (narrative steps) + Credentials + Commands

### 14. Session Distributions (Multiple Pies)
- By Honeypot / Protocol / Country / Attack Type / MITRE / Severity

---

## 📡 Endpoints المطلوبة من Backend (Source B)

| Method | Endpoint | Purpose |
|---|---|---|
| GET | /api/ml/clusters | Cluster list |
| GET | /api/ml/clusters/{id} | Cluster detail |
| GET | /api/ml/temporal | Timeline + periods |
| GET | /api/ml/sessions | Sessions summary |
| GET | /api/ml/sessions/alerts | Critical alerts |
| GET | /api/ml/mitre | Techniques + Tactics |
| GET | /api/ml/mitre/statistics | Statistics table |
| GET | /api/ml/mitre/trends | Trends chart |
| GET | /api/ml/session-replay | Replay list |
| GET | /api/ml/session-replay/{id} | Replay detail |

---
---

# 🎨 جدول المقارنة السريع

| Feature | 🔴 Source A (Live) | 🤖 Source B (ML) |
|---|---|---|
| Total Events | 58,895 | — |
| Clusters | — | 29 |
| Sessions | — | 11,879 |
| MITRE Techniques | 7 (raw) | 6 (ML-analyzed + Tactics) |
| MITRE Tactics | — | ✅ |
| Timeline | Events/day | Sessions/day + periods |
| Top Attackers | By events | By sessions (via replay list) |
| Session Replay | — | ✅ |
| Cluster Behaviors | — | ✅ |
| Critical Alerts | — | ✅ |

---

# 🎯 اقتراحين للتخطيط

## Option 1 — Tabs منفصلة
[Overview] [Live Events] [ML Analytics] [MITRE] [Sessions]

## Option 2 — صفحة واحدة مختلطة
Mix KPI + Charts من الاتنين مع بعض في نفس الصفحة.

**القرار ليك — إنتِ حر تختار.**

---

# 📞 Contact

- Frontend Lead: (fill)
- Backend Integration Lead: (fill)
- ML Service Owner: Hanaa
