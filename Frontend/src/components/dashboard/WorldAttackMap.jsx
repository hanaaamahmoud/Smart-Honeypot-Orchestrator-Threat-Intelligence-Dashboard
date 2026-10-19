// // import { useMemo } from "react";
// // import { geoMercator, geoPath } from "d3-geo";
// // import { feature } from "topojson-client";
// // import worldData from "world-atlas/countries-110m.json";

// // import "../../styles/world-attack-map.css";

// // const mockOrigins = [
// //   {
// //     id: "origin-001",
// //     country: "Germany",
// //     coordinates: [10.4515, 51.1657],
// //     attacks: 42,
// //   },
// //   {
// //     id: "origin-002",
// //     country: "United States",
// //     coordinates: [-95.7129, 37.0902],
// //     attacks: 31,
// //   },
// //   {
// //     id: "origin-003",
// //     country: "Russia",
// //     coordinates: [105.3188, 61.524],
// //     attacks: 27,
// //   },
// //   {
// //     id: "origin-004",
// //     country: "India",
// //     coordinates: [78.9629, 20.5937],
// //     attacks: 24,
// //   },
// //   {
// //     id: "origin-005",
// //     country: "Egypt",
// //     coordinates: [30.8025, 26.8206],
// //     attacks: 18,
// //   },
// // ];

// // const width = 1000;
// // const height = 500;

// // function WorldAttackMap() {
// //   const countries = useMemo(() => {
// //     return feature(
// //       worldData,
// //       worldData.objects.countries
// //     ).features;
// //   }, []);

// //   const projection = useMemo(() => {
// //     return geoMercator()
// //       .scale(155)
// //       .translate([width / 2, height / 1.55]);
// //   }, []);

// //   const pathGenerator = useMemo(() => {
// //     return geoPath().projection(projection);
// //   }, [projection]);

// //   return (
// //     <section className="world-attack-map">
// //       <div className="world-attack-map__header">
// //         <div>
// //           <span className="world-attack-map__eyebrow">
// //             Geographic Intelligence
// //           </span>

// //           <h3 className="world-attack-map__title">
// //             World Attack Map
// //           </h3>
// //         </div>

// //         <div className="world-attack-map__legend">
// //           <span className="world-attack-map__legend-dot" />
// //           Attack Origin
// //         </div>
// //       </div>

// //       <div className="world-attack-map__body">
// //         <svg
// //           viewBox={`0 0 ${width} ${height}`}
// //           className="world-attack-map__svg"
// //           role="img"
// //           aria-label="World map showing attack origins"
// //         >
// //           <g>
// //             {countries.map((country) => (
// //               <path
// //                 key={country.id}
// //                 d={pathGenerator(country)}
// //                 className="world-map-country"
// //               />
// //             ))}
// //           </g>

// //           <g>
// //             {mockOrigins.map((origin) => {
// //               const [x, y] = projection(
// //                 origin.coordinates
// //               );

// //               if (
// //                 !Number.isFinite(x) ||
// //                 !Number.isFinite(y)
// //               ) {
// //                 return null;
// //               }

// //               return (
// //                 <g
// //                   key={origin.id}
// //                   className="world-map-origin"
// //                 >
// //                   <circle
// //                     cx={x}
// //                     cy={y}
// //                     r="11"
// //                     className="world-map-marker-pulse"
// //                   />

// //                   <circle
// //                     cx={x}
// //                     cy={y}
// //                     r="4"
// //                     className="world-map-marker"
// //                   />

// //                   <title>
// //                     {origin.country}: {origin.attacks} attacks
// //                   </title>
// //                 </g>
// //               );
// //             })}
// //           </g>
// //         </svg>
// //       </div>

// //       <div className="world-attack-map__footer">
// //         <span>
// //           {mockOrigins.length} monitored origins
// //         </span>

// //         <span>
// //           Mock GeoIP data
// //         </span>
// //       </div>
// //     </section>
// //   );
// // }

// // export default WorldAttackMap;

// /*
//  * FUTURE WORK
//  *
//  * The backend currently does not provide a dedicated
//  * geographic attack-origin endpoint.
//  *
//  * The previous implementation used hard-coded mock
//  * GeoIP data, which must not be displayed as real data.
//  *
//  * Expected future backend contract:
//  *
//  * GET /attack-origins
//  *
//  * Example future response:
//  *
//  * [
//  *   {
//  *     "country": "Egypt",
//  *     "country_code": "EG",
//  *     "attacks": 42
//  *   }
//  * ]
//  *
//  * Once the backend provides real GeoIP attack-origin data,
//  * this component can be restored and connected through
//  * the API adapter without changing the dashboard architecture.
//  */
// // *********************************************************************************

