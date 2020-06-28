# Generated by Django 3.0.7 on 2020-06-28 03:02

from django.db import migrations, models
import django.db.models.deletion
import jobs.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('tag', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', models.CharField(choices=[(0, jobs.models.Job.Status['UNKNOWN']), (1, jobs.models.Job.Status['CREATED']), (2, jobs.models.Job.Status['PENDING']), (3, jobs.models.Job.Status['STARTED']), (4, jobs.models.Job.Status['COMPLETE'])], default='UN', max_length=2)),
                ('owner', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.Profile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProgressReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('tag', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('metric', models.FloatField()),
                ('error', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Classification',
            fields=[
                ('job_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='jobs.Job')),
            ],
            options={
                'abstract': False,
            },
            bases=('jobs.job',),
        ),
    ]
