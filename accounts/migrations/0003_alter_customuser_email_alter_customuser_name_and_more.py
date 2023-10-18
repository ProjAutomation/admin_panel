# Generated by Django 4.2.6 on 2023-10-18 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0002_customuser_from_far_east_customuser_name_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="email",
            field=models.EmailField(
                max_length=254, unique=True, verbose_name="Электронный адрес"
            ),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="name",
            field=models.CharField(max_length=200, verbose_name="Имя"),
        ),
        migrations.AlterField(
            model_name="customuser",
            name="surname",
            field=models.CharField(max_length=200, verbose_name="Фамилия"),
        ),
    ]
