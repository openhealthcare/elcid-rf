"""
Unittests for the UCLH eLCID OPAL implementation.
"""
import datetime
import json

from django.core.serializers.json import DjangoJSONEncoder
from django.test import TestCase
from django.contrib.auth.models import User
import ffs

from elcid import models
from opal.models import Patient, Episode, Team
from opal import exceptions

HERE = ffs.Path.here()
TEST_DATA = HERE/'test_data'

class DemographicsTest(TestCase):
    fixtures = ['patients_users', 'patients_records']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.patient = Patient.objects.get(pk=1)
        self.demographics = self.patient.demographics_set.get()

    def test_to_dict(self):
        expected_data = {
            'consistency_token': '12345678',
            'patient_id': self.patient.id,
            'id': self.demographics.id,
            'name': 'John Smith',
            'date_of_birth': datetime.date(1972, 6, 20),
            'country_of_birth': '',
            'country_of_birth_fk_id': None,
            'country_of_birth_ft': '',
            'ethnicity': None,
            'gender': None,
            'hospital_number': 'AA1111',
            'nhs_number': None
            }
        self.assertEqual(expected_data, self.demographics.to_dict(self.user))

    def test_update_from_dict(self):
        data = {
            'consistency_token': '12345678',
            'id': self.demographics.id,
            'name': 'Johann Schmidt',
            'date_of_birth': '1972-6-21',
            'hospital_number': 'AA1112',
            }
        self.demographics.update_from_dict(data, self.user)
        demographics = self.patient.demographics_set.get()

        self.assertEqual('Johann Schmidt', demographics.name)
        self.assertEqual(datetime.date(1972, 6, 21), demographics.date_of_birth)
        self.assertEqual('AA1112', demographics.hospital_number)

    def test_update_from_dict_with_missing_consistency_token(self):
        with self.assertRaises(exceptions.APIError):
            self.demographics.update_from_dict({}, self.user)

    def test_update_from_dict_with_incorrect_consistency_token(self):
        with self.assertRaises(exceptions.ConsistencyError):
            self.demographics.update_from_dict({'consistency_token': '87654321'}, self.user)


class LocationTest(TestCase):
    fixtures = ['patients_users', 'patients_records']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.episode = Episode.objects.get(pk=1)
        self.location = self.episode.location_set.get()

    def test_to_dict(self):
        expected_data = {
            'consistency_token': '12345678',
            'episode_id': self.episode.id,
            'id': self.location.id,
            'category': 'Inpatient',
            'hospital': 'UCH',
            'ward': 'T10',
            'bed': '13',
            'opat_discharge': None,
            'opat_referral': None,
            'opat_referral_route': None,
            'opat_referral_team': None,
            'opat_referral_consultant': None,
            'opat_referral_team_address': None,            
            }
        self.assertEqual(expected_data, self.location.to_dict(self.user))

    def test_update_from_dict(self):
        data = {
            'consistency_token': '12345678',
            'id': self.location.id,
            'category': 'Inpatient',
            'hospital': 'HH',
            'ward': 'T10',
            'bed': '13',
            }
        self.location.update_from_dict(data, self.user)
        self.assertEqual('HH', self.location.hospital)


