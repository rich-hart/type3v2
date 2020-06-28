# Generated by Django 3.0.7 on 2020-06-28 02:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tools', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ML',
            fields=[
                ('tool_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tools.Tool')),
            ],
            options={
                'abstract': False,
            },
            bases=('tools.tool',),
        ),
        migrations.CreateModel(
            name='Random',
            fields=[
                ('tool_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tools.Tool')),
            ],
            options={
                'abstract': False,
            },
            bases=('tools.tool',),
        ),
        migrations.CreateModel(
            name='Human',
            fields=[
                ('tool_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='tools.Tool')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=('tools.tool',),
        ),
    ]
