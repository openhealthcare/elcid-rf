import datetime
from django.utils import timezone
from django.urls import reverse
from opal.core.test import OpalTestCase
from plugins.appointments.models import Appointment
from plugins.tb import episode_categories, views, constants


class AppointmentListTestCase(OpalTestCase):
    def setUp(self):
        self.user
        self.assertTrue(
            self.client.login(
                username=self.USERNAME,
                password=self.PASSWORD
            )
        )
        self.url = reverse("tb_clinic_list")

    def test_context_data_today(self):
        patient, episode = self.new_patient_and_episode_please()
        demographics = patient.demographics()
        now = timezone.now()
        pcr = patient.lab_tests.create(
            test_name="TB PCR TEST"
        )
        pcr.observation_set.create(
            observation_name="TB PCR",
            observation_datetime=now - datetime.timedelta(4),
            observation_value="not used~",
            test=pcr
        )
        culture = patient.lab_tests.create(
            test_name="AFB : CULTURE"
        )
        culture.observation_set.create(
            observation_name="TB: Culture Result",
            observation_datetime=now - datetime.timedelta(3),
            observation_value="some value~",
            test=culture
        )
        episode.category_name = episode_categories.TbEpisode.display_name
        consultation = episode.patientconsultation_set.create(
            when=now,
            reason_for_interaction="Because",
            initials="MU"
        )
        episode.save()
        appointment = Appointment.objects.create(
            derived_appointment_type=constants.TB_APPOINTMENT_CODES[0],
            start_datetime=now,
            patient=patient
        )
        ctx = self.client.get(self.url).context
        self.assertEqual(len(ctx["rows_by_date"]), 1)
        dt, rows = list(ctx["rows_by_date"].items())[0]
        self.assertEqual(dt, now.date())
        self.assertEqual(len(rows), 1)
        row = rows[0]
        self.assertEqual(
            row[0], appointment
        )
        self.assertEqual(
            row[1], demographics
        )
        self.assertEqual(
            row[2], episode
        )
        self.assertEqual(
            row[3], consultation
        )
        obs_values = row[4]
        self.assertEqual(
            obs_values["test_type"], "AFB Culture"
        )
        self.assertEqual(
            obs_values["value"], "some value"
        )
        self.assertEqual(
            obs_values["datetime"], now - datetime.timedelta(3)
        )

    def test_context_data_yesterday(self):
        patient, episode = self.new_patient_and_episode_please()
        episode.category_name = episode_categories.TbEpisode.display_name
        episode.save()
        Appointment.objects.create(
            derived_appointment_type=constants.TB_APPOINTMENT_CODES[0],
            start_datetime=timezone.now() - datetime.timedelta(1),
            patient=patient
        )
        ctx = self.client.get(self.url).context
        ctx["rows"] = []

    def test_get_correct_lab_test_on_the_same_day(self):
        """
        If we have 2 results that come back at the
        same time show the culture
        """
        patient, _ = self.new_patient_and_episode_please()
        yesterday = timezone.now() - datetime.timedelta(1)
        before = timezone.now() - datetime.timedelta(2)
        old_pcr = patient.lab_tests.create(
            test_name="TB PCR TEST"
        )
        old_pcr.observation_set.create(
            observation_name="TB PCR",
            observation_datetime=before
        )
        pcr = patient.lab_tests.create(
            test_name="TB PCR TEST"
        )
        pcr.observation_set.create(
            observation_name="TB PCR",
            observation_datetime=yesterday
        )
        afb = patient.lab_tests.create(
            test_name="AFB : CULTURE"
        )
        culture_result = afb.observation_set.create(
            observation_name="TB: Culture Result",
            observation_datetime=yesterday
        )
        view = views.ClinicList()
        patient_id_to_observation = view.patient_id_to_recent_observation(
            [patient.id]
        )
        self.assertEqual(
            patient_id_to_observation[patient.id], culture_result
        )
