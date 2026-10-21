import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  getRecentEvents,
} from "../services/api";

function useAttacks() {
  const [attacks, setAttacks] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState(null);

  const fetchAttacks =
    useCallback(async () => {
      try {
        setLoading(true);
        setError(null);

        const data =
          await getRecentEvents(10);

        setAttacks(
          Array.isArray(data)
            ? data
            : []
        );
      } catch (error) {
        console.error(
          "Unable to load recent attacks:",
          error
        );

        setAttacks([]);
        setError(
          "Unable to load recent attacks."
        );
      } finally {
        setLoading(false);
      }
    }, []);

  useEffect(() => {
    fetchAttacks();
  }, [fetchAttacks]);

  return {
    attacks,
    fetchAttacks,
    loading,
    error,
  };
}

export default useAttacks;