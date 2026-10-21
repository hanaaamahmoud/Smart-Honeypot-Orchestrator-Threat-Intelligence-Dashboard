import { useCallback, useEffect, useMemo, useState } from "react";
import {
  getLiveKpis,
  getByHoneypot,
  getByProtocol,
  getBySeverity,
  getByCountry,
  getByMitre,
  getTimeline,
  getByReputation,
  getLiveTopAttackers,
  getLiveRecentEvents,
} from "../services/api";
import "../styles/dashboard.css";
import "../styles/security-dashboard.css";

const COLORS = [
  "#22d3ee",
  "#a78bfa",
  "#34d399",
  "#f59e0b",
  "#fb7185",
  "#60a5fa",
  "#f472b6",
  "#c084fc",
];
const num = (v) =>
  v === null || v === undefined || v === "" ? "—" : Number(v).toLocaleString();
const list = (v) => (Array.isArray(v) ? v : []);
const labelOf = (x) =>
  String(
    x?.label ??
      x?.name ??
      x?.key ??
      x?.country ??
      x?.protocol ??
      x?.honeypot ??
      x?.severity ??
      x?.mitre_technique ??
      "Unknown",
  );
const valueOf = (x) =>
  Number(x?.value ?? x?.count ?? x?.doc_count ?? x?.events ?? x?.total ?? 0) ||
  0;
const normalise = (arr) =>
  list(arr).map((x) => ({ label: labelOf(x), value: valueOf(x), ...x }));
const timeLabel = (value) => {
  if (!value) return "—";
  const d = new Date(value);
  return Number.isNaN(d.getTime()) ? String(value) : d.toLocaleString();
};

function Panel({ title, subtitle, className = "", children, action }) {
  return (
    <article className={`sec-panel ${className}`}>
      <div className="sec-panel__head">
        <div>
          <h3>{title}</h3>
          {subtitle && <p>{subtitle}</p>}
        </div>
        {action}
      </div>
      {children}
    </article>
  );
}

function Empty({ children = "No data returned by the backend." }) {
  return <div className="sec-empty">{children}</div>;
}

function BarChart({ data, color = COLORS[0], maxItems = 8 }) {
  const rows = normalise(data).slice(0, maxItems);
  const max = Math.max(1, ...rows.map((x) => x.value));
  if (!rows.length) return <Empty />;
  return (
    <div className="sec-bars">
      {rows.map((item, i) => (
        <div className="sec-bar-row" key={`${item.label}-${i}`}>
          <div className="sec-bar-label" title={item.label}>
            {item.label}
          </div>
          <div className="sec-bar-track">
            <span
              style={{
                width: `${Math.max(1, (item.value / max) * 100)}%`,
                background: COLORS[i % COLORS.length] || color,
              }}
            />
          </div>
          <strong>{num(item.value)}</strong>
        </div>
      ))}
    </div>
  );
}

function DonutChart({ data }) {
  const rows = normalise(data)
    .filter((x) => x.value >= 0)
    .slice(0, 8);
  const total = rows.reduce((sum, item) => sum + item.value, 0);
  if (!rows.length || total <= 0) return <Empty />;
  const segments = rows.reduce(
    (state, item, i) => {
      const start = state.cursor;
      const end = start + (item.value / total) * 100;
      return {
        cursor: end,
        parts: [
          ...state.parts,
          `${COLORS[i % COLORS.length]} ${start}% ${end}%`,
        ],
      };
    },
    { cursor: 0, parts: [] },
  ).parts;
  return (
    <div className="sec-donut-layout">
      <div
        className="sec-donut"
        style={{ background: `conic-gradient(${segments.join(",")})` }}
      >
        <div className="sec-donut__hole">
          <strong>{num(total)}</strong>
          <span>events</span>
        </div>
      </div>
      <div className="sec-legend">
        {rows.map((item, i) => (
          <div className="sec-legend__item" key={`${item.label}-${i}`}>
            <span style={{ background: COLORS[i % COLORS.length] }} />
            <span title={item.label}>{item.label}</span>
            <strong>{num(item.value)}</strong>
          </div>
        ))}
      </div>
    </div>
  );
}

