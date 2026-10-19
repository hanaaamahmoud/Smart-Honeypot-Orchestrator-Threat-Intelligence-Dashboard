import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
} from "react";

import {
  getCurrentUser,
  login as loginRequest,
  logout as logoutRequest,
  requestPasswordReset,
  resetPassword,
} from "../services/authService";

const AUTH_STORAGE_KEY =
  "smart_honeypot_mock_session";

const MOCK_USERS_KEY =
  "smart_honeypot_mock_users";

const AuthContext =
  createContext(null);

export function AuthProvider({
  children,
}) {
  const [user, setUser] =
    useState(null);

  const [isLoading, setIsLoading] =
    useState(true);

  const checkSession =
    useCallback(async () => {
      try {
        const currentUser =
          await getCurrentUser();

        setUser(currentUser);
      } catch {
        setUser(null);
      } finally {
        setIsLoading(false);
      }
    }, []);

  useEffect(() => {
    checkSession();
  }, [checkSession]);

  useEffect(() => {
    const handleStorageChange =
      async (event) => {

        /*
         * If another tab changes the
         * authentication session,
         * this tab must immediately
         * become unauthenticated.
         *
         * This handles both:
         *
         * 1. Another tab logs in.
         * 2. Another tab logs out.
         *
         * The current tab does NOT
         * need a refresh.
         */
        if (
          event.key ===
          AUTH_STORAGE_KEY
        ) {
          setUser(null);
          setIsLoading(false);
          return;
        }

        /*
         * If another tab modifies the
         * users database, re-check the
         * current session.
         *
         * This means that if an admin
         * disables or deletes the account
         * currently logged in on another
         * tab, the affected tab will
         * automatically log out.
         */
        if (
          event.key ===
          MOCK_USERS_KEY
        ) {
          await checkSession();
        }
      };

    window.addEventListener(
      "storage",
      handleStorageChange
    );

    return () => {
      window.removeEventListener(
        "storage",
        handleStorageChange
      );
    };
  }, [checkSession]);

  const login = useCallback(
    async (
      email,
      password
    ) => {
      const authenticatedUser =
        await loginRequest(
          email,
          password
        );

      setUser(
        authenticatedUser
      );

      return authenticatedUser;
    },
    []
  );

  const logout =
    useCallback(async () => {
      await logoutRequest();

      setUser(null);
    }, []);

  const forgotPassword =
    useCallback(
      async (email) => {
        return requestPasswordReset(
          email
        );
      },
      []
    );

  const updatePassword =
    useCallback(
      async (
        token,
        password
      ) => {
        return resetPassword(
          token,
          password
        );
      },
      []
    );

  const value = useMemo(
    () => ({
      user,
      isAuthenticated:
        Boolean(user),
      isLoading,

      login,
      logout,

      forgotPassword,
      updatePassword,

      checkSession,
    }),
    [
      user,
      isLoading,
      login,
      logout,
      forgotPassword,
      updatePassword,
      checkSession,
    ]
  );

  return (
    <AuthContext.Provider
      value={value}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context =
    useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used inside AuthProvider"
    );
  }

  return context;
}