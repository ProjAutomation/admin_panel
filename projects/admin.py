from django.contrib import admin

from .models import Brief, Project, MeetingsTimeSlot, MeetingsTimeSlotUser
from .models import ProjectStudent, TrainingStream


admin.site.register(Brief)
admin.site.register(Project)
admin.site.register(TrainingStream)
admin.site.register(ProjectStudent)
admin.site.register(MeetingsTimeSlot)
admin.site.register(MeetingsTimeSlotUser)
