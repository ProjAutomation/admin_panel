from datetime import time
import logging

from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .forms import InvitationForm


logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'index.html')


@require_http_methods(['GET', 'POST'])
@login_required
def slots(request):
    student = request.user
    if request.method == 'POST':
        slot = request.POST.get('slot', '')
        context = {}
        if slot:
            messages.add_message(
                request, messages.SUCCESS,
                f"Вы выбрали слот {slot}, точное время пришлём вам в Телеграмм за день до старта проекта.",
                extra_tags='alert alert-success'
            )
        else:
            messages.add_message(
                request, messages.ERROR,
                "Слот не выбран. Мы напишем вам в Телеграм для уточнения.",
                extra_tags='alert alert-warning'
            )
    else:
        context = {
            'slots': [
                {'start': time(hour=9), 'end': time(hour=13)},
                {'start': time(hour=18), 'end': time(hour=21)},
            ]
        }
    return render(request, 'slots.html', context=context)


@require_http_methods(['GET', 'POST'])
@login_required
def setup(request):
    form = InvitationForm()

    if request.method == 'POST':
        form = InvitationForm(request.POST)
        if form.is_valid():
            stream = form.cleaned_data['training_stream']
            level = stream.brief.level
            students = get_user_model().objects.filter(level=level)
            # TODO: exclude students already added to projects for current
            # `training_stream`
            invite_students(request, students)
    context = {'form': form}
    return render(request, 'setup.html', context=context)


def invite_students(request, students):
    subj = 'Приглашение на проект Devman'
    body = render_to_string(
        'project_invitation_email.txt',
        context={
            # TODO: URL should contain training stream to retrieve time slots
            'slots_url': request.build_absolute_uri(reverse('projects.slots'))
        }
    )
    sender_email = settings.EMAIL_SENDER
    # student_addresses = request.POST.get('emails', '').split(',')
    email_letters = []
    email_addresses = []
    for student in students:
        if not student.email:
            continue
        email_addresses.append(student.email)
        email_letter = (subj, body, sender_email, [student.email])
        email_letters.append(email_letter)
    print(email_letters)
    try:
        send_mass_mail(email_letters)
        msg = "Приглашения отправлены для {}.".format(
            ', '.join(email_addresses))
        messages.add_message(request, messages.SUCCESS, msg,
                             extra_tags='alert alert-success')
    except Exception as e:
        logger.error(e)
        messages.add_message(request, messages.ERROR,
                             "Ошибка при отправке приглашений.",
                             extra_tags='alert alert-danger')
    return redirect('projects.setup')
