# Generated by Django 2.0.13 on 2024-09-26 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0060_auto_copy_over_birth_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientconsultation',
            name='reason_for_mdt',
            field=models.TextField(blank=True, choices=[('New microbiology result', 'New microbiology result'), ('Infection control', 'Infection control'), ('Clinical management', 'Clinical management'), ('Other', 'Other')], null=True),
        ),
    ]
