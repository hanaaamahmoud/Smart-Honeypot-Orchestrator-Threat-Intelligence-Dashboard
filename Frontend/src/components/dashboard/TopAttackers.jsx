import "../../styles/top-attackers.css";

function TopAttackers({
attackers = [],
loading = false,
error = null,
}) {
return ( <section className="top-attackers"> <div className="top-attackers__header"> <div> <span className="top-attackers__eyebrow">
Threat Sources </span>

 
      <h3>
        Top Attackers
      </h3>
    </div>

    <span className="top-attackers__count">
      {attackers.length} Sources
    </span>
  </div>

  {loading ? (
    <div className="top-attackers__empty">
      Loading attacker data...
    </div>
  ) : error ? (
    <div className="top-attackers__empty">
      Attacker ranking is currently unavailable.
    </div>
  ) : attackers.length === 0 ? (
    <div className="top-attackers__empty">
      No attacker ranking data returned.
    </div>
  ) : (
    <div className="top-attackers__list">
      {attackers.map(
        (attacker, index) => (
          <article
            key={`${attacker.ip}-${index}`}
            className="top-attackers__item"
          >
            <div className="top-attackers__rank">
              #{index + 1}
            </div>

            <div className="top-attackers__main">
              <strong>
                {attacker.ip || "—"}
              </strong>

              <span>
                Source IP
              </span>
            </div>

            <div className="top-attackers__value">
              <strong>
                {Number(
                  attacker.count
                ).toLocaleString()}
              </strong>

              <span>
                Events
              </span>
            </div>
          </article>
        )
      )}
    </div>
  )}
</section>
 

);
}

export default TopAttackers;
