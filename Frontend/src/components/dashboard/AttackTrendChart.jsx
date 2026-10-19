import "../../styles/attack-trend-chart.css";

function AttackTrendChart({
  data = [],
}) {
  const width = 760;
  const height = 280;

  const left = 48;
  const right = 20;
  const top = 20;
  const bottom = 45;

  const values =
    data.map(
      (item) =>
        Number(
          item.attacks ?? 0
        )
    );

  const max =
    Math.max(
      ...values,
      1
    );

  const getX =
    (index) =>
      data.length > 1
        ? left +
          (index /
            (data.length -
              1)) *
            (width -
              left -
              right)
        : left +
          (width -
            left -
            right) /
            2;

  const getY =
    (value) =>
      top +
      (height -
        top -
        bottom) -
      (value / max) *
        (height -
          top -
          bottom);

  const points =
    data
      .map(
        (item, index) =>
          `${getX(
            index
          )},${getY(
            Number(
              item.attacks ??
                0
            )
          )}`
      )
      .join(" ");

  return (
    <section className="chart-card">
      <div className="chart-header">
        <div>
          <span className="chart-label-small">
            Activity
          </span>

          <h3 className="chart-title">
            Attack Trend
          </h3>
        </div>

        <span className="chart-period">
          Backend timeline
        </span>
      </div>

      <div className="chart-container">
        {data.length === 0 ? (
          <div className="dashboard-empty-state">
            No timeline data available.
          </div>
        ) : (
          <svg
            viewBox={`0 0 ${width} ${height}`}
            preserveAspectRatio="none"
            className="attack-chart"
            role="img"
            aria-label="Attack events over time"
          >
            <line
              x1={left}
              y1={top}
              x2={left}
              y2={
                height -
                bottom
              }
              className="chart-axis"
            />

            <line
              x1={left}
              y1={
                height -
                bottom
              }
              x2={
                width -
                right
              }
              y2={
                height -
                bottom
              }
              className="chart-axis"
            />

            <polyline
              points={points}
              fill="none"
              className="attack-chart-line"
            />

            {data.map(
              (
                item,
                index
              ) => (
                <circle
                  key={`${item.timestamp ?? "point"}-${index}`}
                  cx={getX(
                    index
                  )}
                  cy={getY(
                    Number(
                      item.attacks ??
                        0
                    )
                  )}
                  r="4"
                  className="attack-chart-point"
                >
                  <title>
                    {String(
                      item.timestamp
                    )}
                    :{" "}
                    {
                      item.attacks
                    }{" "}
                    events
                  </title>
                </circle>
              )
            )}
          </svg>
        )}
      </div>
    </section>
  );
}

export default AttackTrendChart;