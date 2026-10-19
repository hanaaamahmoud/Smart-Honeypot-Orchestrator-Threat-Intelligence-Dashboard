import { Link } from "react-router-dom";
import "../styles/not-found.css";

function NotFound() {
  return (
    <div className="not-found-page">
      <div className="not-found-content">
        <span className="not-found-eyebrow">
          Page not found
        </span>

        <h1>404</h1>

        <p>
          The page you are looking for does not exist.
        </p>

        <Link
          to="/"
          className="not-found-link"
        >
          Back to dashboard
        </Link>
      </div>
    </div>
  );
}

export default NotFound;
