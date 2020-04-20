import cv2
import time
import pyrebase
import numpy as np
import mysql.connector
import face_recognition
from django.http import StreamingHttpResponse

class FaceRecognize():
    config ={
        "apiKey": "AIzaSyCMcEtmZC3UiynMtvFQFqZwdo3yXIhn_HE",
        "authDomain": "learningfirebasedatabasepython.firebaseapp.com",
        "databaseURL":"https://learningfirebasedatabasepython.firebaseio.com/",
        "storageBucket":"Customer.appspot.com"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()
    def stream_handler(message):
            EmployeeID = message["data"]
            print(EmployeeID)
            EmployeeID=""
    my_stream = db.child("Employee/ID").stream(stream_handler)
            
    def getFaceEncode(Employee_id):
        mydb = mysql.connector.connect(
            host="35.221.107.80",
            user="peaga",
            passwd="Ltk99701299",
            database="HutechManagement",
            auth_plugin="mysql_native_password"
        )
        mycursor = mydb.cursor()
        sql = "SELECT Encoding FROM employeesmanagement_faceencoding WHERE Employee_id = %s"
        mycursor.execute(sql, Employee_id)
        myresult = mycursor.fetchone()
        FaceEncode = ''.join(myresult)
        Face_ID = np.fromstring(FaceEncode[1:-1], dtype=float, sep=",")
        return Face_ID

    def detect():
        video_capture = cv2.VideoCapture("http://192.168.1.104:4747/video")
        while True:
            process_this_frame = True
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            if process_this_frame:
                face_locations_hog = face_recognition.face_locations(rgb_small_frame,1,"hog")
                for (top, right, bottom, left) in (face_locations_hog):
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.imwrite('demo.jpg', frame)
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + open('demo.jpg', 'rb').read() + b'\r\n')

    def video_feed(request):
        return StreamingHttpResponse(FaceRecognize.detect(), content_type='multipart/x-mixed-replace; boundary=frame')