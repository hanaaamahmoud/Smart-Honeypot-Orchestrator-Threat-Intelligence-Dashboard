import "../styles/statistics.css";

import useStatistics from "../hooks/useStatistics";

function Statistics() {
  const {
    statistics,
    loading,
    error,
  } = useStatistics();

  return (
    <section className="statistics-page">
      <div className="page-header">
        <span className="page-eyebrow">
          Analytics
        </span>

        <h2 className="page-title">
          Statistics
        </h2>

        <p className="page-description">
          Analyze honeypot activity, attack sources,
          and collected security events.
        </p>
      </div>

      {loading && (
        <p>Loading statistics...</p>
      )}

      {error && (
        <p>Unable to load statistics.</p>
      )}

      {!loading && !error && (
        <div className="statistics-summary-grid">
          <div className="statistics-summary-card">
            <span>Total Attacks</span>
            <strong>
              {statistics.totalAttacks.toLocaleString()}
            </strong>
          </div>

          <div className="statistics-summary-card">
            <span>Active Honeypots</span>
            <strong>
              {statistics.activeHoneypots}
            </strong>
          </div>

          <div className="statistics-summary-card">
            <span>Unique Sources</span>
            <strong>
              {statistics.uniqueSources.toLocaleString()}
            </strong>
          </div>

          <div className="statistics-summary-card">
            <span>Countries</span>
            <strong>
              {statistics.countries}
            </strong>
          </div>
        </div>
      )}
    </section>
  );
}

export default Statistics;
