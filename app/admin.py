from django.contrib import admin

from .models import *

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(ClassRoom)
admin.site.register(Subjects)
admin.site.register(StudentSubject)
