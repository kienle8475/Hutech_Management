from django.db import models
from datetime import date
import uuid
# Create your models here.


class Department(models.Model):
    DepartmentId = models.CharField(
        max_length=10, null=False, primary_key=True)
    DepartmentName = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.DepartmentName


def upload_to_profile(instance, filename):
    extension = filename.split(".")[-1]
    return "images/profile/%s/%s.%s" % (instance.EmployeeId, uuid.uuid4(), extension)


class Employee(models.Model):
    EmployeeId = models.CharField(max_length=10, null=False, primary_key=True)
    FirstName = models.CharField(max_length=20, null=False)
    LastName = models.CharField(max_length=50, null=False)
    DateOfBirth = models.DateField()
    Gender_Choice = [('Male', 'Male'), ('Female', 'Female')]
    Gender = models.CharField(max_length=10, choices=Gender_Choice)
    Image = models.ImageField(upload_to=upload_to_profile)
    Email = models.EmailField(null=True, blank=True)
    Phone = models.CharField(max_length=11, null=True, blank=True)
    Department = models.ForeignKey(
        Department, related_name='Department', on_delete=models.SET_NULL, null=True)
    Status_Choice = [('Enable', 'Enable'), ('Disable', 'Disable')]
    Status = models.CharField(
        max_length=10, choices=Status_Choice, default='Enable')

    def __str__(self):
        return str(self.FirstName)+" " + str(self.LastName)


def upload_to_attendance(instance, filename):
    extension = filename.split(".")[-1]
    return "images/attendance/%s/%s-%s.%s" % (instance.Employee.EmployeeId, date.today().strftime("%Y%m"), uuid.uuid4(), extension)


class Location(models.Model):
    LocationName = models.CharField(max_length=50)
    Address = models.CharField(max_length=100)
    Latitude = models.FloatField(null=True, blank=True)
    Longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return str(self.LocationName)


class Attendance(models.Model):
    Employee = models.ForeignKey(
        Employee, related_name='Employee', on_delete=models.CASCADE)
    TimeIn = models.DateTimeField(null=True, blank=True)
    TimeOut = models.DateTimeField(null=True, blank=True)
    ImageIn = models.ImageField(
        upload_to=upload_to_attendance, null=True, blank=True)
    ImageOut = models.ImageField(
        upload_to=upload_to_attendance, null=True, blank=True)
    Location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True)
    Status_Choice = [('Checked In', 'Checked In'),
                     ('Checked Out', 'Checked Out')]
    Status = models.CharField(
        max_length=15, choices=Status_Choice, default='Enable')

    def __str__(self):
        return str(self.Employee) + " - " + str(date.today().strftime("%Y%m"))


class FaceEncoding (models.Model):
    Employee = models.OneToOneField(
        Employee, on_delete=models.CASCADE)
    Encoding = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.Employee)
