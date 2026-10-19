import {
  getManagedUsers,
  createUser as createAuthUser,
  updateUser as updateAuthUser,
  deleteUser as deleteAuthUser,
} from "./authService";


export async function getUsers() {
  return getManagedUsers();
}


export async function createUser(userData) {
  return createAuthUser(userData);
}


export async function updateUser(
  userId,
  userData
) {
  return updateAuthUser(
    userId,
    userData
  );
}


export async function toggleUserStatus(userId) {

  const users =
    await getManagedUsers();

  const selectedUser =
    users.find(
      (user) =>
        user.id === userId
    );

  if (!selectedUser) {
    throw new Error(
      "USER_NOT_FOUND"
    );
  }


  return updateAuthUser(
    userId,
    {
      status:
        selectedUser.status === "active"
          ? "disabled"
          : "active",
    }
  );
}


export async function deleteUser(userId) {
  return deleteAuthUser(userId);
}