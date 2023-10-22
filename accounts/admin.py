from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import DevmanUserCreationForm, DevmanUserChangeForm
from .models import DevmanUser, Level, UserAvoidance
from .models import UserPreference


class UserAvoidanceAdminInline(admin.StackedInline):
    model = UserAvoidance
    fk_name = 'user'
    extra = 0
    autocomplete_fields = ['avoided_user']
    verbose_name_plural = '🛑 Не хочет работать с'
    verbose_name = 'Нежелательный юзер'


class UserPreferenceAdminInline(admin.StackedInline):
    model = UserPreference
    fk_name = 'user'
    extra = 0
    autocomplete_fields = ['preferred_user']
    verbose_name = 'Предпочтительный юзер'
    verbose_name_plural = '🤝 Хочет работать с'


class DevmanUserAdmin(UserAdmin):
    add_form = DevmanUserCreationForm
    form = DevmanUserChangeForm
    model = DevmanUser
    list_display = [
        "username",
        "email",
        "is_staff",
    ]
    fieldsets = UserAdmin.fieldsets
    add_fieldsets = UserAdmin.add_fieldsets
    inlines = [UserAvoidanceAdminInline, UserPreferenceAdminInline]


admin.site.register(DevmanUser, DevmanUserAdmin)
admin.site.register(Level)
