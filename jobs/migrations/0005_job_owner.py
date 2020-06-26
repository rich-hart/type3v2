# Generated by Django 3.0.7 on 2020-06-26 05:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0004_auto_20200626_0300'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='owner',
            field=models.OneToOneField(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]