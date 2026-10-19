import { useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

import "./active-session-guard.css";


function ActiveSessionGuard({ children }) {

  const navigate = useNavigate();

  const {
    user,
    logout,
  } = useAuth();


  async function handleLogout() {

    await logout();

    window.location.reload();

  }



  if (!user) {

    return children;

  }



  return (

    <div className="active-session-wrapper">


      <div className="active-session-card">


        <div className="active-session-label">
          Security Notice
        </div>



        <h2>
          Active session detected
        </h2>



        <p>

          You are currently signed in as:

        </p>



        <div className="active-session-user">

          {user.email}

          <span>
            {user.role}
          </span>

        </div>



        <p>

          For security reasons,
          please logout from the current
          session before continuing.

        </p>




        <div className="active-session-actions">


          <button

            className="session-logout-btn"

            onClick={
              handleLogout
            }

          >

            Logout current session

          </button>




          <button

            className="session-back-btn"

            onClick={() =>
              navigate("/")
            }

          >

            Back to dashboard

          </button>


        </div>



      </div>


    </div>

  );

}


export default ActiveSessionGuard;
