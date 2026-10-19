import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  getByCountry,
  getByHoneypot,
  getByMitre,
  getByProtocol,
  getByReputation,
  getBySeverity,
  getRecentEvents,
  getStatistics,
  getTimeline,
  getTopAttackers,
} from "../services/api";

const EMPTY = {
  statistics: {
    totalAttacks: 0,
    uniqueAttackers: 0,
    countries: 0,
    topCountries: [],
  },

  attacks: [],
  timeline: [],
  honeypots: [],
  protocols: [],
  severity: [],
  countries: [],
  mitre: [],
  reputation: [],
  topAttackers: [],
};

function useDashboardData() {
  const [
    data,
    setData,
  ] = useState(EMPTY);

  const [
    loading,
    setLoading,
  ] = useState(true);

  const [
    loaded,
    setLoaded,
  ] = useState(false);

  const fetchDashboard =
    useCallback(async () => {
      setLoading(true);

      /*
       * IMPORTANT:
       *
       * Do NOT use Promise.all().
       *
       * If one endpoint returns 503,
       * Promise.all() rejects the entire dashboard.
       *
       * Promise.allSettled() lets successful
       * backend sections render normally.
       */

      const results =
        await Promise.allSettled([
          getStatistics(),
          getRecentEvents(50),
          getTimeline(),
          getByHoneypot(),
          getByProtocol(),
          getBySeverity(),
          getByCountry(),
          getByMitre(),
          getByReputation(),
          getTopAttackers(),
        ]);

      setData({
        statistics:
          results[0].status ===
          "fulfilled"
            ? results[0].value
            : EMPTY.statistics,

        attacks:
          results[1].status ===
          "fulfilled"
            ? results[1].value
            : [],

        timeline:
          results[2].status ===
          "fulfilled"
            ? results[2].value
            : [],

        honeypots:
          results[3].status ===
          "fulfilled"
            ? results[3].value
            : [],

        protocols:
          results[4].status ===
          "fulfilled"
            ? results[4].value
            : [],

        severity:
          results[5].status ===
          "fulfilled"
            ? results[5].value
            : [],

        countries:
          results[6].status ===
          "fulfilled"
            ? results[6].value
            : [],

        mitre:
          results[7].status ===
          "fulfilled"
            ? results[7].value
            : [],

        reputation:
          results[8].status ===
          "fulfilled"
            ? results[8].value
            : [],

        topAttackers:
          results[9].status ===
          "fulfilled"
            ? results[9].value
            : [],
      });

      setLoaded(true);
      setLoading(false);
    }, []);

  useEffect(() => {
    fetchDashboard();
  }, [fetchDashboard]);

  return {
    ...data,
    loading,
    loaded,
    refresh:
      fetchDashboard,
  };
}

export default useDashboardData;