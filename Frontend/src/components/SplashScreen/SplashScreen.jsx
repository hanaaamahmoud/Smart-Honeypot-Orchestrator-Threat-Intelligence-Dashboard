import { useEffect } from "react";
import "./SplashScreen.css";

function SplashScreen({ onComplete }) {
  useEffect(() => {
    const timer = setTimeout(() => {
      onComplete();
    }, 4000);

    return () => clearTimeout(timer);
  }, [onComplete]);

  return (
    <div className="splash-screen">
      <div className="radar-splash">

        <div className="radar-background">
          <div className="radar-circle radar-circle-1" />
          <div className="radar-circle radar-circle-2" />
          <div className="radar-circle radar-circle-3" />

          <div className="radar-line radar-line-horizontal" />
          <div className="radar-line radar-line-vertical" />

          <div className="radar-sweep" />

          <span className="radar-point radar-point-1" />
          <span className="radar-point radar-point-2" />
          <span className="radar-point radar-point-3" />
        </div>

        <div className="radar-center">
          <div className="radar-logo">
            SH
          </div>

          <h1>
            SMART HONEYPOT
          </h1>

          <p>
            THREAT INTELLIGENCE
          </p>
        </div>

        <div className="radar-status">
          <span className="radar-status-dot" />
          SCANNING ENVIRONMENT
        </div>

      </div>
    </div>
  );
}

export default SplashScreen;
