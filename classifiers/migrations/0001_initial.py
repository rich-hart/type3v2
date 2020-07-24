# Generated by Django 3.0.8 on 2020-07-24 17:20

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tools', '0001_initial'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classifier',
            fields=[
                ('tool_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tools.Tool')),
                ('samples', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('tools.tool',),
        ),
        migrations.CreateModel(
            name='ML',
            fields=[
                ('classifier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='classifiers.Classifier')),
            ],
            options={
                'abstract': False,
            },
            bases=('classifiers.classifier',),
        ),
        migrations.CreateModel(
            name='Random',
            fields=[
                ('classifier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='classifiers.Classifier')),
            ],
            options={
                'abstract': False,
            },
            bases=('classifiers.classifier',),
        ),
        migrations.CreateModel(
            name='SVM',
            fields=[
                ('classifier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='classifiers.Classifier')),
            ],
            options={
                'abstract': False,
            },
            bases=('classifiers.classifier',),
        ),
        migrations.CreateModel(
            name='Human',
            fields=[
                ('classifier_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='classifiers.Classifier')),
                ('profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='users.Profile')),
            ],
            options={
                'abstract': False,
            },
            bases=('classifiers.classifier',),
        ),
    ]
