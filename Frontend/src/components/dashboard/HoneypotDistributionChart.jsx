import "../../styles/honeypot-distribution-chart.css";

function HoneypotDistributionChart({ data = [] }) {
  const totalAttacks = data.reduce(
    (total, item) => total + (item.attacks || 0),
    0
  );

  return (
    <section className="honeypot-distribution">
      <div className="honeypot-distribution__header">
        <div>
          <span className="honeypot-distribution__label">
            Attack Distribution
          </span>

          <h3>Honeypot Distribution</h3>
        </div>

        <span className="honeypot-distribution__total">
          {totalAttacks.toLocaleString()} attacks
        </span>
      </div>

      {data.length === 0 ? (
        <div className="honeypot-distribution__empty">
          <span>No distribution data available.</span>
        </div>
      ) : (
        <div className="honeypot-distribution__list">
          {data.map((item) => {
            const percentage =
              totalAttacks > 0
                ? (item.attacks / totalAttacks) * 100
                : 0;

            return (
              <div
                className="honeypot-distribution__item"
                key={item.honeypot}
              >
                <div className="honeypot-distribution__top">
                  <span className="honeypot-distribution__name">
                    {item.honeypot}
                  </span>

                  <span className="honeypot-distribution__value">
                    {item.attacks.toLocaleString()}
                  </span>
                </div>

                <div className="honeypot-distribution__bar">
                  <div
                    className="honeypot-distribution__bar-fill"
                    style={{
                      width: `${percentage}%`,
                    }}
                  />
                </div>

                <div className="honeypot-distribution__bottom">
                  <span>
                    {percentage.toFixed(1)}% of attacks
                  </span>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </section>
  );
}

export default HoneypotDistributionChart;
