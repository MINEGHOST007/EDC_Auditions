# Generated by Django 3.2.16 on 2023-12-27 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0003_posts_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posts',
            name='date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='time',
            field=models.DateField(auto_now_add=True),
        ),
    ]