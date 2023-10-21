# Generated by Django 4.2.6 on 2023-10-21 21:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0007_useravoidance_user_userpreference_user_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("projects", "0006_meetingstimeslotuser"),
    ]

    operations = [
        migrations.RenameField(
            model_name="meetingstimeslotuser",
            old_name="student",
            new_name="user",
        ),
        migrations.AlterField(
            model_name="brief",
            name="level",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="briefs",
                to="accounts.level",
            ),
        ),
        migrations.AlterField(
            model_name="brief",
            name="title",
            field=models.CharField(max_length=128, verbose_name="Название"),
        ),
        migrations.AlterField(
            model_name="meetingstimeslot",
            name="training_stream",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="time_slots",
                to="projects.trainingstream",
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="manager",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="managed_projects",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="project",
            name="stream",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="streams",
                to="projects.trainingstream",
            ),
        ),
        migrations.AlterField(
            model_name="projectstudent",
            name="project",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="students_in_project",
                to="projects.project",
            ),
        ),
        migrations.AlterField(
            model_name="projectstudent",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="participating_projects",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="trainingstream",
            name="brief",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="streams",
                to="projects.brief",
            ),
        ),
    ]
