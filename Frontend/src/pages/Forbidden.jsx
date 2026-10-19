function Forbidden() {
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
        textAlign: "center",
      }}
    >
      <div>
        <div
          style={{
            color: "var(--color-danger)",
            fontSize: "12px",
            fontWeight: 700,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
            marginBottom: "10px",
          }}
        >
          Access denied
        </div>

        <h1
          style={{
            margin: 0,
            fontSize: "32px",
          }}
        >
          403
        </h1>

        <p
          style={{
            margin: "10px 0 0",
            color: "var(--color-text-muted)",
            fontSize: "13px",
          }}
        >
          You do not have permission to access this page.
        </p>
      </div>
    </div>
  );
}

export default Forbidden;
