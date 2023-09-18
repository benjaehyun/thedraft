# Generated by Django 4.2.5 on 2023-09-18 18:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main_app', '0006_company'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
        migrations.AddField(
            model_name='post',
            name='user',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
