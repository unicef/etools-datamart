# Generated by Django 2.2.3 on 2019-08-02 07:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0069_Engagement'),
    ]

    operations = [
        migrations.AddField(
            model_name='intervention',
            name='last_pv_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interventionbudget',
            name='last_pv_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='interventionbylocation',
            name='last_pv_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]