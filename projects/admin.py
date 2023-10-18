from django import forms
from django.contrib import admin

from accounts.models import CustomUser
from .models import ProjectManager, Team, TimeSlot


admin.site.register(ProjectManager)
admin.site.register(TimeSlot)


class TeamAdminForm(forms.ModelForm):
    members = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Team
        fields = '__all__'


class TeamAdmin(admin.ModelAdmin):
    form = TeamAdminForm
    list_display = ['project_manager', 'time_slot', 'list_members']

    def list_members(self, obj):
        return ", ".join(
            [f'{member.name} {member.surname}' for member in obj.members.all()]
            )

    list_members.short_description = "Члены команды"


admin.site.register(Team, TeamAdmin)
