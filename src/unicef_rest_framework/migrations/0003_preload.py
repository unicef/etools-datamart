# Generated by Django 2.2.5 on 2019-09-07 17:01

import django.contrib.postgres.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('unicef_rest_framework', '0002_auto_20190201_1913'),
    ]

    operations = [
        migrations.CreateModel(
            name='Preload',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('params', django.contrib.postgres.fields.JSONField(blank=True, default=dict, null=True)),
                ('enabled', models.BooleanField(blank=True, default=True)),
                ('last_run', models.DateTimeField(blank=True, null=True)),
                ('last_status_code', models.IntegerField(blank=True, null=True)),
                ('as_user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('url',),
                'unique_together': {('url', 'as_user', 'params')},
            },
        ),
    ]