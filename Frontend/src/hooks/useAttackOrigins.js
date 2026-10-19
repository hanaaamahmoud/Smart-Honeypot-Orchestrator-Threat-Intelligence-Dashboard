// import {
//   useCallback,
//   useEffect,
//   useState,
// } from "react";

// import { getStatistics } from "../services/api";

// function useAttackOrigins() {
//   const [origins, setOrigins] =
//     useState([]);

//   const [loading, setLoading] =
//     useState(true);

//   const [error, setError] =
//     useState(null);

//   const fetchAttackOrigins =
//     useCallback(async () => {
//       try {
//         setLoading(true);
//         setError(null);

//         const data =
//           await getStatistics();

//         const countries =
//           Array.isArray(
//             data?.topCountries
//           )
//             ? data.topCountries
//             : [];

//         setOrigins(
//           countries.map(
//             (item) => ({
//               country:
//                 item.country || "_",
//               attacks:
//                 Number(
//                   item.count
//                 ) || 0,
//             })
//           )
//         );
//       } catch (requestError) {
//         console.error(
//           "Failed to load attack origins:",
//           requestError
//         );

//         setOrigins([]);

//         setError(
//           "Unable to load geographic attack data."
//         );
//       } finally {
//         setLoading(false);
//       }
//     }, []);

//   useEffect(() => {
//     fetchAttackOrigins();
//   }, [fetchAttackOrigins]);

//   return {
//     origins,
//     fetchAttackOrigins,
//     loading,
//     error,
//   };
// }

// export default useAttackOrigins;