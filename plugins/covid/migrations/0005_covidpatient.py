# Generated by Django 2.0.13 on 2020-04-29 10:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0037_auto_20181114_1445'),
        ('covid', '0004_auto_20200422_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='CovidPatient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_first_positive', models.DateField()),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='covid_patient', to='opal.Patient')),
            ],
        ),
    ]
