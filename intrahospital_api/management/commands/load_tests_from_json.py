"""
A management command that loads in some json
as outputted by the prod api
"""
import json
from django.core.management.base import BaseCommand
from django.db import transaction
from opal import models
from elcid import models as emodels
from lab import models as lmodels
from intrahospital_api.services.lab_tests import service


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('patient_id', type=int)
        parser.add_argument('file_name', type=str)

    @transaction.atomic
    def process(self, patient, results):
        lmodels.LabTest.objects.filter(
            patient=patient
        ).filter(
            lab_test_type__in=[
                emodels.UpstreamLabTest.get_display_name(),
                emodels.UpstreamBloodCulture.get_display_name(),
            ]
        ).delete()
        service.update_patient(patient, results)

    def handle(self, patient_id, file_name, *args, **options):
        # we assume that there is a user called super
        # which there won't be on prod, but we shouldn't
        # be running this on prod
        with open(file_name) as f:
            results = json.load(f)
        patient = models.Patient.objects.get(id=patient_id)
        self.process(patient, results)
        self.stdout.write("success")
