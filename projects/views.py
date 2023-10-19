from datetime import time
import logging

from django.shortcuts import render, redirect
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.decorators.http import require_http_methods


logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'index.html')


@require_http_methods(['GET', 'POST'])
def slots(request):
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


@require_http_methods(['GET'])
def setup(request):
    return render(request, 'setup.html')


@require_http_methods(['POST'])
def invite(request):
    subj = 'Приглашение на проект Devman'
    body = render_to_string(
        'project_invitation_email.txt',
        context={
            'slots_url': request.build_absolute_uri(reverse('projects.slots'))
        }
    )
    sender_email = settings.EMAIL_SENDER
    student_addresses = request.POST.get('emails', '').split(',')
    emails = []
    for student_addr in student_addresses:
        email = (subj, body, sender_email, [student_addr])
        emails.append(email)
    try:
        send_mass_mail(emails)
        messages.add_message(request, messages.SUCCESS, "Приглашения отправлены!",
                             extra_tags='alert alert-success')
    except Exception as e:
        logger.error(e)
        messages.add_message(request, messages.ERROR,
                             "Ошибка при отправке приглашений.",
                             extra_tags='alert alert-danger')
    return redirect('projects.setup')
