import { useCallback, useEffect, useMemo, useState } from "react";
import {
  getMlTemporal,
  getMlSessionSummary,
  getMlSessionAlerts,
  getMlSessionTopAttackers,
  getMlMitre,
  getMlMitreStatistics,
  getMlMitreTrends,
  getMlSessionReplayList,
  getMlSessionReplayDetail,
  getMlClusters,
} from "../services/api";
import "../styles/security-dashboard.css";
import "../styles/threat-intelligence.css";

const PALETTE = [
  "#22d3ee",
  "#a78bfa",
  "#34d399",
  "#f59e0b",
  "#fb7185",
  "#60a5fa",
  "#f472b6",
  "#c084fc",
];
const arr = (x) => (Array.isArray(x) ? x : []);
const fmt = (x) =>
  x === null || x === undefined || x === "" ? "—" : Number(x).toLocaleString();
const pct = (x) =>
  x === null || x === undefined || x === "" ? "—" : `${Number(x).toFixed(2)}%`;
const unwrapArray = (payload, keys = []) => {
  if (Array.isArray(payload)) return payload;
  for (const k of keys) if (Array.isArray(payload?.[k])) return payload[k];
  return [];
};
const human = (v) =>
  v === null || v === undefined || v === "" ? "—" : String(v);

function Card({ title, subtitle, children, className = "" }) {
  return (
    <article className={`sec-panel ti-panel ${className}`}>
      <div className="sec-panel__head">
        <div>
          <h3>{title}</h3>
          {subtitle && <p>{subtitle}</p>}
        </div>
      </div>
      {children}
    </article>
  );
}
function Empty({ text = "No records returned by the ML API." }) {
  return <div className="sec-empty">{text}</div>;
}
function DataBars({
  data,
  labelKey = "value",
  countKey = "count",
  maxItems = 10,
}) {
  const rows = arr(data)
    .slice(0, maxItems)
    .map((x) => ({
      label: x[labelKey] ?? x.label ?? x.name ?? "Unknown",
      count: Number(x[countKey] ?? x.session_count ?? x.event_count ?? 0),
      percentage: x.percentage,
    }));
  const max = Math.max(1, ...rows.map((x) => x.count));
  if (!rows.length) return <Empty />;
  return (
    <div className="ti-bars">
      {rows.map((x, i) => (
        <div className="ti-bar" key={`${x.label}-${i}`}>
          <div className="ti-bar__top">
            <span title={String(x.label)}>{x.label}</span>
            <strong>
              {fmt(x.count)}
              {x.percentage !== undefined ? (
                <small> · {pct(x.percentage)}</small>
              ) : null}
            </strong>
          </div>
          <div className="sec-bar-track">
            <span
              style={{
                width: `${Math.max(1, (x.count / max) * 100)}%`,
                background: PALETTE[i % PALETTE.length],
              }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
function Donut({ data, labelKey = "value", countKey = "count" }) {
  const rows = arr(data)
    .map((x) => ({
      label: x[labelKey] ?? x.label ?? x.name ?? "Unknown",
      count: Number(x[countKey] ?? 0),
      percentage: x.percentage,
    }))
    .filter((x) => x.count >= 0)
    .slice(0, 8);
  const total = rows.reduce((s, x) => s + x.count, 0);
  if (!rows.length || total === 0) return <Empty />;
  const gradients = rows.reduce(
    (state, x, i) => {
      const start = state.cursor;
      const end = start + (x.count / total) * 100;
      return {
        cursor: end,
        parts: [
          ...state.parts,
          `${PALETTE[i % PALETTE.length]} ${start}% ${end}%`,
        ],
      };
    },
    { cursor: 0, parts: [] },
  ).parts;
  return (
    <div className="sec-donut-layout">
      <div
        className="sec-donut"
        style={{ background: `conic-gradient(${gradients.join(",")})` }}
      >
        <div className="sec-donut__hole">
          <strong>{fmt(total)}</strong>
          <span>sessions</span>
        </div>
      </div>
      <div className="sec-legend">
        {rows.map((x, i) => (
          <div className="sec-legend__item" key={`${x.label}-${i}`}>
            <span style={{ background: PALETTE[i % PALETTE.length] }} />
            <span title={String(x.label)}>{x.label}</span>
            <strong>{fmt(x.count)}</strong>
          </div>
        ))}
      </div>
    </div>
  );
}
function SparkLine({
  data,
  dateKey = "trend_date",
  valueKey = "session_count",
}) {
  const rows = arr(data)
    .map((x) => ({
      date: x[dateKey] ?? x.date,
      value: Number(x[valueKey] ?? x.count ?? 0),
    }))
    .filter((x) => x.date && Number.isFinite(x.value));
  if (!rows.length) return <Empty />;
  const width = 700,
    height = 170,
    pad = 15,
    max = Math.max(1, ...rows.map((x) => x.value));
  const points = rows
    .map(
      (x, i) =>
        `${pad + (rows.length === 1 ? 0 : (i * (width - pad * 2)) / (rows.length - 1))},${height - pad - (x.value / max) * (height - pad * 2)}`,
    )
    .join(" ");
  return (
    <div className="ti-spark">
      <svg
        viewBox={`0 0 ${width} ${height}`}
        role="img"
        aria-label="ML session trend"
      >
        <polyline
          points={points}
          fill="none"
          stroke="#a78bfa"
          strokeWidth="3"
          strokeLinecap="round"
          strokeLinejoin="round"
        />
        {rows.map((x, i) => {
          const cx =
            pad +
            (rows.length === 1
              ? 0
              : (i * (width - pad * 2)) / (rows.length - 1));
          const cy = height - pad - (x.value / max) * (height - pad * 2);
          return (
            <circle
              key={`${x.date}-${i}`}
              cx={cx}
              cy={cy}
              r="2.5"
              fill="#c4b5fd"
            />
          );
        })}
      </svg>
      <div className="ti-spark__labels">
        <span>{rows[0].date}</span>
        <span>{rows[rows.length - 1].date}</span>
      </div>
    </div>
  );
}
function Table({ columns, rows, emptyText }) {
  if (!rows.length) return <Empty text={emptyText || "No rows available."} />;
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
          {rows.map((r, i) => (
            <tr
              key={r.id ?? r.session_id ?? r.cluster_id ?? r.statistic_key ?? i}
            >
              {columns.map((c) => (
                <td key={c.key}>
                  {c.render ? c.render(r[c.key], r) : human(r[c.key])}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
function Button({ children, onClick, disabled = false, secondary = false }) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={`ti-button ${secondary ? "ti-button--secondary" : ""}`}
    >
      {children}
    </button>
  );
}

const firstValue = (...values) =>
  values.find((value) => value !== undefined && value !== null && value !== "");
function redactSensitiveFields(value, reveal) {
  if (Array.isArray(value))
    return value.map((item) => redactSensitiveFields(item, reveal));
  if (!value || typeof value !== "object") return value;
  return Object.fromEntries(
    Object.entries(value).map(([key, item]) => [
      key,
      /password/i.test(key) &&
      !reveal &&
      item !== null &&
      item !== undefined &&
      item !== ""
        ? "••••••••"
        : redactSensitiveFields(item, reveal),
    ]),
  );
}
const toText = (value) =>
  value === undefined || value === null || value === ""
    ? "—"
    : Array.isArray(value)
      ? value.map(toText).join(", ")
      : typeof value === "object"
        ? JSON.stringify(value)
        : String(value);
const formatTimestamp = (value) => {
  if (!value) return "—";
  const date = new Date(value);
  return Number.isNaN(date.getTime()) ? String(value) : date.toLocaleString();
};
function ReplayMetric({ label, value, hint }) {
  return (
    <div className="ti-replay-metric">
      <span>{label}</span>
      <strong>{toText(value)}</strong>
      {hint && <small>{hint}</small>}
    </div>
  );
}
function ReplaySection({ title, subtitle, children }) {
  return (
    <section className="ti-replay-section">
      <div className="ti-replay-section__head">
        <h3>{title}</h3>
        {subtitle && <p>{subtitle}</p>}
      </div>
      {children}
    </section>
  );
}
function ReplayDetails({ replay, techniqueRecords = [] }) {
  const [showPasswords, setShowPasswords] = useState(false);
  const summary = replay?.summary || {};
  const context = summary.context || {};
  const classification = summary.classification || {};
  const credentials = summary.credentials || {};
  const commands = summary.commands || {};
  const flags = summary.flags || {};
  const steps = arr(replay?.narrative?.steps)
    .slice()
    .sort((a, b) => Number(a.index || 0) - Number(b.index || 0));
  const events = arr(replay?.events)
    .slice()
    .sort((a, b) =>
      String(a.timestamp || "").localeCompare(String(b.timestamp || "")),
    );
  const sourceIps = arr(summary.source_ips).length
    ? summary.source_ips
    : [...new Set(events.map((event) => event.source_ip).filter(Boolean))];
  const techniqueId = firstValue(
    classification.mitre_technique,
    events.find((event) => event.mitre_technique)?.mitre_technique,
  );
  const techniqueInfo = techniqueRecords.find(
    (item) =>
      String(item.value ?? item.technique ?? item.technique_id ?? "") ===
      String(techniqueId),
  );
  const credentialAttempts = steps
    .filter((step) =>
      /auth|login|credential/i.test(
        `${step.phase || ""} ${step.step_type || ""} ${step.title || ""}`,
      ),
    )
    .map((step) => ({
      timestamp: step.timestamp,
      username: arr(step.details).find((detail) =>
        /username|user name/i.test(detail.label || ""),
      )?.value,
      password: arr(step.details).find((detail) =>
        /password/i.test(detail.label || ""),
      )?.value,
      title: step.title,
    }))
    .filter((item) => item.username || item.password);
  const hasArtifactEvidence =
    Object.keys(replay || {}).some((key) =>
      /artifact|file|payload|hash|download/i.test(key),
    ) ||
    events.some((event) =>
      Object.keys(event).some((key) =>
        /artifact|file|payload|hash|download/i.test(key),
      ),
    );
  const eventSummary = (event) => {
    const pieces = [
      event.attack_type,
      event.attack_stage,
      event.auth_attempt ? "Authentication attempt" : null,
      Number(event.command_count || 0) > 0
        ? `Command activity (${event.command_count})`
        : null,
    ].filter(Boolean);
    return [...new Set(pieces)].join(" · ") || "Recorded event";
  };

  return (
    <div className="ti-replay-content">
      <div className="ti-replay-intro">
        <div>
          <span className="page-eyebrow">
            SESSION {toText(replay?.id || summary.reconstructed_session_id)}
          </span>
          <h3>
            {toText(
              classification.attack_type ||
                events[0]?.attack_type ||
                "Recorded session activity",
            )}
          </h3>
          <p>
            Reconstructed from the ML service session records. Times are shown
            in your browser’s local timezone.
          </p>
        </div>
        <span
          className={`sec-severity sev-${String(classification.severity || "unknown").toLowerCase()}`}
        >
          {toText(classification.severity || "Severity unavailable")}
        </span>
      </div>

      <ReplaySection title="Who? · Connection details">
        <div className="ti-replay-metrics">
          <ReplayMetric
            label="Session ID"
            value={replay?.id || summary.reconstructed_session_id}
          />
          <ReplayMetric
            label="Source IP(s)"
            value={sourceIps.length ? sourceIps.join(", ") : "Not recorded"}
          />
          <ReplayMetric
            label="Country"
            value={
              context.country || events.find((event) => event.country)?.country
            }
          />
          <ReplayMetric
            label="Protocol / Honeypot"
            value={`${toText(context.protocol || events[0]?.protocol)} / ${toText(context.honeypot || events[0]?.honeypot)}`}
          />
          <ReplayMetric
            label="Duration"
            value={
              summary.duration_seconds !== undefined
                ? `${Number(summary.duration_seconds).toFixed(3)} s`
                : "Not recorded"
            }
          />
          <ReplayMetric
            label="Recorded events"
            value={summary.event_count ?? events.length}
          />
        </div>
      </ReplaySection>

      <ReplaySection
        title="What happened? · Recorded timeline"
        subtitle="Events are shown in recorded order. Expand a step to inspect its captured fields."
      >
        {steps.length ? (
          <ol className="ti-replay-timeline">
            {steps.map((step, index) => (
              <li
                className="ti-replay-step"
                key={`${step.index ?? index}-${step.timestamp || "time"}`}
              >
                <div className="ti-replay-step__marker">
                  {step.icon || index + 1}
                </div>
                <div className="ti-replay-step__body">
                  <div className="ti-replay-step__top">
                    <strong>
                      {toText(
                        step.title ||
                          step.step_type ||
                          step.phase ||
                          `Event ${index + 1}`,
                      )}
                    </strong>
                    <time>
                      {formatTimestamp(step.timestamp)}
                      {step.offset_seconds !== undefined
                        ? ` · +${Number(step.offset_seconds).toFixed(3)}s`
                        : ""}
                    </time>
                  </div>
                  {arr(step.details).length ? (
                    <details className="ti-replay-event-fields">
                      <summary>
                        Captured event fields ({step.details.length})
                      </summary>
                      <dl>
                        {step.details.map((detail, detailIndex) => (
                          <div key={`${detail.label}-${detailIndex}`}>
                            <dt>{toText(detail.label)}</dt>
                            <dd>
                              {/password/i.test(detail.label || "") &&
                              !showPasswords
                                ? "••••••••"
                                : toText(detail.value)}
                            </dd>
                          </div>
                        ))}
                      </dl>
                    </details>
                  ) : (
                    <p className="ti-muted">
                      No additional fields were recorded for this step.
                    </p>
                  )}
                </div>
              </li>
            ))}
          </ol>
        ) : (
          <Empty text="The detail response does not contain narrative timeline steps." />
        )}
      </ReplaySection>

      <div className="ti-replay-two-col">
        <ReplaySection
          title="Credentials observed"
          subtitle="Values below are attempted credentials captured by the honeypot, not proof of a valid account."
        >
          <div className="ti-replay-summary-list">
            <div>
              <span>Unique usernames</span>
              <strong>
                {toText(
                  credentials.unique_usernames?.length
                    ? credentials.unique_usernames.join(", ")
                    : "None returned",
                )}
              </strong>
            </div>
            <div>
              <span>Authentication attempts</span>
              <strong>{toText(credentials.auth_attempt_total)}</strong>
            </div>
            <div>
              <span>Unique password count</span>
              <strong>{toText(credentials.unique_passwords_count)}</strong>
            </div>
          </div>
          {credentialAttempts.length ? (
            <>
              <div className="ti-replay-toggle-row">
                <strong>Captured attempts</strong>
                <button
                  className="ti-button ti-button--secondary"
                  type="button"
                  onClick={() => setShowPasswords((value) => !value)}
                >
                  {showPasswords
                    ? "Hide attempted passwords"
                    : "Reveal attempted passwords"}
                </button>
              </div>
              <div className="ti-replay-credentials">
                {credentialAttempts.map((attempt, index) => (
                  <div key={`${attempt.timestamp || "auth"}-${index}`}>
                    <time>{formatTimestamp(attempt.timestamp)}</time>
                    <span>User: {toText(attempt.username)}</span>
                    <code>
                      {attempt.password === undefined
                        ? "Password not returned"
                        : showPasswords
                          ? String(attempt.password)
                          : "••••••••"}
                    </code>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <p className="ti-replay-note">
              No username/password values were included in the returned
              narrative. Counts above are shown only when present in the
              response.
            </p>
          )}
        </ReplaySection>
        <ReplaySection
          title="Commands & activity"
          subtitle="Only command data returned by the API is shown."
        >
          <div className="ti-replay-summary-list">
            <div>
              <span>Total command count</span>
              <strong>{toText(commands.command_count_total)}</strong>
            </div>
            <div>
              <span>Unique commands</span>
              <strong>{toText(commands.unique_commands_count)}</strong>
            </div>
          </div>
          {arr(commands.sample_commands).length ? (
            <pre className="ti-replay-terminal">
              {commands.sample_commands
                .map((command) =>
                  typeof command === "string"
                    ? command
                    : JSON.stringify(command),
                )
                .join("\n")}
            </pre>
          ) : (
            <p className="ti-replay-note">
              No raw command strings were returned for this session.{" "}
              {Number(commands.command_count_total || 0) > 0
                ? "The records indicate command activity, but do not include the command text."
                : "No command strings are available in this replay record."}
            </p>
          )}
        </ReplaySection>
      </div>

      <ReplaySection
        title="How dangerous? · Classification"
        subtitle="These are classifications returned by the ML analytics layer, not independent proof of successful compromise."
      >
        <div className="ti-replay-metrics">
          <ReplayMetric
            label="Attack type"
            value={classification.attack_type}
          />
          <ReplayMetric label="Severity" value={classification.severity} />
          <ReplayMetric
            label="Attack stage"
            value={classification.attack_stage}
          />
          <ReplayMetric
            label="Suspicious"
            value={
              flags.is_suspicious === undefined
                ? "Not returned"
                : flags.is_suspicious
                  ? "Yes"
                  : "No"
            }
          />
          <ReplayMetric
            label="Brute-force candidate"
            value={
              flags.is_brute_force_candidate === undefined
                ? "Not returned"
                : flags.is_brute_force_candidate
                  ? "Yes"
                  : "No"
            }
          />
          <ReplayMetric
            label="Command activity"
            value={
              flags.has_commands_executed === undefined
                ? "Not returned"
                : flags.has_commands_executed
                  ? "Recorded"
                  : "Not recorded"
            }
          />
        </div>
      </ReplaySection>

      <ReplaySection
        title="MITRE ATT&CK mapping"
        subtitle="Mapping is based on the session classification and recorded event fields."
      >
        {techniqueId ? (
          <div className="ti-replay-mitre">
            <strong>{toText(techniqueId)}</strong>
            <span>
              {toText(
                techniqueInfo?.value_name ||
                  techniqueInfo?.name ||
                  techniqueInfo?.technique_name ||
                  "Technique name not supplied by this response",
              )}
            </span>
            <span>
              Tactic / stage:{" "}
              {toText(techniqueInfo?.tactic || classification.attack_stage)}
            </span>
            <span>
              Session classification: {toText(classification.attack_type)}
            </span>
            <a
              href={`https://attack.mitre.org/techniques/${String(techniqueId).replace(".", "/")}/`}
              target="_blank"
              rel="noreferrer"
            >
              Open MITRE ATT&CK reference ↗
            </a>
          </div>
        ) : (
          <p className="ti-replay-note">
            No MITRE technique ID was returned for this session.
          </p>
        )}
      </ReplaySection>

      <ReplaySection
        title="Evidence · Recorded event details"
        subtitle="These event rows come from the session detail response. No synthetic events are added."
      >
        {events.length ? (
          <div className="sec-table-wrap">
            <table className="sec-table ti-replay-evidence-table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Source IP</th>
                  <th>Recorded activity</th>
                  <th>Severity</th>
                  <th>MITRE</th>
                </tr>
              </thead>
              <tbody>
                {events.map((event, index) => (
                  <tr key={`${event.timestamp || "event"}-${index}`}>
                    <td>{formatTimestamp(event.timestamp)}</td>
                    <td>{toText(event.source_ip)}</td>
                    <td>{eventSummary(event)}</td>
                    <td>{toText(event.severity)}</td>
                    <td>{toText(event.mitre_technique)}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <Empty text="No original event rows were returned for this session." />
        )}
        {hasArtifactEvidence ? (
          <details className="ti-replay-raw">
            <summary>Inspect raw evidence fields</summary>
            <pre>
              {JSON.stringify(
                events.filter((event) =>
                  Object.keys(event).some((key) =>
                    /artifact|file|payload|hash|download/i.test(key),
                  ),
                ),
                null,
                2,
              )}
            </pre>
          </details>
        ) : (
          <p className="ti-replay-note">
            No file artifact, payload, or hash fields were returned for this
            session. That means this response does not provide them; it does not
            prove no file activity occurred elsewhere.
          </p>
        )}
        <details className="ti-replay-raw">
          <summary>Inspect full session JSON</summary>
          <pre>
            {JSON.stringify(
              redactSensitiveFields(replay, showPasswords),
              null,
              2,
            )}
          </pre>
        </details>
      </ReplaySection>
    </div>
  );
}

function ThreatIntelligence() {
  const [data, setData] = useState({});
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [errors, setErrors] = useState([]);
  const [statType, setStatType] = useState("ALL");
  const [sessionFilter, setSessionFilter] = useState("all");
  const [sessionPage, setSessionPage] = useState(0);
  const [replay, setReplay] = useState(null);
  const [replayLoading, setReplayLoading] = useState(false);
  const [replayError, setReplayError] = useState("");
  const [selectedClusterId, setSelectedClusterId] = useState(null);

  const load = useCallback(async (manual = false) => {
    manual ? setRefreshing(true) : setLoading(true);
    const reqs = [
      ["temporal", getMlTemporal],
      ["sessions", getMlSessionSummary],
      ["clusters", getMlClusters],
      ["alerts", getMlSessionAlerts],
      ["sessionAttackers", getMlSessionTopAttackers],
      ["mitre", getMlMitre],
      ["statistics", getMlMitreStatistics],
      ["trends", getMlMitreTrends],
      ["replayList", getMlSessionReplayList],
    ];
    const results = await Promise.allSettled(reqs.map(([, fn]) => fn()));
    const next = {};
    const failed = [];
    results.forEach((r, i) => {
      const key = reqs[i][0];
      if (r.status === "fulfilled") next[key] = r.value;
      else {
        next[key] = null;
        failed.push(
          `${reqs[i][0]}: ${r.reason?.response?.status || r.reason?.message || "request failed"}`,
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

  const sessionPayload = data.sessions || {};
  const summary = sessionPayload.summary || {};
  const distributions = sessionPayload.distributions || {};
  const mitre = data.mitre || {};
  const temporal = data.temporal || {};
  const alertsPayload = data.alerts || {};
  const alerts = unwrapArray(alertsPayload, ["alerts", "items"]);
  const clusterPayload = data.clusters || {};
  const clusterRecords = unwrapArray(clusterPayload, [
    "clusters",
    "items",
    "results",
  ])
    .slice()
    .sort(
      (a, b) =>
        Number(b.session_count ?? b.count ?? 0) -
        Number(a.session_count ?? a.count ?? 0),
    );
  const clusterDistribution = clusterRecords.length
    ? clusterRecords.map((cluster) => ({
        value: `Cluster ${cluster.cluster_id ?? "—"}`,
        count: Number(cluster.session_count ?? cluster.count ?? 0),
        percentage: cluster.percentage,
      }))
    : arr(distributions.by_cluster)
        .slice()
        .sort((a, b) => Number(b.count ?? 0) - Number(a.count ?? 0));
  const selectedCluster =
    clusterRecords.find(
      (cluster) => String(cluster.cluster_id) === String(selectedClusterId),
    ) || null;
  const replayPayload = data.replayList || {};
  const sessions = unwrapArray(replayPayload, ["sessions", "items", "results"]);
  const statistics = unwrapArray(data.statistics, [
    "statistics",
    "items",
    "rows",
  ]);
  const statsFiltered = statistics.filter(
    (x) => statType === "ALL" || x.statistic_type === statType,
  );
  const sessionRows = useMemo(
    () =>
      sessions.filter((x) => {
        if (sessionFilter === "replay") return Boolean(x.has_replay);
        if (sessionFilter === "high")
          return (
            Boolean(x.flags?.is_high_severity) ||
            ["high", "critical"].includes(String(x.severity).toLowerCase())
          );
        if (sessionFilter === "bruteforce")
          return Boolean(x.flags?.is_brute_force_candidate);
        return true;
      }),
    [sessions, sessionFilter],
  );
  const pageSize = 20;
  const visibleSessions = sessionRows.slice(
    sessionPage * pageSize,
    sessionPage * pageSize + pageSize,
  );
  const peak = temporal.highlights?.peak_day;
  const tactics = arr(mitre.mitre_tactics_distribution);
  const techniques = arr(mitre.mitre_technique_distribution);
  const periods = arr(temporal.periods);
  const peakDays = periods
    .flatMap((period) =>
      arr(period.daily_trends).map((day) => ({
        date: day.trend_date,
        sessions: Number(day.session_count ?? 0),
        events: Number(day.event_count ?? 0),
        period: period.period_id,
      })),
    )
    .sort((a, b) => b.sessions - a.sessions || b.events - a.events);
  const trends = data.trends?.series?.MITRE_TECHNIQUE || {};
  const topTrends = Object.entries(trends)
    .sort(
      (a, b) =>
        arr(b[1]).reduce((s, x) => s + Number(x.session_count || 0), 0) -
        arr(a[1]).reduce((s, x) => s + Number(x.session_count || 0), 0),
    )
    .slice(0, 5);

  const openReplay = async (session) => {
    const sessionId = session?.id ?? session?.session_id;
    if (sessionId === null || sessionId === undefined || sessionId === "") {
      setReplay(null);
      setReplayError("This replay record does not include a session ID.");
      setReplayLoading(false);
      return;
    }
    setReplay(null);
    setReplayError("");
    setReplayLoading(true);
    try {
      setReplay(await getMlSessionReplayDetail(sessionId));
    } catch (e) {
      setReplayError(
        `Replay detail is unavailable (${e?.response?.status || e?.message || "request failed"}).`,
      );
    } finally {
      setReplayLoading(false);
    }
  };

  return (
    <section className="security-dashboard threat-intelligence-page">
      <header className="sec-page-header">
        <div>
          <span className="page-eyebrow">SOURCE B · ML ANALYTICS</span>
          <h1>Threat Intelligence</h1>
          <p>
            Model-generated session analytics, behavioral clusters, MITRE ATT&CK
            intelligence, temporal patterns, alerts, and session replay, kept
            separate from raw live-event telemetry.
          </p>
        </div>
        <button
          className="sec-refresh"
          type="button"
          onClick={() => load(true)}
          disabled={refreshing || loading}
        >
          <span>↻</span>
          {refreshing ? "Refreshing…" : "Refresh ML data"}
        </button>
      </header>
      <div className="ti-source-strip">
        <span className="ti-source-dot" />
        <div>
          <strong>ML analytics layer</strong>
          {/* <small>Backend JSON-backed endpoints · read-only analytics</small> */}
        </div>
        <span className="ti-contract">
          {sessionPayload.contract_version
            ? `Contract ${sessionPayload.contract_version}`
            : "API connected when data is available"}
        </span>
      </div>
      {errors.length > 0 && (
        <div className="sec-warning">
          <strong>Some ML endpoints could not be loaded.</strong>
          <span>
            {errors.length} of 9 requests failed. Unavailable endpoints are left
            empty; no analytics values are fabricated.
          </span>
        </div>
      )}
      {loading ? (
        <div className="sec-loading">
          <span className="sec-spinner" /> Loading ML analytics…
        </div>
      ) : (
        <>
          <div className="sec-kpis ti-kpis">
            <div className="sec-kpi kpi-violet">
              <span className="sec-kpi__icon">◈</span>
              <span>Sessions analyzed</span>
              <strong>{fmt(summary.total_sessions)}</strong>
              <small>session_analytics.json</small>
            </div>
            <div className="sec-kpi kpi-cyan">
              <span className="sec-kpi__icon">⌁</span>
              <span>Events in ML sessions</span>
              <strong>
                {fmt(summary.total_events ?? temporal.summary?.total_events)}
              </strong>
              <small>Session-level aggregation</small>
            </div>
            <div className="sec-kpi kpi-green">
              <span className="sec-kpi__icon">▦</span>
              <span>Clusters in use</span>
              <strong>
                {fmt(
                  data.clusters
                    ? (clusterPayload.summary?.total_clusters ??
                        clusterRecords.length)
                    : data.sessions
                      ? summary.total_clusters_used
                      : null,
                )}
              </strong>
              <small>
                {data.clusters
                  ? "Cluster analytics endpoint"
                  : "Cluster endpoint unavailable"}
              </small>
            </div>
            <div className="sec-kpi kpi-amber">
              <span className="sec-kpi__icon">⚠</span>
              <span>High / critical alerts</span>
              <strong>
                {fmt(
                  data.alerts ? (alertsPayload.count ?? alerts.length) : null,
                )}
              </strong>
              <small>ML session alert classification</small>
            </div>
            <div className="sec-kpi kpi-cyan">
              <span className="sec-kpi__icon">◎</span>
              <span>Unique source IPs</span>
              <strong>{fmt(summary.unique_source_ips)}</strong>
              <small>Session analytics</small>
            </div>
            <div className="sec-kpi kpi-violet">
              <span className="sec-kpi__icon">◇</span>
              <span>Countries</span>
              <strong>{fmt(summary.unique_countries)}</strong>
              <small>Geo-enriched sessions</small>
            </div>
            <div className="sec-kpi kpi-green">
              <span className="sec-kpi__icon">⌖</span>
              <span>MITRE techniques</span>
              <strong>
                {fmt(
                  data.mitre
                    ? (mitre.summary?.unique_techniques ?? techniques.length)
                    : null,
                )}
              </strong>
              <small>Mapped ML sessions</small>
            </div>
            <div className="sec-kpi kpi-amber">
              <span className="sec-kpi__icon">◷</span>
              <span>Active periods</span>
              <strong>
                {fmt(
                  data.temporal
                    ? (temporal.summary?.total_active_periods ?? periods.length)
                    : null,
                )}
              </strong>
              <small>Separated periods, not one continuous timeline</small>
            </div>
          </div>

          <div className="sec-grid">
            <Card
              title="Cluster distribution"
              subtitle="Session counts by cluster · from cluster analytics endpoint"
            >
              <DataBars
                data={clusterDistribution}
                labelKey="value"
                countKey="count"
                maxItems={12}
              />
              <div className="ti-inline-note">
                {clusterPayload.summary
                  ? `${fmt(clusterPayload.summary.total_clusters)} clusters · ${fmt(clusterPayload.summary.total_sessions)} sessions · ${fmt(clusterPayload.summary.noise_session_count)} noise sessions`
                  : "Cluster-level distribution from the available API response."}
              </div>
            </Card>
            <Card
              title="Cluster analytics explorer"
              subtitle="Select a cluster to inspect its behavioral profile"
              className="ti-panel--span2"
            >
              {clusterRecords.length ? (
                <>
                  <Table
                    columns={[
                      {
                        key: "cluster_id",
                        label: "Cluster",
                        render: (v) => `#${v}`,
                      },
                      { key: "cluster_type", label: "Cluster type" },
                      {
                        key: "session_count",
                        label: "Sessions",
                        render: (v) => fmt(v),
                      },
                      {
                        key: "percentage",
                        label: "Share",
                        render: (v) => pct(v),
                      },
                      { key: "confidence", label: "Confidence" },
                      {
                        key: "possible_attack_name",
                        label: "Possible activity",
                      },
                      {
                        key: "inspect",
                        label: "Details",
                        render: (_, row) => (
                          <Button
                            secondary
                            onClick={() =>
                              setSelectedClusterId((current) =>
                                String(current) === String(row.cluster_id)
                                  ? null
                                  : row.cluster_id,
                              )
                            }
                          >
                            {String(selectedClusterId) ===
                            String(row.cluster_id)
                              ? "Hide details"
                              : "Inspect"}
                          </Button>
                        ),
                      },
                    ]}
                    rows={clusterRecords}
                  />
                  {selectedCluster && (
                    <div className="ti-cluster-detail">
                      <div className="ti-cluster-detail__head">
                        <div>
                          <span className="page-eyebrow">
                            CLUSTER #{selectedCluster.cluster_id}
                          </span>
                          <h4>{human(selectedCluster.cluster_type)}</h4>
                          <p>{human(selectedCluster.activity_profile)}</p>
                        </div>
                        <span className="ti-contract">
                          {human(selectedCluster.confidence)} confidence
                        </span>
                      </div>
                      <p>{human(selectedCluster.attacker_behavior)}</p>
                      <div className="ti-cluster-metrics">
                        <div>
                          <small>Sessions</small>
                          <strong>{fmt(selectedCluster.session_count)}</strong>
                        </div>
                        <div>
                          <small>Share</small>
                          <strong>{pct(selectedCluster.percentage)}</strong>
                        </div>
                        <div>
                          <small>Avg. events / session</small>
                          <strong>
                            {fmt(selectedCluster.avg_event_count)}
                          </strong>
                        </div>
                        <div>
                          <small>Avg. duration</small>
                          <strong>
                            {human(selectedCluster.avg_session_duration)}
                          </strong>
                        </div>
                        <div>
                          <small>Avg. distance</small>
                          <strong>{human(selectedCluster.avg_distance)}</strong>
                        </div>
                      </div>
                      <div className="ti-cluster-detail__grid">
                        {[
                          ["Top honeypots", selectedCluster.top_honeypots],
                          ["Top countries", selectedCluster.top_countries],
                          ["Top protocols", selectedCluster.top_protocols],
                          ["Attack types", selectedCluster.top_attack_types],
                          [
                            "MITRE techniques",
                            selectedCluster.top_mitre_techniques,
                          ],
                          ["Attack stages", selectedCluster.top_attack_stages],
                          ["Severity", selectedCluster.top_severities],
                        ].map(([title, rows]) => (
                          <div className="ti-cluster-list" key={title}>
                            <h5>{title}</h5>
                            {arr(rows).length ? (
                              arr(rows)
                                .slice(0, 5)
                                .map((item, i) => (
                                  <div key={`${item.value}-${i}`}>
                                    <span>{human(item.value)}</span>
                                    <strong>
                                      {fmt(item.count)}{" "}
                                      <small>{pct(item.percentage)}</small>
                                    </strong>
                                  </div>
                                ))
                            ) : (
                              <span className="ti-muted">
                                No records returned
                              </span>
                            )}
                          </div>
                        ))}
                      </div>
                      <div className="ti-cluster-features">
                        <strong>Evidence features</strong>
                        <div>
                          {arr(selectedCluster.evidence_features).length ? (
                            arr(selectedCluster.evidence_features).map(
                              (feature) => <span key={feature}>{feature}</span>,
                            )
                          ) : (
                            <span className="ti-muted">
                              No evidence features returned
                            </span>
                          )}
                        </div>
                      </div>
                    </div>
                  )}
                </>
              ) : (
                <Empty
                  text={
                    data.clusters === null
                      ? "Cluster analytics endpoint failed. Check the endpoint response and backend logs."
                      : "No cluster records were returned by /api/ml/clusters."
                  }
                />
              )}
            </Card>
            <Card
              title="MITRE tactics"
              subtitle="Session distribution across ATT&CK tactics"
            >
              <Donut data={tactics} />
            </Card>
            <Card
              title="MITRE techniques"
              subtitle="Technique, session count, tactic, and share"
            >
              <Table
                columns={[
                  { key: "value", label: "Technique" },
                  { key: "tactic", label: "Tactic" },
                  { key: "count", label: "Sessions", render: (v) => fmt(v) },
                  { key: "percentage", label: "Share", render: (v) => pct(v) },
                ]}
                rows={techniques}
              />
            </Card>
            <Card
              title="Attack types"
              subtitle="ML-classified session categories"
            >
              <DataBars
                data={arr(mitre.attack_type_distribution)}
                labelKey="value"
                countKey="count"
                maxItems={8}
              />
            </Card>
            <Card
              title="Attack stages"
              subtitle="Observed stages from ML analytics"
            >
              <DataBars
                data={arr(mitre.attack_stage_distribution)}
                labelKey="value"
                countKey="count"
                maxItems={8}
              />
            </Card>
            <Card
              title="Temporal overview"
              subtitle={`${human(temporal.summary?.date_range?.from)} → ${human(temporal.summary?.date_range?.to)} · ${fmt(temporal.summary?.total_days)} active days`}
              className="ti-panel--span2"
            >
              <div className="ti-peak">
                <div>
                  <span>Peak session day</span>
                  <strong>{human(peak?.trend_date)}</strong>
                  <small>
                    {fmt(peak?.session_count)} sessions ·{" "}
                    {fmt(peak?.event_count)} events
                  </small>
                </div>
                <div className="ti-peak-icon">↗</div>
              </div>
              <div className="ti-periods">
                {periods.map((period) => (
                  <div className="ti-period" key={period.period_id}>
                    <div className="ti-period__head">
                      <strong>Period {period.period_id}</strong>
                      <span>
                        {human(period.from)} — {human(period.to)}
                      </span>
                    </div>
                    <div className="ti-period__stats">
                      <div>
                        <small>Sessions</small>
                        <strong>{fmt(period.sessions)}</strong>
                      </div>
                      <div>
                        <small>Events</small>
                        <strong>{fmt(period.events)}</strong>
                      </div>
                      <div>
                        <small>Share</small>
                        <strong>{pct(period.sessions_pct)}</strong>
                      </div>
                    </div>
                    <SparkLine
                      data={period.daily_trends}
                      dateKey="trend_date"
                      valueKey="session_count"
                    />
                  </div>
                ))}
              </div>
              <p className="ti-inline-note">
                Periods are displayed separately to avoid visually implying
                activity during the multi-year gap.
              </p>
            </Card>
            <Card
              title="Peak activity days"
              subtitle="Daily session and event counts from the ML temporal endpoint"
              className="ti-panel--span2"
            >
              <Table
                columns={[
                  { key: "date", label: "Date" },
                  { key: "period", label: "Active period" },
                  { key: "sessions", label: "Sessions", render: (v) => fmt(v) },
                  { key: "events", label: "Events", render: (v) => fmt(v) },
                ]}
                rows={peakDays.slice(0, 20)}
                emptyText="No daily activity records were returned by the temporal endpoint."
              />
              <p className="ti-inline-note">
                Showing up to 20 highest-activity days across the returned
                active periods. This table uses the API response and does not
                fill missing dates with zero activity.
              </p>
            </Card>
            {/* <Card
              title="MITRE technique trends"
              subtitle="Top technique time series · session counts"
              className="ti-panel--span2"
            >
              {topTrends.length ? (
                <div className="ti-trend-list">
                  {topTrends.map(([tech, rows], i) => (
                    <div className="ti-trend-item" key={tech}>
                      <div>
                        <strong>{tech}</strong>
                        <span>
                          {fmt(
                            arr(rows).reduce(
                              (s, x) => s + Number(x.session_count || 0),
                              0,
                            ),
                          )}{" "}
                          sessions across {arr(rows).length} points
                        </span>
                      </div>
                      <SparkLine
                        data={rows}
                        dateKey="date"
                        valueKey="session_count"
                      />
                      <i style={{ background: PALETTE[i % PALETTE.length] }} />
                    </div>
                  ))}
                </div>
              ) : (
                <Empty text="No MITRE trend series were returned." />
              )}
            </Card> */}
            <Card
              title="Session distributions"
              subtitle="Honeypot, protocol, attack, severity, and geography"
            >
              <div className="ti-distribution-grid">
                {[
                  ["Honeypot", distributions.by_honeypot],
                  ["Protocol", distributions.by_protocol],
                  ["Severity", distributions.by_severity],
                  ["Attack type", distributions.by_attack_type],
                  ["Country", distributions.by_country],
                  ["MITRE technique", distributions.by_mitre_technique],
                ].map(([title, rows]) => (
                  <div className="ti-mini-dist" key={title}>
                    <h4>{title}</h4>
                    <DataBars
                      data={rows}
                      labelKey="value"
                      countKey="count"
                      maxItems={5}
                    />
                  </div>
                ))}
              </div>
            </Card>
            <Card
              title="Critical alerts"
              subtitle="High and critical sessions returned by ML service"
            >
              <Table
                columns={[
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
                  { key: "source_ip", label: "Source IP" },
                  { key: "country", label: "Country" },
                  { key: "attack_type", label: "Attack type" },
                  { key: "mitre_technique", label: "MITRE" },
                  { key: "event_count", label: "Events" },
                  { key: "cluster_id", label: "Cluster" },
                ]}
                rows={alerts}
              />
            </Card>
            <Card
              title="Top attackers by sessions"
              subtitle="ML session aggregation"
            >
              <Table
                columns={[
                  { key: "ip", label: "Source IP" },
                  {
                    key: "session_count",
                    label: "Sessions",
                    render: (v) => fmt(v),
                  },
                  {
                    key: "event_count",
                    label: "Events",
                    render: (v) => fmt(v),
                  },
                ]}
                rows={unwrapArray(data.sessionAttackers, [
                  "attackers",
                  "top_source_ips",
                  "items",
                ])}
              />
            </Card>
            <Card
              title="MITRE statistics"
              subtitle="Filterable statistics rows from the ML statistics endpoint"
              className="ti-panel--span2"
            >
              <div className="ti-filter-row">
                <label htmlFor="ti-stat-filter">Statistic type</label>
                <select
                  id="ti-stat-filter"
                  value={statType}
                  onChange={(e) => setStatType(e.target.value)}
                >
                  <option value="ALL">All types</option>
                  {[
                    ...new Set(
                      statistics.map((x) => x.statistic_type).filter(Boolean),
                    ),
                  ].map((x) => (
                    <option key={x} value={x}>
                      {x}
                    </option>
                  ))}
                </select>
                <span>{fmt(statsFiltered.length)} rows</span>
              </div>
              <Table
                columns={[
                  { key: "statistic_type", label: "Type" },
                  { key: "label", label: "Label" },
                  {
                    key: "session_count",
                    label: "Sessions",
                    render: (v) => fmt(v),
                  },
                  {
                    key: "event_count",
                    label: "Events",
                    render: (v) => fmt(v),
                  },
                  {
                    key: "session_share_pct",
                    label: "Share",
                    render: (v) => pct(v),
                  },
                  { key: "mitre_technique", label: "Technique" },
                  { key: "tactic", label: "Tactic" },
                  { key: "attack_type", label: "Attack type" },
                  { key: "attack_stage", label: "Stage" },
                ]}
                rows={statsFiltered}
              />
            </Card>
            <Card
              title="Session explorer"
              subtitle={`${fmt(sessionRows.length)} sessions matching the current filter · ${fmt(sessions.length)} total returned`}
              className="ti-panel--span2"
            >
              <div className="ti-filter-row">
                <label htmlFor="ti-session-filter">Show</label>
                <select
                  id="ti-session-filter"
                  value={sessionFilter}
                  onChange={(e) => {
                    setSessionFilter(e.target.value);
                    setSessionPage(0);
                  }}
                >
                  <option value="all">All sessions</option>
                  <option value="replay">Replay available</option>
                  <option value="high">High / critical</option>
                  <option value="bruteforce">Brute-force candidates</option>
                </select>
                <span>
                  Page {sessionPage + 1} /{" "}
                  {Math.max(1, Math.ceil(sessionRows.length / pageSize))}
                </span>
              </div>
              <Table
                columns={[
                  { key: "id", label: "Session ID" },
                  { key: "events", label: "Events", render: (v) => fmt(v) },
                  { key: "country", label: "Country" },
                  { key: "protocol", label: "Protocol" },
                  { key: "attack", label: "Attack" },
                  { key: "mitre", label: "MITRE" },
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
                    key: "has_replay",
                    label: "Replay",
                    render: (v, row) =>
                      v ? (
                        <Button onClick={() => openReplay(row)}>
                          ▶ Replay
                        </Button>
                      ) : (
                        <span className="ti-muted">Not available</span>
                      ),
                  },
                ]}
                rows={visibleSessions}
              />
              <div className="ti-pagination">
                <Button
                  secondary
                  disabled={sessionPage === 0}
                  onClick={() => setSessionPage((p) => Math.max(0, p - 1))}
                >
                  ← Previous
                </Button>
                <Button
                  secondary
                  disabled={(sessionPage + 1) * pageSize >= sessionRows.length}
                  onClick={() => setSessionPage((p) => p + 1)}
                >
                  Next →
                </Button>
              </div>
            </Card>
          </div>
        </>
      )}
      {(replayLoading || replay || replayError) && (
        <div
          className="ti-modal-backdrop"
          role="presentation"
          onClick={() => {
            setReplay(null);
            setReplayError("");
          }}
        >
          <section
            className="ti-replay-modal"
            role="dialog"
            aria-modal="true"
            aria-label="Session replay details"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="ti-replay-head">
              <div>
                <span className="page-eyebrow">SESSION REPLAY</span>
                <h2>Session investigation</h2>
              </div>
              <button
                type="button"
                className="ti-close"
                aria-label="Close session replay"
                onClick={() => {
                  setReplay(null);
                  setReplayError("");
                }}
              >
                ×
              </button>
            </div>
            {replayLoading ? (
              <div className="sec-loading">
                <span className="sec-spinner" /> Loading replay details…
              </div>
            ) : replayError ? (
              <div className="sec-warning">{replayError}</div>
            ) : (
              <ReplayDetails replay={replay} techniqueRecords={techniques} />
            )}
          </section>
        </div>
      )}
    </section>
  );
}

export default ThreatIntelligence;
