# Generated by Django 2.0.13 on 2020-06-05 10:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('imaging', '0001_initial'),
        ('covid', '0023_auto_20200531_1627'),
    ]

    operations = [
        migrations.CreateModel(
            name='CovidReportCode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('covid_code', models.CharField(blank=True, max_length=10, null=True)),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='imaging.Imaging')),
            ],
        ),
    ]
