from django.contrib import admin
from django.urls import path
from face_api.face_compare import FaceCompare
from face_api.face_recognize import Interactive
urlpatterns = [
    #path('video_feed_compare/', FaceCompare.video_feed),
    path('video_feed_recognize/', Interactive.video_feed),
    path('api/clear_result', Interactive.clearResult)
]
