# Generated by Django 4.1.5 on 2023-02-06 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0014_alter_fmoptions_label'),
    ]

    operations = [
        migrations.AddField(
            model_name='audit',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='audit',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
