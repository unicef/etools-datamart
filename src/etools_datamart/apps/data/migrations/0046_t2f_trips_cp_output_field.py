# Generated by Django 2.2.3 on 2019-07-12 06:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0045_hact_detail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='cp_output',
            field=models.TextField(blank=True, null=True),
        ),
    ]