function TimelineChart({ data }) {
  const rows = list(data)
    .map((x) => ({
      date: x.date ?? x.timestamp ?? x.key_as_string ?? x.timestamp_date,
      count: Number(
        x.count ?? x.value ?? x.doc_count ?? x.events ?? x.attacks ?? 0,
      ),
    }))
    .filter((x) => x.date && Number.isFinite(x.count))
    .slice(-45);
  if (!rows.length) return <Empty />;
  const width = 720,
    height = 190,
    pad = 20;
  const max = Math.max(1, ...rows.map((x) => x.count));
  const points = rows
    .map(
      (x, i) =>
        `${pad + (rows.length === 1 ? 0 : (i * (width - pad * 2)) / (rows.length - 1))},${height - pad - (x.count / max) * (height - pad * 2)}`,
    )
    .join(" ");
  return (
    <div className="sec-timeline">
      <svg
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label="Events over time"
      >
        <defs>
          <linearGradient id="timelineFill" x1="0" x2="0" y1="0" y2="1">
            <stop offset="0%" stopColor="#22d3ee" stopOpacity=".28" />
            <stop offset="100%" stopColor="#22d3ee" stopOpacity="0" />
          </linearGradient>
        </defs>
        <polygon
          points={`${pad},${height - pad} ${points} ${width - pad},${height - pad}`}
          fill="url(#timelineFill)"
        />
        <polyline
          points={points}
          fill="none"
          stroke="#22d3ee"
          strokeWidth="3"
          strokeLinejoin="round"
          strokeLinecap="round"
        />
        {rows.map((x, i) => {
          const cx =
            pad +
            (rows.length === 1
              ? 0
              : (i * (width - pad * 2)) / (rows.length - 1));
          const cy = height - pad - (x.count / max) * (height - pad * 2);
          return (
            <circle
              key={`${x.date}-${i}`}
              cx={cx}
              cy={cy}
              r="2.7"
              fill="#a5f3fc"
            />
          );
        })}
      </svg>
      <div className="sec-timeline__labels">
        <span>{String(rows[0].date).slice(0, 10)}</span>
        <span>
          {String(rows[Math.floor(rows.length / 2)].date).slice(0, 10)}
        </span>
        <span>{String(rows[rows.length - 1].date).slice(0, 10)}</span>
      </div>
    </div>
  );
}

