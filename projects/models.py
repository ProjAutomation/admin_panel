from django.db import models
from django.template.defaultfilters import date as _date


from accounts.models import DevmanUser, Level


class Brief(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name='Название')
    description = models.TextField(
        verbose_name='Описание проекта'
    )
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name='briefs'
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
        related_name='streams',
    )
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.brief} {_date(self.start_date, "d.m")}—{_date(self.end_date, "d.m")}'

    class Meta:
        verbose_name = 'Поток'
        verbose_name_plural = 'Потоки'


class Project(models.Model):
    manager = models.ForeignKey(
        DevmanUser,
        on_delete=models.CASCADE,
        related_name='managed_projects'
    )
    stream = models.ForeignKey(
        TrainingStream,
        on_delete=models.CASCADE,
        related_name='streams'
    )
    meeting_start_time = models.TimeField()

    def __str__(self):
        return (f'Поток {self.stream}, менеджер {self.manager.username},'
                f'начало созвона {self.meeting_start_time}')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class ProjectStudent(models.Model):
    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
        related_name='projects'
    )
    student = models.ForeignKey(
        DevmanUser,
        on_delete=models.CASCADE,
        related_name='students'
    )

    def __str__(self):
        return (
            f'Студент {self.student.username}'
            f'участвует в проекте {self.project}')

    class Meta:
        verbose_name = 'Участие студента в проекте'
        verbose_name_plural = 'Участие студента в проектах'


class MeetingsTimeSlot(models.Model):
    training_stream = models.ForeignKey(
        TrainingStream,
        on_delete=models.CASCADE,
        related_name='time_slots'
    )
    manager = models.ForeignKey(
        DevmanUser,
        on_delete=models.CASCADE,
        related_name='time_slots'
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return (f'Поток {self.training_stream}, созвоны с '
                f'{self.start_time} до {self.end_time}')

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
        DevmanUser,
        on_delete=models.CASCADE,
        related_name='meetings_time_slot'
    )

    def __str__(self):
        return (
            f'{self.student.username} участвует в'
            f'созвоне в {self.meetings_time_slot}')

    class Meta:
        verbose_name = 'Тайм-слот встреч пользователя'
        verbose_name_plural = 'Тайм-слоты встреч пользователя'
