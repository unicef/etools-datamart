# Generated by Django 3.2 on 2021-08-25 21:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0155_auto_20210816_2301'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='approaching_threshold_flag',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='partner',
            name='expiring_assessment_flag',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='partner',
            name='expiring_psea_assessment_flag',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]