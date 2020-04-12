# Generated by Django 3.0.4 on 2020-04-12 07:23

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sprints', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True)),
                ('story_points', models.CharField(max_length=200)),
                ('task_name', models.CharField(max_length=80)),
                ('assigned_person', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('sprint', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sprints.Sprint')),
            ],
        ),
    ]
