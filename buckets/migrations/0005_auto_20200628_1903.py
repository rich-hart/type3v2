# Generated by Django 3.0.7 on 2020-06-28 19:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0004_file_path'),
    ]

    operations = [
        migrations.RenameField(
            model_name='file',
            old_name='path',
            new_name='_path',
        ),
    ]
