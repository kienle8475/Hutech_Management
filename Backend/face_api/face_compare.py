import cv2
import time
import pyrebase
import numpy as np
import mysql.connector
import face_recognition
from django.http import StreamingHttpResponse


class FaceCompare():
    config = {
        "apiKey": "AIzaSyCMcEtmZC3UiynMtvFQFqZwdo3yXIhn_HE",
        "authDomain": "learningfirebasedatabasepython.firebaseapp.com",
        "databaseURL": "https://learningfirebasedatabasepython.firebaseio.com/",
        "storageBucket": "Customer.appspot.com"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    def query(sql, val):
        mydb = mysql.connector.connect(
            host="35.221.107.80",
            user="peaga",
            passwd="Ltk99701299",
            database="HutechManagement",
            auth_plugin="mysql_native_password"
        )
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        results = mycursor.fetchone()
        return results

    def getEncode(StudentID):
        sql = "SELECT Encoding FROM employeesmanagement_faceencoding WHERE Employee_id = %s"
        Student_id = (str(StudentID),)
        results = FaceCompare.query(sql, Student_id)
        if results is not None:
            return(results)
        else:
            return("")

    def CompareFace(message):
        video_capture = cv2.VideoCapture(0)
        StudentID = message["data"]
        print(StudentID)
        results = FaceCompare.getEncode(StudentID)
        Face = ''.join(results)
        FaceEncode = np.fromstring(Face[1: -1], dtype=float, sep=",")
        print(FaceEncode)
        if FaceEncode.size > 0:
            while True:
                process_this_frame = True
                ret, frame = video_capture.read()
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]
                if process_this_frame:
                    face_locations = face_recognition.face_locations(
                        rgb_small_frame, 1, "hog")
                    face_encodings = face_recognition.face_encodings(
                        rgb_small_frame, face_locations)
                    for face_encoding in face_encodings:
                        matches = face_recognition.compare_faces(
                            [FaceEncode], face_encoding, tolerance=0.4)
                for (top, right, bottom, left) in (face_locations):
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    text_x = left
                    text_y = bottom+20
                    cv2.putText(frame, str(matches), (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                                1, (255, 255, 255), thickness=1, lineType=2)
                    cv2.rectangle(frame, (left, top),
                                  (right, bottom), (0, 255, 0), 2)
                cv2.imshow('Face Recoginition', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

        else:
            while True:
                ret, frame = video_capture.read()
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
                rgb_small_frame = small_frame[:, :, ::-1]
                process_this_frame = True
                if process_this_frame:
                    face_locations = face_recognition.face_locations(
                        rgb_small_frame, 2, "hog")
                for (top, right, bottom, left) in (face_locations):
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    text_x = left
                    text_y = bottom+20
                    cv2.rectangle(frame, (left, top),
                                  (right, bottom), (0, 255, 0), 2)
                cv2.imshow('Face Recoginition', frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

    # my_stream = db.child("Student/ID").stream(CompareFace)
    # db.child("Student/ID").stream(CompareFace)
