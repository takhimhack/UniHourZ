/*console.log("Hello world!");
*/
/*

import { initializeApp } from 'firebase/app';

import { getDatabase } from "firebase/database";
import { getAuth, onAuthStateChanged } from "firebase/auth";
*/

/*
const firebaseConfig = ({
    apiKey: "AIzaSyB8qHYVB7tIoTKiSwl0pFnc2SZv6rRhZA8",

    authDomain: "projectdemo-cfd84.firebaseapp.com",

    databaseURL: "https://projectdemo-cfd84-default-rtdb.firebaseio.com",

    projectId: "projectdemo-cfd84",

    storageBucket: "projectdemo-cfd84.appspot.com",

    messagingSenderId: "1018325850707",

    appId: "1:1018325850707:web:fd550dd601d107158e04a6",

    measurementId: "G-B0F8JF9845"

});
*/


/*
const app = initializeApp(firebaseConfig);

const database = getDatabase(app);*/

firebase.auth().onAuthStateChanged(function(user) {
  
 if (user) {
    // User logged in already or has just logged in.
    console.log(user.uid);
  } else {
    // User not logged in or has just logged out.
  }
  /*if (user) {
    // User is signed in.


    var user = firebase.auth().currentUser;

    if(user != null){

      var email_id = user.email;
      document.getElementById("user_para").innerHTML = "Welcome User : " + email_id;
    console.log(user.uid);

    }

  } else {
    // No user is signed in.


  }*/
});
/*
const auth = getAuth();
const user = auth.currentUser;

firebase.auth().onAuthStateChanged((user) => {
  if (user) {
    // User logged in already or has just logged in.
    console.log(user.uid);
  } else {
    // User not logged in or has just logged out.
  }
});


*/


