# Generated by Django 4.2.20 on 2025-03-18 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_task_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Choice',
        ),
        migrations.DeleteModel(
            name='Question',
        ),
    ]
