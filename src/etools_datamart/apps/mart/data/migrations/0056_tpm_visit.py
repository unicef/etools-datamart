# Generated by Django 2.2.3 on 2019-07-22 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0055_tpm_visit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tpmvisit',
            name='cp_output',
        ),
        migrations.RemoveField(
            model_name='tpmvisit',
            name='cp_output_id',
        ),
    ]