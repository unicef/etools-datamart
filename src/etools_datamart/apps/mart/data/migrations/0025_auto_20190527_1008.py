# Generated by Django 2.2 on 2019-05-27 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0024_actionpoint_related_module_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerStaffMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('seen', models.DateTimeField(blank=True, null=True)),
                ('country_name', models.CharField(db_index=True, max_length=100)),
                ('schema_name', models.CharField(db_index=True, max_length=63)),
                ('area_code', models.CharField(db_index=True, max_length=10)),
                ('title', models.CharField(blank=True, max_length=64, null=True)),
                ('first_name', models.CharField(blank=True, max_length=64, null=True)),
                ('last_name', models.CharField(blank=True, max_length=64, null=True)),
                ('email', models.CharField(blank=True, max_length=128, null=True, unique=True)),
                ('phone', models.CharField(blank=True, max_length=64, null=True)),
                ('partner', models.CharField(blank=True, max_length=100, null=True)),
                ('vendor_number', models.CharField(blank=True, max_length=100, null=True)),
                ('active', models.BooleanField(blank=True, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='actionpoint',
            name='action_point_url',
        ),
        migrations.RemoveField(
            model_name='actionpoint',
            name='related_module_url',
        ),
    ]