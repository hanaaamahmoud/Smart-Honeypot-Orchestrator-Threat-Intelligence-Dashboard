import { useState } from "react";
import {
  Link,
  useNavigate,
  useSearchParams,
} from "react-router-dom";

import {
  resetPassword,
} from "../services/authService";

import PasswordInput from "../components/common/PasswordInput";

import "../components/auth/login-form.css";
import ActiveSessionGuard from "../components/auth/ActiveSessionGuard";

function ResetPassword(){
  const navigate = useNavigate();

  const [searchParams] =
    useSearchParams();


  const token =
    searchParams.get("token");


  const [password,setPassword] =
    useState("");


  const [confirmPassword,setConfirmPassword] =
    useState("");


  const [error,setError] =
    useState(token ? "" : "Reset link is missing its token.");


  const [success,setSuccess] =
    useState("");


  const [loading,setLoading] =
    useState(false);



  async function handleSubmit(event){

    event.preventDefault();


    if (loading) return;

    if (!token) {
      setError("Reset link is missing its token. Request a new password-reset link.");
      return;
    }



    setError("");

    setSuccess("");



    if(password !== confirmPassword){

      setError(
        "Passwords do not match."
      );

      return;

    }



    setLoading(true);



    try{


      await resetPassword(
        token,
        password
      );


      setSuccess(
        "Password updated successfully. Redirecting..."
      );



      setTimeout(()=>{

        navigate(
          "/login",
          {
            replace:true
          }
        );

      },1500);



    }


    catch(err){


      switch(err.message){


        case "INVALID_RESET_TOKEN":

          setError(
            "Invalid reset link."
          );

          break;



        case "EXPIRED_RESET_TOKEN":

          setError(
            "Reset link expired."
          );

          break;



        case "INVALID_PASSWORD":

          setError(
            "Password must contain at least 8 characters."
          );

          break;



        default:

          setError(
            "Unable to reset password."
          );

      }


    }


    finally{

      setLoading(false);

    }


  }




 return (

<ActiveSessionGuard>

<form
      className="login-form"
      onSubmit={handleSubmit}
    >


      <div className="login-heading">


        <span>
          Password Recovery
        </span>


        <h2>
          Reset password
        </h2>


        <p>
          Create a new secure password.
        </p>


      </div>





      <PasswordInput

        id="reset-password"

        label="New password"

        value={password}

        onChange={
          e =>
          setPassword(
            e.target.value
          )
        }


        placeholder="Enter new password"


        autoComplete="new-password"


        disabled={loading || !token}


      />





      <PasswordInput

        id="reset-confirm-password"

        label="Confirm password"


        value={confirmPassword}


        onChange={
          e =>
          setConfirmPassword(
            e.target.value
          )
        }


        placeholder="Confirm password"


        autoComplete="new-password"


        disabled={loading || !token}


      />






      {error && (

        <div
          className="login-error"
          role="alert"
        >

          {error}

        </div>

      )}






      {success && (

        <div
          className="login-success"
          role="status"
        >

          {success}

        </div>

      )}






      <button

        className="login-submit"

        disabled={loading || !token}

      >

        {
          loading
          ?
          "Resetting..."
          :
          "Reset password"
        }


      </button>





      <div
        style={{
          marginTop:"16px",
          textAlign:"center"
        }}
      >

        <Link
          to="/login"
          style={{
            color:
            "var(--color-primary-light)"
          }}
        >

          Back to login

        </Link>


      </div>



</form>

</ActiveSessionGuard>
  );

}


export default ResetPassword;