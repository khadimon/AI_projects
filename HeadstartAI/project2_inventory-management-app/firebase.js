// Import the functions you need from the SDKs you need
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";
import {getFirestore} from "firebase/firestore"
// TODO: Add SDKs for Firebase products that you want to use
// https://firebase.google.com/docs/web/setup#available-libraries

// Your web app's Firebase configuration
// For Firebase JS SDK v7.20.0 and later, measurementId is optional
const firebaseConfig = {
  apiKey: "AIzaSyBYSC84wz00dxj8c-m5kQtf6KNAUR5rRgA",
  authDomain: "inventory-management-bf133.firebaseapp.com",
  projectId: "inventory-management-bf133",
  storageBucket: "inventory-management-bf133.appspot.com",
  messagingSenderId: "859653662078",
  appId: "1:859653662078:web:974f86b063098ebb1bbf2f",
  measurementId: "G-DNWHZVBYGP"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);
const firestore = getFirestore(app);

export {firestore};