# Generated by Django 3.2.16 on 2024-01-10 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20240110_1558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='result',
            name='domain',
        ),
    ]