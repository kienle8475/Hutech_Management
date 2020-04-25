import { initializeApp } from 'firebase';

const app = initializeApp({
    apiKey: "AIzaSyCMcEtmZC3UiynMtvFQFqZwdo3yXIhn_HE",
    authDomain: "learningfirebasedatabasepython.firebaseapp.com",
    databaseURL: "https://learningfirebasedatabasepython.firebaseio.com/",
    storageBucket: "Customer.appspot.com"
});

export const db = app.database();
export const StudentRef = db.ref('Student')
export const EmployeeAttendanceRef = db.ref('EmployeeAttendance')