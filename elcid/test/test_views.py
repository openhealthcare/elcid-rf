"""
Unittests for the UCLH eLCID OPAL implementation.
"""
import datetime
import json
from unittest import mock
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import ffs

from opal.core.test import OpalTestCase
from opal.models import Patient
from opal.core.subrecords import subrecords

from elcid import views
from elcid import models
from elcid import episode_categories


HERE = ffs.Path.here()
TEST_DATA = HERE/'test_data'


class ViewsTest(OpalTestCase):
    fixtures = ['patients_users', 'patients_options', 'patients_records']

    def setUp(self):
        self.assertTrue(self.client.login(username=self.user.username,
                                          password=self.PASSWORD))
        self.patient = Patient.objects.get(pk=1)

    def test_try_to_update_nonexistent_demographics_subrecord(self):
        response = self.put_json('/api/v0.1/demographics/1234/', {})
        self.assertEqual(404, response.status_code)

    def test_episode_list_template_view(self):
        self.assertStatusCode('/templates/patient_list.html/team_1', 200)

    def test_episode_detail_template_view(self):
        self.assertStatusCode('/templates/episode_detail.html/1', 200)

    def test_add_patient_template_view(self):
        self.assertStatusCode('/templates/modals/add_episode.html/', 200)

    def test_delete_item_confirmation_template_view(self):
        self.assertStatusCode('/templates/delete_item_confirmation_modal.html/', 200)

    def test_all_modal_templates(self):
        """ This renders all of our modal templates and blows up
            if they fail to render
        """
        for i in subrecords():
            if i.get_form_template():
                url = reverse("{}_modal".format(i.get_api_name()))
                self.assertStatusCode(url, 200)


class DetailSchemaViewTest(OpalTestCase):
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


class ExtractSchemaViewTest(OpalTestCase):
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


class WardSortTestCase(OpalTestCase):
    def test_ward_sort(self):
        wards = [
            "8 West",
            "PITU",
            "ICU 4 East",
            "9 East",
            "8 South",
            "Other",
            "9 North",
            "ICU 4 West",
            "12 West",
            "Outpatients",
        ]

        expected = [
            "8 South",
            "8 West",
            "9 East",
            "9 North",
            "12 West",
            "ICU 4 East",
            "ICU 4 West",
            "Outpatients",
            "PITU",
            "Other"
        ]
        self.assertEqual(
            expected, sorted(wards, key=views.ward_sort_key)
        )

    def test_grouping(self):
        wards = [
            "8 West",
            "8 West",
            "9 East",
            "8 South",
            "9 North",
        ]

        expected = [
            "8 South",
            "8 West",
            "8 West",
            "9 East",
            "9 North",
        ]
        self.assertEqual(
            expected, sorted(wards, key=views.ward_sort_key)
        )