// // import {
// // useMemo,
// // } from "react";

// // import {
// // geoMercator,
// // geoPath,
// // } from "d3-geo";

// // import {
// // feature,
// // } from "topojson-client";

// // import worldData from "world-atlas/countries-110m.json";

// // import "../../styles/world-attack-map.css";

// // /*

// // * Presentation-only geographic coordinates.
// // *
// // * IMPORTANT:
// // * These coordinates are NOT attack data.
// // * The backend supplies the real country + attack count.
// // *
// // * They are only used to place the backend country
// // * result on the existing world map.
// //   */
// //   const COUNTRY_COORDINATES = {
// //   Afghanistan: [67.709953, 33.93911],
// //   Albania: [20.168331, 41.153332],
// //   Algeria: [1.659626, 28.033886],
// //   Argentina: [-63.616672, -38.416097],
// //   Armenia: [45.038189, 40.069099],
// //   Australia: [133.775136, -25.274398],
// //   Austria: [14.550072, 47.516231],
// //   Azerbaijan: [47.576927, 40.143105],
// //   Bahrain: [50.637772, 26.0667],
// //   Bangladesh: [90.356331, 23.684994],
// //   Belarus: [27.953389, 53.709807],
// //   Belgium: [4.469936, 50.503887],
// //   Bolivia: [-63.588653, -16.290154],
// //   Bosnia: [17.679076, 43.915886],
// //   "Bosnia and Herzegovina": [
// //   17.679076,
// //   43.915886,
// //   ],
// //   Brazil: [-51.92528, -14.235004],
// //   Bulgaria: [25.48583, 42.733883],
// //   Cambodia: [104.990963, 12.565679],
// //   Cameroon: [12.354722, 7.369722],
// //   Canada: [-106.346771, 56.130366],
// //   Chile: [-71.542969, -35.675147],
// //   China: [104.195397, 35.86166],
// //   Colombia: [-74.297333, 4.570868],
// //   Croatia: [15.2, 45.1],
// //   Cuba: [-77.781167, 21.521757],
// //   Cyprus: [33.429859, 35.126413],
// //   "Czech Republic": [
// //   15.472962,
// //   49.817492,
// //   ],
// //   Czechia: [15.472962, 49.817492],
// //   Denmark: [9.501785, 56.26392],
// //   Ecuador: [-78.183406, -1.831239],
// //   Egypt: [30.802498, 26.820553],
// //   Estonia: [25.013607, 58.595272],
// //   Ethiopia: [40.489673, 9.145],
// //   Finland: [25.748151, 61.92411],
// //   France: [2.213749, 46.227638],
// //   Georgia: [43.356892, 42.315407],
// //   Germany: [10.451526, 51.165691],
// //   Ghana: [-1.023194, 7.946527],
// //   Greece: [21.824312, 39.074208],
// //   Hungary: [19.503304, 47.162494],
// //   Iceland: [-19.020835, 64.963051],
// //   India: [78.96288, 20.593684],
// //   Indonesia: [113.921327, -0.789275],
// //   Iran: [53.688046, 32.427908],
// //   Iraq: [43.679291, 33.223191],
// //   Ireland: [-8.24389, 53.41291],
// //   Israel: [34.851612, 31.046051],
// //   Italy: [12.56738, 41.87194],
// //   Japan: [138.252924, 36.204824],
// //   Jordan: [36.238414, 30.585164],
// //   Kazakhstan: [66.923684, 48.019573],
// //   Kenya: [37.906193, -0.023559],
// //   Kuwait: [47.481766, 29.31166],
// //   Latvia: [24.603189, 56.879635],
// //   Lebanon: [35.862285, 33.854721],
// //   Libya: [17.228331, 26.3351],
// //   Lithuania: [23.881275, 55.169438],
// //   Luxembourg: [6.129583, 49.815273],
// //   Malaysia: [101.975766, 4.210484],
// //   Mexico: [-102.552784, 23.634501],
// //   Moldova: [28.369885, 47.411631],
// //   Mongolia: [103.846656, 46.862496],
// //   Montenegro: [19.37439, 42.708678],
// //   Morocco: [-7.09262, 31.791702],
// //   Nepal: [84.124008, 28.394857],
// //   Netherlands: [5.291266, 52.132633],
// //   "New Zealand": [174.885971, -40.900557],
// //   Nigeria: [8.675277, 9.081999],
// //   Norway: [8.468946, 60.472024],
// //   Oman: [55.923255, 21.512583],
// //   Pakistan: [69.345116, 30.375321],
// //   Palestine: [35.233154, 31.952162],
// //   Panama: [-80.782127, 8.537981],
// //   Peru: [-75.015152, -9.189967],
// //   Philippines: [121.774017, 12.879721],
// //   Poland: [19.145136, 51.919438],
// //   Portugal: [-8.224454, 39.399872],
// //   Qatar: [51.183884, 25.354826],
// //   Romania: [24.96676, 45.943161],
// //   Russia: [105.318756, 61.52401],
// //   SaudiArabia: [45.079162, 23.885942],
// //   Senegal: [-14.452362, 14.497401],
// //   Serbia: [21.005859, 44.016521],
// //   Singapore: [103.819836, 1.352083],
// //   Slovakia: [19.699024, 48.669026],
// //   Slovenia: [14.995463, 46.151241],
// //   "South Africa": [22.937506, -30.559482],
// //   "South Korea": [127.766922, 35.907757],
// //   Spain: [-3.74922, 40.463667],
// //   Sudan: [30.217636, 12.862807],
// //   Sweden: [18.643501, 60.128161],
// //   Switzerland: [8.227512, 46.818188],
// //   Syria: [38.996815, 34.802075],
// //   Taiwan: [120.960515, 23.69781],
// //   Thailand: [100.992541, 15.870032],
// //   Tunisia: [9.537499, 33.886917],
// //   Turkey: [35.243322, 38.963745],
// //   Ukraine: [31.16558, 48.379433],
// //   "United Arab Emirates": [
// //   53.847818,
// //   23.424076,
// //   ],
// //   "United Kingdom": [
// //   -3.435973,
// //   55.378051,
// //   ],
// //   UK: [-3.435973, 55.378051],
// //   "United States": [
// //   -95.712891,
// //   37.09024,
// //   ],
// //   USA: [-95.712891, 37.09024],
// //   Uruguay: [-55.765835, -32.522779],
// //   Uzbekistan: [64.585262, 41.377491],
// //   Venezuela: [-66.58973, 6.42375],
// //   Vietnam: [108.277199, 14.058324],
// //   Yemen: [48.516388, 15.552727],
// //   Zambia: [27.849332, -13.133897],
// //   Zimbabwe: [29.154857, -19.015438],
// //   };

