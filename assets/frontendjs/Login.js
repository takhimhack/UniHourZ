import { logIn, logOut } from "./firebase.js";
import { get_cookie, set_cookie, check_cookie } from "./cookie_handler.js";

import { retrieve_email, retrieve_password } from "./dom_utils.js";

const form = document.querySelector("form");
form.addEventListener("submit", (event) => {
  event.preventDefault();
});

/* Add event listener for submitting login */
document.getElementById("log in").addEventListener("click", () => {
  submit_login();
});

const login_success_callback = (userCredential) => {
  let user = userCredential.user;
  console.log(user);
};

const login_error_callback = (error) => {
  document.getElementById("errorf").innerHTML = "*Email or Password Invalid.";
};

function submit_login() {
  let email = retrieve_email();
  let password = retrieve_password();
  logIn(email, password, login_success_callback, login_error_callback);
}

function ajaxGetRequest(path, callback) {
  let request = new XMLHttpRequest();
  request.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      callback(this.response);
    }
  };
  request.open("GET", path);
  request.send();
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
