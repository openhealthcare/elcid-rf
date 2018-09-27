import datetime
from intrahospital_api import loader
from intrahospital_api import constants
from elcid import models
from lab import models as lmodels
from django.db import transaction
from django.conf import settings

from opal.core.pathway.pathways import (
    RedirectsToPatientMixin,
    Step,
    PagePathway,
    WizardPathway,
)


class IgnoreDemographicsMixin(object):
    def save(self, data, user=None, episode=None, patient=None):
        if patient:
            if patient.demographics_set.exclude(external_system=None).exists():
                data.pop("demographics")
        return super(IgnoreDemographicsMixin, self).save(
            data, user=user, episode=episode, patient=patient
        )


class SaveTaggingMixin(object):
    @transaction.atomic
    def save(self, data, user=None, episode=None, patient=None):
        tagging = data.pop("tagging", [])
        patient, episode = super(SaveTaggingMixin, self).save(
            data, user=user, episode=episode, patient=patient
        )

        if tagging:
            tag_names = [n for n, v in list(tagging[0].items()) if v]
            episode.set_tag_names(tag_names, user)
        return patient, episode


class RemovePatientPathway(IgnoreDemographicsMixin, SaveTaggingMixin, PagePathway):
    icon = "fa fa-sign-out"
    display_name = "Remove"
    finish_button_text = "Remove"
    finish_button_icon = "fa fa-sign-out"
    modal_template = "pathway/modal_only_cancel.html"
    slug = "remove"
    steps = (
        Step(
            display_name="No",
            template="pathway/remove.html",
            step_controller="RemovePatientCtrl"
        ),
    )


class AddPatientPathway(SaveTaggingMixin, WizardPathway):
    display_name = "Add Patient"
    slug = 'add_patient'
    finish_button_text = "Add Patient"
    finish_button_icon = "fa fa-plus"

    steps = (
        Step(
            template="pathway/rfh_find_patient_form.html",
            step_controller="RfhFindPatientCtrl",
            display_name="Find patient",
            icon="fa fa-user"
        ),
        Step(
            model=models.Location,
            template="pathway/blood_culture_location.html",
            step_controller="TaggingStepCtrl",
        ),
    )

    @transaction.atomic
    def save(self, data, user, patient=None, episode=None):
        """
            saves the patient.

            if the patient already exists, create a new episode.

            if the patient doesn't exist and we're gloss enabled query gloss.

            we expect the patient to have already been updated by gloss
        """
        saved_patient, saved_episode = super(AddPatientPathway, self).save(
            data, user=user, patient=patient, episode=episode
        )

        # there should always be a new episode
        saved_episode.start = datetime.date.today()
        saved_episode.save()

        # if the patient its a new patient and we have
        # got their demographics from the upstream api service
        # bring in their lab tests
        if not patient and settings.ADD_PATIENT_LAB_TESTS:
            demo_system = data["demographics"][0].get("external_system")
            if demo_system == constants.EXTERNAL_SYSTEM:
                loader.load_patient(saved_patient)

        return saved_patient, saved_episode


class CernerDemoPathway(IgnoreDemographicsMixin, SaveTaggingMixin, RedirectsToPatientMixin, PagePathway):
    display_name = 'Cerner Powerchart Template'
    slug = 'cernerdemo'

    steps = (
        models.Demographics,
        models.Location,
        Step(
            template="pathway/blood_culture.html",
            display_name="Blood Culture",
            icon="fa fa-crosshairs",
            step_controller="BloodCulturePathwayFormCtrl",
            model=lmodels.LabTest
        ),
        models.Procedure,
        models.Diagnosis,
        models.Infection,
        models.Line,
        models.Antimicrobial,
        models.Imaging,
        models.FinalDiagnosis,
        models.MicrobiologyInput,
        Step(
            template="pathway/cernerletter.html",
            display_name="Clinical note",
            icon="fa fa-envelope"
        )
    )

    @transaction.atomic
    def save(self, data, user=None, episode=None, patient=None):
        return super(CernerDemoPathway, self).save(
            data, user=user, patient=patient, episode=episode
        )


class BloodCultureStep(Step):
    template = "pathway/blood_culture.html"
    display_name = "Blood Culture"
    icon = "fa fa-crosshairs"
    step_controller = "BloodCulturePathwayFormCtrl"
    model = lmodels.LabTest

    def pre_save(self, data, user, patient=None, episode=None):
        existing_data = data.get(lmodels.LabTest.get_api_name(), [])
        ids = [i["id"] for i in existing_data if "id" in i]
        existing = lmodels.LabTest.objects.filter(patient=patient)
        existing = existing.filter(
            external_system=None
        )
        existing.exclude(id__in=ids).delete()


class BloodCulturePathway(IgnoreDemographicsMixin, PagePathway):
    display_name = "Blood Culture"
    slug = "blood_culture"

    steps = (
        BloodCultureStep(),
    )
