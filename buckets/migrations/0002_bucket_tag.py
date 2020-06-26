# Generated by Django 3.0.7 on 2020-06-26 00:13

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('buckets', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bucket',
            name='tag',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]