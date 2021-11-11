import { delete_cookie } from "./cookie_handler.js";
import { logOut } from "./firebase.js";

/* Add an event listener to for logging out */
document.getElementById("log out").addEventListener("click", () => {
  logOut(success_callback, error_callback);
});

const success_callback = () => {
  /* Do something with a cookie? */
  delete_cookie("authToken");
  delete_cookie("refreshToken");
};

const error_callback = (error) => {
  /* This happens when something when wrong signing a user out */
  console.log("Error! " + error.message);
};
