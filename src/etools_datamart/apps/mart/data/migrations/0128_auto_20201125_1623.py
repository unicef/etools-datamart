# Generated by Django 2.2.11 on 2020-11-25 16:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0127_partnerstaffmember_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportindicator',
            name='section_name',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]