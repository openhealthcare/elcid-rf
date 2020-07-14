# Generated by Django 2.0.13 on 2020-07-14 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('covid', '0031_auto_20200714_0952'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='covidfollowupactions',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='covidfollowupactions',
            name='episode',
        ),
        migrations.RemoveField(
            model_name='covidfollowupactions',
            name='updated_by',
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='anticoagulation',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='anticoagulation_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='anticoagulation_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='cardiology',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='cardiology_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='cardiology_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='ct_chest',
            field=models.NullBooleanField(verbose_name='CT Chest'),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='cxr',
            field=models.NullBooleanField(verbose_name='CXR'),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='ecg',
            field=models.NullBooleanField(verbose_name='ECG'),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='echocardiogram',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='elderly_care',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='elderly_care_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='elderly_care_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='exercise',
            field=models.NullBooleanField(verbose_name='Exercise Testing'),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='fatigue_services',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='fatigue_services_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='fatigue_services_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='hepatology',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='hepatology_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='hepatology_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='neurology',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='neurology_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='neurology_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='other_investigations',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='other_referral',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='other_referral_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='other_referral_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='pft',
            field=models.NullBooleanField(verbose_name='PFT'),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='primary_care',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='primary_care_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='primary_care_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='psychiatry',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='psychiatry_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='psychiatry_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='psychology',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='psychology_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='psychology_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='rehabilitation',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='rehabilitation_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='rehabilitation_gp',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='repeat_bloods',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='respiratory',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='respiratory_done',
            field=models.NullBooleanField(),
        ),
        migrations.AddField(
            model_name='covidfollowupcall',
            name='respiratory_gp',
            field=models.NullBooleanField(),
        ),
        migrations.DeleteModel(
            name='CovidFollowupActions',
        ),
    ]
