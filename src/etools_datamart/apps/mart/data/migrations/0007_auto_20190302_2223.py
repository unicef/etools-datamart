# Generated by Django 2.1.7 on 2019-03-02 22:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0006_auto_20190227_1910'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='fundsreservation',
            unique_together={('schema_name', 'source_id')},
        ),
    ]