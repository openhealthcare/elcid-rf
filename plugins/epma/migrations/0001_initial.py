# Generated by Django 2.0.13 on 2021-10-12 08:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('opal', '0040_auto_20201007_1346'),
    ]

    operations = [
        migrations.CreateModel(
            name='EPMAMedOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('localpatientid', models.CharField(max_length=256)),
                ('o_encntr_id', models.CharField(max_length=256)),
                ('o_order_id', models.CharField(max_length=256)),
                ('e_finnumber', models.CharField(blank=True, max_length=256, null=True)),
                ('e_create_dt_tm', models.DateTimeField(blank=True, null=True)),
                ('e_encntr_type_desc', models.CharField(blank=True, max_length=256, null=True)),
                ('e_treatmentfunction', models.CharField(blank=True, max_length=256, null=True)),
                ('e_mainspecialty', models.CharField(blank=True, max_length=256, null=True)),
                ('e_loc_faciLity_desc', models.CharField(blank=True, max_length=256, null=True)),
                ('e_building', models.CharField(blank=True, max_length=256, null=True)),
                ('e_warddisplay', models.CharField(blank=True, max_length=256, null=True)),
                ('e_leadconsultant', models.CharField(blank=True, max_length=256, null=True)),
                ('o_catalog_cd', models.CharField(max_length=256)),
                ('o_catalog_type_desc', models.CharField(blank=True, max_length=256, null=True)),
                ('o_order_mnemonic', models.CharField(blank=True, max_length=256, null=True)),
                ('o_cki_mltmlink', models.CharField(blank=True, max_length=256, null=True)),
                ('drug_identifier', models.CharField(blank=True, max_length=256, null=True)),
                ('o_orig_order_dt_tm', models.DateTimeField(blank=True, null=True)),
                ('oa_firstactionpersonnelname', models.CharField(blank=True, max_length=256, null=True)),
                ('oa_firstpersonnelposition', models.CharField(blank=True, max_length=256, null=True)),
                ('o_status_desc', models.CharField(blank=True, max_length=256, null=True)),
                ('o_discontinue_ind', models.CharField(blank=True, max_length=256, null=True)),
                ('o_clinical_display_line', models.CharField(blank=True, max_length=256, null=True)),
                ('o_order_signed_date_tm', models.DateTimeField(blank=True, null=True)),
                ('o_start_dt_tm', models.CharField(blank=True, max_length=256, null=True)),
                ('o_stop_dt_tm', models.CharField(blank=True, max_length=256, null=True)),
                ('o_orig_ord_as_flag', models.CharField(blank=True, max_length=256, null=True)),
                ('o_need_rx_verify_ind', models.CharField(blank=True, max_length=256, null=True)),
                ('o_template_order_flag', models.CharField(blank=True, max_length=256, null=True)),
                ('o_active_status_prsnl_id', models.CharField(max_length=256)),
                ('o_last_action_sequence', models.CharField(blank=True, max_length=256, null=True)),
                ('o_updt_dt_tm', models.DateTimeField()),
                ('o_synonym_id', models.CharField(max_length=256)),
                ('ord_cat_syn_cki', models.CharField(blank=True, max_length=256, null=True)),
                ('domain_name', models.CharField(blank=True, max_length=256, null=True)),
                ('load_dt_tm', models.CharField(blank=True, max_length=256, null=True)),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='opal.Patient')),
            ],
        ),
        migrations.CreateModel(
            name='EPMAMedOrderDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.CharField(max_length=256)),
                ('action_sequence', models.CharField(max_length=256)),
                ('detail_sequence', models.CharField(max_length=256)),
                ('oe_field_id', models.CharField(max_length=256)),
                ('oe_field_meaning', models.CharField(blank=True, max_length=256, null=True)),
                ('oe_field_display_value', models.CharField(blank=True, max_length=256, null=True)),
                ('oe_field_dt_tm_value', models.DateTimeField(blank=True, null=True)),
                ('updt_dt_tm', models.DateTimeField()),
                ('load_dt_tm', models.DateTimeField(blank=True, null=True)),
                ('epmamedorder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='epma.EPMAMedOrder')),
            ],
        ),
        migrations.CreateModel(
            name='EPMATherapeuticClassLookup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mcdx_drug_identifier', models.CharField(max_length=256)),
                ('mcdx_multum_category_id', models.CharField(max_length=256)),
                ('mcdx_updt_dt_tm', models.CharField(max_length=256)),
                ('multum_hierarchy_1a', models.CharField(blank=True, max_length=256, null=True)),
                ('multum_hierarchy_1', models.CharField(blank=True, max_length=256, null=True)),
                ('multum_hierarchy_2', models.CharField(blank=True, max_length=256, null=True)),
                ('multum_hierarchy_3', models.CharField(blank=True, max_length=256, null=True)),
                ('mdc_updt_dt_tm', models.DateTimeField(blank=True, null=True)),
                ('load_dt_tm', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
