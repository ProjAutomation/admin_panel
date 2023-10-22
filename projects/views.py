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
from django.core.exceptions import BadRequest


from .forms import InvitationForm
from .models import TrainingStream, MeetingsTimeSlot, Project, ProjectStudent


logger = logging.getLogger(__name__)


def home(request):
    return render(request, 'index.html')


@require_http_methods(['GET', 'POST'])
@login_required
def select_slot(request, stream_pk):
    stream = get_object_or_404(TrainingStream, pk=stream_pk)
    student = request.user

    stream_projects = Project.objects.filter(
        stream=stream,
        students__pk__exact=student.pk
    )
    if stream_projects:
        raise BadRequest(f"Student {student.username} already registered for a project")

    meeting_time_slots = MeetingsTimeSlot.objects.filter(
        training_stream=stream)
    time_intervals = []
    context = {
        'project_title': stream.brief.title,
        'start_date': stream.start_date,
        'end_date': stream.end_date,
    }

    t = datetime.min
    for slot in meeting_time_slots:
        current = timedelta(hours=slot.start_time.hour,
                            minutes=slot.start_time.minute)
        final = timedelta(hours=slot.end_time.hour,
                          minutes=slot.end_time.minute)
        while current < final:
            interval = {}

            interval['start'] = (t+current).time()
            interval['manager_id'] = slot.manager.pk

            current += timedelta(minutes=30)
            interval['end'] = (t+current).time()

            time_intervals.append(interval)
    context['slots'] = time_intervals

    if request.method == 'POST':
        data = request.POST.get('project_meeting_time', '')
        [meeting_start_time, manager_id] = data.split(',')

        if meeting_start_time and manager_id:
            manager = get_object_or_404(get_user_model(), pk=manager_id)

            project, is_created = Project.objects.get_or_create(
                manager=manager,
                stream=stream,
                meeting_start_time=meeting_start_time
            )

            students_on_project_limit = 3

            occupied_students = project.students.all()
            if is_created or len(occupied_students) < students_on_project_limit:
                print(f'Project exists with less than {students_on_project_limit} students.')
                ProjectStudent.objects.create(
                    student=student,
                    project=project
                )
            else:
                print('Create new project.')
                new_project = Project.objects.create(
                    manager=manager,
                    stream=stream,
                    meeting_start_time=meeting_start_time
                )
                ProjectStudent.objects.create(
                    student=student,
                    project=new_project
                )

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

            stream_projects = Project.objects.filter(stream=stream)
            occupied_students_ids = ProjectStudent.objects.filter(
                project__in=stream_projects).values('student_id')
            students = get_user_model().objects.filter(
                level=level).exclude(id__in=occupied_students_ids)

            invite_students(request, students, stream)
    context = {'form': form}
    return render(request, 'setup.html', context=context)


def invite_students(request, students, stream):
    subj = 'Приглашение на проект Devman'
    body = render_to_string(
        'project_invitation_email.txt',
        context={
            'slots_url': request.build_absolute_uri(
                reverse('projects.slots', args=[stream.pk])
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