class DiagnosisTest(TestCase):
    fixtures = ['patients_users', 'patients_records', 'patients_options']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.episode = Episode.objects.get(pk=1)
        self.diagnosis = self.episode.diagnosis_set.all()[0]

    def test_to_dict(self):
        expected_data = {
            'consistency_token': '12345678',
            'episode_id': self.episode.id,
            'id': self.diagnosis.id,
            'condition': 'Some condition',
            'condition_fk_id': 1,
            'condition_ft': '',
            'provisional': False,
            'details': '',
            'date_of_diagnosis': datetime.date(2013, 7, 25),
            }
        self.assertEqual(expected_data, self.diagnosis.to_dict(self.user))

    def test_update_from_dict_with_existing_condition(self):
        data = {
            'consistency_token': '12345678',
            'id': self.diagnosis.id,
            'condition': 'Some other condition',
            }
        self.diagnosis.update_from_dict(data, self.user)
        diagnosis = self.episode.diagnosis_set.all()[0]
        self.assertEqual('Some other condition', diagnosis.condition)

    def test_update_from_dict_with_synonym_for_condition(self):
        data = {
            'consistency_token': '12345678',
            'id': self.diagnosis.id,
            'condition': 'Condition synonym',
            }
        self.diagnosis.update_from_dict(data, self.user)
        diagnosis = self.episode.diagnosis_set.all()[0]
        self.assertEqual('Some other condition', diagnosis.condition)

    def test_update_from_dict_with_new_condition(self):
        data = {
            'consistency_token': '12345678',
            'id': self.diagnosis.id,
            'condition': 'New condition',
            }
        self.diagnosis.update_from_dict(data, self.user)
        diagnosis = self.episode.diagnosis_set.all()[0]
        self.assertEqual('New condition', diagnosis.condition)


class ViewsTest(TestCase):
    fixtures = ['patients_users', 'patients_options', 'patients_records']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.assertTrue(self.client.login(username=self.user.username,
                                          password='password'))
        self.patient = Patient.objects.get(pk=1)

    def assertStatusCode(self, path, expected_status_code):
        response = self.client.get(path)
        self.assertEqual(expected_status_code, response.status_code)

    def post_json(self, path, data):
        json_data = json.dumps(data, cls=DjangoJSONEncoder)
        return self.client.post(path, content_type='application/json', data=json_data)

    def put_json(self, path, data):
        json_data = json.dumps(data, cls=DjangoJSONEncoder)
        return self.client.put(path, content_type='application/json', data=json_data)

    def test_try_to_get_patient_detail_for_nonexistent_patient(self):
        self.assertStatusCode('/patient/%s' % 1234, 404)

    def test_search_with_hospital_number(self):
        self.assertStatusCode('/patient/?hospital_number=AA1111', 200)

    def test_search_with_name(self):
        self.assertStatusCode('/patient/?name=John', 200)

    def test_try_to_search_with_no_search_terms(self):
        self.assertStatusCode('/patient/', 400)

    def test_try_to_create_episode_for_existing_patient_with_active_episode(self):
        data = {
            'demographics': self.patient.demographics_set.get().to_dict(self.user),
            'location': {
                'category': 'Inpatient',
                'hospital': 'UCH',
                'ward': 'T13',
                'bed': 10
                }
            }
        response = self.post_json('/episode/', data)
        self.assertEqual(201, response.status_code)

    def test_create_episode_for_new_patient(self):
        data = {
            'demographics': {
                'hospital_number': 'BB2222',
                'name': 'Johann Schmidt',
                'date_of_birth': '1970-06-01'
                },
            'location': {
                'category': 'Inpatient',
                'hospital': 'UCH',
                'ward': 'T13',
                'bed': 10
                },
            'tagging': [{}]
            }
        response = self.post_json('/episode/', data)
        self.assertEqual(201, response.status_code)

    def test_create_episode_for_patient_without_hospital_number(self):
        data = {
            'demographics': {
                'hospital_number': '',
                'name': 'Johann Schmidt',
                'date_of_birth': '1970-06-01'
                },
            'location': {
                'category': 'Inpatient',
                'hospital': 'UCH',
                'ward': 'T13',
                'bed': 10
                },
            'tagging': [{}]
            }
        response = self.post_json('/episode/', data)
        self.assertEqual(201, response.status_code)

    def test_update_demographics_subrecord(self):
        demographics = self.patient.demographics_set.get()
        data = {
            'consistency_token': '12345678',
            'id': demographics.id,
            'name': 'Johann Schmidt',
            'date_of_birth': '1972-6-21',
            'hospital_number': 'AA1112',
            }
        response = self.put_json('/api/v0.1/demographics/%s/' % demographics.id, data)
        self.assertEqual(202, response.status_code)

    def test_try_to_update_nonexistent_demographics_subrecord(self):
        response = self.put_json('/api/v0.1/demographics/1234/', {})
        self.assertEqual(404, response.status_code)

    def test_try_to_update_demographics_subrecord_with_old_consistency_token(self):
        demographics = self.patient.demographics_set.get()
        data = {
            'consistency_token': '87654321',
            'id': demographics.id,
            'name': 'Johann Schmidt',
            'date_of_birth': '1972-6-21',
            'hospital_number': 'AA1112',
            }
        response = self.put_json('/api/v0.1/demographics/%s/' % demographics.id, data)
        self.assertEqual(409, response.status_code)

    def test_delete_demographics_subrecord(self):
        # In real application, client prevents deletion of demographics
        # subrecord.
        demographics = self.patient.demographics_set.get()
        response = self.client.delete('/api/v0.1/demographics/%s/' % demographics.id)
        self.assertEqual(202, response.status_code)

    def test_create_demographics_subrecord(self):
        # In real application, client prevents creation of demographics
        # subrecord.
        data = {
            'patient_id': self.patient.id,
            'episode_id': self.patient.episode_set.all()[0].id,
            'name': 'Johann Schmidt',
            'date_of_birth': '1972-6-21',
            'hospital_number': 'AA1112',
            }
        response = self.post_json('/api/v0.1/demographics/', data)
        self.assertEqual(201, response.status_code)

    def test_patient_list_template_view(self):
        self.assertStatusCode('/templates/episode_list.html/', 200)

    def test_patient_detail_template_view(self):
        self.assertStatusCode('/templates/episode_detail.html/1', 200)

    def test_search_template_view(self):
        self.assertStatusCode('/templates/search.html/', 200)

    def test_add_patient_template_view(self):
        self.assertStatusCode('/templates/modals/add_episode.html/', 200)

    def test_discharge_patient_template_view(self):
        self.assertStatusCode('/templates/modals/discharge_episode.html/', 200)

    def test_delete_item_confirmation_template_view(self):
        self.assertStatusCode('/templates/modals/delete_item_confirmation.html/', 200)

    def test_location_modal_template_view(self):
        self.assertStatusCode('/templates/modals/location.html/', 200)


