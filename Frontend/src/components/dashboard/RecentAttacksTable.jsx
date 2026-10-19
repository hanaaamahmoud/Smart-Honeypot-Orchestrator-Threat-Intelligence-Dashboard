// import "../../styles/recent-attacks-table.css";

// function formatTime(timestamp) {
//   if (!timestamp) {
//     return "—";
//   }

//   const date =
//     new Date(timestamp);

//   if (
//     Number.isNaN(
//       date.getTime()
//     )
//   ) {
//     return "—";
//   }

//   return date.toLocaleTimeString(
//     [],
//     {
//       hour: "2-digit",
//       minute: "2-digit",
//     }
//   );
// }

// function RecentAttacksTable({
//   data = [],
// }) {
//   return (
//     <section className="dashboard-table-card">
//       <div className="table-header">
//         <div>
//           <span className="table-label">
//             Activity
//           </span>

//           <h3 className="table-title">
//             Recent Attack Events
//           </h3>
//         </div>

//         <span className="table-count">
//           {data.length} Events
//         </span>
//       </div>

//       <div className="table-wrapper">
//         {data.length === 0 ? (
//           <div className="dashboard-empty-state">
//             No attack events are currently
//             available from the backend.
//           </div>
//         ) : (
//           <table className="attacks-table">
//             <thead>
//               <tr>
//                 <th>Time</th>
//                 <th>Source IP</th>
//                 <th>Country</th>
//                 <th>Honeypot</th>
//                 <th>Protocol</th>
//                 <th>Attack Type</th>
//                 <th>Severity</th>
//               </tr>
//             </thead>

//             <tbody>
//               {data.map((attack) => (
//                 <tr
//                   key={
//                     attack.id ||
//                     `${attack.timestamp}-${attack.sourceIp}`
//                   }
//                 >
//                   <td>
//                     {formatTime(
//                       attack.timestamp
//                     )}
//                   </td>

//                   <td className="source-ip">
//                     {attack.sourceIp ||
//                       "Unknown"}
//                   </td>

//                   <td>
//                     {attack.country ||
//                       "Unknown"}
//                   </td>

//                   <td>
//                     {attack.honeypot ||
//                       "Unknown"}
//                   </td>

//                   <td>
//                     {attack.protocol ||
//                       attack.service ||
//                       "Unknown"}
//                   </td>

//                   <td>
//                     {attack.eventType ||
//                       "Unknown"}
//                   </td>

//                   <td>
//                     <span
//                       className={`attack-status attack-status-${
//                         attack.severity ||
//                         "unknown"
//                       }`}
//                     >
//                       {attack.severity ||
//                         "Unknown"}
//                     </span>
//                   </td>
//                 </tr>
//               ))}
//             </tbody>
//           </table>
//         )}
//       </div>
//     </section>
//   );
// }

// export default RecentAttacksTable;
import "../../styles/recent-attacks-table.css";

function eventKey(
  event,
  index
) {
  return [
    event?.id ?? "event",
    event?.timestamp ?? "time",
    event?.sourceIp ?? "ip",
    event?.sessionId ?? "session",
    index,
  ].join("::");
}

function RecentAttacksTable({
  data = [],
}) {
  return (
    <section className="dashboard-table-card">
      <div className="table-header">
        <div>
          <span className="table-label">
            Activity
          </span>

          <h3 className="table-title">
            Recent Attacks
          </h3>
        </div>

        <span className="table-count">
          {data.length} Events
        </span>
      </div>

      <div className="table-wrapper">
        {data.length === 0 ? (
          <div className="dashboard-empty-state">
            No recent events available.
          </div>
        ) : (
          <table className="attacks-table">
            <thead>
              <tr>
                <th>Time</th>
                <th>Source IP</th>
                <th>Country</th>
                <th>Honeypot</th>
                <th>Protocol</th>
                <th>Event</th>
                <th>Severity</th>
              </tr>
            </thead>

            <tbody>
              {data.map(
                (attack, index) => (
                  <tr
                    key={eventKey(
                      attack,
                      index
                    )}
                  >
                    <td>
                      {attack.timestamp
                        ? new Date(
                            attack.timestamp
                          ).toLocaleTimeString(
                            [],
                            {
                              hour: "2-digit",
                              minute:
                                "2-digit",
                            }
                          )
                        : "—"}
                    </td>

                    <td className="source-ip">
                      {attack.sourceIp}
                    </td>

                    <td>
                      {attack.country}
                    </td>

                    <td>
                      {attack.honeypot}
                    </td>

                    <td>
                      {attack.protocol}
                    </td>

                    <td>
                      {attack.eventType}
                    </td>

                    <td>
                      <span
                        className={`attack-status attack-status-${String(
                          attack.severity ||
                            attack.status
                        ).toLowerCase()}`}
                      >
                        {attack.severity ||
                          attack.status}
                      </span>
                    </td>
                  </tr>
                )
              )}
            </tbody>
          </table>
        )}
      </div>
    </section>
  );
}

export default RecentAttacksTable;