# Generated by Django 2.1.5 on 2019-02-01 19:13

import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
from django.db import migrations, models

import month_field.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FAMIndicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(db_index=True, max_length=100)),
                ('schema_name', models.CharField(db_index=True, max_length=63)),
                ('area_code', models.CharField(db_index=True, max_length=10)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('seen', models.DateTimeField(blank=True, null=True)),
                ('source_id', models.IntegerField(blank=True, null=True)),
                ('month', month_field.models.MonthField(verbose_name='Month Value')),
                ('spotcheck_ip_contacted', models.IntegerField(default=0, verbose_name='Spot Check-IP Contacted')),
                ('spotcheck_report_submitted', models.IntegerField(default=0, verbose_name='Spot Check-Report Submitted')),
                ('spotcheck_final_report', models.IntegerField(default=0, verbose_name='Spot Check-Final Report')),
                ('spotcheck_cancelled', models.IntegerField(default=0, verbose_name='Spot Check-Cancelled')),
                ('audit_ip_contacted', models.IntegerField(default=0, verbose_name='Audit-IP Contacted')),
                ('audit_report_submitted', models.IntegerField(default=0, verbose_name='Audit-Report Submitted')),
                ('audit_final_report', models.IntegerField(default=0, verbose_name='Audit-Final Report')),
                ('audit_cancelled', models.IntegerField(default=0, verbose_name='Audit-Cancelled')),
                ('specialaudit_ip_contacted', models.IntegerField(default=0, verbose_name='Special Audit-IP Contacted')),
                ('specialaudit_report_submitted', models.IntegerField(default=0, verbose_name='Special Audit-Report Submitted')),
                ('specialaudit_final_report', models.IntegerField(default=0, verbose_name='Special Audit-Final Report')),
                ('specialaudit_cancelled', models.IntegerField(default=0, verbose_name='Special Audit-Cancelled')),
                ('microassessment_ip_contacted', models.IntegerField(default=0, verbose_name='Micro Assessment-IP Contacted')),
                ('microassessment_report_submitted', models.IntegerField(default=0, verbose_name='Micro Assessment-Report Submitted')),
                ('microassessment_final_report', models.IntegerField(default=0, verbose_name='Micro Assessment-Final Report')),
                ('microassessment_cancelled', models.IntegerField(default=0, verbose_name='Micro Assessment-Cancelled')),
            ],
            options={
                'verbose_name': 'FAM Indicator',
                'ordering': ('month', 'country_name'),
            },
        ),
        migrations.CreateModel(
            name='FundsReservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(db_index=True, max_length=100)),
                ('schema_name', models.CharField(db_index=True, max_length=63)),
                ('area_code', models.CharField(db_index=True, max_length=10)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('seen', models.DateTimeField(blank=True, null=True)),
                ('vendor_code', models.CharField(max_length=20)),
                ('fr_number', models.CharField(max_length=20)),
                ('document_date', models.DateField(blank=True, null=True)),
                ('fr_type', models.CharField(max_length=50)),
                ('currency', models.CharField(max_length=50)),
                ('document_text', models.CharField(max_length=255)),
                ('start_date', models.DateField(blank=True, null=True)),
                ('end_date', models.DateField(blank=True, null=True)),
                ('actual_amt', models.DecimalField(decimal_places=2, max_digits=20)),
                ('intervention_amt', models.DecimalField(decimal_places=2, max_digits=20)),
                ('outstanding_amt', models.DecimalField(decimal_places=2, max_digits=20)),
                ('total_amt', models.DecimalField(decimal_places=2, max_digits=20)),
                ('actual_amt_local', models.DecimalField(decimal_places=2, max_digits=20)),
                ('outstanding_amt_local', models.DecimalField(decimal_places=2, max_digits=20)),
                ('total_amt_local', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('multi_curr_flag', models.BooleanField()),
                ('fr_ref_number', models.CharField(max_length=30)),
                ('line_item', models.SmallIntegerField()),
                ('wbs', models.CharField(max_length=30)),
                ('grant_number', models.CharField(max_length=20)),
                ('fund', models.CharField(max_length=10)),
                ('overall_amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('overall_amount_dc', models.DecimalField(decimal_places=2, max_digits=20)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('line_item_text', models.CharField(max_length=255)),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('donor', models.CharField(blank=True, max_length=256, null=True)),
                ('donor_code', models.CharField(blank=True, max_length=30, null=True)),
                ('pd_ssfa_number', models.CharField(max_length=64, null=True)),
                ('source_id', models.IntegerField()),
                ('source_intervention_id', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Funds Reservation',
            },
        ),
        migrations.CreateModel(
            name='GatewayType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(db_index=True, max_length=100)),
                ('schema_name', models.CharField(db_index=True, max_length=63)),
                ('area_code', models.CharField(db_index=True, max_length=10)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('seen', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(db_index=True, max_length=64)),
                ('admin_level', models.SmallIntegerField(blank=True, null=True)),
                ('source_id', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='HACT',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(db_index=True, max_length=100)),
                ('schema_name', models.CharField(db_index=True, max_length=63)),
                ('area_code', models.CharField(db_index=True, max_length=10)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('seen', models.DateTimeField(blank=True, null=True)),
                ('source_id', models.IntegerField(blank=True, null=True)),
                ('year', models.IntegerField()),
                ('microassessments_total', models.IntegerField(default=0, help_text='Total number of completed Microassessments in the business area in the past year')),
                ('programmaticvisits_total', models.IntegerField(default=0, help_text='Total number of completed Programmatic visits in the business area')),
                ('followup_spotcheck', models.IntegerField(default=0, help_text='Total number of completed Programmatic visits in the business area')),
                ('completed_spotcheck', models.IntegerField(default=0, help_text='Total number of completed Programmatic visits in the business area')),
                ('completed_hact_audits', models.IntegerField(default=0, help_text='Total number of completed scheduled audits for the workspace.')),
                ('completed_special_audits', models.IntegerField(default=0, help_text='Total number of completed special audits for the workspace. ')),
            ],
            options={
                'verbose_name': 'HACT',
                'ordering': ('year', 'country_name'),
            },
        ),
        migrations.CreateModel(
            name='Intervention',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(db_index=True, max_length=100)),
                ('schema_name', models.CharField(db_index=True, max_length=63)),
                ('area_code', models.CharField(db_index=True, max_length=10)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('seen', models.DateTimeField(blank=True, null=True)),
                ('source_id', models.IntegerField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(null=True)),
                ('document_type', models.CharField(max_length=255, null=True)),
                ('number', models.CharField(max_length=64, null=True)),
                ('title', models.CharField(db_index=True, max_length=256, null=True)),
                ('status', models.CharField(max_length=32, null=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('submission_date', models.DateField(null=True)),
                ('submission_date_prc', models.DateField(null=True)),
                ('review_date_prc', models.DateField(null=True)),
                ('prc_review_document', models.CharField(max_length=1024, null=True)),
                ('signed_by_unicef_date', models.DateField(null=True)),
                ('signed_by_partner_date', models.DateField(null=True)),
                ('population_focus', models.CharField(max_length=130, null=True)),
                ('partner_authorized_officer_signatory_id', models.IntegerField(null=True)),
                ('signed_pd_document', models.CharField(max_length=1024, null=True)),
                ('contingency_pd', models.NullBooleanField()),
                ('metadata', django.contrib.postgres.fields.jsonb.JSONField()),
                ('unicef_signatory_first_name', models.CharField(max_length=30, null=True)),
                ('unicef_signatory_last_name', models.CharField(max_length=30, null=True)),
                ('unicef_signatory_email', models.CharField(max_length=254, null=True)),
                ('partner_name', models.CharField(max_length=200, null=True)),
                ('partner_signatory_title', models.CharField(max_length=64, null=True)),
                ('partner_signatory_first_name', models.CharField(max_length=64, null=True)),
                ('partner_signatory_last_name', models.CharField(max_length=64, null=True)),
                ('partner_signatory_email', models.CharField(max_length=128, null=True)),
                ('partner_signatory_phone', models.CharField(max_length=64, null=True)),
                ('unicef_focal_point_first_name', models.CharField(max_length=30, null=True)),
                ('unicef_focal_point_last_name', models.CharField(max_length=30, null=True)),
                ('unicef_focal_point_email', models.CharField(max_length=254, null=True)),
                ('partner_focal_point_title', models.CharField(max_length=64, null=True)),
                ('partner_focal_point_first_name', models.CharField(max_length=64, null=True)),
                ('partner_focal_point_last_name', models.CharField(max_length=64, null=True)),
                ('partner_focal_point_email', models.CharField(max_length=128, null=True)),
                ('partner_focal_point_phone', models.CharField(max_length=64, null=True)),
                ('partner_contribution', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('unicef_cash', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('in_kind_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('partner_contribution_local', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('unicef_cash_local', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('in_kind_amount_local', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('total', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('total_local', models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True)),
                ('currency', models.CharField(blank=True, max_length=4, null=True)),
                ('intervention_id', models.IntegerField(blank=True, null=True)),
                ('agreement_id', models.IntegerField(blank=True, null=True)),
                ('country_programme_id', models.IntegerField(blank=True, null=True)),
                ('unicef_signatory_id', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Intervention',
                'ordering': ('country_name', 'title'),
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(db_index=True, max_length=100)),
                ('schema_name', models.CharField(db_index=True, max_length=63)),
                ('area_code', models.CharField(db_index=True, max_length=10)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('seen', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=254)),
                ('latitude', models.FloatField(blank=True, null=True)),
                ('longitude', models.FloatField(blank=True, null=True)),
                ('p_code', models.CharField(max_length=32)),
                ('point', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
                ('level', models.IntegerField()),
                ('lft', models.IntegerField()),
                ('rght', models.IntegerField()),
                ('tree_id', models.IntegerField()),
                ('created', models.DateTimeField()),
                ('modified', models.DateTimeField()),
                ('is_active', models.BooleanField()),
                ('source_id', models.IntegerField(blank=True, null=True)),
                ('gateway', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='data.GatewayType')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='data.Location')),
            ],
        ),
        migrations.CreateModel(
            name='PDIndicator',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(db_index=True, max_length=100)),
                ('schema_name', models.CharField(db_index=True, max_length=63)),
                ('area_code', models.CharField(db_index=True, max_length=10)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('seen', models.DateTimeField(blank=True, null=True)),
                ('source_id', models.IntegerField(blank=True, null=True)),
                ('context_code', models.CharField(blank=True, max_length=50, null=True)),
                ('assumptions', models.TextField(blank=True, null=True)),
                ('total', models.IntegerField(blank=True, null=True)),
                ('means_of_verification', models.CharField(blank=True, max_length=255, null=True)),
                ('cluster_indicator_id', models.IntegerField(blank=True, null=True)),
                ('cluster_indicator_title', models.CharField(blank=True, max_length=1024, null=True)),
                ('cluster_name', models.CharField(blank=True, max_length=512, null=True)),
                ('response_plan_name', models.CharField(blank=True, max_length=1024, null=True)),
                ('is_active', models.BooleanField(blank=True, null=True)),
                ('is_high_frequency', models.BooleanField(blank=True, null=True)),
                ('denominator_label', models.CharField(blank=True, max_length=256, null=True)),
                ('label', models.TextField(blank=True, null=True)),
                ('measurement_specifications', models.TextField(blank=True, null=True)),
                ('numerator_label', models.CharField(blank=True, max_length=256, null=True)),
                ('target_denominator', models.IntegerField(blank=True, null=True)),
                ('target_numerator', models.IntegerField(blank=True, null=True)),
                ('baseline_denominator', models.IntegerField(blank=True, null=True)),
                ('baseline_numerator', models.IntegerField(blank=True, null=True)),
                ('lower_result_name', models.CharField(blank=True, max_length=500, null=True)),
                ('result_link_intervention', models.IntegerField(blank=True, null=True)),
                ('section_name', models.CharField(blank=True, max_length=45, null=True)),
                ('title', models.CharField(blank=True, max_length=1024, null=True)),
                ('unit', models.CharField(blank=True, max_length=10, null=True)),
                ('display_type', models.CharField(blank=True, max_length=10, null=True)),
                ('disaggregation_name', models.CharField(max_length=255)),
                ('disaggregation_active', models.BooleanField(default=False)),
                ('location_name', models.CharField(blank=True, max_length=254, null=True)),
                ('source_disaggregation_id', models.IntegerField(blank=True, null=True)),
                ('source_location_id', models.IntegerField(blank=True, null=True)),
                ('intervention', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.Intervention')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='data.Location')),
            ],
        ),
        migrations.CreateModel(
            name='PMPIndicators',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(db_index=True, max_length=100)),
                ('schema_name', models.CharField(db_index=True, max_length=63)),
                ('area_code', models.CharField(db_index=True, max_length=10)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('seen', models.DateTimeField(blank=True, null=True)),
                ('source_id', models.IntegerField(blank=True, null=True)),
                ('vendor_number', models.CharField(db_index=True, max_length=255, null=True)),
                ('partner_name', models.CharField(db_index=True, max_length=255, null=True)),
                ('partner_type', models.CharField(db_index=True, max_length=255, null=True)),
                ('pd_ssfa_ref', models.CharField(max_length=255, null=True)),
                ('pd_ssfa_status', models.CharField(db_index=True, max_length=50, null=True)),
                ('pd_ssfa_start_date', models.DateField(null=True)),
                ('pd_ssfa_creation_date', models.DateField(null=True)),
                ('pd_ssfa_end_date', models.DateField(null=True)),
                ('cash_contribution', models.DecimalField(decimal_places=3, help_text='UNICEF US$ Cash contribution', max_digits=20, null=True)),
                ('supply_contribution', models.DecimalField(decimal_places=3, help_text='UNICEF US$ Supply contribution', max_digits=20, null=True)),
                ('total_budget', models.DecimalField(db_index=True, decimal_places=3, help_text='Total Budget', max_digits=20, null=True)),
                ('unicef_budget', models.DecimalField(decimal_places=3, help_text='UNICEF Budget', max_digits=20, null=True)),
                ('currency', models.CharField(help_text='Currency', max_length=201, null=True)),
                ('partner_contribution', models.CharField(help_text='Partner Contribution', max_length=202, null=True)),
                ('unicef_cash', models.CharField(help_text='Unicef Cash', max_length=203, null=True)),
                ('in_kind_amount', models.CharField(help_text='In kind Amount', max_length=204, null=True)),
                ('total', models.CharField(max_length=205, null=True)),
                ('fr_numbers_against_pd_ssfa', models.TextField(help_text='FR numbers against PD / SSFA', null=True)),
                ('fr_currencies', models.CharField(help_text='FR currencies', max_length=207, null=True)),
                ('sum_of_all_fr_planned_amount', models.CharField(help_text='Sum of all FR planned amount', max_length=208, null=True)),
                ('core_value_attached', models.CharField(help_text='Core value attached', max_length=209, null=True)),
                ('partner_link', models.CharField(help_text='Partner Link', max_length=210, null=True)),
                ('intervention_link', models.CharField(help_text='Intervention Link', max_length=211, null=True)),
                ('country_id', models.IntegerField(null=True)),
                ('partner_id', models.IntegerField(null=True)),
                ('intervention_id', models.IntegerField(null=True)),
                ('created', models.DateTimeField(auto_now=True)),
                ('updated', models.DateTimeField(null=True)),
            ],
            options={
                'verbose_name': 'PMP Indicator',
                'ordering': ('country_name', 'partner_name'),
            },
        ),
        migrations.CreateModel(
            name='UserStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(db_index=True, max_length=100)),
                ('schema_name', models.CharField(db_index=True, max_length=63)),
                ('area_code', models.CharField(db_index=True, max_length=10)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('seen', models.DateTimeField(blank=True, null=True)),
                ('source_id', models.IntegerField(blank=True, null=True)),
                ('month', month_field.models.MonthField(verbose_name='Month Value')),
                ('total', models.IntegerField(default=0, verbose_name='Total users')),
                ('unicef', models.IntegerField(default=0, verbose_name='UNICEF uswers')),
                ('logins', models.IntegerField(default=0, verbose_name='Number of logins')),
                ('unicef_logins', models.IntegerField(default=0, verbose_name='Number of UNICEF logins')),
            ],
            options={
                'verbose_name': 'User Access Statistics',
                'ordering': ('-month', 'country_name'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='userstats',
            unique_together={('country_name', 'month')},
        ),
        migrations.AlterUniqueTogether(
            name='intervention',
            unique_together={('schema_name', 'intervention_id')},
        ),
        migrations.AlterUniqueTogether(
            name='hact',
            unique_together={('year', 'country_name')},
        ),
        migrations.AlterUniqueTogether(
            name='gatewaytype',
            unique_together={('schema_name', 'admin_level'), ('schema_name', 'name')},
        ),
        migrations.AddField(
            model_name='fundsreservation',
            name='intervention',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='funds', to='data.Intervention'),
        ),
        migrations.AlterUniqueTogether(
            name='famindicator',
            unique_together={('month', 'country_name')},
        ),
        migrations.AlterUniqueTogether(
            name='pdindicator',
            unique_together={('schema_name', 'source_id', 'source_location_id', 'source_disaggregation_id')},
        ),
        migrations.AlterUniqueTogether(
            name='location',
            unique_together={('schema_name', 'source_id')},
        ),
        migrations.AlterUniqueTogether(
            name='fundsreservation',
            unique_together={('schema_name', 'source_id'), ('schema_name', 'fr_number')},
        ),
    ]