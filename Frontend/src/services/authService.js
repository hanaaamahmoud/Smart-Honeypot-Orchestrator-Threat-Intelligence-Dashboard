const MOCK_USERS_KEY =
  "smart_honeypot_mock_users";

const AUTH_STORAGE_KEY =
  "smart_honeypot_mock_session";

const ACTIVATION_TOKEN_LIFETIME =
  30 * 60 * 1000;

const RESET_TOKEN_LIFETIME =
  30 * 60 * 1000;

const ACTIVATION_RATE_LIMIT =
  60 * 1000;

const RESET_RATE_LIMIT =
  60 * 1000;

const INITIAL_USERS = [
  {
    id: "admin-001",
    email: "admin@smarthoneypot.local",
    password: "Admin@123456",
    name: "System Administrator",
    role: "admin",
    organizationId: "org-demo",
    organizationName: "Demo Organization",
    status: "active",
  },
  {
    id: "subadmin-001",
    email: "subadmin@smarthoneypot.local",
    password: "SubAdmin@123456",
    name: "Security Manager",
    role: "sub-admin",
    organizationId: "org-demo",
    organizationName: "Demo Organization",
    status: "active",
  },
  {
    id: "analyst-001",
    email: "analyst@smarthoneypot.local",
    password: "Analyst@123456",
    name: "SOC Analyst",
    role: "analyst",
    organizationId: "org-demo",
    organizationName: "Demo Organization",
    status: "active",
  },
  {
    id: "reader-001",
    email: "reader@smarthoneypot.local",
    password: "Reader@123456",
    name: "Security Reader",
    role: "reader",
    organizationId: "org-demo",
    organizationName: "Demo Organization",
    status: "active",
  },
];

function delay(time) {
  return new Promise((resolve) =>
    setTimeout(resolve, time)
  );
}

function cleanupExpiredPendingUsers(
  users
) {
  const now = Date.now();

  const activeUsers =
    users.filter((user) => {
      if (
        user.status === "pending" &&
        user.activationExpiresAt &&
        now >
          user.activationExpiresAt
      ) {
        return false;
      }

      return true;
    });

  if (
    activeUsers.length !==
    users.length
  ) {
    saveUsers(activeUsers);
  }

  return activeUsers;
}

function getUsers() {
  try {
    const rawUsers =
      localStorage.getItem(
        MOCK_USERS_KEY
      );

    if (!rawUsers) {
      localStorage.setItem(
        MOCK_USERS_KEY,
        JSON.stringify(INITIAL_USERS)
      );

      return [...INITIAL_USERS];
    }

    const users =
      JSON.parse(rawUsers);

    if (!Array.isArray(users)) {
      throw new Error();
    }

    return cleanupExpiredPendingUsers(
      users
    );
  } catch {
    localStorage.setItem(
      MOCK_USERS_KEY,
      JSON.stringify(INITIAL_USERS)
    );

    return [...INITIAL_USERS];
  }
}

function saveUsers(users) {
  localStorage.setItem(
    MOCK_USERS_KEY,
    JSON.stringify(users)
  );
}

function sanitizeUser(user) {
  if (!user) {
    return null;
  }

  const safeUser = { ...user };
  delete safeUser.password;
  delete safeUser.activationToken;
  delete safeUser.activationExpiresAt;
  delete safeUser.resetToken;
  delete safeUser.resetExpiresAt;

  return safeUser;
}

function getStoredSession() {
  try {
    const session =
      localStorage.getItem(
        AUTH_STORAGE_KEY
      );

    return session
      ? JSON.parse(session)
      : null;
  } catch {
    localStorage.removeItem(
      AUTH_STORAGE_KEY
    );

    return null;
  }
}

function saveSession(user) {
  const session = {
    user: sanitizeUser(user),
    createdAt: Date.now(),
  };

  localStorage.setItem(
    AUTH_STORAGE_KEY,
    JSON.stringify(session)
  );

  return session.user;
}

function generateId(prefix) {
  return `${prefix}-${Date.now()}-${Math.random()
    .toString(36)
    .slice(2, 8)}`;
}

function generateToken() {
  return crypto.randomUUID();
}

