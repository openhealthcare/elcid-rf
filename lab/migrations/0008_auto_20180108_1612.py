# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-01-08 16:12
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lab', '0007_auto_20170706_1533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='labtest',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_lab_labtest_subrecords', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='labtest',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_lab_labtest_subrecords', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='observation',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_lab_observation_subrecords', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='observation',
            name='updated_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_lab_observation_subrecords', to=settings.AUTH_USER_MODEL),
        ),
    ]
