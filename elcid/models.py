"""
elCID implementation specific models!
"""
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.contrib.contenttypes.models import ContentType
from lab import models as lmodels


import opal.models as omodels

from opal.models import (
    EpisodeSubrecord, PatientSubrecord, ExternallySourcedModel
)
from opal.core.fields import ForeignKeyOrFreeText
from opal.core import lookuplists


def get_for_lookup_list(model, values):
    ct = ContentType.objects.get_for_model(model)
    return model.objects.filter(
        models.Q(name__in=values) |
        models.Q(synonyms__name__in=values, synonyms__content_type=ct)
    )


class Demographics(omodels.Demographics, ExternallySourcedModel):
    _is_singleton = True
    _icon = 'fa fa-user'

    def set_death_indicator(self, value, *args, **kwargs):
        if not value:
            return

    pid_fields = (
        'hospital_number', 'nhs_number', 'surname', 'first_name',
        'middle_name', 'post_code',
    )

    class Meta:
        verbose_name_plural = "Demographics"


class DuplicatePatient(PatientSubrecord):
    _no_admin = True
    _icon = 'fa fa-clone'
    _advanced_searchable = False
    reviewed = models.BooleanField(default=False)
    merged = models.BooleanField(default=False)

    def icon(self):
        return self._icon


class LocationCategory(lookuplists.LookupList):
    pass


class Provenance(lookuplists.LookupList):
    pass


class Location(EpisodeSubrecord):
    _is_singleton = True
    _icon = 'fa fa-map-marker'

    category = ForeignKeyOrFreeText(LocationCategory)
    provenance = ForeignKeyOrFreeText(Provenance)
    hospital = ForeignKeyOrFreeText(omodels.Hospital)
    ward = ForeignKeyOrFreeText(omodels.Ward)
    bed = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        try:
            demographics = self.episode.patient.demographics_set.get()
            return u'Location for {0}({1}) {2} {3} {4} {5}'.format(
                demographics.name,
                demographics.hospital_number,
                self.category,
                self.hospital,
                self.ward,
                self.bed
            )
        except:
            return 'demographics'


class HL7Result(lmodels.ReadOnlyLabTest):
    class Meta:
        verbose_name = "HL7 Result"

    @classmethod
    def get_api_name(cls):
        return "hl7_result"

    def to_dict(self, user):
        """
            we don't serialise a subrecord during episode
            serialisation
        """
        return {
            "lab_test_type": self.__class__.get_display_name(),
            "id": self.id
        }

    def dict_for_view(self, user):
        """
            we serialise the usual way but not via the episode
            serialisation
        """
        return super(HL7Result, self).to_dict(user)

    def update_from_dict(self, data, *args, **kwargs):
        populated = (
            i for i in data.keys() if i != "lab_test_type" and i != "id"
        )
        if not any(populated):
            return

        if "id" not in data:
            if 'patient_id' in data:
                self.patient = omodels.Patient.objects.get(id=data['patient_id'])

            if "external_identifier" not in data:
                raise ValueError(
                    "an external identifier is required in {}".format(data)
                )
            if "external_identifier" in data and data["external_identifier"]:
                existing = self.__class__.objects.filter(
                    patient=self.patient,
                    external_identifier=data["external_identifier"],
                ).first()

                if existing:
                    data["id"] = existing.id
            super(HL7Result, self).update_from_dict(data, *args, **kwargs)

    @classmethod
    def get_relevant_tests(self, patient):
        relevent_tests = [
            "C REACTIVE PROTEIN",
            "FULL BLOOD COUNT",
            "UREA AND ELECTROLYTES",
            "LIVER FUNCTION",
            "LIVER PROFILE",
            "GENTAMICIN LEVEL",
            "CLOTTING SCREEN"
        ]
        six_months_ago = datetime.date.today() - datetime.timedelta(6*30)
        qs = HL7Result.objects.filter(
            patient=patient,
            datetime_ordered__gt=six_months_ago
        ).order_by("datetime_ordered")
        return [i for i in qs if i.extras.get("profile_description") in relevent_tests]


class InfectionSource(lookuplists.LookupList):
    pass


class Infection(EpisodeSubrecord):
    _title = 'Infection related issues'
    _icon = 'fa fa-eyedropper'
    # this needs to be fixed
    source = ForeignKeyOrFreeText(InfectionSource)
    site = models.CharField(max_length=255, blank=True)


class MedicalProcedure(lookuplists.LookupList):
    pass


class SurgicalProcedure(lookuplists.LookupList):
    pass


class Procedure(EpisodeSubrecord):
    _title = 'Operation / Procedures'
    _icon = 'fa fa-sitemap'
    date = models.DateField(blank=True, null=True)
    medical_procedure = ForeignKeyOrFreeText(MedicalProcedure)
    surgical_procedure = ForeignKeyOrFreeText(SurgicalProcedure)


