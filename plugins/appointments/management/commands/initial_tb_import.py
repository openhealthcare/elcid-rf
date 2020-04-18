"""
Management command to import all patients who have ever
had a TB appointment.
"""
from django.core.management import BaseCommand
from django.db import transaction
from opal.models import Patient

from intrahospital_api.apis.prod_api import ProdApi as ProdAPI
from intrahospital_api import update_demographics, update_lab_tests

from apps.tb import constants as tb_constants
from plugins.appointments.models import Appointment

Q_GET_ALL_TB_APPOINTMENTS = """
SELECT *
FROM VIEW_ElCid_CRS_OUTPATIENTS
WHERE Derived_Appointment_Type LIKE 'Thoracic TB%'
"""

class Command(BaseCommand):


    @transaction.atomic
    def create_patient_for_mrn(self, mrn):
        """
        Create a patient for MRN
        """
        print('Creating {}'.format(mrn))
        patient = Patient.objects.create()
        demographics = patient.demographics()
        demographics.hospital_number = mrn
        demographics.save()
        print('Hitting upstream database for {} demographics'.format(mrn))
        update_demographics.update_patient_demographics(patient)
        print('Hitting upstream database for {} tests'.format(mrn))
        results = self.api.results_for_hospital_number(mrn)
        update_lab_tests.update_tests(patient, results)
        print('Done')
        return patient

    def handle(self, *args, **kwargs):
        """
        Main entrypoint for loading all TB appointments ever.
        """
        raise NotImplementedError('This command has not been refactored - do not run!')
        Appointment.objects.all().delete()

        self.api     = ProdAPI()
        appointments = self.api.execute_hospital_query(Q_GET_ALL_TB_APPOINTMENTS)
        for appointment in appointments:
            mrn = appointment['vPatient_Number']

            if Patient.objects.filter(demographics__hospital_number=mrn).count() == 0:
                patient = self.create_patient_for_mrn(mrn)
            else:
                try:
                    patient = Patient.objects.get(demographics__hospital_number=mrn)
                except:
                    patient = Patient.objects.filter(demographics__hospital_number=mrn).first()

            our_appointment = Appointment(patient=patient)

            for k, v in appointment.items():
                setattr(our_appointment, Appointment.UPSTREAM_FIELDS_TO_MODEL_FIELDS[k], v)

            our_appointment.save()

            if patient.episode_set.filter(category_name="TB").count() == 0:
                patient.create_episode(category_name="TB")
