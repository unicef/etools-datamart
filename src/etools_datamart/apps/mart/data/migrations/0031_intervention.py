# Generated by Django 2.2.2 on 2019-06-20 07:59

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0030_auto_20190602_1935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='intervention',
            name='partner_focal_point_email',
        ),
        migrations.RemoveField(
            model_name='intervention',
            name='partner_focal_point_first_name',
        ),
        migrations.RemoveField(
            model_name='intervention',
            name='partner_focal_point_last_name',
        ),
        migrations.RemoveField(
            model_name='intervention',
            name='partner_focal_point_phone',
        ),
        migrations.RemoveField(
            model_name='intervention',
            name='partner_focal_point_title',
        ),
        migrations.RemoveField(
            model_name='intervention',
            name='unicef_focal_point_email',
        ),
        migrations.RemoveField(
            model_name='intervention',
            name='unicef_focal_point_first_name',
        ),
        migrations.RemoveField(
            model_name='intervention',
            name='unicef_focal_point_last_name',
        ),
        migrations.RemoveField(
            model_name='interventionbylocation',
            name='partner_focal_point_email',
        ),
        migrations.RemoveField(
            model_name='interventionbylocation',
            name='partner_focal_point_first_name',
        ),
        migrations.RemoveField(
            model_name='interventionbylocation',
            name='partner_focal_point_last_name',
        ),
        migrations.RemoveField(
            model_name='interventionbylocation',
            name='partner_focal_point_phone',
        ),
        migrations.RemoveField(
            model_name='interventionbylocation',
            name='partner_focal_point_title',
        ),
        migrations.RemoveField(
            model_name='interventionbylocation',
            name='unicef_focal_point_email',
        ),
        migrations.RemoveField(
            model_name='interventionbylocation',
            name='unicef_focal_point_first_name',
        ),
        migrations.RemoveField(
            model_name='interventionbylocation',
            name='unicef_focal_point_last_name',
        ),
        migrations.AddField(
            model_name='intervention',
            name='agreement_reference_number',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='amendment_types',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='attachment_types',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='clusters',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='country_programme',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='cp_output',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='cp_output_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='cso_type',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='days_from_prc_review_to_signature',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='days_from_submission_to_signature',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='fr_number',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='last_amendment_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='locations_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='number_of_amendments',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='number_of_attachments',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='offices_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='partner_focal_points',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='partner_focal_points_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='partner_type',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='partner_vendor_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='planned_programmatic_visits',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='unicef_focal_points',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='intervention',
            name='unicef_focal_points_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='agreement_reference_number',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='amendment_types',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='attachment_types',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='clusters',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='country_programme',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='cp_output',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='cp_output_id',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='cso_type',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='days_from_prc_review_to_signature',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='days_from_submission_to_signature',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='fr_number',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='last_amendment_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='locations_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='number_of_amendments',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='number_of_attachments',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='offices_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='partner_focal_points',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='partner_focal_points_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='partner_type',
            field=models.CharField(max_length=64, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='partner_vendor_number',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='planned_programmatic_visits',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='unicef_focal_points',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='unicef_focal_points_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=dict, null=True),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='locations',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='intervention',
            name='offices',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='interventionbylocation',
            name='locations',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='interventionbylocation',
            name='offices',
            field=models.TextField(blank=True, null=True),
        ),
    ]