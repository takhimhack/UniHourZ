import {
  retrieve_email,
  retrieve_password,
  retrieve_registration_select,
  retrieve_name,
  ajaxPostRequest,
  ajaxGetRequest,
} from "./dom_utils.js";

const form = document.querySelector("form");
form.addEventListener("submit", (event) => {
  event.preventDefault();
});

/* add event listener */
document
  .getElementById("registerbutton")
  .addEventListener("click", submit_registration);

/* callback function for registration */
function submit_registration() {
  let json_obj = JSON.stringify({
    name: retrieve_name(),
    email: retrieve_email(),
    password: retrieve_password(),
    typeofUser: retrieve_registration_select(),
  });
  ajaxPostRequest("/userRegistration", json_obj, process_auth_response);
}

const process_auth_response = (callbackData) => {
  let decoded_data = JSON.parse(callbackData);
  /* check to see if decoded reponse isn't valid, and print an error message */
  if (decoded_data["valid"] !== "valid") {
    document.getElementById("errormsg").innerHTML =
      "Credentials Invalid. Make sure you're using a @buffalo.edu email";
  } else {
    window.location = "index.html";
  }
};
