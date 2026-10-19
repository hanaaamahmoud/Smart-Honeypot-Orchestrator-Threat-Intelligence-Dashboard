import { useState } from "react";

import "./password-input.css";


function EyeIcon({ hidden }) {

  return hidden ? (

    <svg
      viewBox="0 0 24 24"
      aria-hidden="true"
    >

      <path
        d="M3 3l18 18"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
      />

      <path
        d="M10.6 10.6a2 2 0 0 0 2.8 2.8"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
      />

      <path
        d="M9.9 4.2A10.8 10.8 0 0 1 12 4c5.2 0 9 4 10 8-1 4-4.8 8-10 8a10.5 10.5 0 0 1-5.8-1.7"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
      />

    </svg>


  ) : (

    <svg
      viewBox="0 0 24 24"
      aria-hidden="true"
    >

      <path
        d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12z"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      />

      <circle
        cx="12"
        cy="12"
        r="3"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      />

    </svg>

  );

}





function PasswordInput({

  id,

  label,

  value,

  onChange,

  placeholder,

  autoComplete = "new-password",

  disabled = false,

  required = true,

}) {


  const [showPassword,setShowPassword] =
    useState(false);



  return (

    <div className="login-field">


      {
        label && (

          <label htmlFor={id}>
            {label}
          </label>

        )
      }





      <div className="password-input-wrapper">


        <input

          id={id}

          type={
            showPassword
            ?
            "text"
            :
            "password"
          }


          value={value}


          onChange={onChange}


          placeholder={placeholder}


          autoComplete={autoComplete}


          disabled={disabled}


          required={required}


        />





        <button

          type="button"

          className="password-toggle"

          onClick={()=>
            setShowPassword(
              current =>
              !current
            )
          }


          disabled={disabled}


          aria-label={
            showPassword
            ?
            "Hide password"
            :
            "Show password"
          }

        >


          <EyeIcon

            hidden={
              showPassword
            }

          />


        </button>


      </div>


    </div>

  );

}


export default PasswordInput;
