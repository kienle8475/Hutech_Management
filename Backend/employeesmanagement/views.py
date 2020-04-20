from django.shortcuts import render
from django.http import JsonResponse
# rest_framework
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.decorators import parser_classes
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
# Face API
from face_api.face_api import FaceDetection
# Create your views here.

# Department
@api_view(['GET'])
def List_Department(request):
    department = Department.objects.all()
    serializer = DepartmentSerializers(department, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def Retrieval_Department(request, pk):
    department = Department.objects.get(DepartmentId=pk)
    serializer = DepartmentSerializers(department, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def Create_Department(request):
    serializer = DepartmentSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['POST', 'PUT', 'PATH'])
def Update_Department(request, pk):
    department = Department.objects.get(DepartmentId=pk)
    serializer = DepartmentSerializers(instance=department, data=request.data)
    if serializer.is_valid():
        serializer.save(raise_exception=True)
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['DELETE'])
def Delete_Department(request, pk):
    department = Department.objects.get(DepartmentId=pk)
    department.delete()
    return Response()


# Employee
@api_view(['GET'])
def List_Employee(request):
    employee = Employee.objects.all()
    serializer = EmployeeSerializers(employee, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def Retrieval_Employee(request, pk):
    employee = Employee.objects.get(EmployeeId=pk)
    serializer = EmployeeSerializers(employee, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def Create_Employee(request):
    serializer = EmployeeSerializers(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['POST', 'PUT', 'PATH'])
def Update_Employee(request, pk):
    employee = Employee.objects.get(EmployeeId=pk)
    serializer = EmployeeSerializers(instance=employee, data=request.data)
    if serializer.is_valid():
        serializer.save(raise_exception=True)
        return Response(serializer.data)
    return Response(serializer.errors)


@api_view(['DELETE'])
def Delete_Employee(request, pk):
    employee = Employee.objects.get(EmployeeId=pk)
    employee.delete()
    return Response()

# Attendance
@api_view(['GET'])
def List_Attendance(request):
    attendance = Attendance.objects.all()
    serializer = AttendanceSerializers(attendance, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def Retrieval_Attendance(request, pk):
    attendance = Attendance.objects.get(EmployeeId=pk)
    serializer = Attendance(employee, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
def Delete_Attendance(request, pk):
    attendance = Attendance.objects.get(EmployeeId=pk)
    attendance.delete()
    return Response()

# Location
@api_view(['GET'])
def List_Location(request):
    location = Location.objects.all()
    serializer = LocationSerializers(location, many=True)
    return Response(serializer.data)

# Face API
@api_view(['POST'])
def Encode_Face(request):
    FaceDetection.encodeFace(data= request.data)
    return Response("Image Encoded")