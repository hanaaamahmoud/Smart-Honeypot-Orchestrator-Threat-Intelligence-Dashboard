import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  getStatistics,
} from "../services/api";

function useStatistics() {
  const [statistics, setStatistics] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState(null);

  const fetchStatistics =
    useCallback(async () => {
      try {
        setLoading(true);
        setError(null);

        const data =
          await getStatistics();

        setStatistics(
          data || null
        );
      } catch (error) {
        console.error(
          "Unable to load statistics:",
          error
        );

        setStatistics(null);

        setError(
          "Unable to load statistics."
        );
      } finally {
        setLoading(false);
      }
    }, []);

  useEffect(() => {
    fetchStatistics();
  }, [fetchStatistics]);

  return {
    statistics,
    fetchStatistics,
    loading,
    error,
  };
}

export default useStatistics;