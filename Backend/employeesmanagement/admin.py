from django.contrib import admin
from employeesmanagement.models import Department
from employeesmanagement.models import Employee
from employeesmanagement.models import Attendance
from employeesmanagement.models import Location
from employeesmanagement.models import FaceEncoding

# Register your models here.

admin.site.register(Department)
admin.site.register(Employee)
admin.site.register(Attendance)
admin.site.register(Location)
admin.site.register(FaceEncoding)


