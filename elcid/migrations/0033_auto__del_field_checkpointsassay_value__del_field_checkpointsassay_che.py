# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'CheckpointsAssay.value'
        db.delete_column(u'elcid_checkpointsassay', 'value')

        # Deleting field 'CheckpointsAssay.checkpoint'
        db.delete_column(u'elcid_checkpointsassay', 'checkpoint')

        # Adding field 'CheckpointsAssay.acc'
        db.add_column(u'elcid_checkpointsassay', 'acc',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.act_mir'
        db.add_column(u'elcid_checkpointsassay', 'act_mir',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.bel'
        db.add_column(u'elcid_checkpointsassay', 'bel',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.cmy_i_mox'
        db.add_column(u'elcid_checkpointsassay', 'cmy_i_mox',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.cmy_ii'
        db.add_column(u'elcid_checkpointsassay', 'cmy_ii',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.ctx_m_1_group'
        db.add_column(u'elcid_checkpointsassay', 'ctx_m_1_group',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.ctx_m_1_like'
        db.add_column(u'elcid_checkpointsassay', 'ctx_m_1_like',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.ctx_m_15_like'
        db.add_column(u'elcid_checkpointsassay', 'ctx_m_15_like',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.ctx_m_2_group'
        db.add_column(u'elcid_checkpointsassay', 'ctx_m_2_group',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.ctx_m_3_like'
        db.add_column(u'elcid_checkpointsassay', 'ctx_m_3_like',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.ctx_m_32_like'
        db.add_column(u'elcid_checkpointsassay', 'ctx_m_32_like',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.ctx_m_8_25_group'
        db.add_column(u'elcid_checkpointsassay', 'ctx_m_8_25_group',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.ctx_m_9_group'
        db.add_column(u'elcid_checkpointsassay', 'ctx_m_9_group',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.dha'
        db.add_column(u'elcid_checkpointsassay', 'dha',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.fox'
        db.add_column(u'elcid_checkpointsassay', 'fox',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.ges'
        db.add_column(u'elcid_checkpointsassay', 'ges',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.gim'
        db.add_column(u'elcid_checkpointsassay', 'gim',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.imp'
        db.add_column(u'elcid_checkpointsassay', 'imp',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.kpc'
        db.add_column(u'elcid_checkpointsassay', 'kpc',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.ndm'
        db.add_column(u'elcid_checkpointsassay', 'ndm',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.oxa_23_like'
        db.add_column(u'elcid_checkpointsassay', 'oxa_23_like',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.oxa_24_like'
        db.add_column(u'elcid_checkpointsassay', 'oxa_24_like',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.oxa_48_like'
        db.add_column(u'elcid_checkpointsassay', 'oxa_48_like',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.oxa_58_like'
        db.add_column(u'elcid_checkpointsassay', 'oxa_58_like',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.per'
        db.add_column(u'elcid_checkpointsassay', 'per',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.shv_e240k'
        db.add_column(u'elcid_checkpointsassay', 'shv_e240k',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.shv_g238a'
        db.add_column(u'elcid_checkpointsassay', 'shv_g238a',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.shv_g238s'
        db.add_column(u'elcid_checkpointsassay', 'shv_g238s',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.shv_wt'
        db.add_column(u'elcid_checkpointsassay', 'shv_wt',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.spm'
        db.add_column(u'elcid_checkpointsassay', 'spm',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.tem_e104k'
        db.add_column(u'elcid_checkpointsassay', 'tem_e104k',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.tem_g238s'
        db.add_column(u'elcid_checkpointsassay', 'tem_g238s',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.tem_r164c'
        db.add_column(u'elcid_checkpointsassay', 'tem_r164c',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.tem_r164h'
        db.add_column(u'elcid_checkpointsassay', 'tem_r164h',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.tem_r164s'
        db.add_column(u'elcid_checkpointsassay', 'tem_r164s',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.tem_wt'
        db.add_column(u'elcid_checkpointsassay', 'tem_wt',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.veb'
        db.add_column(u'elcid_checkpointsassay', 'veb',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.vim'
        db.add_column(u'elcid_checkpointsassay', 'vim',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'CheckpointsAssay.value'
        db.add_column(u'elcid_checkpointsassay', 'value',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'CheckpointsAssay.checkpoint'
        db.add_column(u'elcid_checkpointsassay', 'checkpoint',
                      self.gf('django.db.models.fields.CharField')(max_length='200', null=True, blank=True),
                      keep_default=False)

        # Deleting field 'CheckpointsAssay.acc'
        db.delete_column(u'elcid_checkpointsassay', 'acc')

        # Deleting field 'CheckpointsAssay.act_mir'
        db.delete_column(u'elcid_checkpointsassay', 'act_mir')

        # Deleting field 'CheckpointsAssay.bel'
        db.delete_column(u'elcid_checkpointsassay', 'bel')

        # Deleting field 'CheckpointsAssay.cmy_i_mox'
        db.delete_column(u'elcid_checkpointsassay', 'cmy_i_mox')

        # Deleting field 'CheckpointsAssay.cmy_ii'
        db.delete_column(u'elcid_checkpointsassay', 'cmy_ii')

        # Deleting field 'CheckpointsAssay.ctx_m_1_group'
        db.delete_column(u'elcid_checkpointsassay', 'ctx_m_1_group')

        # Deleting field 'CheckpointsAssay.ctx_m_1_like'
        db.delete_column(u'elcid_checkpointsassay', 'ctx_m_1_like')

        # Deleting field 'CheckpointsAssay.ctx_m_15_like'
        db.delete_column(u'elcid_checkpointsassay', 'ctx_m_15_like')

        # Deleting field 'CheckpointsAssay.ctx_m_2_group'
        db.delete_column(u'elcid_checkpointsassay', 'ctx_m_2_group')

        # Deleting field 'CheckpointsAssay.ctx_m_3_like'
        db.delete_column(u'elcid_checkpointsassay', 'ctx_m_3_like')

        # Deleting field 'CheckpointsAssay.ctx_m_32_like'
        db.delete_column(u'elcid_checkpointsassay', 'ctx_m_32_like')

        # Deleting field 'CheckpointsAssay.ctx_m_8_25_group'
        db.delete_column(u'elcid_checkpointsassay', 'ctx_m_8_25_group')

        # Deleting field 'CheckpointsAssay.ctx_m_9_group'
        db.delete_column(u'elcid_checkpointsassay', 'ctx_m_9_group')

        # Deleting field 'CheckpointsAssay.dha'
        db.delete_column(u'elcid_checkpointsassay', 'dha')

        # Deleting field 'CheckpointsAssay.fox'
        db.delete_column(u'elcid_checkpointsassay', 'fox')

        # Deleting field 'CheckpointsAssay.ges'
        db.delete_column(u'elcid_checkpointsassay', 'ges')

        # Deleting field 'CheckpointsAssay.gim'
        db.delete_column(u'elcid_checkpointsassay', 'gim')

        # Deleting field 'CheckpointsAssay.imp'
        db.delete_column(u'elcid_checkpointsassay', 'imp')

        # Deleting field 'CheckpointsAssay.kpc'
        db.delete_column(u'elcid_checkpointsassay', 'kpc')

        # Deleting field 'CheckpointsAssay.ndm'
        db.delete_column(u'elcid_checkpointsassay', 'ndm')

        # Deleting field 'CheckpointsAssay.oxa_23_like'
        db.delete_column(u'elcid_checkpointsassay', 'oxa_23_like')

        # Deleting field 'CheckpointsAssay.oxa_24_like'
        db.delete_column(u'elcid_checkpointsassay', 'oxa_24_like')

        # Deleting field 'CheckpointsAssay.oxa_48_like'
        db.delete_column(u'elcid_checkpointsassay', 'oxa_48_like')

        # Deleting field 'CheckpointsAssay.oxa_58_like'
        db.delete_column(u'elcid_checkpointsassay', 'oxa_58_like')

        # Deleting field 'CheckpointsAssay.per'
        db.delete_column(u'elcid_checkpointsassay', 'per')

        # Deleting field 'CheckpointsAssay.shv_e240k'
        db.delete_column(u'elcid_checkpointsassay', 'shv_e240k')

        # Deleting field 'CheckpointsAssay.shv_g238a'
        db.delete_column(u'elcid_checkpointsassay', 'shv_g238a')

        # Deleting field 'CheckpointsAssay.shv_g238s'
        db.delete_column(u'elcid_checkpointsassay', 'shv_g238s')

        # Deleting field 'CheckpointsAssay.shv_wt'
        db.delete_column(u'elcid_checkpointsassay', 'shv_wt')

        # Deleting field 'CheckpointsAssay.spm'
        db.delete_column(u'elcid_checkpointsassay', 'spm')

        # Deleting field 'CheckpointsAssay.tem_e104k'
        db.delete_column(u'elcid_checkpointsassay', 'tem_e104k')

        # Deleting field 'CheckpointsAssay.tem_g238s'
        db.delete_column(u'elcid_checkpointsassay', 'tem_g238s')

        # Deleting field 'CheckpointsAssay.tem_r164c'
        db.delete_column(u'elcid_checkpointsassay', 'tem_r164c')

        # Deleting field 'CheckpointsAssay.tem_r164h'
        db.delete_column(u'elcid_checkpointsassay', 'tem_r164h')

        # Deleting field 'CheckpointsAssay.tem_r164s'
        db.delete_column(u'elcid_checkpointsassay', 'tem_r164s')

        # Deleting field 'CheckpointsAssay.tem_wt'
        db.delete_column(u'elcid_checkpointsassay', 'tem_wt')

        # Deleting field 'CheckpointsAssay.veb'
        db.delete_column(u'elcid_checkpointsassay', 'veb')

        # Deleting field 'CheckpointsAssay.vim'
        db.delete_column(u'elcid_checkpointsassay', 'vim')


    models = {
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'elcid.allergies': {
            'Meta': {'object_name': 'Allergies'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'drug_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial']", 'null': 'True', 'blank': 'True'}),
            'drug_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Patient']"}),
            'provisional': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'elcid.antimicrobial': {
            'Meta': {'object_name': 'Antimicrobial'},
            'adverse_event_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial_adverse_event']", 'null': 'True', 'blank': 'True'}),
            'adverse_event_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'delivered_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dose': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'drug_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial']", 'null': 'True', 'blank': 'True'}),
            'drug_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            'frequency_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial_frequency']", 'null': 'True', 'blank': 'True'}),
            'frequency_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'route_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Antimicrobial_route']", 'null': 'True', 'blank': 'True'}),
            'route_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        u'elcid.antimicrobial_susceptability': {
            'Meta': {'ordering': "['name']", 'object_name': 'Antimicrobial_susceptability'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'elcid.appointment': {
            'Meta': {'object_name': 'Appointment'},
            'appointment_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'appointment_with': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'elcid.carers': {
            'Meta': {'object_name': 'Carers'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'gp': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.GP']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nurse': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.CommunityNurse']", 'null': 'True', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Patient']"})
        },
        u'elcid.checkpoints_assay': {
            'Meta': {'ordering': "['name']", 'object_name': 'Checkpoints_assay'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'elcid.checkpointsassay': {
            'Meta': {'object_name': 'CheckpointsAssay'},
            'acc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'act_mir': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'bel': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cmy_i_mox': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cmy_ii': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'ctx_m_15_like': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ctx_m_1_group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ctx_m_1_like': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ctx_m_2_group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ctx_m_32_like': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ctx_m_3_like': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ctx_m_8_25_group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ctx_m_9_group': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'dha': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            'fox': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ges': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gim': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kpc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ndm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oxa_23_like': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oxa_24_like': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oxa_48_like': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oxa_58_like': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'per': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shv_e240k': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shv_g238a': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shv_g238s': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shv_wt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'spm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tem_e104k': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tem_g238s': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tem_r164c': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tem_r164h': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tem_r164s': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tem_wt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'veb': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vim': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'elcid.contactdetails': {
            'Meta': {'object_name': 'ContactDetails'},
            'address_line1': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'address_line2': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Patient']"}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'tel1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tel2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'elcid.demographics': {
            'Meta': {'object_name': 'Demographics'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'country_of_birth_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Destination']", 'null': 'True', 'blank': 'True'}),
            'country_of_birth_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'ethnicity': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'hospital_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'nhs_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Patient']"})
        },
        u'elcid.diagnosis': {
            'Meta': {'object_name': 'Diagnosis'},
            'condition_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Condition']", 'null': 'True', 'blank': 'True'}),
            'condition_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date_of_diagnosis': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provisional': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'elcid.generalnote': {
            'Meta': {'object_name': 'GeneralNote'},
            'comment': ('django.db.models.fields.TextField', [], {}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'elcid.labspecimin': {
            'Meta': {'object_name': 'LabSpecimin'},
            'appearance_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elcid.Specimin_appearance']", 'null': 'True', 'blank': 'True'}),
            'appearance_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'biobanking': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'biobanking_box': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date_biobanked': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_collected': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_tested': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            'epithelial_cell': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'external_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'specimin_type_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elcid.Specimin']", 'null': 'True', 'blank': 'True'}),
            'specimin_type_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'volume_biobanked': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'white_blood_cells': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        u'elcid.labtest': {
            'Meta': {'object_name': 'LabTest'},
            'antimicrobial_susceptability_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elcid.Antimicrobial_susceptability']", 'null': 'True', 'blank': 'True'}),
            'antimicrobial_susceptability_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'biobanked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'carbapenemase': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date_ordered': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_retrieved': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            'esbl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'freezer_box_number': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organism_details_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elcid.Organism_details']", 'null': 'True', 'blank': 'True'}),
            'organism_details_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'retrieved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'significant_organism': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'test': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'elcid.line': {
            'Meta': {'object_name': 'Line'},
            'complications_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Line_complication']", 'null': 'True', 'blank': 'True'}),
            'complications_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            'external_length': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inserted_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'insertion_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'insertion_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'line_type_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Line_type']", 'null': 'True', 'blank': 'True'}),
            'line_type_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'removal_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'removal_reason_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Line_removal_reason']", 'null': 'True', 'blank': 'True'}),
            'removal_reason_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'removal_time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'site_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Line_site']", 'null': 'True', 'blank': 'True'}),
            'site_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'special_instructions': ('django.db.models.fields.TextField', [], {})
        },
        u'elcid.location': {
            'Meta': {'object_name': 'Location'},
            'bed': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'category': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            'hospital': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opat_discharge': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'opat_referral': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'opat_referral_consultant': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'opat_referral_route': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'opat_referral_team': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'opat_referral_team_address': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'ward': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'elcid.microbiologyinput': {
            'Meta': {'object_name': 'MicrobiologyInput'},
            'agreed_plan': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'change_in_antibiotic_prescription': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'clinical_advice_given': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'clinical_discussion': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'discussed_with': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'infection_control_advice_given': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'reason_for_interaction_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Clinical_advice_reason_for_interaction']", 'null': 'True', 'blank': 'True'}),
            'reason_for_interaction_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'referred_to_opat': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'elcid.microbiologytest': {
            'Meta': {'object_name': 'MicrobiologyTest'},
            'adenovirus': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'anti_hbcore_igg': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'anti_hbcore_igm': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'anti_hbs': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'c_difficile_antigen': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'c_difficile_toxin': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'cmv': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'cryptosporidium': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'date_ordered': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'ebna_igg': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'ebv': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'entamoeba_histolytica': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'enterovirus': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            'giardia': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'hbsag': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'hsv': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'hsv_1': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'hsv_2': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'igg': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'igm': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'influenza_a': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'influenza_b': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'metapneumovirus': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'microscopy': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'norovirus': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'organism': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'parainfluenza': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'parasitaemia': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'resistant_antibiotics': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'rotavirus': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'rpr': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'rsv': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'sensitive_antibiotics': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'species': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'syphilis': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'test': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'tppa': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'vca_igg': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'vca_igm': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'viral_load': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'}),
            'vzv': ('django.db.models.fields.CharField', [], {'max_length': '20', 'blank': 'True'})
        },
        u'elcid.opatlineassessment': {
            'Meta': {'object_name': 'OPATLineAssessment'},
            'assessment_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'bionector_change_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'dressing_change_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'dressing_change_reason': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'dressing_type': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'vip_score': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'elcid.opatmeta': {
            'Meta': {'object_name': 'OPATMeta'},
            'cause_of_death': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'death_category': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'deceased': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'readmission_cause': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'readmitted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'reason_for_stopping': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'review_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'stopping_iv_details': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'treatment_outcome': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'unplanned_stop_reason_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['elcid.Unplanned_stop']", 'null': 'True', 'blank': 'True'}),
            'unplanned_stop_reason_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'elcid.opatoutstandingissues': {
            'Meta': {'object_name': 'OPATOutstandingIssues'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'elcid.opatrejection': {
            'Meta': {'object_name': 'OPATRejection'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'decided_by': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'elcid.opatreview': {
            'Meta': {'object_name': 'OPATReview'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'discussion': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'next_review': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'opat_plan': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'rv_type': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'time': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'elcid.organism_details': {
            'Meta': {'ordering': "['name']", 'object_name': 'Organism_details'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'elcid.pastmedicalhistory': {
            'Meta': {'object_name': 'PastMedicalHistory'},
            'condition_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Condition']", 'null': 'True', 'blank': 'True'}),
            'condition_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'blank': 'True'})
        },
        u'elcid.presentingcomplaint': {
            'Meta': {'object_name': 'PresentingComplaint'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'details': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'symptom_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Symptom']", 'null': 'True', 'blank': 'True'}),
            'symptom_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'elcid.primarydiagnosis': {
            'Meta': {'object_name': 'PrimaryDiagnosis'},
            'condition_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Condition']", 'null': 'True', 'blank': 'True'}),
            'condition_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'elcid.ridrtitest': {
            'Meta': {'object_name': 'RidRTITest'},
            'acinetobacter_baumannii': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'aspergillus_spp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cap_coronavirus_229e': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cap_coronavirus_hku1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cap_coronavirus_nl63': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'cap_coronavirus_oc43': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'chlamydophila_pneumoniae': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'cryptococcus_neoformans': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ctx_m': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enterobacter_spp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            'haemophilus_influenzae': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'influenza_a': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'influenza_b': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'klebsiella_spp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'kpc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'legionella_pneumophila': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'meca': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mtc': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mycoplasma_pneumoniae': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'ndm': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nocardia_spp': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'notes': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'orti_coronavirus_229e': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'orti_coronavirus_hku1': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'orti_coronavirus_nl63': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'orti_coronavirus_oc43': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'oxa_48': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pneumocystis_jiroveci': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'pseudomonas_aeruginosa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rhodococcus_equi': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rsva': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'rsvb': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'senotophomonas_maltophilia': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shv_esbl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'staphylococcus_aureus': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'staphylococcus_mrsa': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'streptococcus_pneumoniae': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'tem_esbl': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'test': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'vim': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'elcid.secondarydiagnosis': {
            'Meta': {'object_name': 'SecondaryDiagnosis'},
            'co_priamary': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'condition_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Condition']", 'null': 'True', 'blank': 'True'}),
            'condition_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'elcid.specimin': {
            'Meta': {'ordering': "['name']", 'object_name': 'Specimin'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'elcid.specimin_appearance': {
            'Meta': {'ordering': "['name']", 'object_name': 'Specimin_appearance'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'elcid.todo': {
            'Meta': {'object_name': 'Todo'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'elcid.travel': {
            'Meta': {'object_name': 'Travel'},
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'dates': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'destination_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Destination']", 'null': 'True', 'blank': 'True'}),
            'destination_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'episode': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Episode']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'reason_for_travel_fk': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Travel_reason']", 'null': 'True', 'blank': 'True'}),
            'reason_for_travel_ft': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'specific_exposures': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'elcid.unplanned_stop': {
            'Meta': {'ordering': "['name']", 'object_name': 'Unplanned_stop'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.antimicrobial': {
            'Meta': {'ordering': "['name']", 'object_name': 'Antimicrobial'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.antimicrobial_adverse_event': {
            'Meta': {'ordering': "['name']", 'object_name': 'Antimicrobial_adverse_event'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.antimicrobial_frequency': {
            'Meta': {'ordering': "['name']", 'object_name': 'Antimicrobial_frequency'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.antimicrobial_route': {
            'Meta': {'ordering': "['name']", 'object_name': 'Antimicrobial_route'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.clinical_advice_reason_for_interaction': {
            'Meta': {'ordering': "['name']", 'object_name': 'Clinical_advice_reason_for_interaction'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.communitynurse': {
            'Meta': {'object_name': 'CommunityNurse'},
            'address_line1': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'address_line2': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'tel1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tel2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'opal.condition': {
            'Meta': {'ordering': "['name']", 'object_name': 'Condition'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.destination': {
            'Meta': {'ordering': "['name']", 'object_name': 'Destination'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.episode': {
            'Meta': {'object_name': 'Episode'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'consistency_token': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'date_of_admission': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'discharge_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'patient': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['opal.Patient']"})
        },
        u'opal.gp': {
            'Meta': {'object_name': 'GP'},
            'address_line1': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'address_line2': ('django.db.models.fields.CharField', [], {'max_length': '45', 'null': 'True', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'county': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'post_code': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'tel1': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'tel2': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        u'opal.line_complication': {
            'Meta': {'ordering': "['name']", 'object_name': 'Line_complication'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.line_removal_reason': {
            'Meta': {'ordering': "['name']", 'object_name': 'Line_removal_reason'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.line_site': {
            'Meta': {'ordering': "['name']", 'object_name': 'Line_site'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.line_type': {
            'Meta': {'ordering': "['name']", 'object_name': 'Line_type'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.patient': {
            'Meta': {'object_name': 'Patient'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'opal.symptom': {
            'Meta': {'ordering': "['name']", 'object_name': 'Symptom'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'opal.synonym': {
            'Meta': {'unique_together': "(('name', 'content_type'),)", 'object_name': 'Synonym'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'object_id': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        u'opal.travel_reason': {
            'Meta': {'ordering': "['name']", 'object_name': 'Travel_reason'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        }
    }

    complete_apps = ['elcid']