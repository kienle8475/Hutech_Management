import os
import cv2
import time
import pyrebase
import numpy as np
import mysql.connector
import face_recognition
from datetime import datetime
from django.http import StreamingHttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view


class GetProfileInfo():
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

    def getEncode():
        face_encodings = []
        face_ids = []
        face_names = []
        sql_getFace = "SELECT Encoding FROM employeesmanagement_faceencoding ORDER BY Employee_id"
        sql_getId = "SELECT Employee_id FROM employeesmanagement_faceencoding ORDER BY Employee_id"
        sql_getName = "SELECT CONCAT(FirstName,LastName) FROM HutechManagement.employeesmanagement_employee"
        FaceEncodes = GetProfileInfo.query(sql_getFace)
        for FaceEncode in FaceEncodes:
            FaceDecode = ''.join(FaceEncode)
            Face = np.fromstring(FaceDecode[1:-1], dtype=float, sep=",")
            face_encodings.append(Face)
        FaceIds = GetProfileInfo.query(sql_getId)
        for FaceId in FaceIds:
            face_ids.append(FaceId[0])
        FaceNames = GetProfileInfo.query(sql_getName)
        for FaceName in FaceNames:
            face_names.append(FaceName[0])
        return (face_encodings, face_ids, face_names)

    def getProfileImage(val):
        value = (val,)
        sql_getImage = "SELECT Image FROM HutechManagement.employeesmanagement_employee where EmployeeId = %s"
        ProfileImages = GetProfileInfo.query(sql_getImage, value)
        for profileImage in ProfileImages:
            image = profileImage[0]
        return image


class FaceRecognize():

    def detect():
        # Capture
        video_capture = cv2.VideoCapture(0)
        # Known
        known_face_encodings = GetProfileInfo.getEncode()[0]
        known_face_ids = GetProfileInfo.getEncode()[1]
        known_face_names = GetProfileInfo.getEncode()[2]
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
                    matches = face_recognition.compare_faces(
                        known_face_encodings, face_encoding, tolerance=0.4)
                    face_distances = face_recognition.face_distance(
                        known_face_encodings, face_encoding)
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        eid = known_face_ids[best_match_index]
                        ename = known_face_names[best_match_index]
                    if eid != id_process and eid != "":
                        checkinImageName = str(
                            (datetime.now()).strftime("%Y%m%d%H%M%S"))+".png"
                        cv2.imwrite("./media/%s" % checkinImageName, frame)
                        profileImage = GetProfileInfo.getProfileImage(eid)
                        data = {
                            "CheckinImage": checkinImageName,
                            "EmployeeID": eid,
                            "EmployeeName": ename,
                            "ProfileImage": profileImage
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

            cv2.imwrite('stream.jpg', frame)
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + open('stream.jpg', 'rb').read() + b'\r\n')

        #     cv2.imshow('Face Recoginition', frame)
        #     if cv2.waitKey(1) & 0xFF == ord('q'):
        #         break

        # video_capture.release()
        # cv2.destroyAllWindows()


class Interactive():
    def video_feed(request):
        return StreamingHttpResponse(FaceRecognize.detect(), content_type='multipart/x-mixed-replace; boundary=frame')

    @api_view(['POST'])
    def clearResult(request):
        checkinImage = (GetProfileInfo.db.child(
            "EmployeeAttendance").child("CheckinImage").get()).val()
        data = {
            "CheckinImage": "",
            "EmployeeID": "",
            "EmployeeName": "",
            "ProfileImage": ""
        }
        GetProfileInfo.db.child("EmployeeAttendance").update(data)
        os.remove("./media/%s" % checkinImage)
        return Response()


# FaceRecognize.detect()
# id_process = (GetProfileInfo.db.child(
#     "EmployeeAttendance").child("EmployeeID").get()).val()
# print(id_process)
