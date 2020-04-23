import cv2
import time
import pyrebase
import numpy as np
import mysql.connector
import face_recognition
from django.http import StreamingHttpResponse


class FaceRecognize():
    config = {
        "apiKey": "AIzaSyCMcEtmZC3UiynMtvFQFqZwdo3yXIhn_HE",
        "authDomain": "learningfirebasedatabasepython.firebaseapp.com",
        "databaseURL": "https://learningfirebasedatabasepython.firebaseio.com/",
        "storageBucket": "Customer.appspot.com"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    def query(sql):
        mydb = mysql.connector.connect(
            host="35.221.107.80",
            user="peaga",
            passwd="Ltk99701299",
            database="HutechManagement",
            auth_plugin="mysql_native_password"
        )
        mycursor = mydb.cursor()
        mycursor.execute(sql)
        results = mycursor.fetchall()
        return results

    def getEncode():
        face_encodings = []
        face_ids = []
        face_names = []
        sql_getFace = "SELECT Encoding FROM employeesmanagement_faceencoding"
        sql_getId = "SELECT Employee_id FROM employeesmanagement_faceencoding"
        sql_getName = "SELECT CONCAT(FirstName,LastName) FROM HutechManagement.employeesmanagement_employee"
        FaceEncodes = FaceRecognize.query(sql_getFace)
        for FaceEncode in FaceEncodes:
            FaceDecode = ''.join(FaceEncode)
            Face = np.fromstring(FaceDecode[1:-1], dtype=float, sep=",")
            face_encodings.append(Face)
        FaceIds = FaceRecognize.query(sql_getId)
        for FaceId in FaceIds:
            face_ids.append(FaceId[0])
        FaceNames = FaceRecognize.query(sql_getName)
        for FaceName in FaceNames:
            face_names.append(FaceName[0])
        return (face_encodings, face_ids, face_names)

    def detect():
        video_capture = cv2.VideoCapture(0)
        known_face_encodings = FaceRecognize.getEncode()[0]
        known_face_ids = FaceRecognize.getEncode()[1]
        known_face_names = FaceRecognize.getEncode()[2]
        face_encoding = []
        face_id = []
        face_name = []
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
                face_names = []
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(
                        known_face_encodings, face_encoding, tolerance=0.4)
                    distance = face_recognition.face_distance(
                        known_face_encodings, face_encoding)
                    name = "Unknown"
                    id = ""
                    face_distances = face_recognition.face_distance(
                        known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]
                    face_names.append(name)
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                text_x = left
                text_y = bottom+20
                cv2.putText(frame, name, (text_x, text_y), cv2.FONT_HERSHEY_COMPLEX_SMALL,
                            1, (255, 255, 255), thickness=1, lineType=2)
                cv2.rectangle(frame, (left, top),
                              (right, bottom), (0, 255, 0), 2)
            cv2.imwrite('stream.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open('stream.jpg', 'rb').read() + b'\r\n')

    def video_feed(request):
        return StreamingHttpResponse(FaceRecognize.detect(), content_type='multipart/x-mixed-replace; boundary=frame')
