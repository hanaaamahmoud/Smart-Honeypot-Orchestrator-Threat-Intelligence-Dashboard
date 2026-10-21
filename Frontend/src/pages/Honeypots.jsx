import {
  useCallback,
  useEffect,
  useRef,
  useState,
} from "react";

import { getHoneypots } from "../services/api";
import "../styles/honeypots.css";

const REFRESH_INTERVAL_MS = 30_000;

function getStatusClass(status) {
  const normalized = String(status || "unknown").trim().toLowerCase();
  if (normalized === "running") return "is-running";
  if (normalized === "unknown") return "is-unknown";
  return "is-unhealthy";
}

function Honeypots() {
  const [honeypots, setHoneypots] = useState([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [unavailable, setUnavailable] = useState(false);
  const [lastUpdated, setLastUpdated] = useState(null);
  const inFlightRef = useRef(false);
  const firstLoadRef = useRef(true);

  const load = useCallback(async (manual = false) => {
    // Avoid overlapping requests if a refresh takes longer than the polling interval.
    if (inFlightRef.current) return;
    inFlightRef.current = true;

    if (firstLoadRef.current) setLoading(true);
    if (manual) setRefreshing(true);

    try {
      const data = await getHoneypots();
      setHoneypots(Array.isArray(data) ? data : []);
      setUnavailable(false);
      setLastUpdated(new Date());
    } catch {
      // Do not leave stale cards visible when the orchestrator cannot be reached.
      setHoneypots([]);
      setUnavailable(true);
      setLastUpdated(null);
    } finally {
      inFlightRef.current = false;
      firstLoadRef.current = false;
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    void load();
    const timer = window.setInterval(() => {
      void load();
    }, REFRESH_INTERVAL_MS);

    return () => window.clearInterval(timer);
  }, [load]);

  return (
    <section className="honeypots-page">
      <header className="honeypots-page__header">
        <div>
          <span className="page-eyebrow">Infrastructure</span>
          <h2 className="page-title">Honeypots &amp; Orchestrator</h2>
          <p className="page-description">
            Live Docker container status reported by the Honeypot Orchestrator.
            Status refreshes automatically every 30 seconds.
          </p>
          {lastUpdated && !unavailable && (
            <p className="honeypots-last-updated" aria-live="polite">
              Last updated: {lastUpdated.toLocaleTimeString()}
            </p>
          )}
        </div>

        <button
          type="button"
          className="honeypots-refresh"
          onClick={() => void load(true)}
          disabled={loading || refreshing}
        >
          {loading || refreshing ? "Refreshing…" : "Refresh now"}
        </button>
      </header>

      <div className="honeypots-notice">
        This panel reports status only. Start, stop, restart, configuration,
        and deployment controls are not shown because the provided API does not
        expose those actions.
      </div>

      {unavailable ? (
        <div className="honeypots-state honeypots-state--error" role="alert">
          <span className="honeypots-state__icon" aria-hidden="true">!</span>
          <div>
            <strong>Orchestrator service is unavailable.</strong>
            <p>Check that the backend and orchestrator are running, then refresh.</p>
          </div>
          <button type="button" className="honeypots-state__retry" onClick={() => void load(true)}>
            Try again
          </button>
        </div>
      ) : loading ? (
        <div className="honeypots-state" role="status">Loading orchestrator status…</div>
      ) : honeypots.length === 0 ? (
        <div className="honeypots-state" role="status">No honeypot containers were returned by the orchestrator.</div>
      ) : (
        <div className="honeypots-grid">
          {honeypots.map((honeypot, index) => {
            const status = String(honeypot.status || "unknown").trim() || "unknown";
            return (
              <article className="honeypot-card" key={honeypot.id || `${honeypot.name || "honeypot"}-${index}`}>
                <div className="honeypot-card__top">
                  <div>
                    <span className="honeypot-card__eyebrow">Orchestrator · Container</span>
                    <h3>{honeypot.name || "Unnamed honeypot"}</h3>
                  </div>
                  <span className={`honeypot-card__status ${getStatusClass(status)}`}>
                    <span className="honeypot-card__status-dot" aria-hidden="true" />
                    {status}
                  </span>
                </div>

                <div className="honeypot-card__details">
                  <span>Data source</span>
                  <strong>GET /honeypots</strong>
                </div>
                {status.toLowerCase() === "unknown" && (
                  <p className="honeypot-card__hint">Container was not found by the orchestrator.</p>
                )}
              </article>
            );
          })}
        </div>
      )}
    </section>
  );
}

export default Honeypots;
