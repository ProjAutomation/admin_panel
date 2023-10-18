from django.contrib import admin

from .models import ProjectManager, Team, TimeSlot


admin.site.register(ProjectManager)
admin.site.register(Team)
admin.site.register(TimeSlot)