function Table({
  columns,
  rows,
  empty = "No records returned by the backend.",
}) {
  if (!rows.length) return <Empty>{empty}</Empty>;
  return (
    <div className="sec-table-wrap">
      <table className="sec-table">
        <thead>
          <tr>
            {columns.map((c) => (
              <th key={c.key}>{c.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, i) => (
            <tr key={row.id ?? row.ip ?? `${i}`}>
              {columns.map((c) => (
                <td key={c.key}>
                  {c.render ? c.render(row[c.key], row) : (row[c.key] ?? "—")}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function Dashboard() {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [errors, setErrors] = useState([]);
  const [selectedEvent, setSelectedEvent] = useState(null);

  const load = useCallback(async (manual = false) => {
    manual ? setRefreshing(true) : setLoading(true);
    const requests = [
      ["kpis", getLiveKpis],
      ["honeypots", getByHoneypot],
      ["protocols", getByProtocol],
      ["severity", getBySeverity],
      ["countries", getByCountry],
      ["mitre", getByMitre],
      ["timeline", getTimeline],
      ["reputation", getByReputation],
      ["attackers", getLiveTopAttackers],
      ["recent", getLiveRecentEvents],
    ];
    const results = await Promise.allSettled(requests.map(([, fn]) => fn()));
    const next = {};
    const failed = [];
    results.forEach((result, i) => {
      const key = requests[i][0];
      if (result.status === "fulfilled") next[key] = result.value;
      else {
        next[key] = null;
        failed.push(
          `${requests[i][0]}: ${result.reason?.response?.status || result.reason?.message || "request failed"}`,
        );
      }
    });
    setData(next);
    setErrors(failed);
    setLoading(false);
    setRefreshing(false);
  }, []);

  useEffect(() => {
    const timer = setTimeout(() => {
      void load();
    }, 0);
    return () => clearTimeout(timer);
  }, [load]);

  const kpis = data.kpis || {};
  const countries = normalise(data.countries);
  const attackers = useMemo(
    () =>
      list(data.attackers).map((x) => ({
        ip: x.ip ?? x.source_ip ?? "Unknown",
        count: Number(x.count ?? x.value ?? x.doc_count ?? 0),
      })),
    [data.attackers],
  );
  const recent = useMemo(() => list(data.recent).slice(0, 12), [data.recent]);
  const timeline = useMemo(() => list(data.timeline), [data.timeline]);
  const eventsTotal = kpis.totalEvents ?? kpis.total_events ?? null;
  const uniqueIPs = kpis.uniqueIPs ?? kpis.unique_ips ?? null;
  const uniqueCountries = kpis.uniqueCountries ?? kpis.unique_countries ?? null;
  const honeypotCount =
    kpis.activeHoneypots ??
    kpis.uniqueHoneypots ??
    kpis.unique_honeypots ??
    null;

  return (
    <section className="security-dashboard">
      <header className="sec-page-header">
        <div>
          <span className="page-eyebrow">LIVE TELEMETRY · SOURCE A</span>
          <h1>Security Overview</h1>
          <p>
            Live event analytics queried by the backend from Elasticsearch. No
            dashboard mock data is used.
          </p>
        </div>
        <button
          className="sec-refresh"
          type="button"
          onClick={() => load(true)}
          disabled={refreshing || loading}
        >
          <span>↻</span> {refreshing ? "Refreshing…" : "Refresh data"}
        </button>
      </header>
      {errors.length > 0 && (
        <div className="sec-warning">
          <strong>Some backend sources are unavailable.</strong>
          <span>
            {errors.length} of 10 requests failed. Successful panels remain
            visible; failed panels are not filled with sample values.
          </span>
        </div>
      )}
      {loading ? (
        <div className="sec-loading">
          <span className="sec-spinner" /> Loading Elasticsearch analytics…
        </div>
      ) : (
        <>
          <div className="sec-kpis">
            <div className="sec-kpi kpi-cyan">
              <span className="sec-kpi__icon">⌁</span>
              <span>Total events</span>
              <strong>{num(eventsTotal)}</strong>
              <small>GET /api/live/kpis</small>
            </div>
            <div className="sec-kpi kpi-violet">
              <span className="sec-kpi__icon">◎</span>
              <span>Unique source IPs</span>
              <strong>{num(uniqueIPs)}</strong>
              <small>Cardinality aggregation</small>
            </div>
            <div className="sec-kpi kpi-green">
              <span className="sec-kpi__icon">◌</span>
              <span>Countries</span>
              <strong>{num(uniqueCountries)}</strong>
              <small>GeoIP-enriched events</small>
            </div>
            <div className="sec-kpi kpi-amber">
              <span className="sec-kpi__icon">⌘</span>
              <span>Honeypots seen</span>
              <strong>{num(honeypotCount)}</strong>
              <small>Distinct honeypots in telemetry</small>
            </div>
          </div>
          <div className="sec-grid sec-grid--wide">
            {/* <Panel
              title="Event activity"
              subtitle="Daily event count · latest 45 buckets"
              className="sec-panel--span2"
            >
              <TimelineChart data={timeline} />
            </Panel> */}
            <Panel
              title="Severity distribution"
              subtitle="Events grouped by severity"
            >
              <DonutChart data={data.severity} />
            </Panel>
            <Panel
              title="Events by honeypot"
              subtitle="Source service breakdown"
            >
              <DonutChart data={data.honeypots} />
            </Panel>
            <Panel
              title="Protocol distribution"
              subtitle="Protocols observed in events"
            >
              <DonutChart data={data.protocols} />
            </Panel>
            <Panel
              title="IP reputation"
              subtitle="Enriched source reputation levels"
            >
              <BarChart data={data.reputation} maxItems={8} />
            </Panel>
            <Panel
              title="MITRE ATT&CK techniques"
              subtitle="Technique IDs present in indexed events"
            >
              <BarChart data={data.mitre} maxItems={10} />
            </Panel>
            <Panel
              title="Top source countries"
              subtitle="Top countries returned by the backend"
            >
              <BarChart data={countries} maxItems={10} />
            </Panel>
            {/* <Panel
              title="Top attackers"
              subtitle="Top source IPs · ordered by event count"
              className="sec-panel--span2"
            >
              <Table
                columns={[
                  { key: "ip", label: "Source IP" },
                  { key: "count", label: "Events", render: (v) => num(v) },
                ]}
                rows={attackers.slice(0, 10)}
              />
            </Panel> */}
            <Panel
              title="Recent events"
              subtitle="Latest events from GET /api/live/recent · select a row to inspect every returned field"
              className="sec-panel--full"
            >
              <Table
                columns={[
                  {
                    key: "timestamp",
                    label: "Timestamp",
                    render: (v, row) =>
                      timeLabel(v ?? row.time ?? row["@timestamp"]),
                  },
                  { key: "honeypot", label: "Honeypot" },
                  { key: "protocol", label: "Protocol" },
                  {
                    key: "source_ip",
                    label: "Source IP",
                    render: (v, row) => v ?? row.sourceIp ?? "—",
                  },
                  { key: "country", label: "Country" },
                  { key: "mitre_technique", label: "MITRE" },
                  {
                    key: "severity",
                    label: "Severity",
                    render: (v) =>
                      v ? (
                        <span
                          className={`sec-severity sev-${String(v).toLowerCase()}`}
                        >
                          {v}
                        </span>
                      ) : (
                        "—"
                      ),
                  },
                  {
                    key: "details",
                    label: "All fields",
                    render: (_, row) => (
                      <button
                        type="button"
                        className="sec-detail-button"
                        onClick={() => setSelectedEvent(row)}
                      >
                        Inspect
                      </button>
                    ),
                  },
                ]}
                rows={recent}
              />
            </Panel>
          </div>
        </>
      )}
      {selectedEvent && (
        <div
          className="sec-detail-backdrop"
          role="presentation"
          onClick={() => setSelectedEvent(null)}
        >
          <section
            className="sec-detail-modal"
            role="dialog"
            aria-modal="true"
            aria-label="Raw event details"
            onClick={(event) => event.stopPropagation()}
          >
            <div className="sec-detail-head">
              <div>
                <span className="page-eyebrow">RAW EVENT</span>
                <h2>Event details</h2>
                <p>All fields returned for this event by the backend.</p>
              </div>
              <button
                type="button"
                className="sec-detail-close"
                aria-label="Close event details"
                onClick={() => setSelectedEvent(null)}
              >
                ×
              </button>
            </div>
            <pre className="sec-detail-json">
              {JSON.stringify(selectedEvent, null, 2)}
            </pre>
          </section>
        </div>
      )}
    </section>
  );
}

export default Dashboard;
