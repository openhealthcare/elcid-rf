# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-11 12:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0034_auto_20171214_1845'),
        ('tb', '0004_bcg_tbhistory'),
    ]

    operations = [
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
        migrations.CreateModel(
            name='TBTreatmentCentre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='tbhistory',
            name='date_of_other_tb_contact',
        ),
        migrations.RemoveField(
            model_name='tbhistory',
            name='date_of_previous_tb_infection',
        ),
        migrations.RemoveField(
            model_name='tbhistory',
            name='other_tb_contact',
        ),
        migrations.RemoveField(
            model_name='tbhistory',
            name='personal_history_of_tb',
        ),
        migrations.AddField(
            model_name='tbhistory',
            name='country_treated_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='opal.Destination'),
        ),
        migrations.AddField(
            model_name='tbhistory',
            name='country_treated_ft',
            field=models.CharField(blank=True, default=b'', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tbhistory',
            name='details',
            field=models.TextField(default=b''),
        ),
        migrations.AddField(
            model_name='tbhistory',
            name='how_long_ago_days',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tbhistory',
            name='how_long_ago_months',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tbhistory',
            name='how_long_ago_years',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='tbhistory',
            name='previous_tb_contact',
            field=models.CharField(blank=True, choices=[(b'Personal', b'Personal'), (b'Other', b'Other'), (b'None', b'None')], default=b'None', max_length=100),
        ),
        migrations.AddField(
            model_name='tbhistory',
            name='site_of_tb_ft',
            field=models.CharField(blank=True, default=b'', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='tbhistory',
            name='tb_type',
            field=models.CharField(blank=True, choices=[(b'Active', b'Active'), (b'Latent', b'Latent'), (b'Unknown', b'Unknown')], max_length=256, null=True),
        ),
        migrations.AddField(
            model_name='tbhistory',
            name='treatment_centre_ft',
            field=models.CharField(blank=True, default=b'', max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='socialhistory',
            name='arrival_in_the_uk',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name=b'Year of arrival in the UK'),
        ),
        migrations.AddField(
            model_name='tbhistory',
            name='site_of_tb_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tb.TBSite'),
        ),
        migrations.AddField(
            model_name='tbhistory',
            name='treatment_centre_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tb.TBTreatmentCentre'),
        ),
    ]
