from rest_framework import viewsets, permissions
# models
from employeesmanagement.models import Department
from employeesmanagement.models import Employee
from employeesmanagement.models import Attendance
from employeesmanagement.models import Location
from employeesmanagement.models import FaceEncoding
# serializers
from employeesmanagement.serializers import DepartmentSerializers
from employeesmanagement.serializers import EmployeeSerializers
from employeesmanagement.serializers import AttendanceSerializers
from employeesmanagement.serializers import LocationSerializers
from employeesmanagement.serializers import FaceEncodingSerializers


class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = DepartmentSerializers


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = EmployeeSerializers


class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = AttendanceSerializers


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = LocationSerializers


class FaceEncodingViewSet(viewsets.ModelViewSet):
    queryset = FaceEncoding.objects.all()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = FaceEncodingSerializers
