import "../../styles/recent-attacks-table.css";

function TopAttackersTable({
  data = [],
}) {
  return (
    <section className="dashboard-table-card">
      <div className="table-header">
        <div>
          <span className="table-label">
            Threat Activity
          </span>

          <h3 className="table-title">
            Top Attackers
          </h3>
        </div>

        <span className="table-count">
          {data.length} Sources
        </span>
      </div>

      <div className="table-wrapper">
        <table className="attacks-table">
          <thead>
            <tr>
              <th>Rank</th>
              <th>Source IP</th>
              <th>Attack Count</th>
            </tr>
          </thead>

          <tbody>
            {data.length === 0 ? (
              <tr>
                <td
                  colSpan="3"
                  style={{
                    textAlign: "center",
                    padding: "32px",
                  }}
                >
                  No attacker data available.
                </td>
              </tr>
            ) : (
              data.map(
                (attacker, index) => (
                  <tr
                    key={attacker.id}
                  >
                    <td>
                      #{index + 1}
                    </td>

                    <td className="source-ip">
                      {attacker.ip}
                    </td>

                    <td>
                      {attacker.count.toLocaleString()}
                    </td>
                  </tr>
                )
              )
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default TopAttackersTable;