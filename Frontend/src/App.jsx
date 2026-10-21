import {
  useCallback,
  useState,
} from "react";

import {
  BrowserRouter,
  Route,
  Routes,
} from "react-router-dom";

import MainLayout from "./layouts/MainLayout";

import Dashboard from "./pages/Dashboard";
import LiveAttacks from "./pages/LiveAttacks";
import Statistics from "./pages/Statistics";
import AttackDetails from "./pages/AttackDetails";
import Honeypots from "./pages/Honeypots";
import ThreatIntelligence from "./pages/ThreatIntelligence";

import Login from "./pages/Login";
import ActivateAccount from "./pages/ActivateAccount";
import ForgotPassword from "./pages/ForgotPassword";
import ResetPassword from "./pages/ResetPassword";

import Management from "./pages/Management";
import Forbidden from "./pages/Forbidden";
import NotFound from "./pages/NotFound";

import SplashScreen from "./components/SplashScreen/SplashScreen";

import {
  AuthProvider,
} from "./context/AuthContext";

import ProtectedRoute from "./routes/ProtectedRoute";
import RoleRoute from "./routes/RoleRoute";

function App() {
  const [
    showSplash,
    setShowSplash,
  ] = useState(true);

  const handleSplashComplete =
    useCallback(() => {
      setShowSplash(false);
    }, []);

  if (showSplash) {
    return (
      <SplashScreen
        onComplete={
          handleSplashComplete
        }
      />
    );
  }

  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route
            path="/login"
            element={<Login />}
          />

          <Route
            path="/forgot-password"
            element={
              <ForgotPassword />
            }
          />

          <Route
            path="/activate"
            element={
              <ActivateAccount />
            }
          />

          <Route
            path="/reset-password"
            element={
              <ResetPassword />
            }
          />

          <Route
            path="/forbidden"
            element={
              <Forbidden />
            }
          />

          <Route
            element={
              <ProtectedRoute />
            }
          >
            <Route
              element={
                <MainLayout />
              }
            >
              <Route
                path="/"
                element={
                  <Dashboard />
                }
              />

              <Route
                path="/live-attacks"
                element={
                  <LiveAttacks />
                }
              />

              <Route
                path="/honeypots"
                element={
                  <Honeypots />
                }
              />

              <Route
                path="/threat-intelligence"
                element={
                  <ThreatIntelligence />
                }
              />

              <Route
                path="/statistics"
                element={
                  <Statistics />
                }
              />

              <Route
                path="/attacks/:id"
                element={
                  <AttackDetails />
                }
              />

              <Route
                element={
                  <RoleRoute
                    allowedRoles={[
                      "admin",
                      "sub-admin",
                    ]}
                  />
                }
              >
                <Route
                  path="/management"
                  element={
                    <Management />
                  }
                />
              </Route>
            </Route>
          </Route>

          <Route
            path="*"
            element={
              <NotFound />
            }
          />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}

export default App;