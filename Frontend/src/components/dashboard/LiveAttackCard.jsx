import "../../styles/live-attack-card.css";

function LiveAttackCard({
  attack,
}) {
  return (
    <article className="live-attack-card">
      <div className="live-attack-card__header">
        <div>
          <span className="live-attack-card__status">
            LIVE
          </span>

          <h3>
            {attack.eventType ||
              "Unknown attack"}
          </h3>
        </div>

        <span className="live-attack-card__time">
          {attack.timestamp ||
            "—"}
        </span>
      </div>

      <div className="live-attack-card__details">
        <div>
          <span>
            Source IP
          </span>

          <strong>
            {attack.sourceIp ||
              "Unknown"}
          </strong>
        </div>

        <div>
          <span>
            Country
          </span>

          <strong>
            {attack.country ||
              "Unknown"}
          </strong>
        </div>

        <div>
          <span>
            Honeypot
          </span>

          <strong>
            {attack.honeypot ||
              "Unknown"}
          </strong>
        </div>

        <div>
          <span>
            Protocol
          </span>

          <strong>
            {attack.protocol ||
              attack.service ||
              "Unknown"}
          </strong>
        </div>
      </div>

      <div className="live-attack-card__footer">
        <span>
          Severity:{" "}
          {attack.severity ||
            "Unknown"}
        </span>
      </div>
    </article>
  );
}

export default LiveAttackCard;