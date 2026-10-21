const MOCK_USERS = [
  {
    id: "admin-001",
    name: "System Administrator",
    email: "admin@smarthoneypot.local",
    role: "admin",
    organizationId: "org-demo",
    organizationName: "Demo Organization",
    status: "active",
  },
  {
    id: "subadmin-001",
    name: "Security Manager",
    email: "subadmin@smarthoneypot.local",
    role: "sub-admin",
    organizationId: "org-demo",
    organizationName: "Demo Organization",
    status: "active",
  },
  {
    id: "analyst-001",
    name: "SOC Analyst",
    email: "analyst@smarthoneypot.local",
    role: "analyst",
    organizationId: "org-demo",
    organizationName: "Demo Organization",
    status: "active",
  },
  {
    id: "reader-001",
    name: "Security Reader",
    email: "reader@smarthoneypot.local",
    role: "reader",
    organizationId: "org-demo",
    organizationName: "Demo Organization",
    status: "active",
  },
];

let users = [...MOCK_USERS];

function delay(ms = 300) {
  return new Promise((resolve) => {
    setTimeout(resolve, ms);
  });
}

export async function getUsers() {
  await delay();

  return [...users];
}

export async function createUser(userData) {
  await delay();

  const existingUser = users.find(
    (user) =>
      user.email.toLowerCase() ===
      userData.email.trim().toLowerCase()
  );

  if (existingUser) {
    throw new Error("EMAIL_ALREADY_EXISTS");
  }

  const newUser = {
    id: `user-${Date.now()}`,
    name: userData.name.trim(),
    email: userData.email.trim().toLowerCase(),
    role: userData.role,
    organizationId: "org-demo",
    organizationName: "Demo Organization",
    status: "active",
  };

  users = [...users, newUser];

  return newUser;
}

export async function updateUser(id, userData) {
  await delay();

  const index = users.findIndex(
    (user) => user.id === id
  );

  if (index === -1) {
    throw new Error("USER_NOT_FOUND");
  }

  const updatedUser = {
    ...users[index],
    ...userData,
    email:
      userData.email?.trim().toLowerCase() ||
      users[index].email,
  };

  users = users.map((user) =>
    user.id === id ? updatedUser : user
  );

  return updatedUser;
}

export async function disableUser(id) {
  await delay();

  const user = users.find(
    (item) => item.id === id
  );

  if (!user) {
    throw new Error("USER_NOT_FOUND");
  }

  if (user.role === "admin") {
    throw new Error("CANNOT_DISABLE_ADMIN");
  }

  users = users.map((item) =>
    item.id === id
      ? {
          ...item,
          status:
            item.status === "active"
              ? "disabled"
              : "active",
        }
      : item
  );

  return users.find(
    (item) => item.id === id
  );
}

export async function deleteUser(id) {
  await delay();

  const user = users.find(
    (item) => item.id === id
  );

  if (!user) {
    throw new Error("USER_NOT_FOUND");
  }

  if (user.role === "admin") {
    throw new Error("CANNOT_DELETE_ADMIN");
  }

  users = users.filter(
    (item) => item.id !== id
  );

  return true;
}
