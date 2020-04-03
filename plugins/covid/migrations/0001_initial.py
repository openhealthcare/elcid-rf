# Generated by Django 2.0.9 on 2020-04-03 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CovidDashboard',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patients_tested', models.IntegerField()),
                ('positive', models.IntegerField()),
                ('negative', models.IntegerField()),
            ],
        ),
    ]
