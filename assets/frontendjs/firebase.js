import {
  getAuth,
  signInWithEmailAndPassword,
  signOut,
} from "https://www.gstatic.com/firebasejs/9.4.0/firebase-auth.js";

import { initializeApp } from "https://www.gstatic.com/firebasejs/9.4.0/firebase-app.js";

import { ajaxGetRequest } from "./dom_utils.js";

let auth = null;

// send an ajax get request to the server to return config credentials
ajaxGetRequest("/getConfig", (information) => {
  let decodedInformation = JSON.parse(information);
  //decoded information is the config information. Assign auth accordingly
  auth = getAuth(initializeApp(decodedInformation));
});

export const logIn = (email, password, success_callback, error_callback) => {
  signInWithEmailAndPassword(auth, email, password)
    .then(success_callback)
    .catch(error_callback);
};

export const logOut = (success_callback, error_callback) => {
  signOut(auth).then(success_callback).catch(error_callback);
};
