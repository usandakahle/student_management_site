from django.contrib import admin
from .models import Unit, User_record, User_unit,Task, Submission

admin.site.register(Unit)
admin.site.register(User_record)
admin.site.register(User_unit)
admin.site.register(Task)
admin.site.register(Submission)