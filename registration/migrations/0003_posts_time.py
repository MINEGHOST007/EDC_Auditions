# Generated by Django 3.2.16 on 2023-12-27 21:30

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20231225_1343'),
    ]

    operations = [
        migrations.AddField(
            model_name='posts',
            name='time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
