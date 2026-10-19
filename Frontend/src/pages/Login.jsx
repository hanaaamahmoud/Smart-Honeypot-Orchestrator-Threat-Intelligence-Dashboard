import LoginForm from "../components/auth/LoginForm";
import "../styles/login.css";

function Login() {
  return (
    <div className="login-page">
      <div className="login-container">
        <div className="login-brand">
          <div className="login-brand-icon">
            SH
          </div>

          <div>
            <h1>Smart Honeypot</h1>
            <p>
              Threat Intelligence Platform
            </p>
          </div>
        </div>

        <LoginForm />
      </div>
    </div>
  );
}

export default Login;
