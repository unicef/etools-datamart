# Generated by Django 2.2.3 on 2019-07-22 08:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0054_funds_fundsrereservation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tpmvisit',
            name='pd_ssfa_reference_number',
        ),
        migrations.RemoveField(
            model_name='tpmvisit',
            name='pd_ssfa_title',
        ),
    ]