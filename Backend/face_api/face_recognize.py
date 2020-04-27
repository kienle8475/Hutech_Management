import os
import cv2
import time
import pyrebase
import numpy as np
import mysql.connector
from mtcnn import MTCNN
import face_recognition
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

    def detect_mtcnn():
        # Capture
        video_capture = cv2.VideoCapture(0)
        detector = MTCNN()
        Known_encodings = Profile.getProfile()[0]
        Known_ids = Profile.getProfile()[1]
        Known_names = Profile.getProfile()[2]
        Known_images = Profile.getProfile()[3]
        # Process Frame
        id_process = ""
        while True:
            process_this_frame = True
            ret, frame = video_capture.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
            rgb_small_frame = small_frame[:, :, ::-1]
            face_locations = []
            if process_this_frame:
                face = detector.detect_faces(rgb_small_frame)
                if len(face) > 0:
                    bounding_box = face[0]['box']
                    face_locations.append(
                        (bounding_box[1], (bounding_box[0]+bounding_box[2]), (bounding_box[1] + bounding_box[3]), bounding_box[0]))
                    face_encodings = face_recognition.face_encodings(
                        rgb_small_frame, face_locations)
                    for face_encoding in face_encodings:
                        ename = ""
                        eid = ""
                        eimage = ""
                        matches = face_recognition.compare_faces(
                            Known_encodings, face_encoding, tolerance=0.4)
                        face_distances = face_recognition.face_distance(
                            Known_encodings, face_encoding)
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            eid = Known_ids[best_match_index]
                            ename = Known_names[best_match_index]
                            eimage = Known_images[best_match_index]
                        if eid != id_process and eid != "":
                            checkinImageName = str(
                                (datetime.now()).strftime("%Y%m%d%H%M%S"))+".png"
                            checkinTime = str(
                                (datetime.now()).strftime("%Y-%m-%d %H:%M"))
                            cv2.imwrite("./media/%s" %
                                        checkinImageName, rgb_small_frame)
                            data = {
                                "CheckinImage": checkinImageName,
                                "CheckinTime": checkinTime,
                                "EmployeeID": eid,
                                "EmployeeName": ename,
                                "ProfileImage": eimage
                            }
                            Database.db.child(
                                "EmployeeAttendance").update(data)
                        id_process = (Database.db.child(
                            "EmployeeAttendance").child("EmployeeID").get()).val()
            cv2.imwrite('./media/stream.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open('./media/stream.jpg', 'rb').read() + b'\r\n')

    def detect_hog():
        # Capture
        video_capture = cv2.VideoCapture(0)
        Known_encodings = Profile.getProfile()[0]
        Known_ids = Profile.getProfile()[1]
        Known_names = Profile.getProfile()[2]
        Known_images = Profile.getProfile()[3]
        # Process Frame
        id_process = ""
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
                    ename = ""
                    eid = ""
                    eimage = ""
                    matches = face_recognition.compare_faces(
                        known_encodings, face_encoding, tolerance=0.4)
                    face_distances = face_recognition.face_distance(
                        known_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        eid = known_ids[best_match_index]
                        ename = known_names[best_match_index]
                        eimage = Known_images[best_match_index]
                    if eid != id_process and eid != "":
                        checkinImageName = str(
                            (datetime.now()).strftime("%Y%m%d%H%M%S"))+".png"
                        checkinTime = str(
                            (datetime.now()).strftime("%Y-%m-%d %H:%M"))
                        cv2.imwrite("./media/%s" %
                                    checkinImageName, rgb_small_frame)
                        data = {
                            "CheckinImage": checkinImageName,
                            "CheckinTime": checkinTime,
                            "EmployeeID": eid,
                            "EmployeeName": ename,
                            "ProfileImage": eimage
                        }
                        GetProfileInfo.db.child(
                            "EmployeeAttendance").update(data)
                    id_process = (GetProfileInfo.db.child(
                        "EmployeeAttendance").child("EmployeeID").get()).val()
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
        return StreamingHttpResponse(FaceRecognize.detect_hog(), content_type='multipart/x-mixed-replace; boundary=frame')

    @api_view(['POST'])
    def clearResult(request):
        checkinImage = (Database.db.child(
            "EmployeeAttendance").child("CheckinImage").get()).val()
        os.remove("./media/%s" % checkinImage)
        data = {
            "CheckinImage": "face-approved.png",
            "CheckinTime": "",
            "EmployeeID": "",
            "EmployeeName": "",
            "ProfileImage": "face-recognition.jpg"
        }
        Database.db.child("EmployeeAttendance").update(data)
        return Response()
