from django.contrib.auth.models import AbstractUser
from django.db import models


class Level(models.Model):
    title = models.CharField(
        max_length=128,
        verbose_name='Уровень студента')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Уровень знаний'
        verbose_name_plural = 'Уровни знаний'


class DevmanUser(AbstractUser):
    telegram_username = models.CharField(
        max_length=200,
        verbose_name='Аккаунт в телеграмме', blank=True)
    timezone = models.CharField(
        max_length=63,
        verbose_name='Часовой пояс', blank=True)
    level = models.ForeignKey(
        Level,
        on_delete=models.CASCADE,
        related_name='students',
        null=True
    )

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


class UserAvoidance(models.Model):
    user = models.ForeignKey(
        DevmanUser,
        on_delete=models.CASCADE,
        related_name='avoiding_user'
    )
    avoided_user = models.ForeignKey(
        DevmanUser,
        on_delete=models.CASCADE,
        related_name='avoided_user'
    )

    def __str__(self):
        return f"{self.user} avoids {self.avoided_user.username}"

    class Meta:
        verbose_name = 'Нежелательный тиммейт'
        verbose_name_plural = 'Нежелательные тиммейты'


class UserPreference(models.Model):
    user = models.ForeignKey(
        DevmanUser,
        on_delete=models.CASCADE,
        related_name='preferring_user')
    preferred_user = models.ForeignKey(
        DevmanUser,
        on_delete=models.CASCADE,
        related_name='preferred_user'
    )

    def __str__(self):
        return f"{self.user.username} prefers {self.preferred_user.username}"

    class Meta:
        verbose_name = 'Желательный тиммейт'
        verbose_name_plural = 'Желательные тиммейты'
