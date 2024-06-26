# Generated by Django 3.2.12 on 2022-03-12 17:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tracking', '0001_initial'),
        ('unicef_rest_framework', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pathcounter',
            name='service',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='unicef_rest_framework.service'),
        ),
        migrations.AddField(
            model_name='monthlycounter',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='apirequestlog',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='usercounter',
            unique_together={('day', 'user')},
        ),
        migrations.AlterUniqueTogether(
            name='pathcounter',
            unique_together={('day', 'path')},
        ),
        migrations.AlterUniqueTogether(
            name='monthlycounter',
            unique_together={('day', 'user')},
        ),
    ]
