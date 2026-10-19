import "../../styles/honeypot-status.css";

function HoneypotStatus({
  honeypots = [],
  loading = false,
  error = null,
}) {
  return (
    <section className="honeypot-status">
      <div className="honeypot-status__header">
        <div>
          <span className="honeypot-status__eyebrow">
            Infrastructure
          </span>

          <h3>
            Honeypot Status
          </h3>
        </div>

        <span className="honeypot-status__count">
          {honeypots.length} Honeypots
        </span>
      </div>

      {loading ? (
        <div className="honeypot-status__empty">
          Loading honeypot status...
        </div>
      ) : error ? (
        <div className="honeypot-status__empty">
          Orchestrator status is currently
          unavailable.
        </div>
      ) : honeypots.length === 0 ? (
        <div className="honeypot-status__empty">
          No honeypot status is currently
          available.
        </div>
      ) : (
        <div className="honeypot-status__list">
          {honeypots.map(
            (honeypot) => {
              const status =
                honeypot.status ||
                "unknown";

              const isRunning =
                status ===
                "running";

              return (
                <article
                  key={
                    honeypot.id ||
                    honeypot.name
                  }
                  className="honeypot-status__item"
                >
                  <div className="honeypot-status__main">
                    <div
                      className={`honeypot-status__indicator ${
                        isRunning
                          ? "is-running"
                          : "is-not-running"
                      }`}
                    />

                    <div>
                      <h4>
                        {
                          honeypot.name
                        }
                      </h4>

                      <span>
                        {
                          honeypot.service ||
                          "Unknown service"
                        }
                      </span>
                    </div>
                  </div>

                  <div className="honeypot-status__metrics">
                    <div>
                      <span>
                        Status
                      </span>

                      <strong
                        className={
                          isRunning
                            ? "status-running"
                            : "status-not-running"
                        }
                      >
                        {
                          status
                        }
                      </strong>
                    </div>

                    <div>
                      <span>
                        Events
                      </span>

                      <strong>
                        {
                          honeypot.events ??
                          0
                        }
                      </strong>
                    </div>

                    <div>
                      <span>
                        Last Activity
                      </span>

                      <strong>
                        {
                          honeypot.lastActivity ||
                          "—"
                        }
                      </strong>
                    </div>
                  </div>
                </article>
              );
            }
          )}
        </div>
      )}
    </section>
  );
}

export default HoneypotStatus;