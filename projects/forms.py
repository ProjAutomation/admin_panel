from django import forms

from .models import TrainingStream


class InvitationForm(forms.Form):
    training_stream = forms.ModelChoiceField(
        label='Учебный поток',
        localize=True,
        queryset=TrainingStream.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
