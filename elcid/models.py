"""
elCID implementation specific models!
"""
import datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from opal.utils import camelcase_to_underscore
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

    @classmethod
    def get_modal_footer_template(cls):
        return "partials/demographics_footer.html"

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

    def __str__(self):
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


class InfectionSource(lookuplists.LookupList):
    pass


class Infection(EpisodeSubrecord):
    """
    This model is deprecated
    """
    _icon = 'fa fa-eyedropper'
    # this needs to be fixed
    source = ForeignKeyOrFreeText(InfectionSource)
    site = models.CharField(max_length=255, blank=True)

    class Meta:
        verbose_name = "Infection Related Issues"


class Procedure(EpisodeSubrecord):
    _icon = 'fa fa-sitemap'
    date = models.DateField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Operation / Procedures"


class PrimaryDiagnosisCondition(lookuplists.LookupList): pass


class PrimaryDiagnosis(EpisodeSubrecord):
    """
    This is the confirmed primary diagnosisa
    """
    _is_singleton = True
    _icon = 'fa fa-eye'

    condition = ForeignKeyOrFreeText(PrimaryDiagnosisCondition)
    confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Primary Diagnosis'
        verbose_name_plural = "Primary Diagnoses"


class Consultant(lookuplists.LookupList):
    pass


class Diagnosis(omodels.Diagnosis):
    category = models.CharField(max_length=256, blank=True, null=True)

    PRIMARY = "primary"


class Iv_stop(lookuplists.LookupList):
    class Meta:
        verbose_name = "IV stop"


class Drug_delivered(lookuplists.LookupList):
    class Meta:
        verbose_name_plural = "Drugs delivered"


class Antimicrobial(EpisodeSubrecord):
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

    class Meta:
        verbose_name = "Clinical Advice"
        verbose_name_plural = "Clinical Advice"


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


# Unused but required by migrations
class RfhObservation(object):
    def __str__(self):
        return "{} for {}".format(
            self.observation_type, self.lab_test
        )


class FinalDiagnosis(EpisodeSubrecord):
    _icon = 'fa fa-pencil-square'

    source = models.CharField(max_length=255, blank=True)
    contaminant = models.BooleanField(default=False)
    community_related = models.BooleanField(default=False)
    hcai_related = models.BooleanField(
        verbose_name="HCAI related", default=False
    )

    class Meta:
        verbose_name = "Final Diagnosis"
        verbose_name_plural = "Final Diagnoses"


class ImagingTypes(lookuplists.LookupList):
    pass


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


class ReferralReason(lookuplists.LookupList):
    pass


class ReferralRoute(omodels.EpisodeSubrecord):
    _icon = 'fa fa-level-up'
    _is_singleton = True

    date_of_referral = models.DateField(null=True, blank=True)

    referral_type = ForeignKeyOrFreeText(omodels.ReferralType)

    referral_reason = ForeignKeyOrFreeText(ReferralReason)

    details = models.TextField()

    class Meta:
        verbose_name = "Referral Route"


class SymptomComplex(omodels.SymptomComplex):
    class Meta:
        verbose_name = "Presenting Symptoms"


class PastMedicalHistory(omodels.PastMedicalHistory):
    pass


class GP(omodels.PatientSubrecord):
    name = models.CharField(
        max_length=256
    )
    contact_details = models.TextField()


class BloodCultureSet(omodels.PatientSubrecord):
    _icon = "fa fa-crosshairs"

    date_ordered = models.DateField(blank=True, null=True)
    source = ForeignKeyOrFreeText(BloodCultureSource)
    lab_number = models.CharField(blank=True, null=True, max_length=256)

    class Meta:
        verbose_name = "Blood Cultures"

    @classmethod
    def _get_fieldnames_to_serialize(cls, *args, **kwargs):
        field_names = super()._get_fieldnames_to_serialize(*args, **kwargs)
        field_names.append("isolates")
        return field_names

    def get_isolates(self, user, *args, **kwargs):
        return [
            i.to_dict(user) for i in self.isolates.all()
        ]

    def set_isolates(self, *args, **kwargs):
        pass


class GramStainOutcome(lookuplists.LookupList):
    def __str__(self):
        return self.name


class QuickFishOutcome(lookuplists.LookupList):
    def __str__(self):
        return self.name


class GPCStaphOutcome(lookuplists.LookupList):
    def __str__(self):
        return self.name


class GPCStrepOutcome(lookuplists.LookupList):
    def __str__(self):
        return self.name


class GNROutcome(lookuplists.LookupList):
    def __str__(self):
        return self.name


class BloodCultureIsolate(
    omodels.UpdatesFromDictMixin,
    omodels.ToDictMixin,
    omodels.TrackedModel,
    models.Model
):
    AEROBIC = "Aerobic"
    ANAEROBIC = "Anaerobic"

    AEROBIC_OR_ANAEROBIC = (
        (AEROBIC, AEROBIC,),
        (ANAEROBIC, ANAEROBIC,),
    )

    consistency_token = models.CharField(max_length=8)
    aerobic_or_anaerobic = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        choices=AEROBIC_OR_ANAEROBIC,
        verbose_name="Blood culture bottle type"
    )
    date_positive = models.DateField(blank=True, null=True)
    blood_culture_set = models.ForeignKey(
        "BloodCultureSet",
        on_delete=models.CASCADE,
        related_name="isolates"
    )
    gram_stain = ForeignKeyOrFreeText(GramStainOutcome)
    quick_fish = ForeignKeyOrFreeText(
        QuickFishOutcome, verbose_name="Candida Quick FiSH"
    )
    gpc_staph = ForeignKeyOrFreeText(GPCStaphOutcome, verbose_name="Staph Quick FiSH")
    gpc_strep = ForeignKeyOrFreeText(GPCStrepOutcome, verbose_name="Strep Quick FiSH")
    sepsityper_organism = ForeignKeyOrFreeText(
        omodels.Microbiology_organism, related_name="sepsityper_organism"
    )
    organism = ForeignKeyOrFreeText(omodels.Microbiology_organism)
    sensitivities = models.ManyToManyField(
        omodels.Antimicrobial, blank=True, related_name="sensitive_isolates"
    )
    resistance = models.ManyToManyField(
        omodels.Antimicrobial, blank=True, related_name="resistant_isolates"
    )
    notes = models.TextField(blank=True)

    @classmethod
    def get_api_name(cls):
        return camelcase_to_underscore(cls._meta.object_name)


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
