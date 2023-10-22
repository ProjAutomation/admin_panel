from django.contrib import admin

from .models import Brief, TrainingStream, MeetingsTimeSlot, Project, \
    ProjectStudent, MeetingsTimeSlotUser


@admin.register(Brief)
class BriefAdmin(admin.ModelAdmin):
    list_display = ['title', 'level']


@admin.register(TrainingStream)
class TrainingStreamAdmin(admin.ModelAdmin):
    list_display = ['brief', 'start_date', 'end_date']


@admin.register(MeetingsTimeSlot)
class MeetingsTimeSlotStreamAdmin(admin.ModelAdmin):
    list_display = ['training_stream', 'start_time', 'end_time']


class ProjectStudentAdminInline(admin.StackedInline):
    model = ProjectStudent
    extra = 0
    autocomplete_fields = ['student']
    verbose_name = 'Студент'
    verbose_name_plural = 'Студенты'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['stream', 'manager', 'meeting_start_time']
    inlines = [ProjectStudentAdminInline]