function createActivationData() {
  return {
    token: generateToken(),
    expiresAt:
      Date.now() +
      ACTIVATION_TOKEN_LIFETIME,
  };
}

function createResetData() {
  return {
    token: generateToken(),
    expiresAt:
      Date.now() +
      RESET_TOKEN_LIFETIME,
  };
}

function canManageTarget(
  creator,
  targetUser
) {
  if (!creator || !targetUser) {
    return false;
  }

  if (
    creator.organizationId !==
    targetUser.organizationId
  ) {
    return false;
  }

  if (creator.role === "admin") {
    return targetUser.role !== "admin";
  }

  if (
    creator.role === "sub-admin"
  ) {
    return (
      targetUser.role === "analyst" ||
      targetUser.role === "reader"
    );
  }

  return false;
}

export async function login(
  email,
  password
) {
  await delay(500);

  const normalizedEmail =
    email.trim().toLowerCase();

  const users = getUsers();

  const user = users.find(
    (item) =>
      item.email.toLowerCase() ===
      normalizedEmail
  );

  if (!user) {
    throw new Error(
      "INVALID_CREDENTIALS"
    );
  }

  if (
    user.status === "pending"
  ) {
    throw new Error(
      "ACCOUNT_NOT_ACTIVATED"
    );
  }

  if (
    user.status !== "active"
  ) {
    throw new Error(
      "ACCOUNT_DISABLED"
    );
  }

  if (
    user.password !== password
  ) {
    throw new Error(
      "INVALID_CREDENTIALS"
    );
  }

  return saveSession(user);
}

export async function logout() {
  await delay(150);

  localStorage.removeItem(
    AUTH_STORAGE_KEY
  );
}

export async function getCurrentUser() {
  await delay(200);

  const session =
    getStoredSession();

  if (!session?.user) {
    return null;
  }

  const users = getUsers();

  const user = users.find(
    (item) =>
      item.id ===
      session.user.id
  );

  if (
    !user ||
    user.status !== "active"
  ) {
    localStorage.removeItem(
      AUTH_STORAGE_KEY
    );

    return null;
  }

  return sanitizeUser(user);
}

export async function refreshSession() {
  return getCurrentUser();
}

export async function getManagedUsers() {
  await delay(250);

  const session =
    getStoredSession();

  if (!session?.user) {
    throw new Error(
      "UNAUTHENTICATED"
    );
  }

  if (
    session.user.role !== "admin" &&
    session.user.role !== "sub-admin"
  ) {
    throw new Error(
      "FORBIDDEN"
    );
  }

  return getUsers()
    .filter(
      (user) =>
        user.organizationId ===
        session.user.organizationId
    )
    .map(sanitizeUser);
}

export async function createUser({
  name,
  email,
  role,
}) {
  await delay(400);

  const session =
    getStoredSession();

  if (!session?.user) {
    throw new Error(
      "UNAUTHENTICATED"
    );
  }

  const creator =
    session.user;

  if (
    creator.role !== "admin" &&
    creator.role !== "sub-admin"
  ) {
    throw new Error(
      "FORBIDDEN"
    );
  }

  if (
    creator.role ===
      "sub-admin" &&
    role === "sub-admin"
  ) {
    throw new Error(
      "FORBIDDEN"
    );
  }

  const normalizedEmail =
    email.trim().toLowerCase();

  const users = getUsers();

  if (
    users.some(
      (user) =>
        user.email.toLowerCase() ===
        normalizedEmail
    )
  ) {
    throw new Error(
      "EMAIL_ALREADY_EXISTS"
    );
  }

  const activation =
    createActivationData();

  const newUser = {
    id: generateId("user"),
    email: normalizedEmail,
    password: null,
    name: name.trim(),
    role,
    organizationId:
      creator.organizationId,
    organizationName:
      creator.organizationName,
    status: "pending",
    activationToken:
      activation.token,
    activationExpiresAt:
      activation.expiresAt,
    activationCreatedAt:
      Date.now(),
    createdBy: creator.id,
    createdAt: Date.now(),
  };

  users.push(newUser);

  saveUsers(users);

  return {
    user: sanitizeUser(newUser),
    activationToken:
      activation.token,
    activationExpiresAt:
      activation.expiresAt,
  };
}

