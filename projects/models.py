from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.models import CustomUser


class ProjectManager(AbstractUser):
    name = models.CharField(
        max_length=200,
        verbose_name='Имя')
    surname = models.CharField(
        max_length=200,
        verbose_name='Фамилия')
    email = models.EmailField(
        max_length=254,
        verbose_name='Электронный адрес',
        unique=True)
    telegram = models.CharField(
        max_length=200,
        verbose_name='Телеграмм')
    start_from = models.TimeField(
        verbose_name='Начало рабочего дня')
    end_from = models.TimeField(
        verbose_name='Конец рабочего дня'
    )
    groups = None
    user_permissions = None

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        verbose_name = 'Проджект менеджер'
        verbose_name_plural = 'Проджект менеджеры'


class TimeSlot(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_occupied = models.BooleanField(default=False)
    project_manager = models.ForeignKey(
        ProjectManager,
        on_delete=models.CASCADE,
        related_name='timeslots'
    )

    def __str__(self):
        return f'{self.start_time} - {self.end_time}'

    def is_available(self):
        return not self.is_occupied

    class Meta:
        verbose_name = 'Тайм-слот'
        verbose_name_plural = 'Тайм-слоты'


class Team(models.Model):
    members = models.ManyToManyField(
        CustomUser,
        related_name='teams',
        verbose_name='Члены команды'
    )
    time_slot = models.ForeignKey(
        TimeSlot,
        on_delete=models.CASCADE,
        related_name='team',
        verbose_name='Тайм-слот'
    )
    project_manager = models.ForeignKey(
        ProjectManager,
        on_delete=models.CASCADE,
        related_name='teams_managed',
        verbose_name='Проджект менеджер'
    )

    def __str__(self):
        return f'Team - PM: {self.project_manager}, Slot: {self.time_slot}'

    class Meta:
        verbose_name = 'Команда'
        verbose_name_plural = 'Команды'


class Membership(models.Model):
    member = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        verbose_name='Участник')
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        verbose_name='Команда')
    prefers_teammates = models.ManyToManyField(
        CustomUser,
        related_name='preferred_teammates',
        blank=True,
        null=True,
        verbose_name='Предпочитаемый тиммейт')
    not_prefers_teammates = models.ManyToManyField(
        CustomUser,
        related_name='non_preferred_teammates',
        blank=True,
        null=True,
        verbose_name='Непредпочтительный тиммейт')
    prefers_project_manager = models.ForeignKey(
        ProjectManager,
        related_name='preferred_project_manager',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Предпочитаемый ПМ')
    not_prefers_project_manager = models.ForeignKey(
        'ProjectManager',
        related_name='non_preferred_project_manager',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Непредпочтительный ПМ')

    class Meta:
        verbose_name = 'Участие в команде'
        verbose_name_plural = 'Участие в команде'
