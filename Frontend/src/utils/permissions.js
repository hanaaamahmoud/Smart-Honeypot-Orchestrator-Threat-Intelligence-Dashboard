export const ROLES = {
  ADMIN: "admin",
  SUB_ADMIN: "sub-admin",
  ANALYST: "analyst",
  READER: "reader",
};

export const ROLE_PERMISSIONS = {
  [ROLES.ADMIN]: [
    "dashboard.view",
    "live-attacks.view",
    "statistics.view",
    "attack-details.view",
    "users.view",
    "users.create",
    "users.edit",
    "users.disable",
    "users.delete",
  ],

  [ROLES.SUB_ADMIN]: [
    "dashboard.view",
    "live-attacks.view",
    "statistics.view",
    "attack-details.view",
    "users.view",
    "users.create",
    "users.edit",
    "users.disable",
  ],

  [ROLES.ANALYST]: [
    "dashboard.view",
    "live-attacks.view",
    "statistics.view",
    "attack-details.view",
  ],

  [ROLES.READER]: [
    "dashboard.view",
    "statistics.view",
    "attack-details.view",
  ],
};

export function hasPermission(
  role,
  permission
) {
  if (!role || !permission) {
    return false;
  }

  const permissions =
    ROLE_PERMISSIONS[role];

  if (!permissions) {
    return false;
  }

  return permissions.includes(permission);
}

export function hasAnyPermission(
  role,
  permissions
) {
  if (!Array.isArray(permissions)) {
    return false;
  }

  return permissions.some(
    (permission) =>
      hasPermission(role, permission)
  );
}
