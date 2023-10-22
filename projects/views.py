from datetime import time, timedelta, datetime
import logging

from django.shortcuts import render, redirect, get_object_or_404

from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mass_mail
from django.template.loader import render_to_string
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .forms import InvitationForm
from .models import TrainingStream, MeetingsTimeSlot, Project, ProjectStudent


logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'index.html')


@require_http_methods(['GET', 'POST'])
@login_required
def select_slot(request, stream_pk):
    meeting_time_slots = MeetingsTimeSlot.objects.filter(
        training_stream__pk=stream_pk)
    time_intervals = []

    t = datetime.min
    for meeting_start_time in meeting_time_slots:
        current = timedelta(hours=meeting_start_time.start_time.hour,
                            minutes=meeting_start_time.start_time.minute)
        final = timedelta(hours=meeting_start_time.end_time.hour,
                          minutes=meeting_start_time.end_time.minute)
        while current < final:
            interval = {}

            interval['start'] = (t+current).time()

            current += timedelta(minutes=30)
            interval['end'] = (t+current).time()

            time_intervals.append(interval)

    if request.method == 'POST':
        meeting_start_time = request.POST.get('project_meeting_time', '')
        context = {}
        if meeting_start_time:
            student = request.user

            # TODO: Fake data! Use real.
            # ...............
            project = Project.objects.create(
                manager_id=1,
                stream_id=1,
                meeting_start_time=meeting_start_time
            )
            ProjectStudent.objects.create(
                student=student,
                project=project
            )
            # ...............

            messages.add_message(
                request, messages.SUCCESS,
                f"Вы добавлены в проект со временем созвона {meeting_start_time}.",
                extra_tags='alert alert-success'
            )
        else:
            messages.add_message(
                request, messages.ERROR,
                "Время созвона не выбрано, мы напишем вам в Телеграм для уточнения.",
                extra_tags='alert alert-warning'
            )
    else:
        context = {
            'slots':  time_intervals
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
            invite_students(request, students, stream.pk)
    context = {'form': form}
    return render(request, 'setup.html', context=context)


def invite_students(request, students, stream_pk):
    subj = 'Приглашение на проект Devman'
    body = render_to_string(
        'project_invitation_email.txt',
        context={
            'slots_url': request.build_absolute_uri(
                reverse('projects.slots', args=[stream_pk])
            )
        }
    )
    sender_email = settings.EMAIL_SENDER
    email_letters = []
    email_addresses = []
    for student in students:
        if not student.email:
            continue
        email_addresses.append(student.email)
        email_letter = (subj, body, sender_email, [student.email])
        email_letters.append(email_letter)
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
