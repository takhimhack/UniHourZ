function submitLogin() {
  let name = "";
  let email = "";
  let password = "";
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
  let json_obj = JSON.stringify({
    name: name,
    email: email,
    password: password,
  });
  ajaxPostRequest("/userLogin", json_obj, processloginresponse);
}

function processloginresponse(login_response) {
  let decoded_response = JSON.parse(login_response);
  /* We have an invalid login from the web server */
  if (decoded_response.valid === 0) {
    document.getElementById("errormsg").innerHTML =
      "Error. Your account does not appear to end with buffalo.edu!";
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
