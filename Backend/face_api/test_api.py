import face_recognition
import cv2
import numpy as np

Image = face_recognition.load_image_file(
    "D:/Hutech_Management/Backend/media/images/profile/1711062340/29b044d1-fe40-430d-9419-92e75c1cb6be.png")
FaceLocation = face_recognition.face_locations(Image, 1, "hog")
Encoding = face_recognition.face_encodings(Image, FaceLocation)[0]
StrFaceEncodeing = np.array2string(Encoding, separator=',')

ListDimension = []
for Dimension in Encoding:
    ListDimension.append(Dimension)
str1 = ', '.join(str(e) for e in ListDimension)
print(str1)
print(type(str1))
