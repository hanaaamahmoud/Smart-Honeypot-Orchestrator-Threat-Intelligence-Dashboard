import { useNavigate } from "react-router-dom";

function Unauthorized() {
  const navigate = useNavigate();

  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "32px",
        background: "var(--color-bg-main)",
        color: "var(--color-text-primary)",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "460px",
          padding: "36px",
          textAlign: "center",
          background: "var(--color-surface)",
          border: "1px solid var(--color-border)",
          borderRadius: "var(--radius-xl)",
          boxShadow: "var(--shadow-lg)",
        }}
      >
        <div
          style={{
            width: "58px",
            height: "58px",
            margin: "0 auto 20px",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            borderRadius: "50%",
            background: "var(--color-danger-soft)",
            color: "var(--color-danger-light)",
            fontSize: "26px",
            fontWeight: "800",
          }}
        >
          !
        </div>

        <div
          style={{
            marginBottom: "8px",
            color: "var(--color-danger-light)",
            fontSize: "10px",
            fontWeight: "700",
            letterSpacing: "0.12em",
            textTransform: "uppercase",
          }}
        >
          Access Restricted
        </div>

        <h1
          style={{
            margin: "0 0 10px",
            fontSize: "24px",
          }}
        >
          Access Denied
        </h1>

        <p
          style={{
            margin: "0 0 24px",
            color: "var(--color-text-muted)",
            fontSize: "12px",
            lineHeight: "1.6",
          }}
        >
          You do not have permission to access this resource.
        </p>

        <button
          onClick={() => navigate("/")}
          style={{
            width: "100%",
            height: "44px",
            border: "1px solid var(--color-border)",
            borderRadius: "var(--radius-md)",
            background: "var(--color-surface-hover)",
            color: "var(--color-text-primary)",
            fontSize: "12px",
            fontWeight: "700",
            cursor: "pointer",
          }}
        >
          Back to Dashboard
        </button>
      </div>
    </div>
  );
}

export default Unauthorized;
