# Generated by Django 2.0.13 on 2021-07-22 13:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0054_patientconsultation_infection_control'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='afbculture',
            name='observation',
        ),
        migrations.RemoveField(
            model_name='afbreflab',
            name='observation',
        ),
        migrations.RemoveField(
            model_name='afbsmear',
            name='observation',
        ),
        migrations.RemoveField(
            model_name='tbpcr',
            name='observation',
        ),
    ]
