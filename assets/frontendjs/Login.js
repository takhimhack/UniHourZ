import { logIn, logOut } from "./firebase.js";
import { get_cookie, set_cookie, check_cookie } from "./cookie_handler.js";

import { retrieve_email, retrieve_password } from "./dom_utils.js";

const form = document.querySelector("form");
form.addEventListener("submit", (event) => {
  event.preventDefault();
});

/* Add an event listener to check the cookie once the page loads */
document.getElementById("mainBody").addEventListener("load", (event) => {
  /* Check the user cookie. If they have it, redirect them to landing.html with their information */
  event.preventDefault();
});

/* Add event listener for submitting login */
document.getElementById("log in").addEventListener("click", submit_login);

const login_success_callback = (userCredential) => {
  let user = userCredential.user;

  /* get the auth token and force a refresh */
  /* set a cookie with this information */

  user.getIdToken(true).then((userAuthToken) => {
    set_cookie("authToken", userAuthToken, 10);
  });

  /* Send a get request to get the right page. */
};

const login_error_callback = (error) => {
  document.getElementById("errorf").innerHTML =
    "*Email or Password Invalid." + error;
};

function submit_login() {
  let email = retrieve_email();
  let password = retrieve_password();
  logIn(email, password, login_success_callback, login_error_callback);
}
