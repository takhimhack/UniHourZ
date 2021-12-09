export function retrieve_name() {
  return document.getElementById("Name") !== null
    ? document.getElementById("Name").value
    : "";
}

export function retrieve_email() {
  return document.getElementById("inputemail") !== null
    ? document.getElementById("inputemail").value
    : "";
}

export function retrieve_password() {
  if (document.getElementById("password") !== null) {
    return document.getElementById("password").value;
  } else if (document.getElementById("password_two") !== null) {
    return document.getElementById("password_two").value;
  } else {
    return "";
  }
}

export function retrieve_registration_select() {
  if (document.getElementById("reg_select") !== null) {
    let selector = document.getElementById("reg_select");
    return selector.options[selector.selectedIndex].value === "12"
      ? "Student"
      : "Instructor";
  } else {
    return "Student";
  }
}

export function retrieve_discord_tag() {
  let value = "";
  if (document.getElementById("discord_tag") !== null) {
    return document.getElementById("discord_tag").value;
  }
  return "";
}

export function ajaxGetRequest(path, callback) {
  let request = new XMLHttpRequest();
  request.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      callback(this.response);
    }
  };
  request.open("GET", path);
  request.send();
}

export function ajaxPostRequest(path, data, callback) {
  let request = new XMLHttpRequest();
  request.onreadystatechange = function () {
    if (this.readyState === 4 && this.status === 200) {
      callback(this.response);
    }
  };
  request.open("POST", path);
  request.send(data);
}
