# from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.models import CustomUser, Level


class Brief(models.Model):
    title = models.CharField(
        max_length=10,
        verbose_name='Название')
    description = models.TextField(
        verbose_name='Описание проекта'
    )
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name='brief'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Бриф'
        verbose_name_plural = 'Брифы'


class TrainingStream(models.Model):
    brief = models.ForeignKey(
        Brief,
        on_delete=models.CASCADE,
        related_name='stream'
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.start_date} - {self.end_date}'

    class Meta:
        verbose_name = 'Поток'
        verbose_name_plural = 'Потоки'


class Project(models.Model):
    manager = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='project'
    )
    stream = models.ForeignKey(
        TrainingStream,
        on_delete=models.CASCADE,
        related_name='project'
    )
    meeting_startime = models.TimeField()

    def __str__(self):
        return (f'Поток {self.stream}, менеджер {self.manager},'
                f'начало созвона {self.meeting_startime}')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class ProjectStudent(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='students'
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='projects'
    )

    def __str__(self):
        return f'Студент {self.student} участвует в проекте {self.project},'

    class Meta:
        verbose_name = 'Участие студента в проекте'
        verbose_name_plural = 'Участие студента в проектах'


class MeetingsTimeSlot(models.Model):
    training_stream = models.ForeignKey(
        TrainingStream,
        on_delete=models.CASCADE,
        related_name='time_slot'
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'Студент {self.student} участвует в проекте {self.project}.'

    class Meta:
        verbose_name = 'Тайм-слот встреч'
        verbose_name_plural = 'Тайм-слоты встреч'


class MeetingsTimeSlotUser(models.Model):
    meetings_time_slot = models.ForeignKey(
        MeetingsTimeSlot,
        on_delete=models.CASCADE,
        related_name='meetings_time_slot'
    )
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='meetings_time_slot'
    )

    def __str__(self):
        return (
            f'Студент {self.student} участвует в'
            f'созвоне в {self.meetings_time_slot}')

    class Meta:
        verbose_name = 'Тайм-слот встреч пользователя'
        verbose_name_plural = 'Тайм-слоты встреч пользователя'
