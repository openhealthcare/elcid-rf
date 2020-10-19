# Generated by Django 2.0.13 on 2020-10-19 15:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import opal.models


class Migration(migrations.Migration):

    dependencies = [
        ('opal', '0037_auto_20181114_1445'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('covid', '0047_auto_20201013_0900'),
    ]

    operations = [
        migrations.CreateModel(
            name='CovidSixMonthFollowUp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(blank=True, null=True)),
                ('updated', models.DateTimeField(blank=True, null=True)),
                ('consistency_token', models.CharField(max_length=8)),
                ('when', models.DateTimeField(blank=True, null=True)),
                ('clinician', models.CharField(blank=True, max_length=255, null=True)),
                ('position', models.CharField(blank=True, choices=[('Consultant', 'Consultant'), ('Registrar', 'Registrar'), ('Associate Specialist', 'Associate Specialist'), ('Other', 'Other')], max_length=255, null=True)),
                ('cxr_completed', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Declined', 'Declined')], max_length=255, null=True)),
                ('bloods_completed', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Declined', 'Declined')], max_length=255, null=True)),
                ('incomplete_reason', models.TextField(blank=True, null=True)),
                ('current_breathlessness', models.CharField(blank=True, choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], max_length=5, null=True)),
                ('max_breathlessness', models.CharField(blank=True, choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], max_length=5, null=True)),
                ('breathlessness_trend', models.CharField(blank=True, choices=[('Same', 'Same'), ('Better', 'Better'), ('Worse', 'Worse')], max_length=10, null=True)),
                ('current_cough', models.CharField(blank=True, choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], max_length=5, null=True)),
                ('max_cough', models.CharField(blank=True, choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], max_length=5, null=True)),
                ('cough_trend', models.CharField(blank=True, choices=[('Same', 'Same'), ('Better', 'Better'), ('Worse', 'Worse')], max_length=10, null=True)),
                ('current_fatigue', models.CharField(blank=True, choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], max_length=5, null=True)),
                ('max_fatigue', models.CharField(blank=True, choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], max_length=5, null=True)),
                ('fatigue_trend', models.CharField(blank=True, choices=[('Same', 'Same'), ('Better', 'Better'), ('Worse', 'Worse')], max_length=10, null=True)),
                ('current_sleep_quality', models.CharField(blank=True, choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], max_length=5, null=True)),
                ('max_sleep_quality', models.CharField(blank=True, choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], max_length=5, null=True)),
                ('sleep_quality_trend', models.CharField(blank=True, choices=[('Same', 'Same'), ('Better', 'Better'), ('Worse', 'Worse')], max_length=10, null=True)),
                ('poor_sleep_noise', models.NullBooleanField()),
                ('poor_sleep_medications', models.NullBooleanField()),
                ('poor_sleep_other', models.CharField(blank=True, max_length=255, null=True)),
                ('chest_pain', models.NullBooleanField(help_text='Chest pain')),
                ('chest_tightness', models.NullBooleanField(help_text='Chest tightness')),
                ('myalgia', models.NullBooleanField()),
                ('confusion', models.NullBooleanField(help_text='Confusion or fuzzy head')),
                ('peripheral_oedema', models.NullBooleanField()),
                ('focal_weakness', models.NullBooleanField()),
                ('anosmia', models.NullBooleanField()),
                ('diarrhoea', models.NullBooleanField()),
                ('abdominal_pain', models.NullBooleanField(verbose_name='Abdominal pain')),
                ('anorexia', models.NullBooleanField()),
                ('back_to_normal', models.NullBooleanField(verbose_name='Do you feel back to normal?')),
                ('why_not_back_to_normal', models.TextField(blank=True, null=True)),
                ('baseline_health_proximity', models.IntegerField(blank=True, null=True, verbose_name='How close to 100% of usual health do you feel?')),
                ('back_to_work', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A')], max_length=20, null=True, verbose_name='If working, are you back to work?')),
                ('current_et', models.CharField(blank=True, help_text='Metres', max_length=50, null=True, verbose_name='Current ET (metres)')),
                ('mrc_dyspnoea_scale', models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5')], max_length=50, null=True, verbose_name='MRC Dyspnoea Scale')),
                ('limited_by', models.CharField(blank=True, choices=[('SOB', 'SOB'), ('Fatigue', 'Fatigue'), ('Other', 'Other')], max_length=50, null=True)),
                ('current_cfs', models.CharField(blank=True, choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9')], max_length=50, null=True, verbose_name='Current Clinical Frailty Score')),
                ('interest', models.CharField(blank=True, choices=[('0', '(0) Not At All'), ('1', '(1) Several days'), ('2', '(2) More than half the days'), ('3', '(3) Nearly every day')], max_length=50, null=True, verbose_name='Little interest or pleasure in doing things')),
                ('depressed', models.CharField(blank=True, choices=[('0', '(0) Not At All'), ('1', '(1) Several days'), ('2', '(2) More than half the days'), ('3', '(3) Nearly every day')], max_length=50, null=True, verbose_name='Feeling down, depressed or hopeless')),
                ('tsq1', models.NullBooleanField(verbose_name='Upsetting thoughts or memories about your hospital admission that have come into your mind against your will')),
                ('tsq2', models.NullBooleanField(verbose_name='Upsetting dreams about the event')),
                ('tsq3', models.NullBooleanField(verbose_name='Acting or feeling as though it is happening again')),
                ('tsq4', models.NullBooleanField(verbose_name='Feeling upset by reminders of the event')),
                ('tsq5', models.NullBooleanField(verbose_name='Bodily reactions such as fast heartbeat, sweatiness, dizziness when reminded of the event')),
                ('tsq6', models.NullBooleanField(verbose_name='Difficulty falling or staying asleep')),
                ('tsq7', models.NullBooleanField(verbose_name='Irritability or bursts of anger')),
                ('tsq8', models.NullBooleanField(verbose_name='Difficulty concentrating')),
                ('tsq9', models.NullBooleanField(verbose_name='Being more aware of potential danger to yourself and others')),
                ('tsq10', models.NullBooleanField(verbose_name='Being jumpy or startled at something unexpected')),
                ('other_concerns', models.TextField(blank=True, null=True)),
                ('call_satisfaction', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('Not sure', 'Not sure')], max_length=20, null=True, verbose_name='Did you find this call useful?')),
                ('recontact', models.NullBooleanField(verbose_name='Would you be willing to be contacted again to take part in research?')),
                ('haem_fu', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A')], max_length=250, null=True, verbose_name='Did patient receive haematology/anticoagulation clinic review if needed')),
                ('cardiology_fu', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A')], max_length=250, null=True, verbose_name='Did patient receive Cardiology clinic follow up if required?')),
                ('ipat_fu', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A')], max_length=250, null=True, verbose_name='Did patient access self referral to IAPT if received information?')),
                ('smoking_fu', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A')], max_length=250, null=True, verbose_name='Did patient receive smoking cessation input if consented?')),
                ('ct_chest', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A')], max_length=250, null=True, verbose_name='Did patient receive CT chest ?')),
                ('pulmonary_function', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A')], max_length=250, null=True, verbose_name='Did patient receive pulmonary function tests?')),
                ('msk_input', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A')], max_length=250, null=True, verbose_name='Did patient receive MSK input if required?')),
                ('patient_type', models.CharField(blank=True, choices=[('Inpatient', 'Inpatient'), ('Outpatient', 'Outpatient')], max_length=250, null=True)),
                ('resp_clinic', models.CharField(blank=True, choices=[('Yes', 'Yes'), ('No', 'No'), ('N/A', 'N/A')], max_length=250, null=True, verbose_name='Did patient receive a respiratory face to face clinic review if required?')),
                ('calls_post_discharge', models.CharField(blank=True, choices=[('One', 'One'), ('Two', 'Two'), ('Three', 'Three'), ('Four or more', 'Four or more')], max_length=250, null=True, verbose_name='How many telephone calls did the patient receive after discharge?')),
                ('cxrs', models.CharField(blank=True, choices=[('One', 'One'), ('Two or more', 'Two or more')], max_length=250, null=True, verbose_name='How many CXRs did the patient require?')),
                ('gp_copy', models.TextField(blank=True, null=True, verbose_name='Copy for clinic letter')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_covid_covidsixmonthfollowup_subrecords', to=settings.AUTH_USER_MODEL)),
                ('episode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opal.Episode')),
                ('updated_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='updated_covid_covidsixmonthfollowup_subrecords', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(opal.models.UpdatesFromDictMixin, opal.models.ToDictMixin, models.Model),
        ),
    ]