class RenalHandoverTestCase(OpalTestCase):
    def test_vanilla(self):
        patient_1, episode_1 = self.new_patient_and_episode_please()
        episode_1.set_tag_names(["renal"], None)
        patient_1.demographics_set.update(
            first_name="Wilma",
            surname="Flintstone",
            hospital_number="123"
        )
        location = episode_1.location_set.get()
        location.ward = "10 East"
        location.bed = "1"
        location.save()
        microinput = episode_1.microbiologyinput_set.create(
            clinical_discussion=["some_discussion"],
            when=timezone.now() - datetime.timedelta(1)
        )
        diagnosis = episode_1.diagnosis_set.create()
        diagnosis.condition = "Cough"
        diagnosis.save()

        primary_diagnosis = episode_1.primarydiagnosis_set.get()
        primary_diagnosis.condition = "Fever"
        primary_diagnosis.save()

        line = episode_1.line_set.create()
        line.line_type = "Hickman"
        line.save()

        bcs = episode_1.patient.bloodcultureset_set.create(
            lab_number="123",
            date_ordered=timezone.now() - datetime.timedelta(1)
        )

        ctx = views.RenalHandover().get_context_data()
        episode = ctx["ward_and_episodes"][0]["episodes"][0]
        episode['clinical_advices'] = list(episode['clinical_advices'])
        episode['lines'] = list(episode['lines'])
        episode['blood_culture_sets'] = list(episode['blood_culture_sets'])

        self.assertEqual(
            ctx["ward_and_episodes"][0]["ward"], "10 East"
        )

        self.assertEqual(
            ctx["ward_and_episodes"][0]["episodes"], [{
                'name': 'Wilma Flintstone',
                'hospital_number': '123',
                'diagnosis': 'Cough',
                'clinical_advices': [microinput],
                'unit_ward': '10 East/1',
                'primary_diagnosis': 'Fever',
                'lines': [line],
                "blood_culture_sets": [bcs]
            }]
        )

    def test_aggregate_by_ward(self):
        patient_1, episode_1 = self.new_patient_and_episode_please()
        patient_1.demographics_set.update(
            first_name="Wilma",
            surname="Flintstone"
        )
        patient_2, episode_2 = self.new_patient_and_episode_please()
        patient_2.demographics_set.update(
            first_name="Betty",
            surname="Rubble"
        )
        episode_1.set_tag_names(["renal"], None)
        episode_2.set_tag_names(["renal"], None)

        location_1 = episode_1.location_set.get()
        location_1.ward = "10 East"
        location_1.bed = "1"
        location_1.save()
        location_2 = episode_2.location_set.get()
        location_2.ward = "10 East"
        location_2.bed = "2"
        location_2.save()
        ctx = views.RenalHandover().get_context_data()
        result = ctx["ward_and_episodes"][0]
        self.assertEqual(
            result["ward"], "10 East"
        )
        self.assertEqual(
            len(result["episodes"]), 2
        )

    def test_split_by_ward(self):
        patient_1, episode_1 = self.new_patient_and_episode_please()
        patient_1.demographics_set.update(
            first_name="Wilma",
            surname="Flintstone"
        )
        patient_2, episode_2 = self.new_patient_and_episode_please()
        patient_2.demographics_set.update(
            first_name="Betty",
            surname="Rubble"
        )
        episode_1.set_tag_names(["renal"], None)
        episode_2.set_tag_names(["renal"], None)

        location_1 = episode_1.location_set.get()
        location_1.ward = "10 East"
        location_1.bed = "1"
        location_1.save()
        location_2 = episode_2.location_set.get()
        location_2.ward = "10 West"
        location_2.bed = "2"
        location_2.save()
        ctx = views.RenalHandover().get_context_data()
        east_10 = ctx["ward_and_episodes"][0]
        self.assertEqual(
            east_10["ward"], "10 East"
        )
        self.assertEqual(
            len(east_10["episodes"]), 1
        )
        west_10 = ctx["ward_and_episodes"][1]
        self.assertEqual(
            west_10["ward"], "10 West"
        )
        self.assertEqual(
            len(west_10["episodes"]), 1
        )

    def test_aggregate_clinical_advice(self):
        patient, episode_1 = self.new_patient_and_episode_please()

        episode_2 = patient.episode_set.create()
        episode_3 = patient.episode_set.create()

        location = episode_2.location_set.get()
        location.ward = "10 East"
        location.bed = "1"
        location.save()

        episode_2.set_tag_names(["renal"], None)

        first = timezone.now() - datetime.timedelta(4)
        second = timezone.now() - datetime.timedelta(2)
        third = timezone.now() - datetime.timedelta(1)

        episode_1.microbiologyinput_set.create(
            clinical_discussion="second",
            when=second
        )

        episode_2.microbiologyinput_set.create(
            clinical_discussion="first",
            when=first
        )

        episode_3.microbiologyinput_set.create(
            clinical_discussion="third",
            when=third
        )

        ctx = views.RenalHandover().get_context_data()

        self.assertEqual(
            len(ctx["ward_and_episodes"]), 1
        )

        self.assertEqual(
            len(ctx["ward_and_episodes"][0]["episodes"]), 1
        )
        micro_inputs = ctx["ward_and_episodes"][0]["episodes"][0][
            "clinical_advices"
        ]
        discussion = list(micro_inputs.values_list(
            "clinical_discussion", flat=True
        ))
        self.assertEqual(
            discussion, ["first", "second", "third"]
        )

    def test_ignore_old_clinical_advice(self):
        patient, episode = self.new_patient_and_episode_please()
        over_hundred_days = timezone.now().date() - datetime.timedelta(101)
        episode.microbiologyinput_set.create(
            clinical_discussion="something",
            when=over_hundred_days
        )
        location = episode.location_set.get()
        location.ward = "10 East"
        location.bed = "1"
        location.save()

        episode.set_tag_names(["renal"], None)
        ctx = views.RenalHandover().get_context_data()
        ca = ctx["ward_and_episodes"][0]["episodes"][0]["clinical_advices"]
        self.assertEqual(len(ca), 0)

    def test_ignore_old_blood_tests(self):
        patient, episode = self.new_patient_and_episode_please()
        over_hundred_days = timezone.now() - datetime.timedelta(101)
        episode.microbiologyinput_set.create(
            clinical_discussion="something",
            when=over_hundred_days
        )
        location = episode.location_set.get()
        location.ward = "10 East"
        location.bed = "1"
        location.save()
        bcs = episode.patient.bloodcultureset_set.create(
            lab_number="123", date_ordered=over_hundred_days
        )
        episode.set_tag_names(["renal"], None)
        ctx = views.RenalHandover().get_context_data()
        bcs = ctx["ward_and_episodes"][0]["episodes"][0]["blood_culture_sets"]
        self.assertEqual(len(bcs), 0)

    def test_other(self):
        # if the patient has no ward we should just put them in `other`
        patient_1, episode_1 = self.new_patient_and_episode_please()
        patient_1.demographics_set.update(
            first_name="Wilma",
            surname="Flintstone"
        )
        episode_1.set_tag_names(["renal"], None)

        location_1 = episode_1.location_set.get()
        location_1.bed = "1"
        location_1.save()
        ctx = views.RenalHandover().get_context_data()
        self.assertEqual(ctx["ward_and_episodes"][0]["ward"], "Other")
        self.assertEqual(len(ctx["ward_and_episodes"][0]["episodes"]), 1)

    def test_single_patient_with_multiple_episodes(self):
        # if the patient has multiple renal episodes we should just use
        # the most recent
        # if the patient has no ward we should just put them in `other`
        patient_1, episode_1 = self.new_patient_and_episode_please()
        episode_1.start = timezone.now() - datetime.timedelta(2)
        episode_2 = patient_1.episode_set.create(
            start=timezone.now() - datetime.timedelta(1)
        )

        primary_diagnosis = episode_1.primarydiagnosis_set.get()
        primary_diagnosis.condition = "Should not appear"
        primary_diagnosis.save()

        primary_diagnosis = episode_2.primarydiagnosis_set.get()
        primary_diagnosis.condition = "Should appear"
        primary_diagnosis.save()

        episode_1.set_tag_names(["renal"], None)
        episode_2.set_tag_names(["renal"], None)

        ctx = views.RenalHandover().get_context_data()
        self.assertEqual(len(ctx["ward_and_episodes"][0]["episodes"]), 1)

        self.assertEqual(len(ctx["ward_and_episodes"]), 1)
        self.assertEqual(ctx["ward_and_episodes"][0]["ward"], "Other")
        self.assertEqual(len(ctx["ward_and_episodes"][0]["episodes"]), 1)
        self.assertEqual(
            ctx["ward_and_episodes"][0]["episodes"][0]["primary_diagnosis"],
            "Should appear"
        )