class ListSchemaViewTest(TestCase):
    fixtures = ['patients_users', 'patients_options', 'patients_records']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.assertTrue(self.client.login(username=self.user.username,
                                          password='password'))
        self.patient = Patient.objects.get(pk=1)
        schema_file = TEST_DATA/'list.schema.json'
        self.schema = schema_file.json_load()

    def assertStatusCode(self, path, expected_status_code):
        response = self.client.get(path)
        self.assertEqual(expected_status_code, response.status_code)


class DetailSchemaViewTest(TestCase):
    fixtures = ['patients_users', 'patients_options', 'patients_records']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.assertTrue(self.client.login(username=self.user.username,
                                          password='password'))
        self.patient = Patient.objects.get(pk=1)
        schema_file = TEST_DATA/'detail.schema.json'
        self.schema = schema_file.json_load()

    def assertStatusCode(self, path, expected_status_code):
        response = self.client.get(path)
        self.assertEqual(expected_status_code, response.status_code)


class ExtractSchemaViewTest(TestCase):
    fixtures = ['patients_users', 'patients_options', 'patients_records']

    def setUp(self):
        self.user = User.objects.get(pk=1)
        self.assertTrue(self.client.login(username=self.user.username,
                                          password='password'))
        self.patient = Patient.objects.get(pk=1)
        schema_file = TEST_DATA/'extract.schema.json'
        self.schema = schema_file.json_load()

    def assertStatusCode(self, path, expected_status_code):
        response = self.client.get(path)
        self.assertEqual(expected_status_code, response.status_code)