export function getMockActivationUrl(
  token
) {
  const frontendUrl = import.meta.env.VITE_FRONTEND_URL || window.location.origin;
  return `${frontendUrl.replace(/\/$/, "")}/activate?token=${encodeURIComponent(token)}`;
}

export async function resendActivation(
  userId
) {
  await delay(400);

  const session =
    getStoredSession();

  if (!session?.user) {
    throw new Error(
      "UNAUTHENTICATED"
    );
  }

  const users = getUsers();

  const index =
    users.findIndex(
      (user) =>
        user.id === userId
    );

  if (index === -1) {
    throw new Error(
      "USER_NOT_FOUND"
    );
  }

  const user =
    users[index];

  if (
    !canManageTarget(
      session.user,
      user
    )
  ) {
    throw new Error(
      "FORBIDDEN"
    );
  }

  if (
    user.status !== "pending"
  ) {
    throw new Error(
      "ACCOUNT_ALREADY_ACTIVATED"
    );
  }

  if (
    user.activationCreatedAt &&
    Date.now() -
      user.activationCreatedAt <
      ACTIVATION_RATE_LIMIT
  ) {
    throw new Error(
      "ACTIVATION_RATE_LIMIT"
    );
  }

  const activation =
    createActivationData();

  users[index] = {
    ...user,
    activationToken:
      activation.token,
    activationExpiresAt:
      activation.expiresAt,
    activationCreatedAt:
      Date.now(),
  };

  saveUsers(users);

  return {
    user: sanitizeUser(
      users[index]
    ),
    activationToken:
      activation.token,
    activationExpiresAt:
      activation.expiresAt,
  };
}

export async function activateAccount(
  token,
  password
) {
  await delay(400);

  const users = getUsers();

  const index =
    users.findIndex(
      (user) =>
        user.activationToken ===
        token
    );

  if (index === -1) {
    throw new Error(
      "INVALID_ACTIVATION_TOKEN"
    );
  }

  const user =
    users[index];

  if (
    user.status === "active"
  ) {
    throw new Error(
      "ACCOUNT_ALREADY_ACTIVATED"
    );
  }

  if (
    !user.activationExpiresAt ||
    Date.now() >
      user.activationExpiresAt
  ) {
    throw new Error(
      "EXPIRED_ACTIVATION_TOKEN"
    );
  }

  if (
    !password ||
    password.length < 8
  ) {
    throw new Error(
      "INVALID_PASSWORD"
    );
  }

  users[index] = {
    ...user,
    password,
    status: "active",
    activationToken: null,
    activationExpiresAt: null,
    activatedAt: Date.now(),
  };

  saveUsers(users);

  return sanitizeUser(
    users[index]
  );
}

export async function requestPasswordReset(
  email
) {
  await delay(400);

  const normalizedEmail =
    email.trim().toLowerCase();

  const users = getUsers();

  const user =
    users.find(
      (item) =>
        item.email.toLowerCase() ===
        normalizedEmail
    );

  if (!user) {
    return {
      message:
        "If the account exists, a reset link has been generated.",
    };
  }

  if (
    user.resetCreatedAt &&
    Date.now() -
      user.resetCreatedAt <
      RESET_RATE_LIMIT
  ) {
    throw new Error(
      "RESET_RATE_LIMIT"
    );
  }

  const resetData =
    createResetData();

  user.resetToken =
    resetData.token;

  user.resetExpiresAt =
    resetData.expiresAt;

  user.resetCreatedAt =
    Date.now();

  saveUsers(users);

  return {
    message:
      "If the account exists, a reset link has been sent.",

    ...(import.meta.env.DEV && {
      resetToken:
        resetData.token,
    }),
  };
}

