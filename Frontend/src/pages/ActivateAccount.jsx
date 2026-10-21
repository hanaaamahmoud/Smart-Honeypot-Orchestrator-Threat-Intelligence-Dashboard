import ActiveSessionGuard from "../components/auth/ActiveSessionGuard";
import { useState, useEffect } from "react";
import {
  Link,
  useSearchParams,
  useNavigate,
} from "react-router-dom";

import {
  activateAccount,
  resendActivation,
} from "../services/authService";

import PasswordInput from "../components/common/PasswordInput";

import "../components/auth/login-form.css";


function ActivateAccount() {
const session =
  localStorage.getItem(
    "smart_honeypot_mock_session"
  );

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
    useState("");

  const [success,setSuccess] =
    useState("");

  const [loading,setLoading] =
    useState(false);



  const [invalidToken,setInvalidToken] =
    useState(false);


  const [expiredToken,setExpiredToken] =
    useState(false);




  useEffect(()=>{


    if(!token){

      setInvalidToken(true);

      setError(
        "Invalid activation link."
      );

    }


  },[token]);







  async function handleSubmit(event){


    event.preventDefault();


    if(loading || invalidToken){

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


      await activateAccount(
        token,
        password
      );



      setSuccess(
        "Account activated successfully. Redirecting..."
      );



      setTimeout(()=>{

        navigate(
          "/login",
          {
            replace:true,
          }
        );

      },1500);



    }


    catch(err){


      switch(err.message){


        case "INVALID_ACTIVATION_TOKEN":

          setInvalidToken(true);

          setError(
            "Invalid activation link."
          );

          break;



        case "EXPIRED_ACTIVATION_TOKEN":

          setExpiredToken(true);

          setError(
            "Activation link expired."
          );

          break;



        case "ACCOUNT_ALREADY_ACTIVATED":

          setError(
            "This account is already activated."
          );

          break;



        case "INVALID_PASSWORD":

          setError(
            "Password must contain at least 8 characters."
          );

          break;



        default:

          setError(
            "Unable to activate account."
          );


      }


    }


    finally{

      setLoading(false);

    }


  }







  async function handleRequestNewLink(){


    setError("");

    setSuccess("");



    try{


      const userId =
        localStorage.getItem(
          "smart_honeypot_last_activation_user"
        );



      if(!userId){

        throw new Error(
          "USER_NOT_FOUND"
        );

      }



      const result =
        await resendActivation(
          userId
        );

      setSuccess(
        "New activation link generated."
      );


    }


    catch(err){


      if(
        err.message ===
        "ACTIVATION_RATE_LIMIT"
      ){

        setError(
          "Please wait before requesting another activation link."
        );


      }

      else{

        setError(
          "Unable to generate new activation link."
        );

      }


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
          Account Activation
        </span>


        <h2>
          Activate account
        </h2>


        <p>
          Create a secure password to activate your account.
        </p>


      </div>





      <PasswordInput

        id="activation-password"

        label="Password"

        value={password}

        onChange={
          e =>
          setPassword(
            e.target.value
          )
        }

        placeholder="Create password"

        autoComplete="new-password"

        disabled={
          loading ||
          invalidToken
        }

      />






      <PasswordInput

        id="confirm-password"

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

        disabled={
          loading ||
          invalidToken
        }

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








      {(invalidToken || expiredToken) && (

        <button

          type="button"

          className="activation-link-button"

          onClick={
            handleRequestNewLink
          }

        >

          Request new activation link


        </button>


      )}







      {!invalidToken && !expiredToken && (

        <button

          className="login-submit"

          type="submit"

          disabled={loading}

        >

          {
            loading
            ?
            "Activating..."
            :
            "Activate account"
          }


        </button>

      )}







      <div
        style={{
          marginTop:"16px",
          textAlign:"center",
        }}
      >

        <Link
          to="/login"
          style={{
            color:
            "var(--color-primary-light)",

            fontSize:"11px",

            textDecoration:"none",
          }}
        >

          Back to login

        </Link>


      </div>



</form>

</ActiveSessionGuard>
  );


}


export default ActivateAccount;