# Generated by Django 3.0.4 on 2020-04-12 07:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0003_auto_20200404_0907'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='assigned_person',
        ),
        migrations.RemoveField(
            model_name='task',
            name='sprint',
        ),
        migrations.DeleteModel(
            name='Sprint',
        ),
        migrations.DeleteModel(
            name='Task',
        ),
    ]
