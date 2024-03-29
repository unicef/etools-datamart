# Generated by Django 3.2.12 on 2022-04-20 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0004_auto_20220410_1500'),
    ]

    operations = [
        migrations.AddField(
            model_name='spotcheckfindings',
            name='date_of_cancel',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='spotcheckfindings',
            name='date_of_comments_by_ip',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='spotcheckfindings',
            name='date_of_comments_by_unicef',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='spotcheckfindings',
            name='date_of_draft_report_to_unicef',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='spotcheckfindings',
            name='date_of_report_submit',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='spotcheckfindings',
            name='partner_contacted_at',
            field=models.DateField(blank=True, null=True),
        ),
    ]
