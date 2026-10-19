import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import {
  createUser,
  deleteUser,
  getUsers,
  toggleUserStatus,
  updateUser,
} from "../services/usersService";
import "../styles/users.css";

const ROLES = [
  {
    value: "sub-admin",
    label: "Sub Admin",
  },
  {
    value: "analyst",
    label: "Analyst",
  },
  {
    value: "reader",
    label: "Reader",
  },
];

function Users() {
  const { user } = useAuth();

  const [users, setUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingUser, setEditingUser] = useState(null);

  const [form, setForm] = useState({
    name: "",
    email: "",
    role: "reader",
  });
const [error, setError] =
  useState("");

const [success, setSuccess] =
  useState("");

const [activationLink, setActivationLink] =
  useState("");

  async function loadUsers() {
    try {
      setIsLoading(true);
      const data = await getUsers();
      setUsers(data);
    } catch {
      setError("Unable to load users.");
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    const timer = setTimeout(() => { void loadUsers(); }, 0);
    return () => clearTimeout(timer);
  }, []);

  function openCreateForm() {
    setEditingUser(null);

    setForm({
      name: "",
      email: "",
      role: "reader",
    });

    setError("");
    setIsFormOpen(true);
  }

  function openEditForm(selectedUser) {
    setEditingUser(selectedUser);

    setForm({
      name: selectedUser.name,
      email: selectedUser.email,
      role: selectedUser.role,
    });

    setError("");
    setIsFormOpen(true);
  }

  function closeForm() {
    setIsFormOpen(false);
    setEditingUser(null);
  }

  function handleChange(event) {
    const {
      name,
      value,
    } = event.target;

    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  }

 async function handleSubmit(event) {
  event.preventDefault();

  setError("");
  setSuccess("");
  setActivationLink("");

  if (!form.name.trim()) {
    setError("Name is required.");
    return;
  }

  if (!form.email.trim()) {
    setError("Email is required.");
    return;
  }

  try {
    if (editingUser) {
      await updateUser(
        editingUser.id,
        form
      );

      setSuccess(
        "User updated successfully."
      );
    } else {
      const result = await createUser(form);

      if (result?.activationToken) {
        const frontendUrl = import.meta.env.VITE_FRONTEND_URL || window.location.origin;
        setActivationLink(`${frontendUrl.replace(/\/$/, "")}/activate?token=${encodeURIComponent(result.activationToken)}`);
        setSuccess("User created successfully. Activation link generated.");
      } else {
        setSuccess("User created successfully, but no activation token was returned.");
      }
    }

    await loadUsers();

        if (editingUser) {
      closeForm();
    }

  } catch (err) {
    setError(err?.message || "Unable to create user.");
}
}
  async function handleToggleStatus(selectedUser) {
    setError("");

    try {
      await toggleUserStatus(
        selectedUser.id
      );

      await loadUsers();
    } catch {
      setError(
        "Unable to update user status."
      );
    }
  }

  async function handleDelete(selectedUser) {
    const confirmed =
      window.confirm(
        `Delete ${selectedUser.name}?`
      );

    if (!confirmed) {
      return;
    }

    setError("");

    try {
      await deleteUser(
        selectedUser.id
      );

      await loadUsers();
    } catch (err) {
      if (
        err.message ===
        "ADMIN_CANNOT_BE_DELETED"
      ) {
        setError(
          "The primary admin account cannot be deleted."
        );
        return;
      }

      setError(
        "Unable to delete user."
      );
    }
  }

  return (
    <div className="users-page">
      <div className="users-header">
        <div>
          <span className="page-eyebrow">
            Administration
          </span>

          <h1 className="page-title">
            User Management
          </h1>

          <p className="page-description">
            Manage organization users,
            roles, and account status.
          </p>
        </div>

        <button
          className="users-create-button"
          type="button"
          onClick={openCreateForm}
        >
          Create User
        </button>
      </div>

      {error && (
  <div className="users-error">
    {error}
  </div>
)}

{success && (
  <div className="users-success">
    {success}

    {activationLink && (
      <div className="activation-url">
        <strong>
          Activation Link:
        </strong>

        <code>
          {activationLink}
        </code>
      </div>
    )}
  </div>
)}

      <div className="users-card">
        {isLoading ? (
          <div className="users-loading">
            Loading users...
          </div>
        ) : (
          <div className="users-table-wrapper">
            <table className="users-table">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>

              <tbody>
                {users.map((item) => {
                  const isCurrentUser =
                    item.id === user?.id;

                  return (
                    <tr key={item.id}>
                      <td>
                        <div className="users-user">
                          <div className="users-avatar">
                            {item.name
                              .charAt(0)
                              .toUpperCase()}
                          </div>

                          <div>
                            <strong>
                              {item.name}
                            </strong>

                            {isCurrentUser && (
                              <span>
                                Current user
                              </span>
                            )}
                          </div>
                        </div>
                      </td>

                      <td>
                        {item.email}
                      </td>

                      <td>
                        <span
                          className={`users-role users-role-${item.role}`}
                        >
                          {item.role}
                        </span>
                      </td>

                      <td>
                        <span
                          className={`users-status users-status-${item.status}`}
                        >
                          {item.status}
                        </span>
                      </td>

                      <td>
                        <div className="users-actions">
                          {item.role !== "admin" && (
                            <>
                              <button
                                type="button"
                                onClick={() =>
                                  openEditForm(item)
                                }
                              >
                                Edit
                              </button>

                              <button
                                type="button"
                                onClick={() =>
                                  handleToggleStatus(
                                    item
                                  )
                                }
                              >
                                {item.status ===
                                "active"
                                  ? "Disable"
                                  : "Enable"}
                              </button>

                              <button
                                type="button"
                                className="danger"
                                onClick={() =>
                                  handleDelete(
                                    item
                                  )
                                }
                              >
                                Delete
                              </button>
                            </>
                          )}
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {isFormOpen && (
        <div className="users-modal-overlay">
          <div className="users-modal">
            <div className="users-modal-header">
              <div>
                <span>
                  Administration
                </span>

                <h2>
                  {editingUser
                    ? "Edit User"
                    : "Create User"}
                </h2>
              </div>

              <button
                type="button"
                onClick={closeForm}
                aria-label="Close"
              >
                ×
              </button>
            </div>

            <form
              className="users-form"
              onSubmit={handleSubmit}
            >
              <label>
                Name

                <input
                  name="name"
                  value={form.name}
                  onChange={handleChange}
                  placeholder="User name"
                />
              </label>

              <label>
                Email

                <input
                  name="email"
                  type="email"
                  value={form.email}
                  onChange={handleChange}
                  placeholder="user@company.com"
                />
              </label>

              <label>
                Role

                <select
                  name="role"
                  value={form.role}
                  onChange={handleChange}
                >
                  {ROLES.map((role) => (
                    <option
                      key={role.value}
                      value={role.value}
                    >
                      {role.label}
                    </option>
                  ))}
                </select>
              </label>

              <div className="users-form-actions">
                <button
                  type="button"
                  onClick={closeForm}
                >
                  Cancel
                </button>

                <button
                  type="submit"
                >
                  {editingUser
                    ? "Save Changes"
                    : "Create User"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}

export default Users;
