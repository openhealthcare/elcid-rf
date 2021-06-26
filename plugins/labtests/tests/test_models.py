import datetime
import copy
from django.utils import timezone
from opal.core.test import OpalTestCase
from opal.models import Patient
from plugins.labtests import models


class LabTestTestCase(OpalTestCase):
    def setUp(self):
        self.api_dict = {
            "clinical_info":  'testing',
            "datetime_ordered": "17/07/2015 04:15:10",
            "external_identifier": "11111",
            "site": u'^&        ^',
            "status": "Sucess",
            "test_code": "AN12",
            "test_name": "Anti-CV2 (CRMP-5) antibodies",
            "accession_number": "123456",
            "encounter_consultant_name": "DR. M. SMITH",
            "encounter_location_name": "RAL 6 NORTH",
            "encounter_location_code": "6N",
            "observations": [{
                "last_updated": "18/07/2015 04:15:10",
                "observation_datetime": "19/07/2015 04:15:10",
                "observation_name": "Aerobic bottle culture",
                "observation_number": "12312",
                "observation_value": "123",
                "reference_range": "3.5 - 11",
                "units": "g"
            }]
        }
        self.patient, _ = self.new_patient_and_episode_please()

    def create_lab_test(self):
        lt = self.patient.lab_tests.create(**{
            "clinical_info":  'testing',
            "datetime_ordered": timezone.make_aware(datetime.datetime(2015, 6, 17, 4, 15, 10)),
            "lab_number": "11111",
            "site": u'^&        ^',
            "status": "Sucess",
            "test_code": "AN12",
            "test_name": "Anti-CV2 (CRMP-5) antibodies",
        })

        lt.observation_set.create(
            last_updated=timezone.make_aware(datetime.datetime(2015, 6, 18, 4, 15, 10)),
            observation_datetime=timezone.make_aware(datetime.datetime(2015, 4, 15, 4, 15, 10)),
            observation_number="12312",
            reference_range="3.5 - 11",
            units="g",
            observation_value="234",
            observation_name="Aerobic bottle culture"
        )
        return lt

    def test_create_from_api_dict_simple(self):
        lt = models.LabTest()
        lt.create_from_api_dict(self.patient, self.api_dict)
        self.assertEqual(
            lt.patient, self.patient
        )
        self.assertEqual(
            lt.clinical_info, 'testing'
        )
        self.assertEqual(
            lt.datetime_ordered,
            timezone.make_aware(datetime.datetime(
                2015, 7, 17, 4, 15, 10
            ))
        )
        self.assertEqual(
            lt.lab_number, '11111'
        )
        self.assertEqual(
            lt.status, 'Sucess'
        )
        self.assertEqual(
            lt.test_code, 'AN12'
        )
        self.assertEqual(
            lt.test_name, 'Anti-CV2 (CRMP-5) antibodies'
        )

        self.assertEqual(
            lt.site, '^&        ^'
        )

        obs = lt.observation_set.get()
        self.assertEqual(
            obs.last_updated,
            timezone.make_aware(datetime.datetime(
                2015, 7, 18, 4, 15, 10
            ))
        )
        self.assertEqual(
            obs.observation_datetime,
            timezone.make_aware(datetime.datetime(
                2015, 7, 19, 4, 15, 10
            ))
        )
        self.assertEqual(
            obs.observation_name,
            "Aerobic bottle culture"
        )
        self.assertEqual(
            obs.observation_number,
            "12312"
        )
        self.assertEqual(
            obs.reference_range,
            "3.5 - 11"
        )
        self.assertEqual(
            obs.units,
            "g"
        )
        self.assertEqual(
            obs.observation_value,
            "123"
        )

    def test_create_from_api_dict_datetime_ordered_is_none(self):
        lt = models.LabTest()
        api_dict = copy.deepcopy(self.api_dict)
        api_dict["datetime_ordered"] = None
        lt.create_from_api_dict(self.patient, api_dict)
        self.assertIsNone(lt.datetime_ordered)
        self.assertEqual(lt.test_name, "Anti-CV2 (CRMP-5) antibodies")

    def test_create_from_api_dict_observation_datetime_is_none(self):
        lt = models.LabTest()
        api_dict = copy.deepcopy(self.api_dict)
        api_dict["observations"][0]["observation_datetime"] = None
        lt.create_from_api_dict(self.patient, api_dict)
        obs = lt.observation_set.get()
        self.assertIsNone(obs.observation_datetime)
        self.assertEqual(
            obs.observation_name, "Aerobic bottle culture"
        )

    def test_patient_deletion_behaviour(self):
        self.create_lab_test()
        self.patient.delete()
        self.assertFalse(
            models.LabTest.objects.all().exists()
        )

    def test_lab_test_deletion_behaviour(self):
        lt = self.create_lab_test()
        lt.delete()
        self.assertEqual(
            Patient.objects.get().id, self.patient.id
        )

    def test_observation_deletion_behaviour(self):
        lt = self.create_lab_test()
        obs = lt.observation_set.get()
        obs.delete()
        self.assertEqual(
            models.LabTest.objects.get().id,
            lt.id
        )

    def test_site(self):
        lt = self.create_lab_test()
        lt.site = "S     ^Swab & Tips etc.         &CANS ^"
        self.assertEqual(
            lt.cleaned_site, 'Swab & Tips etc. CANS'
        )
        lt.site = "PDF   ^PD Fluid                 &PERF ^Peritoneal "
        self.assertEqual(
            lt.cleaned_site,
            'PD Fluid Peritoneal'
        )
        lt.site = "^&                              ^"
        self.assertEqual(lt.cleaned_site, '')
        lt.site = "ASF   ^Ascitic Fluid            &ASC  ^"
        self.assertEqual(
            lt.cleaned_site,
            'Ascitic Fluid ASC'
        )
        lt.site = "F     ^Fluid                    &ABD  ^Abdominal"
        self.assertEqual(
            lt.cleaned_site,
            'Fluid Abdominal'
        )
        lt.site = "DONOR ^&     ^"
        self.assertEqual(
            lt.cleaned_site,
            'DONOR'
        )
        lt.site = "B^Blood&         "
        self.assertEqual(
            lt.cleaned_site,
            'Blood'
        )


