# Generated by Django 3.0.4 on 2020-05-04 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sprints', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sprint',
            name='planned_story_points',
            field=models.IntegerField(default=0),
        ),
    ]