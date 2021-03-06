# Generated by Django 2.2.7 on 2019-12-08 21:39

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prp', '0003_datareport'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datareport',
            name='country_intervention_reference_numbername',
        ),
        migrations.RemoveField(
            model_name='datareport',
            name='country_programme',
        ),
        migrations.AddField(
            model_name='datareport',
            name='locations_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datareport',
            name='due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datareport',
            name='locations',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datareport',
            name='report_submission_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datareport',
            name='reporting_period_due_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datareport',
            name='reporting_period_end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='datareport',
            name='reporting_period_start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
