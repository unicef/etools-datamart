# Generated by Django 2.2.7 on 2019-12-08 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prp', '0002_remove_indicatorbylocation_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='DataReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('seen', models.DateTimeField(blank=True, null=True)),
                ('indicator_report', models.CharField(blank=True, max_length=2048, null=True)),
                ('progress_report', models.CharField(blank=True, max_length=2048, null=True)),
                ('programme_document', models.CharField(blank=True, max_length=2048, null=True)),
                ('country_name', models.CharField(blank=True, max_length=2048, null=True)),
                ('business_area', models.CharField(blank=True, max_length=2048, null=True)),
                ('partner_name', models.CharField(blank=True, max_length=2048, null=True)),
                ('partner_vendor_number', models.CharField(blank=True, max_length=2048, null=True)),
                ('etools_intervention_id', models.CharField(blank=True, max_length=2048, null=True)),
                ('prp_intervention_id', models.CharField(blank=True, max_length=2048, null=True)),
                ('country_intervention_reference_numbername', models.CharField(blank=True, max_length=2048, null=True)),
                ('country_programme', models.CharField(blank=True, max_length=2048, null=True)),
                ('cp_output', models.CharField(blank=True, max_length=2048, null=True)),
                ('intervention_reference_number', models.CharField(blank=True, max_length=2048, null=True)),
                ('etools_cp_output_id', models.CharField(blank=True, max_length=2048, null=True)),
                ('cp_output_indicators', models.CharField(blank=True, max_length=2048, null=True)),
                ('etools_cp_output_indicators_id', models.CharField(blank=True, max_length=2048, null=True)),
                ('pd_result', models.CharField(blank=True, max_length=2048, null=True)),
                ('etools_pd_result_id', models.CharField(blank=True, max_length=2048, null=True)),
                ('performance_indicator', models.CharField(blank=True, max_length=2048, null=True)),
                ('section', models.CharField(blank=True, max_length=2048, null=True)),
                ('cluster_indicator', models.CharField(blank=True, max_length=2048, null=True)),
                ('indicator_type', models.CharField(blank=True, max_length=2048, null=True)),
                ('baseline', models.CharField(blank=True, max_length=2048, null=True)),
                ('target', models.CharField(blank=True, max_length=2048, null=True)),
                ('high_frequency', models.CharField(blank=True, max_length=2048, null=True)),
                ('means_of_verification', models.CharField(blank=True, max_length=2048, null=True)),
                ('locations', models.CharField(blank=True, max_length=2048, null=True)),
                ('report_number', models.CharField(blank=True, max_length=2048, null=True)),
                ('due_date', models.CharField(blank=True, max_length=2048, null=True)),
                ('reporting_period_start_date', models.CharField(blank=True, max_length=2048, null=True)),
                ('reporting_period_end_date', models.CharField(blank=True, max_length=2048, null=True)),
                ('reporting_period_due_date', models.CharField(blank=True, max_length=2048, null=True)),
                ('report_submission_date', models.CharField(blank=True, max_length=2048, null=True)),
                ('submitted_by', models.CharField(blank=True, max_length=2048, null=True)),
                ('narrative', models.CharField(blank=True, max_length=2048, null=True)),
                ('pd_output_progress_status', models.CharField(blank=True, max_length=2048, null=True)),
                ('pd_output_narrative_assessment', models.CharField(blank=True, max_length=2048, null=True)),
                ('calculation_method_across_location', models.CharField(blank=True, max_length=2048, null=True)),
                ('calculation_method_across_reporting_periods', models.CharField(blank=True, max_length=2048, null=True)),
                ('current_location', models.CharField(blank=True, max_length=2048, null=True)),
                ('previous_location_progress', models.CharField(blank=True, max_length=2048, null=True)),
                ('total_cummulative_progress_in_location', models.CharField(blank=True, max_length=2048, null=True)),
            ],
        ),
    ]