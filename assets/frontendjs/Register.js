const form = document.querySelector("form");
form.addEventListener("submit", (event) => {
  event.preventDefault();
});

function submit_registration() {
  let json_obj = JSON.stringify({
    name: retrieve_name(),
    email: retrieve_email(),
    password: retrieve_password(),
    typeofUser: retrieve_registration_select(),
  });
  console.log(json_obj);
  ajaxPostRequest("/userRegistration", json_obj, process_auth_response);
}
