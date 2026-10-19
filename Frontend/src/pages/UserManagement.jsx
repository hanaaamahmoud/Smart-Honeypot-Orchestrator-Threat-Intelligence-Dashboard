import { useEffect, useState } from "react";
import {
  createUser,
  deleteUser,
  disableUser,
  getUsers,
  updateUser,
} from "../services/userService";
import "../styles/user-management.css";

const ROLES = [
  "sub-admin",
  "analyst",
  "reader",
];

const initialForm = {
  name: "",
  email: "",
  role: "analyst",
};

function UserManagement() {
  const [users, setUsers] = useState([]);
  const [isLoading, setIsLoading] = useState(true);

  const [showForm, setShowForm] = useState(false);
  const [editingUser, setEditingUser] =
    useState(null);

  const [form, setForm] =
    useState(initialForm);

  const [error, setError] = useState("");
  const [actionLoading, setActionLoading] =
    useState(false);

  async function loadUsers() {
    try {
      setIsLoading(true);
      setError("");

      const data = await getUsers();

      setUsers(data);
    } catch {
      setError(
        "Unable to load users."
      );
    } finally {
      setIsLoading(false);
    }
  }

  useEffect(() => {
    loadUsers();
  }, []);

  function openCreateForm() {
    setEditingUser(null);
    setForm(initialForm);
    setError("");
    setShowForm(true);
  }

  function openEditForm(user) {
    setEditingUser(user);

    setForm({
      name: user.name,
      email: user.email,
      role:
        user.role === "admin"
          ? "analyst"
          : user.role,
    });

    setError("");
    setShowForm(true);
  }

  function closeForm() {
    if (actionLoading) {
      return;
    }

    setShowForm(false);
    setEditingUser(null);
    setForm(initialForm);
    setError("");
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
    setActionLoading(true);

    try {
      if (editingUser) {
        const updated =
          await updateUser(
            editingUser.id,
            form
          );

        setUsers((current) =>
          current.map((user) =>
            user.id === updated.id
              ? updated
              : user
          )
        );
      } else {
        const created =
          await createUser(form);

        setUsers((current) => [
          ...current,
          created,
        ]);
      }

      closeForm();
    } catch (err) {
      setError(
        getUserErrorMessage(
          err.message
        )
      );
    } finally {
      setActionLoading(false);
    }
  }

  async function handleDisable(user) {
    const action =
      user.status === "active"
        ? "disable"
        : "enable";

    const confirmed = window.confirm(
      `Are you sure you want to ${action} ${user.name}?`
    );

    if (!confirmed) {
      return;
    }

    try {
      setError("");
      setActionLoading(true);

      const updated =
        await disableUser(user.id);

      setUsers((current) =>
        current.map((item) =>
          item.id === updated.id
            ? updated
            : item
        )
      );
    } catch (err) {
      setError(
        getUserErrorMessage(
          err.message
        )
      );
    } finally {
      setActionLoading(false);
    }
  }

  async function handleDelete(user) {
    const confirmed = window.confirm(
      `Delete ${user.name}? This action cannot be undone.`
    );

    if (!confirmed) {
      return;
    }

    try {
      setError("");
      setActionLoading(true);

      await deleteUser(user.id);

      setUsers((current) =>
        current.filter(
          (item) =>
            item.id !== user.id
        )
      );
    } catch (err) {
      setError(
        getUserErrorMessage(
          err.message
        )
      );
    } finally {
      setActionLoading(false);
    }
  }

  return (
    <div className="user-management-page">
      <div className="user-management-header">
        <div>
          <span className="page-eyebrow">
            Administration
          </span>

          <h1 className="page-title">
            User Management
          </h1>

          <p className="page-description">
            Manage users and access roles
            for your organization.
          </p>
        </div>

        <button
          type="button"
          className="user-create-button"
          onClick={openCreateForm}
          disabled={actionLoading}
        >
          Create User
        </button>
      </div>

      {error && (
        <div className="user-management-error">
          {error}
        </div>
      )}

      <div className="user-management-card">
        {isLoading ? (
          <div className="user-management-loading">
            Loading users...
          </div>
        ) : users.length === 0 ? (
          <div className="user-management-empty">
            No users found.
          </div>
        ) : (
          <div className="user-table-wrapper">
            <table className="user-table">
              <thead>
                <tr>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>

              <tbody>
                {users.map((user) => (
                  <tr key={user.id}>
                    <td>
                      <strong>
                        {user.name}
                      </strong>
                    </td>

                    <td>
                      {user.email}
                    </td>

                    <td>
                      <span
                        className={`user-role user-role-${user.role}`}
                      >
                        {user.role}
                      </span>
                    </td>

                    <td>
                      <span
                        className={`user-status user-status-${user.status}`}
                      >
                        {user.status}
                      </span>
                    </td>

                    <td>
                      <div className="user-actions">
                        {user.role !==
                          "admin" && (
                          <>
                            <button
                              type="button"
                              onClick={() =>
                                openEditForm(
                                  user
                                )
                              }
                              disabled={
                                actionLoading
                              }
                            >
                              Edit
                            </button>

                            <button
                              type="button"
                              onClick={() =>
                                handleDisable(
                                  user
                                )
                              }
                              disabled={
                                actionLoading
                              }
                            >
                              {user.status ===
                              "active"
                                ? "Disable"
                                : "Enable"}
                            </button>

                            <button
                              type="button"
                              className="user-delete-button"
                              onClick={() =>
                                handleDelete(
                                  user
                                )
                              }
                              disabled={
                                actionLoading
                              }
                            >
                              Delete
                            </button>
                          </>
                        )}

                        {user.role ===
                          "admin" && (
                          <span className="user-protected-label">
                            Protected
                          </span>
                        )}
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {showForm && (
        <div className="user-modal-backdrop">
          <div className="user-modal">
            <div className="user-modal-header">
              <div>
                <span className="page-eyebrow">
                  {editingUser
                    ? "Edit User"
                    : "New User"}
                </span>

                <h2>
                  {editingUser
                    ? "Update User"
                    : "Create User"}
                </h2>
              </div>

              <button
                type="button"
                className="user-modal-close"
                onClick={closeForm}
                disabled={
                  actionLoading
                }
              >
                ×
              </button>
            </div>

            <form
              className="user-form"
              onSubmit={handleSubmit}
            >
              <div className="user-form-field">
                <label htmlFor="user-name">
                  Name
                </label>

                <input
                  id="user-name"
                  name="name"
                  value={form.name}
                  onChange={
                    handleChange
                  }
                  placeholder="Full name"
                  disabled={
                    actionLoading
                  }
                  required
                />
              </div>

              <div className="user-form-field">
                <label htmlFor="user-email">
                  Email
                </label>

                <input
                  id="user-email"
                  name="email"
                  type="email"
                  value={form.email}
                  onChange={
                    handleChange
                  }
                  placeholder="user@company.com"
                  disabled={
                    actionLoading
                  }
                  required
                />
              </div>

              <div className="user-form-field">
                <label htmlFor="user-role">
                  Role
                </label>

                <select
                  id="user-role"
                  name="role"
                  value={form.role}
                  onChange={
                    handleChange
                  }
                  disabled={
                    actionLoading
                  }
                >
                  {ROLES.map(
                    (role) => (
                      <option
                        key={role}
                        value={role}
                      >
                        {role}
                      </option>
                    )
                  )}
                </select>
              </div>

              <div className="user-form-actions">
                <button
                  type="button"
                  className="user-form-cancel"
                  onClick={closeForm}
                  disabled={
                    actionLoading
                  }
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="user-form-submit"
                  disabled={
                    actionLoading
                  }
                >
                  {actionLoading
                    ? "Saving..."
                    : editingUser
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

function getUserErrorMessage(
  errorCode
) {
  switch (errorCode) {
    case "EMAIL_ALREADY_EXISTS":
      return "This email is already registered.";

    case "USER_NOT_FOUND":
      return "User was not found.";

    case "CANNOT_DISABLE_ADMIN":
      return "The main administrator cannot be disabled.";

    case "CANNOT_DELETE_ADMIN":
      return "The main administrator cannot be deleted.";

    default:
      return "Something went wrong. Please try again.";
  }
}

export default UserManagement;
