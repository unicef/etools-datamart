# Generated by Django 2.2.13 on 2021-01-05 14:16

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0133_auditspecial'),
    ]

    operations = [
        migrations.AddField(
            model_name='audit',
            name='partner',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='auditspecial',
            name='partner',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
    ]