// // const width = 1000;
// // const height = 500;

// // function WorldAttackMap({
// // origins = [],
// // }) {
// // const countries =
// // useMemo(() => {
// // return feature(
// // worldData,
// // worldData.objects.countries
// // ).features;
// // }, []);

// // const projection =
// // useMemo(() => {
// // return geoMercator()
// // .scale(155)
// // .translate([
// // width / 2,
// // height / 1.55,
// // ]);
// // }, []);

// // const pathGenerator =
// // useMemo(() => {
// // return geoPath()
// // .projection(projection);
// // }, [projection]);

// // const mapOrigins =
// // useMemo(() => {
// // return origins
// // .map((origin, index) => {
// // const country =
// // origin?.country;

 
// //       const coordinates =
// //         COUNTRY_COORDINATES[
// //           country
// //         ];

// //       if (
// //         !country ||
// //         !coordinates
// //       ) {
// //         return null;
// //       }

// //       return {
// //         id:
// //           `backend-origin-${country}-${index}`,

// //         country,

// //         coordinates,

// //         attacks:
// //           Number(
// //             origin.count
// //           ) || 0,
// //       };
// //     })
// //     .filter(Boolean);
// // }, [origins]);
 

// // return ( <section className="world-attack-map"> <div className="world-attack-map__header"> <div> <span className="world-attack-map__eyebrow">
// // Geographic Intelligence </span>

 
// //       <h3 className="world-attack-map__title">
// //         World Attack Map
// //       </h3>
// //     </div>

// //     <div className="world-attack-map__legend">
// //       <span className="world-attack-map__legend-dot" />
// //       Backend Attack Origin
// //     </div>
// //   </div>

// //   <div className="world-attack-map__body">
// //     {mapOrigins.length === 0 ? (
// //       <div className="world-attack-map__empty">
// //         <strong>
// //           No geographic attack data returned.
// //         </strong>

// //         <span>
// //           The map will populate automatically
// //           when the backend returns country data.
// //         </span>
// //       </div>
// //     ) : (
// //       <svg
// //         viewBox={`0 0 ${width} ${height}`}
// //         className="world-attack-map__svg"
// //         role="img"
// //         aria-label="World map showing backend attack origins"
// //       >
// //         <g>
// //           {countries.map(
// //             (country) => (
// //               <path
// //                 key={country.id}
// //                 d={pathGenerator(
// //                   country
// //                 )}
// //                 className="world-map-country"
// //               />
// //             )
// //           )}
// //         </g>

