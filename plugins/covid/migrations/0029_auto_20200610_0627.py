# Generated by Django 2.0.13 on 2020-06-10 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0028_auto_20200610_0602'),
    ]

    operations = [
        migrations.AddField(
            model_name='covidfollowupactions',
            name='anticoagulation_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='anticoagulation_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='cardiology_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='cardiology_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='elderly_care_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='elderly_care_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='fatigue_services_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='fatigue_services_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='hepatology_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='hepatology_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='neurology_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='neurology_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='other_referral_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='other_referral_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='primary_care_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='primary_care_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='psychiatry_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='psychiatry_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='psychology_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='psychology_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='rehabilitation_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='rehabilitation_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='respiratory_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupactions',
            name='respiratory_gp',
            field=models.NullBooleanField(),
        ),
    ]
