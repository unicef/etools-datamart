# Generated by Django 2.2.4 on 2019-08-02 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0074_Engagement'),
    ]

    operations = [
        migrations.AddField(
            model_name='partner',
            name='last_pv_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]