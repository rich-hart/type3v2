# Generated by Django 3.0.7 on 2020-06-26 00:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentBinaryClassification',
            fields=[
                ('job_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='jobs.Job')),
            ],
            options={
                'abstract': False,
            },
            bases=('jobs.job',),
        ),
    ]
