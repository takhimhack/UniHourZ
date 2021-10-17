function submitLogin() {
  let name = "";
  let email = "";
  let password = "";
  let loginType = "login";
  let typeofUser = "";
  if (document.getElementById("Name") !== null) {
    name = document.getElementById("Name").value;
    document.getElementById("Name").value = "";
  }
  if (document.getElementById("inputemail") !== null) {
    email = document.getElementById("inputemail").value;
    document.getElementById("inputemail").value = "";
  }
  if (document.getElementById("password") !== null) {
    password = document.getElementById("password").value;
    document.getElementById("password").value = "";
  } else if (document.getElementById("password_two") !== null) {
    password = document.getElementById("password_two").value;
    document.getElementById("password_two").value = "";
  }
  if (document.getElementById("reg_select") !== null) {
    loginType = "registration";
    let selector = document.getElementById("reg_select");
    typeofUser =
      selector.options[selector.selectedIndex].value === 12
        ? "Student"
        : "Instructor";
  }
  let json_obj = JSON.stringify({
    name: name,
    email: email,
    password: password,
    loginType: loginType,
    typeofUser: typeofUser,
  });
  ajaxPostRequest("/userLogin", json_obj, processloginresponse);
}

function processloginresponse(login_response) {
  let decoded_response = JSON.parse(login_response);
  /* We have an invalid login from the web server */
  if (decoded_response.valid !== "valid") {
    document.getElementById("errormsg").innerHTML = decoded_response.valid;
  } else {
    document.getElementById("errormsg").innerHTML = "";
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
