# Generated by Django 2.2.6 on 2019-10-21 08:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0106_auto_20191021_0851'),
    ]

    operations = [
        migrations.AddField(
            model_name='famindicator',
            name='audit_field_visit',
            field=models.TextField(blank=True, null=True),
        ),
    ]