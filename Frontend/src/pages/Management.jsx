import { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import {
  createUser,
  getManagedUsers,
  getMockActivationUrl,
  updateUser,
  deleteUser,
} from "../services/authService";
import "../styles/management.css";

const EDIT_DRAFT_KEY =
  "smart_honeypot_management_edit_draft";

const EMPTY_FORM = {
  name: "",
  email: "",
  role: "analyst",
};

function Management() {
  const { user } = useAuth();

  const [users, setUsers] = useState([]);

  const [showCreateForm, setShowCreateForm] =
    useState(false);

  const [showEditForm, setShowEditForm] =
    useState(false);

  const [editingUser, setEditingUser] =
    useState(null);

  const [form, setForm] =
    useState(EMPTY_FORM);

  const [loading, setLoading] =
    useState(true);

  const [creating, setCreating] =
    useState(false);

  const [actionLoading, setActionLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const [message, setMessage] =
    useState("");

  const [activationUrl, setActivationUrl] =
    useState("");

  /*
   * Restore edit state when Management mounts again.
   *
   * This is what allows the edit modal to survive:
   *
   * Management
   *    ↓
   * Sidebar page
   *    ↓
   * Management
   *
   * without losing what was typed.
   */
  useEffect(() => {
    try {
      const rawDraft =
        sessionStorage.getItem(
          EDIT_DRAFT_KEY
        );

      if (!rawDraft) {
        return;
      }

      const draft =
        JSON.parse(rawDraft);

      if (
        draft?.showEditForm &&
        draft?.editingUser
      ) {
        setShowEditForm(true);

        setEditingUser(
          draft.editingUser
        );

        setForm({
          name:
            draft.form?.name ?? "",
          email:
            draft.form?.email ?? "",
          role:
            draft.form?.role ??
            draft.editingUser.role ??
            "analyst",
        });
      }
    } catch {
      sessionStorage.removeItem(
        EDIT_DRAFT_KEY
      );
    }
  }, []);

  /*
   * Save the edit modal state whenever
   * the user changes anything inside it.
   */
  useEffect(() => {
    if (
      !showEditForm ||
      !editingUser
    ) {
      return;
    }

    sessionStorage.setItem(
      EDIT_DRAFT_KEY,
      JSON.stringify({
        showEditForm: true,
        editingUser,
        form,
      })
    );
  }, [
    showEditForm,
    editingUser,
    form,
  ]);

  /*
   * Prevent the page behind the modal
   * from scrolling while the modal is open.
   */
  useEffect(() => {
    if (!showEditForm) {
      return;
    }

    const previousOverflow =
      document.body.style.overflow;

    document.body.style.overflow =
      "hidden";

    return () => {
      document.body.style.overflow =
        previousOverflow;
    };
  }, [showEditForm]);

  async function loadUsers() {
    try {
      setLoading(true);
      setError("");

      const managedUsers =
        await getManagedUsers();

      setUsers(
        managedUsers.filter(
          (item) =>
            item.id !== user?.id
        )
      );
    } catch {
      setError(
        "Unable to load users."
      );
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    if (user?.id) {
      loadUsers();
    }
  }, [user?.id]);

  const canManageUser = (
    targetUser
  ) => {
    if (user?.role === "admin") {
      return (
        targetUser.role !== "admin"
      );
    }

    if (
      user?.role === "sub-admin"
    ) {
      return (
        targetUser.role ===
          "analyst" ||
        targetUser.role ===
          "reader"
      );
    }

    return false;
  };

  const handleChange = (
    event
  ) => {
    const {
      name,
      value,
    } = event.target;

    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleCreateUser =
    async (event) => {
      event.preventDefault();

      setCreating(true);
      setError("");
      setMessage("");
      setActivationUrl("");

      try {
        const result =
          await createUser({
            name: form.name,
            email: form.email,
            role: form.role,
            organizationId:
              user.organizationId,
            organizationName:
              user.organizationName,
          });

        const url =
          getMockActivationUrl(
            result.activationToken
          );

        setMessage(
          "User created successfully."
        );

        setActivationUrl(url);

        setForm(EMPTY_FORM);

        setShowCreateForm(
          false
        );

        await loadUsers();
      } catch (err) {
        if (
          err.message ===
          "EMAIL_ALREADY_EXISTS"
        ) {
          setError(
            "This email is already registered."
          );
        } else {
          setError(
            "Unable to create user."
          );
        }
      } finally {
        setCreating(false);
      }
    };

  /*
   * Open edit modal.
   *
   * Important:
   * We DON'T use prompt().
   * We keep the whole form inside React state
   * and persist it in sessionStorage.
   */
  const handleEdit = (
    targetUser
  ) => {
    setEditingUser(
      targetUser
    );

    setForm({
      name:
        targetUser.name ?? "",
      email:
        targetUser.email ?? "",
      role:
        targetUser.role ??
        "analyst",
    });

    setError("");
    setMessage("");
    setActivationUrl("");

    setShowEditForm(true);
  };

  const handleEditChange = (
    event
  ) => {
    const {
      name,
      value,
    } = event.target;

    setForm((current) => ({
      ...current,
      [name]: value,
    }));
  };

  const handleSaveEdit =
    async (event) => {
      event.preventDefault();

      if (!editingUser) {
        return;
      }

      const trimmedName =
        form.name.trim();

      const normalizedEmail =
        form.email
          .trim()
          .toLowerCase();

      if (!trimmedName) {
        setError(
          "Name cannot be empty."
        );
        return;
      }

      if (!normalizedEmail) {
        setError(
          "Email cannot be empty."
        );
        return;
      }

      try {
        setActionLoading(true);
        setError("");
        setMessage("");

        await updateUser(
          editingUser.id,
          {
            name: trimmedName,
            email:
              normalizedEmail,
            role: form.role,
          }
        );

        /*
         * Only after successful save
         * do we close the modal and
         * remove its saved draft.
         */
        sessionStorage.removeItem(
          EDIT_DRAFT_KEY
        );

        setShowEditForm(false);
        setEditingUser(null);
        setForm(EMPTY_FORM);

        setMessage(
          "User updated successfully."
        );

        await loadUsers();
      } catch (err) {
        if (
          err.message ===
          "EMAIL_ALREADY_EXISTS"
        ) {
          setError(
            "This email is already registered."
          );
        } else {
          setError(
            "Unable to update user."
          );
        }
      } finally {
        setActionLoading(false);
      }
    };

  /*
   * IMPORTANT:
   *
   * Pending accounts are NOT treated
   * as active accounts.
   *
   * Active     → Disabled
   * Disabled   → Active
   * Pending    → Pending
   *
   * So Disable/Enable cannot accidentally
   * activate an account that was never activated.
   */
  const handleDisable = async (
    targetUser
  ) => {
    if (
      targetUser.status ===
      "pending"
    ) {
      setError(
        "Pending accounts must be activated before they can be disabled."
      );
      return;
    }

    const action =
      targetUser.status ===
      "active"
        ? "disable"
        : "enable";

    const confirmed =
      window.confirm(
        `Are you sure you want to ${action} ${targetUser.name}?`
      );

    if (!confirmed) {
      return;
    }

    try {
      setActionLoading(true);
      setError("");
      setMessage("");

      await updateUser(
        targetUser.id,
        {
          status:
            targetUser.status ===
            "active"
              ? "disabled"
              : "active",
        }
      );

      setMessage(
        `User ${action}d successfully.`
      );

      await loadUsers();
    } catch {
      setError(
        "Unable to update user status."
      );
    } finally {
      setActionLoading(false);
    }
  };

  const handleDelete = async (
    targetUser
  ) => {
    const confirmed =
      window.confirm(
        `Delete ${targetUser.name}? This action cannot be undone.`
      );

    if (!confirmed) {
      return;
    }

    try {
      setActionLoading(true);
      setError("");
      setMessage("");

      await deleteUser(
        targetUser.id
      );

      /*
       * If the deleted user happened
       * to be the user being edited,
       * remove the saved edit draft too.
       */
      if (
        editingUser?.id ===
        targetUser.id
      ) {
        sessionStorage.removeItem(
          EDIT_DRAFT_KEY
        );

        setShowEditForm(false);
        setEditingUser(null);
        setForm(EMPTY_FORM);
      }

      setMessage(
        "User deleted successfully."
      );

      await loadUsers();
    } catch (err) {
      if (
        err.message ===
        "CANNOT_DELETE_ADMIN"
      ) {
        setError(
          "Admin account cannot be deleted."
        );
      } else {
        setError(
          "Unable to delete user."
        );
      }
    } finally {
      setActionLoading(false);
    }
  };

  /*
   * Cancel / X:
   *
   * These are the ONLY normal ways
   * to intentionally close the edit modal.
   */
  const closeEditForm = () => {
    if (actionLoading) {
      return;
    }

    sessionStorage.removeItem(
      EDIT_DRAFT_KEY
    );

    setShowEditForm(false);
    setEditingUser(null);
    setForm(EMPTY_FORM);
    setError("");
  };

  return (
    <div className="management-page">

      <div className="management-header">

        <div>
          <span className="management-eyebrow">
            Administration
          </span>

          <h1 className="management-title">
            User Management
          </h1>

          <p className="management-description">
            Manage users, roles, access, and account status.
          </p>
        </div>

        <button
          type="button"
          className="management-create-button"
          onClick={() => {
            setShowCreateForm(
              (current) => !current
            );

            setError("");
            setMessage("");
            setActivationUrl("");
          }}
          disabled={
            creating ||
            actionLoading
          }
        >
          {showCreateForm
            ? "Cancel"
            : "Create User"}
        </button>

      </div>

      {message && (
        <div className="management-message">
          {message}

          {activationUrl && (
            <div className="management-activation">
              <span>
                Mock activation path:
              </span>

              <code>
                {activationUrl}
              </code>
            </div>
          )}
        </div>
      )}

      {error && (
        <div className="management-error">
          {error}
        </div>
      )}

      {showCreateForm && (
        <form
          className="management-create-card"
          onSubmit={
            handleCreateUser
          }
        >

          <div className="management-create-heading">
            <span>
              New account
            </span>

            <h2>
              Create User
            </h2>
          </div>

          <div className="management-form-grid">

            <div className="management-field">
              <label htmlFor="user-name">
                Full Name
              </label>

              <input
                id="user-name"
                name="name"
                value={form.name}
                onChange={
                  handleChange
                }
                placeholder="Enter full name"
                disabled={creating}
                required
              />
            </div>

            <div className="management-field">
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
                disabled={creating}
                required
              />
            </div>

            <div className="management-field">
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
                disabled={creating}
              >
                <option value="analyst">
                  Analyst
                </option>

                <option value="reader">
                  Reader
                </option>

                {user?.role ===
                  "admin" && (
                  <option value="sub-admin">
                    Sub-admin
                  </option>
                )}
              </select>
            </div>

          </div>

          <div className="management-invite-note">
            No password is created by the administrator.
            The user activates the account and creates
            their own password.
          </div>

          <button
            className="management-submit-button"
            type="submit"
            disabled={creating}
          >
            {creating
              ? "Creating..."
              : "Create User"}
          </button>

        </form>
      )}

      <div className="management-card">

        <div className="management-card-header">

          <div>
            <h2>
              Users
            </h2>

            <p>
              {users.length} managed accounts
            </p>
          </div>

        </div>

        {loading ? (
          <div className="management-loading">
            Loading users...
          </div>
        ) : (
          <div className="management-table-wrapper">

            <table className="management-table">

              <thead>
                <tr>
                  <th>User</th>
                  <th>Role</th>
                  <th>Status</th>
                  <th>Actions</th>
                </tr>
              </thead>

              <tbody>

                {users.map(
                  (item) => (
                    <tr
                      key={item.id}
                    >

                      <td>
                        <div className="management-user">

                          <div className="management-avatar">
                            {item.name
                              .charAt(
                                0
                              )
                              .toUpperCase()}
                          </div>

                          <div>
                            <strong>
                              {item.name}
                            </strong>

                            <span>
                              {item.email}
                            </span>
                          </div>

                        </div>
                      </td>

                      <td>
                        <span
                          className={`role-badge role-${item.role}`}
                        >
                          {item.role}
                        </span>
                      </td>

                      <td>
                        <span
                          className={`status-badge status-${item.status}`}
                        >
                          {item.status}
                        </span>
                      </td>

                      <td>

                        {canManageUser(
                          item
                        ) ? (

                          <div className="management-actions">

                            <button
                              type="button"
                              disabled={
                                actionLoading
                              }
                              onClick={() =>
                                handleEdit(
                                  item
                                )
                              }
                            >
                              Edit
                            </button>

                            <button
                              type="button"
                              disabled={
                                actionLoading ||
                                item.status ===
                                  "pending"
                              }
                              onClick={() =>
                                handleDisable(
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
                              className="danger-action"
                              disabled={
                                actionLoading
                              }
                              onClick={() =>
                                handleDelete(
                                  item
                                )
                              }
                            >
                              Delete
                            </button>

                          </div>

                        ) : (

                          <span className="no-actions">
                            No actions
                          </span>

                        )}

                      </td>

                    </tr>
                  )
                )}

              </tbody>

            </table>

          </div>
        )}

      </div>

      {/*
       * EDIT MODAL
       *
       * This is intentionally outside
       * management-card and uses fixed positioning.
       *
       * Therefore the sidebar has absolutely
       * no influence on its centering.
       */}
      {showEditForm && (
        <div className="management-modal-backdrop">

          <div
            className="management-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="management-edit-title"
          >

            <div className="management-modal-header">

              <div>
                <span>
                  Administration
                </span>

                <h2 id="management-edit-title">
                  Edit User
                </h2>
              </div>

              <button
                type="button"
                className="management-modal-close"
                onClick={
                  closeEditForm
                }
                disabled={
                  actionLoading
                }
                aria-label="Close edit dialog"
              >
                ×
              </button>

            </div>

            <div className="management-modal-user">

              <div className="management-modal-avatar">
                {editingUser?.name
                  ?.charAt(0)
                  .toUpperCase()}
              </div>

              <div>
                <strong>
                  {editingUser?.name}
                </strong>

                <span>
                  Editing account information
                </span>
              </div>

            </div>

            <form
              className="management-edit-form"
              onSubmit={
                handleSaveEdit
              }
            >

              <div className="management-field">
                <label htmlFor="edit-user-name">
                  Full Name
                </label>

                <input
                  id="edit-user-name"
                  name="name"
                  value={form.name}
                  onChange={
                    handleEditChange
                  }
                  disabled={
                    actionLoading
                  }
                  required
                />
              </div>

              <div className="management-field">
                <label htmlFor="edit-user-email">
                  Email
                </label>

                <input
                  id="edit-user-email"
                  name="email"
                  type="email"
                  value={form.email}
                  onChange={
                    handleEditChange
                  }
                  disabled={
                    actionLoading
                  }
                  required
                />
              </div>

              <div className="management-field">
                <label htmlFor="edit-user-role">
                  Role
                </label>

                <select
                  id="edit-user-role"
                  name="role"
                  value={form.role}
                  onChange={
                    handleEditChange
                  }
                  disabled={
                    actionLoading
                  }
                >

                  <option value="analyst">
                    Analyst
                  </option>

                  <option value="reader">
                    Reader
                  </option>

                  {user?.role ===
                    "admin" && (
                    <option value="sub-admin">
                      Sub-admin
                    </option>
                  )}

                </select>
              </div>

              <div className="management-edit-actions">

                <button
                  type="button"
                  className="management-modal-cancel"
                  onClick={
                    closeEditForm
                  }
                  disabled={
                    actionLoading
                  }
                >
                  Cancel
                </button>

                <button
                  type="submit"
                  className="management-modal-save"
                  disabled={
                    actionLoading
                  }
                >
                  {actionLoading
                    ? "Saving..."
                    : "Save Changes"}
                </button>

              </div>

            </form>

          </div>

        </div>
      )}

    </div>
  );
}

export default Management;
