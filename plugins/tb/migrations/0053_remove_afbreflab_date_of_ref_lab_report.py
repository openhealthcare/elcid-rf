# Generated by Django 2.0.13 on 2021-07-20 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tb', '0052_auto_20210720_0942'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='afbreflab',
            name='date_of_ref_lab_report',
        ),
    ]
