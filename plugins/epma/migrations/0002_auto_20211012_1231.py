# Generated by Django 2.0.13 on 2021-10-12 12:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('epma', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='epmamedorder',
            name='created_in_elcid',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='epmamedorderdetail',
            name='created_in_elcid',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='epmatherapeuticclasslookup',
            name='created_in_elcid',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='epmamedorder',
            name='load_dt_tm',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='epmamedorder',
            name='o_clinical_display_line',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='epmamedorder',
            name='o_start_dt_tm',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