class ObservationTestCase(OpalTestCase):
    def test_value_numeric(self):
        observation = models.Observation()

        inputs_to_expected_results = (
            ("<1", float(1),),
            ("1>", float(1),),
            (" 1 ", float(1),),
            ("< 1", float(1),),
            (" < 1", float(1),),
            ("1 ~ some other things", float(1),),
            (".1 ", None),
            ("0.1 ", 0.1),
            ("1E", None),
            ("'1'", None),
            ("21.06.2019", None)
        )
        for input_value, expected in inputs_to_expected_results:
            observation.observation_value = input_value
            self.assertEqual(observation.value_numeric, expected)

    def test_cleaned_reference_range(self):
        observation = models.Observation()

        inputs_to_expected_results = (
            ("1.5 - 4", (1.5, 4,)),
            ('0 - 129', (0, 129,)),
            ('-2 - 3', (-2, 3,)),
            ('-5 - -2', (-5, -2,)),
            ('-5 --2', (-5, -2,)),
            ("[      < 17     ]", None),
            ("1-6", (1, 6)),
            (" -   ", None),
            ("  ", None),
        )
        for input_value, expected in inputs_to_expected_results:
            observation.reference_range = input_value
            if expected:
                expected = {"min": expected[0], "max": expected[1]}
            self.assertEqual(observation.cleaned_reference_range, expected)

    def test_is_pending_true(self):
        observation = models.Observation()
        observation.observation_value = 'Pending'
        self.assertTrue(observation.is_pending)

    def test_is_pending_false(self):
        observation = models.Observation()
        observation.observation_value = 'Not pending'
        self.assertFalse(observation.is_pending)

    def test_is_outside_reference_range_is_no_reference_range(self):
        observation = models.Observation()
        observation.reference_range = "-"
        observation.observation_value = "1"
        self.assertIsNone(observation.is_outside_reference_range())

    def test_is_outside_reference_range_is_no_value(self):
        observation = models.Observation()
        observation.reference_range = "1.5 - 4"
        observation.observation_value = "asdf"
        self.assertIsNone(observation.is_outside_reference_range())

    def test_is_outside_reference_range_max(self):
        observation = models.Observation()
        observation.reference_range = "1.5 - 4"
        observation.observation_value = "5"
        self.assertTrue(observation.is_outside_reference_range())

    def test_is_outside_reference_range_min(self):
        observation = models.Observation()
        observation.reference_range = "1.5 - 4"
        observation.observation_value = "0.5"
        self.assertTrue(observation.is_outside_reference_range())

    def test_is_outside_reference_range_false(self):
        observation = models.Observation()
        observation.reference_range = "1.5 - 4"
        observation.observation_value = "3"
        self.assertFalse(observation.is_outside_reference_range())
