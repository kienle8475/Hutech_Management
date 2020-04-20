from django.contrib import admin
from django.urls import path
from face_api.face_compare import FaceCompare
from face_api.face_recognize import FaceRecognize
urlpatterns=[
    path('video_feed_compare/', FaceCompare.video_feed, name="video-feed"),
    path('video_feed_recognize/', FaceRecognize.video_feed, name="video-feed")
]