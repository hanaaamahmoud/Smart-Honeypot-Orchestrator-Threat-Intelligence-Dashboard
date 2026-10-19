import { useEffect, useRef, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

import "./Navbar.css";

function Navbar({ onMenuClick }) {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const [showUserMenu, setShowUserMenu] =
    useState(false);

  const [isLoggingOut, setIsLoggingOut] =
    useState(false);

  const userMenuRef = useRef(null);

  useEffect(() => {
    const handleOutsideClick = (event) => {
      if (
        userMenuRef.current &&
        !userMenuRef.current.contains(
          event.target
        )
      ) {
        setShowUserMenu(false);
      }
    };

    document.addEventListener(
      "pointerdown",
      handleOutsideClick,
      true
    );

    return () => {
      document.removeEventListener(
        "pointerdown",
        handleOutsideClick,
        true
      );
    };
  }, []);

  const handleLogout = async () => {
    if (isLoggingOut) {
      return;
    }

    setIsLoggingOut(true);

    try {
      await logout();

      navigate("/login", {
        replace: true,
      });
    } finally {
      setIsLoggingOut(false);
      setShowUserMenu(false);
    }
  };

  const toggleUserMenu = () => {
    setShowUserMenu(
      (current) => !current
    );
  };

  return (
    <header className="navbar">
      <div className="navbar-left">

        <button
          type="button"
          className="menu-button"
          onClick={onMenuClick}
          aria-label="Open navigation menu"
        >
          ☰
        </button>

        <div className="navbar-page">
          <span className="navbar-eyebrow">
            Security Operations
          </span>

          <h1 className="navbar-title">
            Threat Intelligence Dashboard
          </h1>
        </div>

      </div>

      <div className="navbar-right">

        {/* <div className="navbar-status">
          <span className="navbar-status-dot" />

          <div className="navbar-status-text">
            <span className="navbar-status-title">
              Monitoring Active
            </span>

            <span className="navbar-status-subtitle">
              Honeypot environment online
            </span>
          </div>
        </div> */}

        {user && (
          <div
            className="navbar-user"
            ref={userMenuRef}
          >

            <button
              type="button"
              className="navbar-user-button"
              onClick={toggleUserMenu}
              aria-expanded={showUserMenu}
              aria-haspopup="menu"
            >
              <span className="navbar-user-avatar">
                {user.name
                  ?.charAt(0)
                  .toUpperCase()}
              </span>

              <span className="navbar-user-info">
                <strong>
                  {user.name}
                </strong>

                <span>
                  {user.role}
                </span>
              </span>

              <span className="navbar-user-arrow">
                {showUserMenu
                  ? "▲"
                  : "▼"}
              </span>
            </button>

            {showUserMenu && (
              <div
                className="navbar-user-menu"
                role="menu"
              >
                <div className="navbar-user-menu-header">
                  <strong>
                    {user.name}
                  </strong>

                  <span>
                    {user.email}
                  </span>
                </div>

                <button
                  type="button"
                  className="navbar-logout-button"
                  onClick={handleLogout}
                  disabled={isLoggingOut}
                  role="menuitem"
                >
                  {isLoggingOut
                    ? "Signing out..."
                    : "Sign out"}
                </button>
              </div>
            )}

          </div>
        )}

      </div>
    </header>
  );
}

export default Navbar;