/* Sets the cookie information. Expires after exDays */
export const set_cookie = (authToken, refreshToken, inputEmail, exDays) => {
  const d = new Date();
  d.setTime(d.getTime() + exDays * 24 * 60 * 60 * 1000);
  let expires = "expires=" + d.toUTCString();
  let email = "email=" + inputEmail;
  document.cookie =
    "authToken=" +
    authToken +
    ";" +
    "refreshToken=" +
    refreshToken +
    ";" +
    email +
    ";" +
    expires +
    ";";
};

/* get a key stored in a cookie */
export const get_cookie = (key) => {
  let name = key + "=";
  let decodedCookie = decodeURIComponent(document.cookie).split(";");

  /* Find the value in the cookie */
  for (let character of decodedCookie) {
    /* Get the first non white space character after a semi colon */
    while (character.charAt(0) === " ") character = character.substring(1);

    if (character.indexOf(name) === 0) {
      return character.substring(name.length, character.length);
    }
  }
  return "";
};

/* returns true if name exists in the cookie */
export const check_cookie = () => {
  let name = get_cookie("email");
  /* might need to do additional validation with da cookie */
  return name !== null && name !== "";
};
