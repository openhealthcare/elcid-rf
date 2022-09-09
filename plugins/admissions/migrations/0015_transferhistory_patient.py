# Generated by Django 2.2.16 on 2022-01-07 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0040_auto_20201007_1346'),
        ('admissions', '0014_merge_20220107_1155'),
    ]

    operations = [
        migrations.AddField(
            model_name='transferhistory',
            name='patient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='opal.Patient'),
        ),
    ]
