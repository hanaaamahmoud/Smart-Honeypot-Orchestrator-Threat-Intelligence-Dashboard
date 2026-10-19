import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  getHoneypots,
} from "../services/api";

function useHoneypotStatus() {
  const [honeypots, setHoneypots] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState(null);

  const fetchHoneypotStatus =
    useCallback(async () => {
      try {
        setLoading(true);
        setError(null);

        const data =
          await getHoneypots();

        setHoneypots(
          Array.isArray(data)
            ? data
            : []
        );
      } catch (error) {
        console.error(
          "Unable to load honeypot status:",
          error
        );

        setHoneypots([]);

        setError(
          "Unable to load honeypot status."
        );
      } finally {
        setLoading(false);
      }
    }, []);

  useEffect(() => {
    fetchHoneypotStatus();
  }, [
    fetchHoneypotStatus,
  ]);

  return {
    honeypots,
    fetchHoneypotStatus,
    loading,
    error,
  };
}

export default useHoneypotStatus;