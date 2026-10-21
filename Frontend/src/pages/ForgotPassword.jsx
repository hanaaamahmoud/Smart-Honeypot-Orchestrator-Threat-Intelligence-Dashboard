import {
 useState,
 useEffect
} from "react";import { Link } from "react-router-dom";

import {
  requestPasswordReset
} from "../services/authService";

import "../components/auth/login-form.css";


function ForgotPassword(){

  const [email,setEmail]=useState("");

  const [message,setMessage]=useState("");

  const [error,setError]=useState("");

  const [loading,setLoading]=useState(false);
  const [cooldown,setCooldown]=useState(0);

const [resetLink,setResetLink] =
  useState("");

  async function handleSubmit(e){

    e.preventDefault();


    if(
 loading ||
 cooldown > 0
)
return;

    setLoading(true);

    setError("");

    setMessage("");



    try{

      const result =
      await requestPasswordReset(
        email
      );


setMessage(
  result.message
);


if(result.resetToken){

 const resetUrl =
 `/reset-password?token=${result.resetToken}`;

 setResetLink(resetUrl);

}
else{

 setResetLink("");

}
setCooldown(60);

    }

    catch{

      setError(
        "Unable to process request."
      );

    }

    finally{

      setLoading(false);

    }

  }


useEffect(()=>{

 if(cooldown <= 0)
 return;


 const timer =
 setTimeout(()=>{

 setCooldown(
  value=>value-1
 );

 },1000);


 return ()=>clearTimeout(timer);


},[cooldown]);
  return (

    <form
      className="login-form"
      onSubmit={handleSubmit}
    >

      <div className="login-heading">

        <span>
          Account Recovery
        </span>


        <h2>
          Forgot password
        </h2>


        <p>
          Enter your email to reset your password.
        </p>


      </div>



      <div className="login-field">

        <label>
          Email
        </label>


        <input

          type="email"

          value={email}

          onChange={
            e=>setEmail(
              e.target.value
            )
          }

          autoComplete="email"

          placeholder="Enter your email"

          disabled={loading}

          required

        />


      </div>




      {error && (

        <div className="login-error">
          {error}
        </div>

      )}



      {message && (

        <div className="login-success">
          {message}
        </div>

      )}


{resetLink && import.meta.env.DEV && (

  <div className="reset-link-box">

    <span>
      Development reset link
    </span>


    <a
      href={resetLink}
      className="reset-link-button"
    >
      Open reset page
    </a>


  </div>

)}
      <button

className="login-submit"

disabled={
 loading ||
 cooldown > 0
}

>

        {
          loading
?
"Sending..."
:
cooldown > 0
?
`Wait ${cooldown}s`
:
"Send reset link"
        }


      </button>




      <div
        style={{
          marginTop:"15px",
          textAlign:"center"
        }}
      >

        <Link to="/login">
          Back to login
        </Link>

      </div>



    </form>

  );

}


export default ForgotPassword;