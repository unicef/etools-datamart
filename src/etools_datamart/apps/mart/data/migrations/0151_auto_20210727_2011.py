# Generated by Django 3.1.13 on 2021-07-27 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0150_auto_20210716_1547'),
    ]

    operations = [
        migrations.AddField(
            model_name='fmquestion',
            name='output',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Output WBS'),
        ),
        migrations.AddField(
            model_name='fmquestion',
            name='reference_number',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='fmquestion',
            name='vendor_number',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]