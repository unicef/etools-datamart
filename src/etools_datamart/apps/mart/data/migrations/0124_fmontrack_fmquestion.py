# Generated by Django 2.2.11 on 2020-07-29 15:37

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0123_interventionbylocation_p_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='FMOntrack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('seen', models.DateTimeField(blank=True, null=True)),
                ('country_name', models.CharField(max_length=100)),
                ('schema_name', models.CharField(db_index=True, max_length=63)),
                ('area_code', models.CharField(db_index=True, max_length=10)),
                ('entity', models.CharField(blank=True, max_length=255, null=True, verbose_name='Entity')),
                ('narrative_finding', models.TextField(blank=True, null=True, verbose_name='Overall Finding Narrative')),
                ('overall_finding_rating', models.CharField(blank=True, max_length=50, null=True, verbose_name='Overall Finding Narrative')),
                ('monitoring_activity', models.CharField(blank=True, max_length=64, null=True, verbose_name='Monitoring Activity')),
                ('monitoring_activity_end_date', models.CharField(blank=True, max_length=50, null=True, verbose_name='Monitoring Activity End Date')),
                ('location', models.CharField(blank=True, max_length=254, null=True, verbose_name='Location')),
                ('site', models.CharField(blank=True, max_length=254, null=True, verbose_name='Location')),
                ('outcome', models.CharField(blank=True, max_length=30, null=True, verbose_name='Outcome WBS')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='FMQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('seen', models.DateTimeField(blank=True, null=True)),
                ('country_name', models.CharField(max_length=100)),
                ('schema_name', models.CharField(db_index=True, max_length=63)),
                ('area_code', models.CharField(db_index=True, max_length=10)),
                ('title', models.TextField(blank=True, null=True, verbose_name='Question Title')),
                ('answer_type', models.CharField(blank=True, max_length=15, null=True, verbose_name='Answer Type')),
                ('answer_options', models.TextField(blank=True, null=True, verbose_name='Answer Options')),
                ('entity_type', models.CharField(blank=True, max_length=100, null=True, verbose_name='Entity Type')),
                ('entity_instance', models.CharField(blank=True, max_length=255, null=True, verbose_name='Entity Instance')),
                ('question_collection_methods', models.TextField(blank=True, null=True, verbose_name='Question Collection Methods')),
                ('collection_method', models.CharField(blank=True, max_length=100, null=True, verbose_name='Collection Method')),
                ('answer', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Answer')),
                ('summary_answer', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True, verbose_name='Summary Answer')),
                ('monitoring_activity_id', models.IntegerField(blank=True, null=True, verbose_name='Monitoring Activity ID')),
                ('specific_details', models.TextField(blank=True, null=True, verbose_name='Specific Details')),
                ('date_of_capture', models.CharField(blank=True, max_length=50, null=True, verbose_name='Date of Capture')),
                ('monitoring_activity_end_date', models.CharField(blank=True, max_length=50, null=True, verbose_name='Monitoring Activity End Date')),
                ('location', models.CharField(blank=True, max_length=254, null=True, verbose_name='Location')),
                ('site', models.CharField(blank=True, max_length=254, null=True, verbose_name='Location')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
    ]