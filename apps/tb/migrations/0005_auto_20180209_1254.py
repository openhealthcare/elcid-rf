# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-09 12:54
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0034_auto_20171214_1845'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('tb', '0004_bcg_tbhistory'),
    ]

    operations = [
        migrations.CreateModel(
            name='PersonalTBHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('how_long_ago_years', models.IntegerField(blank=True, null=True)),
                ('how_long_ago_months', models.IntegerField(blank=True, null=True)),
                ('how_long_ago_days', models.IntegerField(blank=True, null=True)),
                ('type_of_tb', models.CharField(blank=True, choices=[(b'Active', b'Active'), (b'Latent', b'Latent'), (b'Unknown', b'Unknown')], max_length=40, null=True)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_tb_personaltbhistory_subrecords', to=settings.AUTH_USER_MODEL)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opal.Patient')),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
        migrations.CreateModel(
            name='TBSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='socialhistory',
            name='arrival_in_the_uk',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name=b'Year of arrival in the UK'),
        ),
        migrations.AddField(
            model_name='personaltbhistory',
            name='sites',
            field=models.ManyToManyField(blank=True, to='tb.TBSite'),
        ),
        migrations.AddField(
            model_name='personaltbhistory',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_tb_personaltbhistory_subrecords', to=settings.AUTH_USER_MODEL),
        ),
    ]
