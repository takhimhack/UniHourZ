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

function submit_login() {
  let json_obj = JSON.stringify({
    email: retrieve_email(),
    password: retrieve_password(),
  });
  console.log(json_obj);
  ajaxPostRequest("/userLogin", json_obj, process_auth);
}

function retrieve_name() {
  return document.getElementById("Name") !== null
    ? document.getElementById("Name").value
    : "";
}

function retrieve_email() {
  return document.getElementById("inputemail") !== null
    ? document.getElementById("inputemail").value
    : "";
}

function retrieve_password() {
  if (document.getElementById("password") !== null) {
    return document.getElementById("password").value;
  } else if (document.getElementById("password_two") !== null) {
    return document.getElementById("password_two").value;
  } else {
    return "";
  }
}

function retrieve_registration_select() {
  if (document.getElementById("reg_select") !== null) {
    loginType = "registration";
    let selector = document.getElementById("reg_select");
    return selector.options[selector.selectedIndex].value === "12"
      ? "Student"
      : "Instructor";
  } else {
    return "Student";
  }
}

function process_auth_response(login_response) {
  let decoded_response = JSON.parse(login_response);
  /* We have an invalid login from the web server */
  if (decoded_response.valid !== "valid") {
    document.getElementById("errormsg").innerHTML = decoded_response.valid;
  } else {
    document.getElementById("errormsg").innerHTML = "";
    window.location = "index.html";
  }
}

function process_auth(login_response) {
  let decoded_response = JSON.parse(login_response);
  if (decoded_response.valid !== "valid") {
    document.getElementById("errorf").innerHTML = decoded_response.message;
  } else {
    window.location = "landing.html";
    document.getElementById("welcome").innerHTML = decoded_response.user;
  }
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
