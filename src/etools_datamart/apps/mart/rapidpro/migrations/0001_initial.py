# Generated by Django 3.2.12 on 2022-03-12 17:14

import django.contrib.postgres.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.CharField(blank=True, max_length=100, null=True)),
                ('uuid', models.UUIDField(blank=True, db_index=True, null=True, unique=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('language', models.CharField(blank=True, max_length=100, null=True)),
                ('urns', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, default=list, null=True, size=None)),
                ('groups', models.JSONField(blank=True, default=dict, null=True)),
                ('fields', models.JSONField(blank=True, default=dict, null=True)),
                ('blocked', models.BooleanField(blank=True, null=True)),
                ('stopped', models.BooleanField(blank=True, null=True)),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('modified_on', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.CharField(blank=True, max_length=100, null=True)),
                ('uuid', models.UUIDField(db_index=True, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('archived', models.BooleanField(default=False)),
                ('expires', models.IntegerField(blank=True, null=True)),
                ('created_on', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('country', models.CharField(blank=True, max_length=100, null=True)),
                ('primary_language', models.CharField(blank=True, max_length=100, null=True)),
                ('languages', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
                ('timezone', models.CharField(blank=True, max_length=100, null=True)),
                ('date_style', models.CharField(blank=True, max_length=100, null=True)),
                ('credits', models.JSONField(default=dict)),
                ('anon', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('api_token', models.CharField(max_length=40)),
                ('server', models.CharField(default='https://app.rapidpro.io/', max_length=100)),
                ('is_active', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Runs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.CharField(blank=True, max_length=100, null=True)),
                ('active', models.IntegerField(default=0)),
                ('completed', models.IntegerField(default=0)),
                ('expired', models.IntegerField(default=0)),
                ('interrupted', models.IntegerField(default=0)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapidpro.organization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='organization',
            name='source',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rapidpro.source'),
        ),
        migrations.CreateModel(
            name='Label',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.CharField(blank=True, max_length=100, null=True)),
                ('uuid', models.UUIDField(db_index=True, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapidpro.organization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.CharField(blank=True, max_length=100, null=True)),
                ('uuid', models.UUIDField(blank=True, db_index=True, null=True, unique=True)),
                ('name', models.TextField(blank=True, null=True)),
                ('query', models.TextField(blank=True, null=True)),
                ('count', models.IntegerField(blank=True, null=True)),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapidpro.organization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FlowStart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.CharField(blank=True, max_length=100, null=True)),
                ('uuid', models.UUIDField(db_index=True, unique=True)),
                ('restart_participants', models.BooleanField(null=True)),
                ('status', models.CharField(max_length=100)),
                ('extra', models.JSONField(default=dict)),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('modified_on', models.DateTimeField(blank=True, null=True)),
                ('contacts', models.ManyToManyField(to='rapidpro.Contact')),
                ('flow', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rapidpro.flow')),
                ('groups', models.ManyToManyField(to='rapidpro.Group')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapidpro.organization')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='flow',
            name='labels',
            field=models.ManyToManyField(to='rapidpro.Label'),
        ),
        migrations.AddField(
            model_name='flow',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapidpro.organization'),
        ),
        migrations.AddField(
            model_name='flow',
            name='runs',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rapidpro.runs'),
        ),
        migrations.AddField(
            model_name='contact',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapidpro.organization'),
        ),
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_id', models.CharField(blank=True, max_length=100, null=True)),
                ('uuid', models.UUIDField(db_index=True, unique=True)),
                ('archived', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=100)),
                ('group', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='rapidpro.group')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rapidpro.organization')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
