# Generated by Django 5.1.1 on 2024-09-09 07:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='file_name',
        ),
    ]
