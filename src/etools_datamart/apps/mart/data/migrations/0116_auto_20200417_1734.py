# Generated by Django 2.2.11 on 2020-04-17 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0115_pdindicator_pd_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeoName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('toponym_name', models.CharField(max_length=254, null=True)),
                ('name', models.CharField(max_length=254, null=True)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('geoname_id', models.CharField(max_length=50, null=True)),
                ('country_code', models.CharField(max_length=20, null=True)),
                ('country_name', models.CharField(max_length=150, null=True)),
                ('fcl', models.CharField(max_length=50, null=True)),
                ('fcode', models.CharField(max_length=50, null=True)),
                ('distance', models.FloatField(null=True)),
            ],
            options={
                'unique_together': {('lat', 'lng')},
            },
        ),
        migrations.AddField(
            model_name='location',
            name='geoname',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.deletion.DO_NOTHING, to='data.GeoName'),
        ),
    ]