class AddAntifungalPatientsTestCase(OpalTestCase):
    def setUp(self):
        self.url = reverse('add_antifungal_patients')

    def login(self):
        self.user
        self.assertTrue(self.client.login(username=self.user.username,
                                          password='password'))

    def test_login_required(self):
        response = self.client.get(self.url)
        self.assertTrue(
            response.url.startswith('/accounts/login/')
        )

    def test_get(self):
        self.login()
        response = self.client.get(self.url)
        self.assertEqual(
            response.template_name,
            ['add_antifungal_patients.html']
        )
        self.assertStatusCode(self.url, 200)

    @mock.patch('elcid.views.loader.load_patient')
    def test_add_patients_that_are_not_found(self, load_patient):
        patient, _ = self.new_patient_and_episode_please()
        patient.demographics_set.update(
            first_name="Jane",
            surname="Doe"
        )
        demographics_dict = patient.demographics().to_dict(self.user)
        demographics_dict.pop("patient_id")
        demographics_dict.pop("id")
        patient.delete()
        self.login()
        result = self.client.post(
            self.url,
            {"demographics": json.dumps([demographics_dict])},
            follow=True
        )
        self.assertEqual(result.status_code, 200)
        patient = Patient.objects.get()
        self.assertEqual(
            patient.demographics().first_name, "Jane"
        )
        self.assertTrue(load_patient.called_once_with(patient))
        self.assertEqual(
            patient.chronicantifungal_set.get().reason,
            models.ChronicAntifungal.DISPENSARY_REPORT
        )

    @mock.patch('elcid.views.loader.load_patient')
    def test_does_not_add_patients_that_exist(self, load_patient):
        patient, _ = self.new_patient_and_episode_please()
        patient.demographics_set.update(
            first_name="Jane",
            surname="Doe"
        )
        demographics_dict = patient.demographics().to_dict(self.user)

        self.login()
        result = self.client.post(
            self.url,
            {"demographics": json.dumps([demographics_dict])},
            follow=True
        )
        self.assertEqual(result.status_code, 200)
        patient = Patient.objects.get()
        self.assertEqual(
            patient.demographics().first_name, "Jane"
        )
        self.assertFalse(load_patient.called)
        self.assertEqual(
            patient.chronicantifungal_set.get().reason,
            models.ChronicAntifungal.DISPENSARY_REPORT
        )

    def test_creates_a_new_antifungal(self):
        patient, _ = self.new_patient_and_episode_please()
        patient.demographics_set.update(
            first_name="Jane",
            surname="Doe"
        )
        patient.chronicantifungal_set.create(
            reason=models.ChronicAntifungal.REASON_TO_INTERACTION
        )
        demographics_dict = patient.demographics().to_dict(self.user)

        self.login()
        result = self.client.post(
            self.url,
            {"demographics": json.dumps([demographics_dict])},
            follow=True
        )
        self.assertEqual(result.status_code, 200)
        patient = Patient.objects.get()
        self.assertEqual(
            patient.chronicantifungal_set.all().count(),
            2
        )

    def test_creates_a_new_infection_service_episode(self):
        patient, episode = self.new_patient_and_episode_please()
        episode.category_name = "TB"
        episode.save()
        patient.demographics_set.update(
            first_name="Jane",
            surname="Doe"
        )
        demographics_dict = patient.demographics().to_dict(self.user)

        self.login()
        result = self.client.post(
            self.url,
            {"demographics": json.dumps([demographics_dict])},
            follow=True
        )
        self.assertEqual(result.status_code, 200)
        patient = Patient.objects.get()
        self.assertEqual(patient.episode_set.count(), 2)
        infectious_episodes = patient.episode_set.filter(
            category_name=episode_categories.InfectionService.display_name
        )
        self.assertEqual(infectious_episodes.count(), 1)
