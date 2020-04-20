from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
# models
from employeesmanagement.models import Department
from employeesmanagement.models import Employee
from employeesmanagement.models import Attendance
from employeesmanagement.models import Location
from employeesmanagement.models import FaceEncoding


class DepartmentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class EmployeeSerializers(serializers.ModelSerializer):
    DepartmentName = serializers.StringRelatedField(source="Department")
    Image = Base64ImageField(required=False)

    class Meta:
        model = Employee
        fields = "__all__"


class AttendanceSerializers(serializers.ModelSerializer):
    EmployeeName = serializers.StringRelatedField(
        read_only=True, source="Employee")
    Location = serializers.StringRelatedField()

    class Meta:
        model = Attendance
        fields = "__all__"


class LocationSerializers(serializers.ModelSerializer):

    class Meta:
        model = Location
        fields = "__all__"


class FaceEncodingSerializers(serializers.ModelSerializer):

    class Meta:
        model = FaceEncoding
        fields = "__all__"
