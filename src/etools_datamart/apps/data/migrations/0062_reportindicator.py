# Generated by Django 2.2.3 on 2019-07-23 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0061_reportindicator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportindicator',
            name='baseline_denominator',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='reportindicator',
            name='baseline_numerator',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]