# Generated by Django 3.2.16 on 2023-12-07 18:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_alter_student_user'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='response',
            unique_together={('student', 'question')},
        ),
    ]
