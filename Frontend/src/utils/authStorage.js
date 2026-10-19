// const ACCESS_TOKEN_KEY = "smart_honeypot_access_token";
// const USER_KEY = "smart_honeypot_user";
// const LAST_ACTIVITY_KEY = "smart_honeypot_last_activity";

// export function setAuthData({ accessToken, user }) {
//   if (accessToken) {
//     localStorage.setItem(ACCESS_TOKEN_KEY, accessToken);
//   }

//   if (user) {
//     localStorage.setItem(USER_KEY, JSON.stringify(user));
//   }

//   localStorage.setItem(
//     LAST_ACTIVITY_KEY,
//     String(Date.now())
//   );
// }

// export function getAccessToken() {
//   return localStorage.getItem(ACCESS_TOKEN_KEY);
// }

// export function getCurrentUser() {
//   const storedUser = localStorage.getItem(USER_KEY);

//   if (!storedUser) {
//     return null;
//   }

//   try {
//     return JSON.parse(storedUser);
//   } catch {
//     return null;
//   }
// }

// export function getLastActivity() {
//   const value = localStorage.getItem(LAST_ACTIVITY_KEY);

//   if (!value) {
//     return null;
//   }

//   const timestamp = Number(value);

//   if (Number.isNaN(timestamp)) {
//     return null;
//   }

//   return timestamp;
// }

// export function updateLastActivity() {
//   localStorage.setItem(
//     LAST_ACTIVITY_KEY,
//     String(Date.now())
//   );
// }

// export function clearAuthData() {
//   localStorage.removeItem(ACCESS_TOKEN_KEY);
//   localStorage.removeItem(USER_KEY);
//   localStorage.removeItem(LAST_ACTIVITY_KEY);
// }

const ACCESS_TOKEN_KEY =
  "smart_honeypot_access_token";

const USER_KEY =
  "smart_honeypot_user";

const LAST_ACTIVITY_KEY =
  "smart_honeypot_last_activity";

/**
 * Store the authentication data returned by the backend.
 *
 * NOTE:
 * The current project uses localStorage temporarily for the
 * frontend/backend integration stage.
 *
 * In the final production implementation, authentication
 * should preferably use a secure HttpOnly backend-managed
 * session.
 */
export function setAuthData({
  accessToken,
  user,
}) {
  if (accessToken) {
    localStorage.setItem(
      ACCESS_TOKEN_KEY,
      accessToken
    );
  }

  if (user) {
    localStorage.setItem(
      USER_KEY,
      JSON.stringify(user)
    );
  }

  updateLastActivity();
}

/**
 * Return the backend access token.
 */
export function getAccessToken() {
  return localStorage.getItem(
    ACCESS_TOKEN_KEY
  );
}

/**
 * Return the currently stored user.
 */
export function getCurrentUser() {
  const storedUser =
    localStorage.getItem(USER_KEY);

  if (!storedUser) {
    return null;
  }

  try {
    return JSON.parse(storedUser);
  } catch {
    return null;
  }
}

/**
 * Return the timestamp of the latest user activity.
 */
export function getLastActivity() {
  const value =
    localStorage.getItem(
      LAST_ACTIVITY_KEY
    );

  if (!value) {
    return null;
  }

  const timestamp = Number(value);

  if (Number.isNaN(timestamp)) {
    return null;
  }

  return timestamp;
}

/**
 * Update the latest activity timestamp.
 */
export function updateLastActivity() {
  localStorage.setItem(
    LAST_ACTIVITY_KEY,
    String(Date.now())
  );
}

/**
 * Clear all frontend authentication data.
 */
export function clearAuthData() {
  localStorage.removeItem(
    ACCESS_TOKEN_KEY
  );

  localStorage.removeItem(
    USER_KEY
  );

  localStorage.removeItem(
    LAST_ACTIVITY_KEY
  );
}