class PrimaryDiagnosisCondition(lookuplists.LookupList): pass


class PrimaryDiagnosis(EpisodeSubrecord):
    """
    This is the confirmed primary diagnosisa
    """
    _is_singleton = True
    _title = 'Primary Diagnosis'
    _icon = 'fa fa-eye'

    condition = ForeignKeyOrFreeText(PrimaryDiagnosisCondition)
    confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Primary diagnoses"


class Consultant(lookuplists.LookupList):
    pass


class Diagnosis(omodels.Diagnosis):
    """
    This is a working-diagnosis list, will often contain things that are
    not technically diagnoses, but is for historical reasons, called diagnosis.
    """


class Iv_stop(lookuplists.LookupList):
    class Meta:
        verbose_name = "IV stop"


class Drug_delivered(lookuplists.LookupList):
    class Meta:
        verbose_name_plural = "Drugs delivered"


class Antimicrobial(EpisodeSubrecord):
    _title = 'Antimicrobials'
    _sort = 'start_date'
    _icon = 'fa fa-flask'
    _modal = 'lg'

    drug          = ForeignKeyOrFreeText(omodels.Antimicrobial)
    dose          = models.CharField(max_length=255, blank=True)
    route         = ForeignKeyOrFreeText(omodels.Antimicrobial_route)
    start_date    = models.DateField(null=True, blank=True)
    end_date      = models.DateField(null=True, blank=True)
    delivered_by  = ForeignKeyOrFreeText(Drug_delivered)
    reason_for_stopping = ForeignKeyOrFreeText(Iv_stop)
    adverse_event = ForeignKeyOrFreeText(omodels.Antimicrobial_adverse_event)
    comments      = models.TextField(blank=True, null=True)
    frequency     = ForeignKeyOrFreeText(omodels.Antimicrobial_frequency)
    no_antimicrobials = models.NullBooleanField(default=False)


class RenalFunction(lookuplists.LookupList):
    pass


class LiverFunction(lookuplists.LookupList):
    pass


class MicrobiologyInput(EpisodeSubrecord):
    _title = 'Clinical Advice'
    _sort = 'when'
    _icon = 'fa fa-comments'
    _modal = 'lg'
    _list_limit = 3
    _angular_service = 'MicrobiologyInput'

    when = models.DateTimeField(null=True, blank=True)
    initials = models.CharField(max_length=255, blank=True)
    reason_for_interaction = ForeignKeyOrFreeText(
        omodels.Clinical_advice_reason_for_interaction
    )
    infection_control = models.TextField(blank=True)
    clinical_discussion = models.TextField(blank=True)
    agreed_plan = models.TextField(blank=True)
    discussed_with = models.CharField(max_length=255, blank=True)
    clinical_advice_given = models.NullBooleanField()
    infection_control_advice_given = models.NullBooleanField()
    change_in_antibiotic_prescription = models.NullBooleanField()
    referred_to_opat = models.NullBooleanField()
    white_cell_count = models.IntegerField(null=True, blank=True)
    c_reactive_protein = models.CharField(max_length=255, blank=True)
    maximum_temperature = models.IntegerField(null=True, blank=True)
    renal_function = ForeignKeyOrFreeText(RenalFunction)
    liver_function = ForeignKeyOrFreeText(LiverFunction)


class Line(EpisodeSubrecord):
    _sort = 'insertion_datetime'
    _icon = 'fa fa-bolt'

    line_type = ForeignKeyOrFreeText(omodels.Line_type)
    site = ForeignKeyOrFreeText(omodels.Line_site)
    insertion_datetime = models.DateTimeField(blank=True, null=True)
    inserted_by = models.CharField(max_length=255, blank=True, null=True)
    external_length = models.CharField(max_length=255, blank=True, null=True)
    removal_datetime = models.DateTimeField(blank=True, null=True)
    complications = ForeignKeyOrFreeText(omodels.Line_complication)
    removal_reason = ForeignKeyOrFreeText(omodels.Line_removal_reason)
    special_instructions = models.TextField()
    button_hole = models.NullBooleanField()
    tunnelled_or_temp = models.CharField(max_length=200, blank=True, null=True)
    fistula = models.NullBooleanField(blank=True, null=True)
    graft = models.NullBooleanField(blank=True, null=True)


class BloodCultureSource(lookuplists.LookupList):
    pass


class RfhObservation(object):
    def __unicode__(self):
        return "{} for {}".format(
            self.observation_type, self.lab_test
        )


class SourceObservation(lmodels.Observation, RfhObservation):
    class Meta:
        proxy = True
        auto_created = True

    lookup_list = BloodCultureSource


