# Generated by Django 3.2.16 on 2022-12-07 19:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0013_alter_attachment_hyperlink'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fmoptions',
            name='label',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]