# Generated by Django 2.0.13 on 2021-10-11 08:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admissions', '0010_auto_20210720_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferhistory',
            name='created_in_elcid',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
