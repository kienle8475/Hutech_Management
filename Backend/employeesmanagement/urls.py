from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path, include
from rest_framework import routers
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token
# API
from .api import DepartmentViewSet
from .api import EmployeeViewSet
from .api import AttendanceViewSet
from .api import LocationViewSet
from .api import FaceEncodingViewSet
# View
from employeesmanagement import views


# Router for API Test - Django Rest ViewSet
router = routers.DefaultRouter()
router.register('department', DepartmentViewSet, 'department')
router.register('employee', EmployeeViewSet, 'employee')
router.register('attendance', AttendanceViewSet, 'attendance')
router.register('location', LocationViewSet, 'location')
router.register('faceencoding', FaceEncodingViewSet, 'faceencoding')

# URL Patterns
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api/auth/token/', obtain_jwt_token),
    path('api/auth/token/refresh/', refresh_jwt_token),

    # Department
    path('api/department/', views.List_Department),
    path('api/department/<str:pk>', views.Retrieval_Department),
    path('api/create-department/', views.Create_Department),
    path('api/update-department/<str:pk>', views.Update_Department),
    path('api/delete-department/<str:pk>', views.Delete_Department),

    # Employee
    path('api/employee/', views.List_Employee),
    path('api/employee/<str:pk>', views.Retrieval_Employee),
    path('api/create-employee/', views.Create_Employee),
    path('api/update-employee/<str:pk>', views.Update_Employee),
    path('api/delete-employee/<str:pk>', views.Delete_Employee),

    # Attendance
    path('api/attendance/', views.List_Attendance),
    path('api/attendance/<str:pk>', views.Retrieval_Attendance),
    path('api/delete-attendance/<str:pk>', views.Delete_Attendance),

    # Attendance
    path('api/location/', views.List_Location),
    path('api/checkin-employee/', views.Save_Checkin_Record),

    # Face API
    path('api/encode-face/', views.Encode_Face)
]
