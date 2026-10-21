import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../../context/AuthContext";
import PasswordInput from "../common/PasswordInput";

import "./login-form.css";
import {
 Link
} from "react-router-dom";

function LoginForm() {

  const navigate = useNavigate();

  const { login } = useAuth();


  const [email, setEmail] =
    useState("");

  const [password, setPassword] =
    useState("");


  const [error, setError] =
    useState("");

  const [loading, setLoading] =
    useState(false);



  async function handleSubmit(event) {

    event.preventDefault();


    if (loading) {
      return;
    }


    setError("");
    setLoading(true);



    try {

      await login(
        email,
        password
      );


      navigate(
        "/",
        {
          replace: true,
        }
      );


    } catch (err) {


      switch (err.message) {


        case "INVALID_CREDENTIALS":

          setError(
            "Invalid email or password."
          );

          break;



        case "ACCOUNT_DISABLED":

          setError(
            "This account has been disabled."
          );

          break;



        case "ACCOUNT_NOT_ACTIVATED":

          setError(
            "This account is not activated."
          );

          break;



        default:

          setError(
            "Unable to sign in. Please try again."
          );

      }


    } finally {

      setLoading(false);

    }

  }



  return (

    <form
      className="login-form"
      onSubmit={handleSubmit}
    >


      <div className="login-heading">

        <span>
          Secure Access
        </span>


        <h2>
          Sign in
        </h2>


        <p>
          Access the Smart Honeypot
          monitoring dashboard.
        </p>

      </div>




      <div className="login-field">

        <label htmlFor="email">
          Email
        </label>


        <input

          id="email"

          type="email"

          value={email}

          onChange={(event) =>
            setEmail(
              event.target.value
            )
          }

          placeholder="Enter your email"

          autoComplete="email"

          disabled={loading}

          required

        />

      </div>




      <PasswordInput

        id="password"

        label="Password"

        value={password}

        onChange={(event) =>
          setPassword(
            event.target.value
          )
        }

        placeholder="Enter your password"

        autoComplete="current-password"

        disabled={loading}

      />





      {error && (

        <div

          className="login-error"

          role="alert"

        >

          {error}

        </div>

      )}






      <button

        className="login-submit"

        type="submit"

        disabled={loading}

      >

        {
          loading
            ? "Signing in..."
            : "Sign in"
        }


      </button>
      <div
 style={{
  marginTop:"14px",
  textAlign:"center"
 }}
>
 <Link
  to="/forgot-password"
  style={{
   color:"var(--color-primary-light)",
   fontSize:"11px",
   textDecoration:"none"
  }}
 >
  Forgot password?
 </Link>
</div>
      <div
 style={{
  marginTop:"14px",
  textAlign:"center"
 }}
>
</div>
    </form>

  );

}


export default LoginForm;