class BloodCultureMixin(object):
    # note the isolate field isn't an official reference, its just
    # used to group isolates on the front end (at present)
    _extras = ['isolate', 'aerobic', 'source', 'lab_number']
    source = SourceObservation()

    @classmethod
    def get_record(cls):
        return "lab/records/blood_culture.html"

    def update_from_dict(self, data, *args, **kwargs):
        result = data.get("result", None)
        if "date_ordered" in data:
            date_ordered = data.pop("date_ordered")
            if isinstance(date_ordered, str):
                date_ordered = date_ordered.strip()
                data["datetime_ordered"] = datetime.combine(
                    date_ordered, datetime.min.time()
                )

        if result:
            result = result.get("result", None)

        if result:
            result = result.strip()

        if not result or result == 'Not Done':
            if self.id:
                self.delete()
        else:
            super(BloodCultureMixin, self).update_from_dict(data, *args, **kwargs)


class GramStainResult(lmodels.Observation, RfhObservation):
    class Meta:
        proxy = True
        auto_created = True

    RESULT_CHOICES = (
        ("Yeast", "Yeast"),
        ("Gram +ve Cocci Cluster", "Gram +ve Cocci Cluster"),
        ("Gram +ve Cocci Chains", "Gram +ve Cocci Chains"),
        ("Gram -ve Rods", "Gram -ve Rods"),
        ("Not Done", "Not Done"),
    )


class GramStain(BloodCultureMixin, lmodels.LabTest):
    _title="Gram Stain"
    result = GramStainResult()


class QuickFishResult(lmodels.Observation, RfhObservation):
    class Meta:
        proxy = True
        auto_created = True

    RESULT_CHOICES = (
        ("C. albicans", "C. albicans"),
        ("C. parapsilosis", "C. parapsilosis"),
        ("C. glabrata", "C. glabrata"),
        ("Negative", "Negative"),
        ("Not Done", "Not Done"),
    )


class QuickFISH(BloodCultureMixin, lmodels.LabTest):
    _title = "QuickFISH"
    result = QuickFishResult()


class GPCStaphResult(lmodels.Observation, RfhObservation):
    class Meta:
        proxy = True
        auto_created = True

    RESULT_CHOICES = (
        ("S. aureus", "S. aureus"),
        ("CNS", "CNS"),
        ("Negative", "Negative"),
        ("Not Done", "Not Done"),
    )


class GPCStaph(BloodCultureMixin, lmodels.LabTest):
    result = GPCStaphResult()
    _title = 'GPC Staph'


class GPCStrepResult(lmodels.Observation, RfhObservation):
    class Meta:
        proxy = True
        auto_created = True

    RESULT_CHOICES = (
        ("E.faecalis", "E.faecalis"),
        ("Other enterococci", "Other enterococci"),
        ("Negative", "Negative"),
        ("Not Done", "Not Done"),
    )


class GPCStrep(BloodCultureMixin, lmodels.LabTest):
    result = GPCStrepResult()
    _title = "GPC Strep"


class GNRResult(lmodels.Observation, RfhObservation):
    class Meta:
        proxy = True
        auto_created = True

    RESULT_CHOICES = (
        ("E.faecalis", "E.coli"),
        ("K. pneumoniae", "K. pneumoniae"),
        ("P. aeruginosa", "P. aeruginosa"),
        ("Negative", "Negative"),
        ("Not Done", "Not Done"),
    )


class GNR(BloodCultureMixin, lmodels.LabTest):
    _title = 'GNR'
    result = GNRResult()


class Organism(lmodels.Observation, RfhObservation):
    class Meta:
        proxy = True

    lookup_list = omodels.Microbiology_organism


class BloodCultureOrganism(BloodCultureMixin, lmodels.LabTest):
    _title = 'Organism'
    result = Organism()


class FinalDiagnosis(EpisodeSubrecord):
    _icon = 'fa fa-pencil-square'
    _title = "Final Diagnosis"

    source = models.CharField(max_length=255, blank=True)
    contaminant = models.BooleanField(default=False)
    community_related = models.BooleanField(default=False)
    hcai_related = models.BooleanField(verbose_name="HCAI related", default=False)


class ImagingTypes(lookuplists.LookupList): pass


class Imaging(EpisodeSubrecord):
    _icon = 'fa fa-eye'

    date = models.DateField(blank=True, null=True)
    imaging_type = ForeignKeyOrFreeText(ImagingTypes)
    site = models.CharField(max_length=200, blank=True, null=True)
    details = models.TextField(blank=True, null=True)


class PositiveBloodCultureHistory(PatientSubrecord):
    when = models.DateTimeField(default=datetime.datetime.now)

    @classmethod
    def _get_field_default(cls, name):
        # this should not be necessary...
        return None


# method for updating
@receiver(post_save, sender=omodels.Tagging)
def record_positive_blood_culture(sender, instance, **kwargs):
    from elcid.patient_lists import Bacteraemia

    if instance.value == Bacteraemia.tag:
        pbch, _ = PositiveBloodCultureHistory.objects.get_or_create(
            patient_id=instance.episode.patient.id
        )
        pbch.when = datetime.datetime.now()
        pbch.save()
