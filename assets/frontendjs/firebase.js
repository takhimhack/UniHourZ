import {
  getAuth,
  signInWithEmailAndPassword,
  signOut,
} from "https://www.gstatic.com/firebasejs/9.4.0/firebase-auth.js";

import { initializeApp } from "https://www.gstatic.com/firebasejs/9.4.0/firebase-app.js";

const config_user = {
  apiKey: "AIzaSyB8qHYVB7tIoTKiSwl0pFnc2SZv6rRhZA8",
  authDomain: "projectdemo-cfd84.firebaseapp.com",
  databaseURL: "https://projectdemo-cfd84-default-rtdb.firebaseio.com",
  storageBucket: "projectdemo-cfd84.appspot.com",
};

const auth = getAuth(initializeApp(config_user));

export const logIn = (email, password, success_callback, error_callback) => {
  signInWithEmailAndPassword(auth, email, password)
    .then(success_callback)
    .catch(error_callback);
};

export const logOut = (success_callback, error_callback) => {
  signOut(auth).then(success_callback).catch(error_callback);
};
