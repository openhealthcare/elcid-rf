# Generated by Django 2.0.13 on 2021-05-24 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0004_auto_20210329_1137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='derived_appointment_type',
            field=models.CharField(blank=True, db_index=True, help_text='Cleaned up Appointment type (Taken from Full Appointment type)', max_length=100, null=True),
        ),
    ]