// //         <g>
// //           {mapOrigins.map(
// //             (origin) => {
// //               const projected =
// //                 projection(
// //                   origin.coordinates
// //                 );

// //               if (
// //                 !projected
// //               ) {
// //                 return null;
// //               }

// //               const [
// //                 x,
// //                 y,
// //               ] = projected;

// //               if (
// //                 !Number.isFinite(x) ||
// //                 !Number.isFinite(y)
// //               ) {
// //                 return null;
// //               }

// //               return (
// //                 <g
// //                   key={origin.id}
// //                   className="world-map-origin"
// //                 >
// //                   <circle
// //                     cx={x}
// //                     cy={y}
// //                     r="11"
// //                     className="world-map-marker-pulse"
// //                   />

// //                   <circle
// //                     cx={x}
// //                     cy={y}
// //                     r="4"
// //                     className="world-map-marker"
// //                   />

// //                   <title>
// //                     {origin.country}:{" "}
// //                     {origin.attacks}{" "}
// //                     attacks
// //                   </title>
// //                 </g>
// //               );
// //             }
// //           )}
// //         </g>
// //       </svg>
// //     )}
// //   </div>

// //   <div className="world-attack-map__footer">
// //     <span>
// //       {mapOrigins.length} monitored origins
// //     </span>

// //     <span>
// //       Backend geographic data
// //     </span>
// //   </div>
// // </section>
 

// // );
// // }

// // export default WorldAttackMap;

// import { useMemo } from "react";
// import { geoMercator, geoPath } from "d3-geo";
// import { feature } from "topojson-client";
// import worldData from "world-atlas/countries-110m.json";

// import "../../styles/world-attack-map.css";

// const COUNTRY_COORDINATES = {
//   Egypt: [30.8025, 26.8206],
//   Germany: [10.4515, 51.1657],
//   "United States": [-95.7129, 37.0902],
//   USA: [-95.7129, 37.0902],
//   Russia: [105.3188, 61.524],
//   India: [78.9629, 20.5937],
//   China: [104.1954, 35.8617],
//   Brazil: [-51.9253, -14.235],
//   France: [2.2137, 46.2276],
//  "nited Kingdo": [-3.436, 55.3781],
//   Canada: [-106.3468, 56.1304],
//   Australia: [133.7751, -25.2744],
//   Japan: [138.2529, 36.2048],
//   Turkey: [35.2433, 38.9637],
//   Netherlands: [5.2913, 52.1326],
//   Ukraine: [31.1656, 48.3794],
//   Iran: [53.688, 32.4279],
//   Pakistan: [69.3451, 30.3753],
//   "South Africa": [22.9375, -30.5595],
// };

// const width = 1000;
// const height = 500;

// function WorldAttackMap({ data = [] }) {
//   const countries = useMemo(() => {
//     return feature(
//       worldData,
//       worldData.objects.countries
//     ).features;
//   }, []);

//   const projection = useMemo(() => {
//     return geoMercator()
//       .scale(155)
//       .translate([width / 2, height / 1.55]);
//   }, []);

//   const pathGenerator = useMemo(() => {
//     return geoPath().projection(projection);
//   }, [projection]);

//   const origins = useMemo(() => {
//     if (!Array.isArray(data)) {
//       return [];
//     }

//     return data
//       .map((item, index) => {
//         const country =
//           item.country ||
//           item.name ||
//           item.countryName;

//         const coordinates =
//           COUNTRY_COORDINATES[country];

//         if (!country || !coordinates) {
//           return null;
//         }

//         return {
//           id:
//             `${country}-${index}`,
//           country,
//           coordinates,
//           attacks:
//             Number(item.count ?? item.attacks ?? 0),
//         };
//       })
//       .filter(Boolean);
//   }, [data]);

//   return (
//     <section className="world-attack-map">
//       <div className="world-attack-map__header">
//         <div>
//           <span className="world-attack-map__eyebrow">
//             Geographic Intelligence
//           </span>

//           <h3 className="world-attack-map__title">
//             World Attack Map
//           </h3>
//         </div>

//         <div className="world-attack-map__legend">
//           <span className="world-attack-map__legend-dot" />
//           Attack Origin
//         </div>
//       </div>

//       <div className="world-attack-map__body">
//         <svg
//           viewBox={`0 0 ${width} ${height}`}
//           className="world-attack-map__svg"
//           role="img"
//           aria-label="World map showing attack origins"
//         >
//           <g>
//             {countries.map((country) => (
//               <path
//                 key={country.id}
//                 d={pathGenerator(country)}
//                 className="world-map-country"
//               />
//             ))}
//           </g>

