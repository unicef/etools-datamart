# Generated by Django 2.2.3 on 2019-07-29 21:00

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0065_partner'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='planned_engagement',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
    ]