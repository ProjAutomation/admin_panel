# Generated by Django 4.2.6 on 2023-10-18 16:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("projects", "0005_remove_team_member_team_members"),
    ]

    operations = [
        migrations.AlterField(
            model_name="team",
            name="members",
            field=models.ManyToManyField(
                related_name="teams",
                to=settings.AUTH_USER_MODEL,
                verbose_name="Члены команды",
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="project_manager",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="teams_managed",
                to="projects.projectmanager",
                verbose_name="Проджект менеджер",
            ),
        ),
        migrations.AlterField(
            model_name="team",
            name="time_slot",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="team",
                to="projects.timeslot",
                verbose_name="Тайм-слот",
            ),
        ),
        migrations.CreateModel(
            name="Membership",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "not_prefers_project_manager",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="non_preferred_project_manager",
                        to="projects.projectmanager",
                    ),
                ),
                (
                    "not_prefers_teammates",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        related_name="non_preferred_teammates",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "prefers_project_manager",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="preferred_project_manager",
                        to="projects.projectmanager",
                    ),
                ),
                (
                    "prefers_teammates",
                    models.ManyToManyField(
                        blank=True,
                        null=True,
                        related_name="preferred_teammates",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "team",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="projects.team"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