//           <g>
//             {origins.map((origin) => {
//               const [x, y] =
//                 projection(
//                   origin.coordinates
//                 );

//               if (
//                 !Number.isFinite(x) ||
//                 !Number.isFinite(y)
//               ) {
//                 return null;
//               }

//               return (
//                 <g
//                   key={origin.id}
//                   className="world-map-origin"
//                 >
//                   <circle
//                     cx={x}
//                     cy={y}
//                     r="11"
//                     className="world-map-marker-pulse"
//                   />

//                   <circle
//                     cx={x}
//                     cy={y}
//                     r="4"
//                     className="world-map-marker"
//                   />

//                   <title>
//                     {origin.country}:{" "}
//                     {origin.attacks} attacks
//                   </title>
//                 </g>
//               );
//             })}
//           </g>
//         </svg>

//         {origins.length === 0 && (
//           <div className="world-attack-map__empty">
//             No attack origin data available yet.
//           </div>
//         )}
//       </div>

//       <div className="world-attack-map__footer">
//         <span>
//           {origins.length} monitored origins
//         </span>

//         <span>
//           Live threat-intelligence data
//         </span>
//       </div>
//     </section>
//   );
// }

// export default WorldAttackMap;
import "../../styles/world-attack-map.css";

const COUNTRY_COORDINATES = {
  Egypt: [30.8025, 26.8206],
  Germany: [10.4515, 51.1657],
  "United States": [
    -95.7129,
    37.0902,
  ],
  Russia: [
    105.3188,
    61.524,
  ],
  India: [
    78.9629,
    20.5937,
  ],
  France: [
    2.2137,
    46.2276,
  ],
  China: [
    104.1954,
    35.8617,
  ],
  Brazil: [
    -51.9253,
    -14.235,
  ],
  Japan: [
    138.2529,
    36.2048,
  ],
  "United Kingdom": [
    -3.436,
    55.3781,
  ],
  Turkey: [
    35.2433,
    38.9637,
  ],
  Netherlands: [
    5.2913,
    52.1326,
  ],
  Canada: [
    -106.3468,
    56.1304,
  ],
  Ukraine: [
    31.1656,
    48.3794,
  ],
};

const width = 1000;
const height = 500;

function project([
  longitude,
  latitude,
]) {
  return [
    ((longitude + 180) /
      360) *
      width,

    ((90 - latitude) /
      180) *
      height,
  ];
}

function WorldAttackMap({
  data = [],
}) {
  const origins =
    data
      .filter(
        (item) =>
          COUNTRY_COORDINATES[
            item.label
          ]
      )
      .slice(0, 14);

  return (
    <section className="world-attack-map">
      <div className="world-attack-map__header">
        <div>
          <span className="world-attack-map__eyebrow">
            Geographic Intelligence
          </span>

          <h3 className="world-attack-map__title">
            World Attack Origins
          </h3>
        </div>

        <div className="world-attack-map__legend">
          <span className="world-attack-map__legend-dot" />
          Real backend data
        </div>
      </div>

      <div className="world-attack-map__body">
        {origins.length ===
        0 ? (
          <div className="dashboard-empty-state">
            No country data
            available from
            the backend.
          </div>
        ) : (
          <div className="world-map-real">
            {origins.map(
              (
                origin,
                index
              ) => {
                const [
                  x,
                  y,
                ] =
                  project(
                    COUNTRY_COORDINATES[
                      origin.label
                    ]
                  );

                return (
                  <div
                    key={`${origin.label}-${index}`}
                    className="world-map-origin"
                    style={{
                      left: `${
                        (x /
                          width) *
                        100
                      }%`,
                      top: `${
                        (y /
                          height) *
                        100
                      }%`,
                    }}
                  >
                    <span className="world-map-marker-pulse" />

                    <span className="world-map-marker" />

                    <span className="world-map-tooltip">
                      {
                        origin.label
                      }
                      :{" "}
                      {origin.value.toLocaleString()}{" "}
                      events
                    </span>
                  </div>
                );
              }
            )}

            <div className="world-map-grid-label">
              Coordinates are
              display metadata;
              attack counts come
              from the backend.
            </div>
          </div>
        )}
      </div>

      <div className="world-attack-map__footer">
        <span>
          {data.length} countries
          in backend
          aggregation
        </span>

        <span>
          No mock attack
          origins
        </span>
      </div>
    </section>
  );
}

export default WorldAttackMap;