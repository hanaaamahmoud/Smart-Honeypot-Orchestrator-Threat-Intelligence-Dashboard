import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  getAttackTrend,
} from "../services/api";

function useAttackTrend() {
  const [attackTrend, setAttackTrend] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState(null);

  const fetchAttackTrend =
    useCallback(async () => {
      /*
       * Future backend integration.
       *
       * Backend currently exposes:
       * - /statistics
       * - /events/recent
       * - /attackers/top
       *
       * It does not currently expose an attack-trend
       * aggregation endpoint.
       */

      try {
        setLoading(true);
        setError(null);

        const data =
          await getAttackTrend();

        setAttackTrend(
          Array.isArray(data)
            ? data
            : []
        );
      } catch (error) {
        console.warn(
          "Attack trend API is not implemented yet."
        );

        setAttackTrend([]);

        setError(
          "Attack trend is not available yet."
        );
      } finally {
        setLoading(false);
      }
    }, []);

  useEffect(() => {
    fetchAttackTrend();
  }, [
    fetchAttackTrend,
  ]);

  return {
    attackTrend,
    fetchAttackTrend,
    loading,
    error,
  };
}

export default useAttackTrend;