import axios from "axios";

const API_BASE_URL =
  import.meta.env.VITE_BACKEND_URL ||
  import.meta.env.VITE_API_BASE_URL ||
  "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 15000,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  const token =
    localStorage.getItem("smart_honeypot_access_token") ||
    localStorage.getItem("access_token");

  if (token) {
    config.headers = config.headers || {};
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

function unwrap(payload) {
  if (
    payload &&
    typeof payload === "object" &&
    !Array.isArray(payload) &&
    "data" in payload
  ) {
    return payload.data;
  }

  return payload;
}

function asArray(value) {
  if (Array.isArray(value)) {
    return value;
  }

  if (!value || typeof value !== "object") {
    return [];
  }

  const possibleKeys = [
    "items",
    "events",
    "data",
    "results",
    "buckets",
    "countries",
    "attackers",
    "honeypots",
    "protocols",
    "severities",
    "techniques",
    "timeline",
    "points",
  ];

  for (const key of possibleKeys) {
    if (Array.isArray(value[key])) {
      return value[key];
    }
  }

  return [];
}

function firstValue(item, keys, fallback = null) {
  for (const key of keys) {
    const value = item?.[key];

    if (value !== undefined && value !== null && value !== "") {
      return value;
    }
  }

  return fallback;
}

function stableEventId(event, index = 0) {
  const explicitId = firstValue(event, [
    "id",
    "event_id",
    "eventId",
    "uuid",
    "_id",
  ]);

  if (explicitId !== null) {
    return String(explicitId);
  }

  return [
    firstValue(event, ["timestamp"], "unknown-time"),
    firstValue(event, ["source_ip", "sourceIp"], "unknown-ip"),
    firstValue(event, ["session_id", "sessionId"], "unknown-session"),
    firstValue(event, ["protocol"], "unknown-protocol"),
    index,
  ].join("|");
}

export function normalizeEvent(event, index = 0) {
  return {
    ...event,

    id: stableEventId(event, index),

    timestamp: firstValue(event, ["timestamp", "time", "@timestamp"], null),

    sourceIp: firstValue(event, ["source_ip", "sourceIp"], "Unknown"),

    country: firstValue(event, ["country"], "Unknown"),

    honeypot: firstValue(event, ["honeypot"], "Unknown"),

    service: firstValue(event, ["service", "protocol"], "Unknown"),

    protocol: firstValue(event, ["protocol"], "Unknown"),

    eventType: firstValue(
      event,
      ["event_type", "eventType", "attack_type", "attackType"],
      "Event",
    ),

    status: firstValue(event, ["status", "severity"], "detected"),

    severity: firstValue(event, ["severity"], "Unknown"),

    mitreTechnique: firstValue(
      event,
      ["mitre_technique", "mitreTechnique"],
      null,
    ),

    attackStage: firstValue(event, ["attack_stage", "attackStage"], null),

    sessionId: firstValue(event, ["session_id", "sessionId"], null),
  };
}

function normalizeBuckets(payload, labelKeys, valueKeys) {
  const data = unwrap(payload);

  /*
   * Supports Elasticsearch aggregation response:
   *
   * {
   *   aggregations: {
   *     something: {
   *       buckets: [...]
   *     }
   *   }
   * }
   */

  if (
    data &&
    typeof data === "object" &&
    !Array.isArray(data) &&
    data.aggregations
  ) {
    const aggregationValues = Object.values(data.aggregations);

    const buckets = aggregationValues.find((value) =>
      Array.isArray(value?.buckets),
    )?.buckets;

    if (buckets) {
      return buckets.map((bucket) => ({
        label: String(bucket.key),
        value: Number(bucket.doc_count ?? bucket.value ?? 0),
      }));
    }
  }

  /*
   * Supports already-normalized backend response.
   */

  return asArray(data).map((item) => ({
    label: String(firstValue(item, labelKeys, "Unknown")),

    value: Number(firstValue(item, valueKeys, 0)) || 0,
  }));
}

function normalizeTimeline(payload) {
  const data = unwrap(payload);

  if (
    data &&
    typeof data === "object" &&
    !Array.isArray(data) &&
    data.aggregations
  ) {
    const aggregationValues = Object.values(data.aggregations);

    const buckets = aggregationValues.find((value) =>
      Array.isArray(value?.buckets),
    )?.buckets;

    if (buckets) {
      return buckets.map((bucket) => ({
        timestamp: bucket.key_as_string ?? bucket.key,

        attacks: Number(bucket.doc_count ?? 0),
      }));
    }
  }

  return asArray(data)
    .map((item) => ({
      timestamp: firstValue(
        item,
        ["timestamp", "date", "day", "key_as_string", "key"],
        null,
      ),

      attacks:
        Number(
          firstValue(item, ["attacks", "count", "doc_count", "value"], 0),
        ) || 0,
    }))

    .filter((item) => item.timestamp !== null)

    .sort(
      (a, b) =>
        new Date(a.timestamp).getTime() - new Date(b.timestamp).getTime(),
    );
}

/* =========================
   REAL DASHBOARD ENDPOINTS
========================= */

export async function getStatistics() {
  const response = await api.get("/statistics");

  const data = unwrap(response.data) || {};

  return {
    totalAttacks: Number(data.totalAttacks ?? 0),

    uniqueAttackers: Number(data.uniqueAttackers ?? 0),

    countries: Array.isArray(data.topCountries)
      ? data.topCountries.length
      : Number(data.countries ?? 0),

    topCountries: Array.isArray(data.topCountries) ? data.topCountries : [],
  };
}

export async function getRecentEvents(limit = 50) {
  const response = await api.get("/events/recent");

  return asArray(unwrap(response.data)).slice(0, limit).map(normalizeEvent);
}

export async function getTopAttackers() {
  const response = await api.get("/attackers/top");

  return asArray(unwrap(response.data)).map((item) => ({
    ip: firstValue(item, ["ip", "source_ip"], "Unknown"),

    count: Number(firstValue(item, ["count", "attacks", "doc_count"], 0)) || 0,
  }));
}

/* =========================
   LIVE / ELASTICSEARCH
========================= */

export async function getByHoneypot() {
  const response = await api.get("/api/live/by-honeypot");

  return normalizeBuckets(
    response.data,
    ["honeypot", "name", "key", "label"],
    ["attacks", "count", "doc_count", "value"],
  );
}

export async function getByProtocol() {
  const response = await api.get("/api/live/by-protocol");

  return normalizeBuckets(
    response.data,
    ["protocol", "name", "key", "label"],
    ["attacks", "count", "doc_count", "value"],
  );
}

export async function getBySeverity() {
  const response = await api.get("/api/live/by-severity");

  return normalizeBuckets(
    response.data,
    ["severity", "name", "key", "label"],
    ["attacks", "count", "doc_count", "value"],
  );
}

export async function getByCountry() {
  const response = await api.get("/api/live/by-country");

  return normalizeBuckets(
    response.data,
    ["country", "name", "key", "label"],
    ["attacks", "count", "doc_count", "value"],
  );
}

export async function getByMitre() {
  const response = await api.get("/api/live/by-mitre");

  return normalizeBuckets(
    response.data,
    ["mitre_technique", "mitreTechnique", "technique", "name", "key"],
    ["attacks", "count", "doc_count", "value"],
  );
}

export async function getTimeline() {
  const response = await api.get("/api/live/timeline");

  return normalizeTimeline(response.data);
}

export async function getByReputation() {
  const response = await api.get("/api/live/by-reputation");

  return normalizeBuckets(
    response.data,
    ["ip_reputation_level", "ip_reputation", "reputation", "name", "key"],
    ["attacks", "count", "doc_count", "value"],
  );
}

/* =========================
   ORCHESTRATOR
========================= */

export async function getHoneypots() {
  const response = await api.get("/honeypots");

  return asArray(unwrap(response.data)).map((item, index) => ({
    id: String(item.id ?? item.name ?? `honeypot-${index}`),

    name: item.name ?? "Unknown",

    status: item.status ?? "unknown",
  }));
}

/* =========================
   WEBSOCKET
========================= */

export function getWebSocketUrl() {
  const configured =
    import.meta.env.VITE_BACKEND_WS_URL || import.meta.env.VITE_WS_URL;

  if (configured) {
    try {
      const url = new URL(configured, window.location.href);
      if (url.protocol === "http:") url.protocol = "ws:";
      if (url.protocol === "https:") url.protocol = "wss:";
      if (!url.pathname || url.pathname === "/") url.pathname = "/ws";
      else if (!url.pathname.endsWith("/ws"))
        url.pathname = `${url.pathname.replace(/\/$/, "")}/ws`;
      return url.toString();
    } catch {
      // Fall through to the API base URL below.
    }
  }

  try {
    const base = new URL(API_BASE_URL, window.location.href);
    const isProxy =
      base.origin === window.location.origin &&
      base.pathname.startsWith("/backend");
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    if (isProxy) {
      const path = `${base.pathname.replace(/\/$/, "")}/ws`;
      return `${protocol}//${window.location.host}${path}`;
    }
    base.protocol = base.protocol === "https:" ? "wss:" : "ws:";
    base.pathname = `${base.pathname.replace(/\/$/, "")}/ws`;
    base.search = "";
    base.hash = "";
    return base.toString();
  } catch {
    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    return `${protocol}//${window.location.host}/backend/ws`;
  }
}

export function createEventsWebSocket() {
  return new WebSocket(getWebSocketUrl());
}

/* =========================
   BACKEND LIVE + ML CONTRACTS
   These methods return the backend payload as-is. The UI normalizes
   shapes defensively and never substitutes sample/mock data.
========================= */

async function getPayload(path) {
  const response = await api.get(path);
  return unwrap(response.data);
}

export const getLiveKpis = () => getPayload("/api/live/kpis");
export const getLiveTopAttackers = () => getPayload("/api/live/top-attackers");
export const getLiveRecentEvents = () => getPayload("/api/live/recent");
export const getMlTemporal = () => getPayload("/api/ml/temporal");
export const getMlSessionSummary = () => getPayload("/api/ml/sessions/summary");
export const getMlSessionAlerts = () => getPayload("/api/ml/sessions/alerts");
export const getMlSessionTopAttackers = () =>
  getPayload("/api/ml/sessions/top-attackers");
export const getMlMitre = () => getPayload("/api/ml/mitre");
export const getMlMitreStatistics = () =>
  getPayload("/api/ml/mitre/statistics");
export const getMlMitreTrends = () => getPayload("/api/ml/mitre/trends");
export const getMlSessionReplayList = () =>
  getPayload("/api/ml/session-replay");
export const getMlSessionReplayDetail = (sessionId) =>
  getPayload(`/api/ml/session-replay/${encodeURIComponent(sessionId)}`);

// Cluster analytics endpoint registered by the current backend. The endpoint
// returns summary metadata and per-cluster behavioral analytics.
export const getMlClusters = () => getPayload("/api/ml/clusters");

export { API_BASE_URL };

export default api;
