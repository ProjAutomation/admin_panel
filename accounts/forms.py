from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import DevmanUser


class DevmanUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = DevmanUser
        fields = UserCreationForm.Meta.fields


class DevmanUserChangeForm(UserChangeForm):
    class Meta:
        model = DevmanUser
        fields = UserChangeForm.Meta.fields
