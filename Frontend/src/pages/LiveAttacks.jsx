import {
  useMemo,
} from "react";

import LiveAttackCard from "../components/dashboard/LiveAttackCard";
import useSocket from "../hooks/useSocket";

import "../styles/live-attacks.css";

function LiveAttacks() {
  const {
    isConnected,
    events,
  } = useSocket();

  const attacks =
    useMemo(
      () => events,
      [events]
    );

  const failedAttempts =
    attacks.filter(
      (attack) =>
        attack.severity ===
        "failed"
    ).length;

  const detectedEvents =
    attacks.filter(
      (attack) =>
        attack.severity !==
          "failed" &&
        attack.severity !==
          "unknown"
    ).length;

  return (
    <section className="live-attacks-page">
      <div className="live-attacks-header">
        <div>
          <span className="page-eyebrow">
            Real-Time Monitoring
          </span>

          <h2>
            Live Attacks
          </h2>

          <p>
            Real-time attack events
            received from the backend
            WebSocket stream.
          </p>
        </div>

        <div
          className={
            isConnected
              ? "socket-status socket-status--connected"
              : "socket-status socket-status--disconnected"
          }
        >
          <span />

          {isConnected
            ? "Connected"
            : "Disconnected"}
        </div>
      </div>

      <div className="live-attacks-summary">
        <div>
          <span>
            Live Events
          </span>

          <strong>
            {attacks.length}
          </strong>
        </div>

        <div>
          <span>
            Detected
          </span>

          <strong>
            {detectedEvents}
          </strong>
        </div>

        <div>
          <span>
            Failed
          </span>

          <strong>
            {failedAttempts}
          </strong>
        </div>
      </div>

      {attacks.length === 0 ? (
        <div className="dashboard-empty-state">
          No live attack events received yet.
        </div>
      ) : (
        <div className="live-attacks-grid">
          {attacks.map(
            (attack) => (
              <LiveAttackCard
                key={
                  attack.id
                }
                attack={
                  attack
                }
              />
            )
          )}
        </div>
      )}
    </section>
  );
}

export default LiveAttacks;