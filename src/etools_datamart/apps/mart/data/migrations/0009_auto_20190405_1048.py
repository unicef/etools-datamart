# Generated by Django 2.2 on 2019-04-05 10:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0008_auto_20190321_1015'),
    ]

    operations = [
        migrations.CreateModel(
            name='ActionPoint',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country_name', models.CharField(db_index=True, max_length=100)),
                ('schema_name', models.CharField(db_index=True, max_length=63)),
                ('area_code', models.CharField(db_index=True, max_length=10)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('seen', models.DateTimeField(blank=True, null=True)),
                ('source_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('location_source_id', models.IntegerField(blank=True, null=True)),
                ('location_name', models.CharField(blank=True, max_length=254, null=True)),
                ('location_pcode', models.CharField(blank=True, max_length=32, null=True)),
                ('location_level', models.IntegerField(blank=True, null=True)),
                ('location_levelname', models.CharField(blank=True, max_length=32, null=True)),
                ('author_username', models.CharField(max_length=200)),
                ('assigned_by_username', models.CharField(max_length=200)),
                ('assigned_to_username', models.CharField(max_length=200)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(blank=True, choices=[('open', 'Open'), ('completed', 'Completed')], max_length=10, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('due_date', models.DateField(blank=True, null=True)),
                ('date_of_completion', models.DateTimeField(blank=True, null=True)),
                ('high_priority', models.BooleanField(blank=True, null=True)),
                ('intervention_source_id', models.IntegerField(blank=True, null=True)),
                ('intervention_number', models.CharField(max_length=64, null=True)),
                ('office', models.CharField(blank=True, max_length=64, null=True)),
                ('partner_source_id', models.IntegerField(blank=True, null=True)),
                ('partner_name', models.CharField(blank=True, max_length=300, null=True)),
                ('engagement_source_id', models.IntegerField(blank=True, null=True)),
                ('engagement_type', models.CharField(blank=True, max_length=64, null=True)),
                ('section_source_id', models.IntegerField(blank=True, null=True)),
                ('section_type', models.CharField(blank=True, max_length=64, null=True)),
                ('travel_activity_source_id', models.IntegerField(blank=True, null=True)),
                ('travel_activity_travel_type', models.CharField(blank=True, max_length=64, null=True)),
                ('category_source_id', models.IntegerField(blank=True, null=True)),
                ('category_module', models.CharField(blank=True, choices=[('apd', 'Action Points'), ('t2f', 'Trip Management'), ('tpm', 'Third Party Monitoring'), ('audit', 'Financial Assurance')], max_length=64, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='travelactivity',
            name='result_code',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='travelactivity',
            name='result_sector',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='travelactivity',
            name='result_type',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='travelactivity',
            name='result_vision_id',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='travelactivity',
            name='source_result_id',
            field=models.IntegerField(null=True),
        ),
    ]