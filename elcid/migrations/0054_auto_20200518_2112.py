# Generated by Django 2.0.13 on 2020-05-18 21:12

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('elcid', '0053_auto_20200518_2104'),
    ]

    operations = [
        migrations.AlterField(
            model_name='line',
            name='line_type_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='elcid.LineType'),
        ),
        migrations.AlterField(
            model_name='line',
            name='site_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='elcid.LineSite'),
        ),
        migrations.AlterField(
            model_name='line',
            name='complications_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='elcid.LineComplication'),
        ),
        migrations.AlterField(
            model_name='line',
            name='removal_reason_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='elcid.LineRemovalReason'),
        ),
    ]
