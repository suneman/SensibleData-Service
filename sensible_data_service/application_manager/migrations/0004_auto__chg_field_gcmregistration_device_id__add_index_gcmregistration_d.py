# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'GcmRegistration.device_id' to match new field type.
        db.rename_column(u'application_manager_gcmregistration', 'device_id', 'device_id_id')
        # Changing field 'GcmRegistration.device_id'
        db.alter_column(u'application_manager_gcmregistration', 'device_id_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['application_manager.Device']))
        # Adding index on 'GcmRegistration', fields ['device_id']
        db.create_index(u'application_manager_gcmregistration', ['device_id_id'])


    def backwards(self, orm):
        # Removing index on 'GcmRegistration', fields ['device_id']
        db.delete_index(u'application_manager_gcmregistration', ['device_id_id'])


        # Renaming column for 'GcmRegistration.device_id' to match new field type.
        db.rename_column(u'application_manager_gcmregistration', 'device_id_id', 'device_id')
        # Changing field 'GcmRegistration.device_id'
        db.alter_column(u'application_manager_gcmregistration', 'device_id', self.gf('django.db.models.fields.CharField')(max_length=256))

    models = {
        u'application_manager.application': {
            'Meta': {'object_name': 'Application'},
            '_id': ('django.db.models.fields.CharField', [], {'default': "'8e2eebb0fc4d8012d9fc'", 'unique': 'True', 'max_length': '20', 'db_index': 'True'}),
            'client': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['oauth2app.Client']", 'null': 'True', 'blank': 'True'}),
            'connector_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'params': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['application_manager.Parameter']", 'null': 'True', 'blank': 'True'}),
            'scopes': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['connectors.Scope']", 'symmetrical': 'False'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'application_manager.device': {
            'Meta': {'object_name': 'Device'},
            'device_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'application_manager.gcmregistration': {
            'Meta': {'object_name': 'GcmRegistration'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['application_manager.Application']", 'null': 'True'}),
            'device_id': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['application_manager.Device']"}),
            'gcm_id': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'application_manager.parameter': {
            'Meta': {'object_name': 'Parameter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '240', 'db_index': 'True'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '240', 'db_index': 'True'})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'connectors.connector': {
            'Meta': {'object_name': 'Connector'},
            'connector_type': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'grant_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'revoke_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        },
        u'connectors.scope': {
            'Meta': {'object_name': 'Scope'},
            'connector': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['connectors.Connector']"}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'scope': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'oauth2app.client': {
            'Meta': {'object_name': 'Client'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'key': ('django.db.models.fields.CharField', [], {'default': "'3063fd7081007e94114beba4f36a2f'", 'unique': 'True', 'max_length': '30', 'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            'redirect_uri': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'}),
            'secret': ('django.db.models.fields.CharField', [], {'default': "'b5aaf4b3d7a5a0aca6e7b86f75e727'", 'unique': 'True', 'max_length': '30'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        }
    }

    complete_apps = ['application_manager']