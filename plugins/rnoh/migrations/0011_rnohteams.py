# Generated by Django 2.0.13 on 2022-03-11 09:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('opal', '0040_auto_20201007_1346'),
        ('rnoh', '0010_auto_20220311_0855'),
    ]

    operations = [
        migrations.CreateModel(
            name='RNOHTeams',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, null=True, verbose_name='Created')),
                ('updated', models.DateTimeField(blank=True, null=True, verbose_name='Updated')),
                ('consistency_token', models.CharField(max_length=8, verbose_name='Consistency Token')),
                ('outstanding', models.NullBooleanField()),
                ('mdt_spinal', models.NullBooleanField(verbose_name='MDT-Spinal')),
                ('mdt_jru', models.NullBooleanField(verbose_name='MDT-JRU')),
                ('mdt_lru', models.NullBooleanField(verbose_name='MDT-LRU')),
                ('mdt_upper_limb', models.NullBooleanField(verbose_name='MDT-Upper-Limb')),
                ('opat', models.NullBooleanField(verbose_name='OPAT')),
                ('misc', models.NullBooleanField(verbose_name='Misc')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_rnoh_rnohteams_subrecords', to=settings.AUTH_USER_MODEL, verbose_name='Created By')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opal.Patient', verbose_name='Patient')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_rnoh_rnohteams_subrecords', to=settings.AUTH_USER_MODEL, verbose_name='Updated By')),
            ],
            options={
                'verbose_name': 'RNOH Teams',
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
    ]
