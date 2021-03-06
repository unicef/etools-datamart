# Generated by Django 2.2.3 on 2019-07-11 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0043_audit_engagement'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.IntegerField(blank=True, db_index=True, null=True)),
                ('last_modify_date', models.DateTimeField(auto_now=True)),
                ('seen', models.DateTimeField(blank=True, null=True)),
                ('country_name', models.CharField(db_index=True, max_length=100)),
                ('schema_name', models.CharField(db_index=True, max_length=63)),
                ('area_code', models.CharField(db_index=True, max_length=10)),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('donor', models.CharField(blank=True, max_length=128, null=True)),
                ('expiry', models.DateField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('modified', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
