import os
import cv2
import time
import pyrebase
import numpy as np
import mysql.connector
import face_recognition
from mtcnn import MTCNN
from datetime import datetime
from django.http import StreamingHttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from tensorflow.keras.models import model_from_json


class Database():
    config = {
        "apiKey": "AIzaSyCMcEtmZC3UiynMtvFQFqZwdo3yXIhn_HE",
        "authDomain": "learningfirebasedatabasepython.firebaseapp.com",
        "databaseURL": "https://learningfirebasedatabasepython.firebaseio.com/",
        "storageBucket": "Customer.appspot.com"
    }
    firebase = pyrebase.initialize_app(config)
    db = firebase.database()

    def query(sql, val=""):
        mydb = mysql.connector.connect(
            host="35.221.107.80",
            user="peaga",
            passwd="Ltk99701299",
            database="HutechManagement",
            auth_plugin="mysql_native_password"
        )
        mycursor = mydb.cursor()
        mycursor.execute(sql, val)
        results = mycursor.fetchall()
        return results


class Profile():

    def getProfile():
        faces = []
        ids = []
        names = []
        images = []
        sql_string = ("select Encoding, Employee_id, CONCAT(FirstName,' ',LastName), Image " +
                      "from HutechManagement.employeesmanagement_faceencoding encode, HutechManagement.employeesmanagement_employee employee " +
                      "where encode.Employee_id = employee.EmployeeId")
        Employees = Database.query(sql_string)
        for Employee in Employees:
            FaceDecode = ''.join(Employee[0])
            Face = np.fromstring(FaceDecode[1:-1], dtype=float, sep=",")
            faces.append(Face)
            ids.append(Employee[1])
            names.append(Employee[2])
            images.append(Employee[3])
        return(faces, ids, names, images)


class FaceRecognize():
    checkinImageName = ""
    previous_id = ""

    def detectMTCNN(detector, frame):
        # Input frame
        # Detect face using MTCNN
        # Return face location
        face_locations = []
        face = detector.detect_faces(frame)
        if len(face) > 0:
            bounding_box = face[0]['box']
            top = bounding_box[1]
            right = bounding_box[0]+bounding_box[2]
            bottom = bounding_box[1] + bounding_box[3]
            left = bounding_box[0]
            face_locations.append((top, right, bottom, left))
        return face_locations

    def detectHOG(frame):
        # Input frame
        # Detect face using HOG
        # Return face location
        face_locations = []
        face_locations = face_recognition.face_locations(frame, 1, "hog")
        return face_locations

    def faceRecognize(model="MTCNN"):
        video_capture = cv2.VideoCapture(0)
        Known_encodings = Profile.getProfile()[0]
        Known_ids = Profile.getProfile()[1]
        Known_names = Profile.getProfile()[2]
        Known_images = Profile.getProfile()[3]
        detector = MTCNN()
        while True:
            employee_id = ""
            employee_name = ""
            employee_image = ""
            data = []
            process_this_frame = True
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, :: -1]
            if process_this_frame:
                if model == "MTCNN":
                    face_locations = FaceRecognize.detectMTCNN(
                        detector, rgb_small_frame)
                elif model == "HOG":
                    face_locations = FaceRecognize.detectHOG(rgb_small_frame)
                face_encodings = face_recognition.face_encodings(
                    rgb_small_frame, face_locations)
                if not face_encodings and FaceRecognize.previous_id != "":
                    Interactive.resetData()
                for face_encoding in face_encodings:
                    matches = face_recognition.compare_faces(
                        Known_encodings, face_encoding, tolerance=0.4)
                    face_distances = face_recognition.face_distance(
                        Known_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        employee_id = Known_ids[best_match_index]
                        employee_name = Known_names[best_match_index]
                        employee_image = Known_images[best_match_index]
                if employee_id != "" and FaceRecognize.previous_id == "":
                    FaceRecognize.checkinImageName = str(
                        (datetime.now()).strftime("%Y%m%d%H%M%S"))+".png"
                    cv2.imwrite("./media/%s" %
                                FaceRecognize.checkinImageName, frame)
                    data = [employee_id, employee_name,
                            employee_image, FaceRecognize.checkinImageName]
                    Interactive.streamToFrontend(data)
                for (top, right, bottom, left) in (face_locations):
                    top *= 4
                    right *= 4
                    bottom *= 4
                    left *= 4
                    text_x = left
                    text_y = bottom+20
                    cv2.rectangle(frame, (left, top),
                                  (right, bottom), (0, 255, 0), 2)
            cv2.imwrite('./media/stream.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open('./media/stream.jpg', 'rb').read() + b'\r\n')


class Interactive():
    def video_feed(request):
        return StreamingHttpResponse(FaceRecognize.faceRecognize("HOG"), content_type='multipart/x-mixed-replace; boundary=frame')

    def streamToFrontend(data):
        checkinTime = str((datetime.now()).strftime("%Y-%m-%d %H:%M"))
        dataToStream = {
            "CheckinImage": data[3],
            "CheckinTime": checkinTime,
            "EmployeeID": data[0],
            "EmployeeName": data[1],
            "ProfileImage": data[2]
        }
        Database.db.child("EmployeeAttendance").update(dataToStream)
        FaceRecognize.previous_id = data[0]

    def resetData():
        checkinImage = FaceRecognize.checkinImageName
        os.remove("./media/%s" % checkinImage)
        FaceRecognize.checkinImageName = ""
        data = {
            "CheckinImage": "face-approved.jpg",
            "CheckinTime": "",
            "EmployeeID": "",
            "EmployeeName": "",
            "ProfileImage": "face-recognition.jpg"
        }
        Database.db.child("EmployeeAttendance").update(data)
        FaceRecognize.previous_id = ""

    @api_view(['POST'])
    def clearResult(request):
        if FaceRecognize.previous_id != "":
            Interactive.resetData()
        return Response()
