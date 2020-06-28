# Generated by Django 3.0.7 on 2020-06-28 03:02

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Object',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('tag', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('tag', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FSObject',
            fields=[
                ('object_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='buckets.Object')),
                ('parent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='buckets.Object')),
            ],
            options={
                'abstract': False,
            },
            bases=('buckets.object',),
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
