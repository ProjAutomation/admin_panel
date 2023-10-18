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

    def __str__(self):
        return f'{self.name} {self.surname}'


class TimeSlot(models.Model):
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_occupied = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.start_time} - {self.end_time}'

    def is_available(self):
        return not self.is_occupied


class Team(models.Model):
    member = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='team',
    )
    time_slot = models.OneToOneField(
        TimeSlot,
        on_delete=models.CASCADE,
        related_name='time_slot',
    )
    project_manager = models.ForeignKey(
        ProjectManager,
        on_delete=models.CASCADE,
        related_name='project_manager'
    )
