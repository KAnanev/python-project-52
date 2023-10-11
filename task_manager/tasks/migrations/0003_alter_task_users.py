# Generated by Django 4.2.5 on 2023-10-11 10:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tasks', '0002_alter_task_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='users',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, unique=True, verbose_name='Пользователи'),
        ),
    ]
