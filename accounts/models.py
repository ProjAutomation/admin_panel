from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    BEGINNER = 'Новичок'
    BEGINNER_PLUS = 'Новичок+'
    JUNIOR = 'Джун'
    SKILL_CHOICES = [
        (BEGINNER, 'Новичок'),
        (BEGINNER_PLUS, 'Новичок+'),
        (JUNIOR, 'Джун'),
    ]
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
    skill = models.CharField(
        max_length=9,
        choices=SKILL_CHOICES,
        default=BEGINNER)
    from_far_east = models.BooleanField(
        default=False,
        verbose_name='С Дальнего Востока')

    def __str__(self):
        return self.username

    @property
    def is_from_far_east(self):
        return self.from_far_east

    @is_from_far_east.setter
    def is_from_far_east(self, value):

        if self.is_staff:
            self.from_far_east = value
        else:
            raise PermissionError(
                'Only admin users can set "from_far_east" attribute.'
                )
