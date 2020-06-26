# Generated by Django 3.0.7 on 2020-06-26 05:58

from django.db import migrations, models
import jobs.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0005_job_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='status',
            field=models.CharField(choices=[('UN', 'UNKNOWN')], default=jobs.models.Job.StatusType['UNKNOWN'], max_length=2),
        ),
    ]
