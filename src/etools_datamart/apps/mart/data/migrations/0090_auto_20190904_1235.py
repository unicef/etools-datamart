# Generated by Django 2.2.4 on 2019-09-04 12:35

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0089_auto_20190901_0643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='engagement',
            name='audit_opinion',
            field=models.CharField(blank=True, choices=[('unqualified', 'Unqualified'), ('qualified', 'Qualified'), ('disclaimer_opinion', 'Disclaimer opinion'), ('adverse_opinion', 'Adverse opinion')], db_index=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='engagement',
            name='status',
            field=models.CharField(blank=True, db_index=True, max_length=300, null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='end_date',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='mode_of_travel',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(choices=[('Plane', 'Plane'), ('Bus', 'Bus'), ('Car', 'Car'), ('Boat', 'Boat'), ('Rail', 'Rail')], max_length=5), blank=True, db_index=True, null=True, size=None, verbose_name='Mode of Travel'),
        ),
        migrations.AlterField(
            model_name='trip',
            name='start_date',
            field=models.DateField(blank=True, db_index=True, null=True),
        ),
    ]