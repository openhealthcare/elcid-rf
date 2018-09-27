# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-02-18 10:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0010_auto_20180217_2107'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bcg',
            name='bcg_type',
            field=models.CharField(blank=True, choices=[(b'neonatal', b'neonatal'), (b'school', b'school'), (b'other', b'other')], max_length=255, verbose_name=b'BCG Type'),
        ),
    ]
