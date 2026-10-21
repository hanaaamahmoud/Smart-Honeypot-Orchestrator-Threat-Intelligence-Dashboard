import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import "./Sidebar.css";

function Sidebar({ isOpen, onClose }) {
  const { user } = useAuth();

  const role = user?.role;

  const canViewLiveAttacks = [
    "admin",
    "sub-admin",
    "analyst",
  ].includes(role);

  const canViewManagement = [
    "admin",
    "sub-admin",
  ].includes(role);

  const handleNavigation = () => {
    onClose();
  };

  return (
    <aside className={`sidebar ${isOpen ? "sidebar-open" : ""}`}>
      <div className="sidebar-brand">
        <div className="brand-icon">
          SH
        </div>

        <div className="brand-text">
          <span className="brand-title">
            Smart Honeypot
          </span>

          <span className="brand-subtitle">
            Threat Intelligence
          </span>
        </div>
      </div>

      <nav className="sidebar-nav">
        <NavLink
          to="/"
          end
          onClick={handleNavigation}
          className={({ isActive }) =>
            `sidebar-link ${isActive ? "active" : ""}`
          }
        >
          <span className="sidebar-link-icon">
            ⌂
          </span>

          <span>Dashboard</span>
        </NavLink>

        {canViewLiveAttacks && (
          <NavLink
            to="/live-attacks"
            onClick={handleNavigation}
            className={({ isActive }) =>
              `sidebar-link ${isActive ? "active" : ""}`
            }
          >
            <span className="sidebar-link-icon">
              ◉
            </span>

            <span>Live Attacks</span>
          </NavLink>
        )}

        <NavLink
          to="/threat-intelligence"
          onClick={handleNavigation}
          className={({ isActive }) =>
            `sidebar-link ${isActive ? "active" : ""}`
          }
        >
          <span className="sidebar-link-icon">⌬</span>
          <span>Threat Intelligence / ML</span>
        </NavLink>

        <NavLink
          to="/honeypots"
          onClick={handleNavigation}
          className={({ isActive }) =>
            `sidebar-link ${isActive ? "active" : ""}`
          }
        >
          <span className="sidebar-link-icon">
            ◈
          </span>

          <span>Honeypots & Orchestrator</span>
        </NavLink>

        {canViewManagement && (
          <NavLink
            to="/management"
            onClick={handleNavigation}
            className={({ isActive }) =>
              `sidebar-link ${isActive ? "active" : ""}`
            }
          >
            <span className="sidebar-link-icon">
              ⚙
            </span>

            <span>Management</span>
          </NavLink>
        )}
      </nav>

      <div className="sidebar-footer">
        {/* <div className="system-status">
          <span className="status-dot"></span>

          <div>
            <span className="status-title">
              System Online
            </span>

            <span className="status-subtitle">
              Monitoring active
            </span>
          </div>
        </div> */}
      </div>
    </aside>
  );
}

export default Sidebar;
