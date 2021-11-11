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
    loginType = "registration";
    let selector = document.getElementById("reg_select");
    return selector.options[selector.selectedIndex].value === "12"
      ? "Student"
      : "Instructor";
  } else {
    return "Student";
  }
}