export async function resetPassword(
  token,
  password
) {
  await delay(400);

  const users = getUsers();

  const index =
    users.findIndex(
      (user) =>
        user.resetToken === token
    );

  if (index === -1) {
    throw new Error(
      "INVALID_RESET_TOKEN"
    );
  }

  if (
    Date.now() >
    users[index].resetExpiresAt
  ) {
    throw new Error(
      "EXPIRED_RESET_TOKEN"
    );
  }

  if (
    !password ||
    password.length < 8
  ) {
    throw new Error(
      "INVALID_PASSWORD"
    );
  }

  users[index] = {
    ...users[index],
    password,
    resetToken: null,
    resetExpiresAt: null,
  };

  saveUsers(users);

  localStorage.removeItem(
    AUTH_STORAGE_KEY
  );

  return sanitizeUser(
    users[index]
  );
}

export async function deleteUser(
  userId
) {
  await delay(300);

  const session =
    getStoredSession();

  if (!session?.user) {
    throw new Error(
      "UNAUTHENTICATED"
    );
  }

  const users = getUsers();

  const user =
    users.find(
      (item) =>
        item.id === userId
    );

  if (!user) {
    throw new Error(
      "USER_NOT_FOUND"
    );
  }

  if (
    user.role === "admin"
  ) {
    throw new Error(
      "CANNOT_DELETE_ADMIN"
    );
  }

  if (
    !canManageTarget(
      session.user,
      user
    )
  ) {
    throw new Error(
      "FORBIDDEN"
    );
  }

  const filtered =
    users.filter(
      (item) =>
        item.id !== userId
    );

  saveUsers(filtered);

  return true;
}

export async function updateUser(
  userId,
  updates
) {
  await delay(300);

  const session =
    getStoredSession();

  if (!session?.user) {
    throw new Error(
      "UNAUTHENTICATED"
    );
  }

  const users = getUsers();

  const index =
    users.findIndex(
      (user) =>
        user.id === userId
    );

  if (index === -1) {
    throw new Error(
      "USER_NOT_FOUND"
    );
  }

  const targetUser =
    users[index];

  if (
    !canManageTarget(
      session.user,
      targetUser
    )
  ) {
    throw new Error(
      "FORBIDDEN"
    );
  }

  if (
    updates.status &&
    updates.status !==
      targetUser.status
  ) {
    throw new Error(
      "USE_STATUS_ENDPOINT"
    );
  }

  if (
    updates.role === "admin"
  ) {
    throw new Error(
      "FORBIDDEN"
    );
  }

  if (
    session.user.role ===
      "sub-admin" &&
    updates.role ===
      "sub-admin"
  ) {
    throw new Error(
      "FORBIDDEN"
    );
  }

  const normalizedEmail =
    updates.email
      ?.trim()
      .toLowerCase();

  if (
    normalizedEmail &&
    users.some(
      (user, userIndex) =>
        userIndex !== index &&
        user.email.toLowerCase() ===
          normalizedEmail
    )
  ) {
    throw new Error(
      "EMAIL_ALREADY_EXISTS"
    );
  }

  users[index] = {
    ...targetUser,
    ...updates,
    ...(normalizedEmail
      ? {
          email:
            normalizedEmail,
        }
      : {}),
  };

  saveUsers(users);

  return sanitizeUser(
    users[index]
  );
}

export async function disableUser(
  userId
) {
  await delay(300);

  const session =
    getStoredSession();

  if (!session?.user) {
    throw new Error(
      "UNAUTHENTICATED"
    );
  }

  const users = getUsers();

  const index =
    users.findIndex(
      (user) =>
        user.id === userId
    );

  if (index === -1) {
    throw new Error(
      "USER_NOT_FOUND"
    );
  }

  const targetUser =
    users[index];

  if (
    !canManageTarget(
      session.user,
      targetUser
    )
  ) {
    throw new Error(
      "FORBIDDEN"
    );
  }

  if (
    targetUser.role === "admin"
  ) {
    throw new Error(
      "CANNOT_DISABLE_ADMIN"
    );
  }

  if (
    targetUser.status ===
    "pending"
  ) {
    throw new Error(
      "CANNOT_CHANGE_PENDING_STATUS"
    );
  }

  users[index] = {
    ...targetUser,
    status:
      targetUser.status ===
      "active"
        ? "disabled"
        : "active",
  };

  saveUsers(users);

  return sanitizeUser(
    users[index]
  );
}