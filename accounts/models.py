from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    telegram_username = models.CharField(
        max_length=200,
        verbose_name='Аккаунт в телеграмме')
    timezone = models.CharField(
        max_length=63,
        verbose_name='Часовой пояс')

    def __str__(self):
        return self.telegram_username

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

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Level(models.Model):
    title = models.CharField(
        max_length=10,
        verbose_name='Уровень студента')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Уровень знаний'
        verbose_name_plural = 'Уровни знаний'


class StudentLevel(models.Model):
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='student_level'
    )
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name='student_level'
    )

    class Meta:
        verbose_name = 'Уровень студента'
        verbose_name_plural = 'Уровни студентов'


class UserAvoidance(models.Model):
    avoided_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='avoiding_user'
    )

    def __str__(self):
        return self.avoided_user

    class Meta:
        verbose_name = 'Нежелательный тиммейт'
        verbose_name_plural = 'Нежелательные тиммейты'


class UserPreference(models.Model):
    preferred_user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='preferring_user'
    )

    def __str__(self):
        return self.preferred_user

    class Meta:
        verbose_name = 'Желательный тиммейт'
        verbose_name_plural = 'Желательные тиммейты'
