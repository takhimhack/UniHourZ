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
    window.location = "home.html";

  });


  /* Send a get request to get the right page. */
};

const login_error_callback = (error) => {
  document.getElementById("errorf").innerHTML =
    "*Email or Password Invalid." + error;
};

function redirect_page(server_response){
    let decoded = JSON.parse(server_response);
    if (decoded.valid === 'valid'){
        window.location = "/instructor/instructor-version-home.html";
    } else {
        window.location = "/student/student-version-home.html";

    }
}

function ajaxPostRequest(path, data, callback) {
    let request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (this.readyState === 4 && this.status === 200) {
            callback(this.response);
        }
    };
    request.open("POST", path);
    request.send(data);
}

function submit_login() {
    let email = retrieve_email();
  let password = retrieve_password();
  logIn(email, password, login_success_callback, login_error_callback);
}
