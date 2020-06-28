# Generated by Django 3.0.7 on 2020-06-28 03:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bases', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FSObject',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bases.Object')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='buckets.FSObject')),
            ],
            options={
                'abstract': False,
            },
            bases=('bases.object',),
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='bases.Object')),
            ],
            options={
                'abstract': False,
            },
            bases=('bases.object',),
        ),
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('fsobject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='buckets.FSObject')),
            ],
            options={
                'abstract': False,
            },
            bases=('buckets.fsobject',),
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('fsobject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='buckets.FSObject')),
            ],
            options={
                'abstract': False,
            },
            bases=('buckets.fsobject',),
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('fsobject_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='buckets.FSObject')),
            ],
            options={
                'abstract': False,
            },
            bases=('buckets.fsobject',),
        ),
        migrations.CreateModel(
            name='Audio',
            fields=[
                ('file_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='buckets.File')),
            ],
            options={
                'abstract': False,
            },
            bases=('buckets.file',),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('file_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='buckets.File')),
            ],
            options={
                'abstract': False,
            },
            bases=('buckets.file',),
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('file_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='buckets.File')),
            ],
            options={
                'abstract': False,
            },
            bases=('buckets.file',),
        ),
    ]
