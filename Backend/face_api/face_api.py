import face_recognition
import cv2
import numpy as np
import base64
import os
import re
import mysql.connector


class ImagePreProcessing:
    def getEmployeeId(data):
        employeeId = data['EmployeeId']
        return employeeId

    def getImage(data):
        # Decode image from base64
        imageEncode = data['Image']
        base64Image = re.sub('^data:image/.+;base64,', '', imageEncode)
        imageDecode = base64.b64decode(base64Image)
        # Save image to temp
        imageString = np.frombuffer(imageDecode, dtype=np.uint8)
        # decode from imageString
        image = cv2.imdecode(imageString, flags=1)
        # Write image
        cv2.imwrite('./media/images/temp.png', image)


class SaveFaceEncode:
    def saveToDatabase(Employee, Encoding):
        mydb = mysql.connector.connect(
            host="35.221.107.80",
            user="peaga",
            passwd="Ltk99701299",
            database="HutechManagement",
            auth_plugin="mysql_native_password"
        )
        mycursor = mydb.cursor()
        sql = "INSERT INTO employeesmanagement_faceencoding (Employee_id, Encoding) VALUES (%s, %s)"
        val = (Employee, Encoding)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")


class FaceDetection:
    def encodeFace(data):
        ImagePreProcessing.getImage(data)
        Image = face_recognition.load_image_file("./media/images/temp.png")
        Employee = ImagePreProcessing.getEmployeeId(data)
        FaceLocation = face_recognition.face_locations(Image, 1, "hog")
        Encoding = face_recognition.face_encodings(Image, FaceLocation)[0]
        StrFaceEncodeing = np.array2string(Encoding, separator=',')
        SaveFaceEncode.saveToDatabase(Employee, StrFaceEncodeing)
        os.remove("./media/images/temp.png")
