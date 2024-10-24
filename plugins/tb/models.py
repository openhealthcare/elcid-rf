"""
Models for tb
"""
import datetime

from django.db import models as fields
from django.db.models import Max
from opal.core.fields import ForeignKeyOrFreeText, enum
from opal.core import lookuplists
from opal import models

from elcid.models import PreviousMRN

from plugins.tb import constants


class RecreationalDrug(lookuplists.LookupList):
    pass


class SocialHistory(PreviousMRN, models.EpisodeSubrecord):
    _is_singleton = True
    _icon = 'fa fa-clock-o'

    HOMELESSNESS_TYPE_CHOICES = (
        ("Hostel", "Hostel",),
        ("Sofa surfing", "Sofa surfing",),
        ("Street", "Street",),
        ("Other", "Other",),
    )

    HOMELESSNESS_CHOICES = (
        ('Never', 'Never',),
        ('Current', 'Current',),
        ('Past', 'Past'),
    )

    ALCOHOL_CHOICES = (
        ("None", "None",),
        ("Occasional", "Occasional",),
        ("Excess", "Excess",),
        ("Dependent", "Dependent",),
    )

    SMOKING_CHOICES = (
        ("Never", "Never",),
        ("Current", "Current",),
        ("Past", "Past",),
    )

    RECREATIONAL_DRUG_USE = (
        ("Never", "Never",),
        ("Current", "Current",),
        ("Dependent", "Dependent",),
        ("Past", "Past",),
    )

    PRISON_CHOICES = (
        ("Never", "Never",),
        ("Current", "Current",),
        ("Within the last 5 years", "Within the last 5 years",),
        ("Over 5 years ago", "Over 5 years ago",),
    )

    notes = fields.TextField(blank=True, null=True)

    smoking = fields.CharField(
        max_length=250,
        choices=SMOKING_CHOICES,
        blank=True,
        null=True
    )

    drinking = fields.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Alcohol",
        choices=ALCOHOL_CHOICES
    )
    history_of_alcohol_dependence = fields.BooleanField(
        default=False
    )
    recreational_drug_use = fields.CharField(
        max_length=250,
        choices=RECREATIONAL_DRUG_USE,
        blank=True,
        null=True
    )
    opiate_replacement_therapy = fields.BooleanField(
        default=False,
        verbose_name="on opiate replacement therapy"
    )
    drug_community_worker = fields.CharField(
        verbose_name="Drug/alcohol worker",
        max_length=256,
        blank=True,
        null=True,
    )

    homelessness_type = fields.CharField(
        blank=True,
        null=True,
        choices=HOMELESSNESS_TYPE_CHOICES,
        max_length=256
    )

    homelessness = fields.CharField(
        blank=True,
        null=True,
        choices=HOMELESSNESS_CHOICES,
        max_length=256
    )

    housing_officer = fields.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    recreational_drug_type = ForeignKeyOrFreeText(RecreationalDrug)
    receiving_treatment = fields.BooleanField(default=False)
    prison_history = fields.CharField(
        max_length=250,
        choices=PRISON_CHOICES,
        blank=True,
        null=True
    )
    prison_history_details = fields.TextField(
        default="", blank=True
    )
    probation_officer = fields.CharField(
        max_length=256,
        blank=True,
        null=True
    )

    mental_health_issues = fields.BooleanField(
        default=False
    )

    # if they patient has mental health issues
    # store the Community pysiatric nurse (CPN) or
    # the Community mental health team (CMHT)
    community_nurse = fields.CharField(
        max_length=256,
        blank=True,
        null=True,
        verbose_name="CPN/CMHT"
    )

    class Meta:
        verbose_name = "Social History"
        verbose_name_plural = "Social Histories"


class Pregnancy(PreviousMRN, models.PatientSubrecord):
    _is_singleton = True

    pregnant = fields.BooleanField(default=False)
    breast_feeding = fields.BooleanField(default=False)


class Nationality(PreviousMRN, models.PatientSubrecord):
    _is_singleton = True

    birth_place = ForeignKeyOrFreeText(
        models.Destination, verbose_name="Country of Birth"
    )
    immigration_concerns = fields.BooleanField(default=False)
    immigration_details = fields.TextField(blank=True)
    immigration_support_officer = fields.TextField(blank=True)

    arrival_in_the_uk = fields.CharField(
        max_length=250,
        blank=True,
        null=True,
        verbose_name="Year of arrival in the UK"
    )

    class Meta:
        verbose_name = "Nationality & Citizenship"
        verbose_name_plural = "Nationality & Citizenship"


class Employment(PreviousMRN, models.PatientSubrecord):
    _is_singleton = True

    FINANICAL_STATUS_CHOICES = (
        ("Nil income", "Nil income"),
        ("On benefits", "On benefits",),
        ("Other(SS/NASS)", "Other(SS/NASS)",),
        ("Employed", "Employed",),
    )

    occupation = fields.TextField(blank=True, null=True)
    financial_status = fields.CharField(
        max_length=256,
        blank=True,
        choices=FINANICAL_STATUS_CHOICES
    )


class CommuninicationConsiderations(PreviousMRN, models.PatientSubrecord):
    _is_singleton = True

    class Meta:
        verbose_name = "Communication"
        verbose_name_plural = "Communinication Considerations"

    needs_an_interpreter = fields.BooleanField(
        default=False
    )
    language = fields.CharField(
        max_length=256, blank=True
    )
    sensory_impairment = fields.BooleanField(
        default=False
    )


class AccessConsiderations(PreviousMRN, models.PatientSubrecord):
    _is_singleton = True

    ACCESS_ASSISTANCE = (
        ("provision", "provision",),
        ("finance", "finance",),
    )

    class Meta:
        verbose_name = "Access & Transport"
        verbose_name_plural = "Access Considerations"

    mobility_problem = fields.BooleanField(
        default=False
    )

    needs_help_with_transport = fields.BooleanField(
        default=False
    )
    access_assistance = fields.CharField(
        blank=True,
        null=True,
        choices=ACCESS_ASSISTANCE,
        max_length=256
    )


class PatientConsultation(PreviousMRN, models.PatientConsultation):
    # the reason for interacton for the MDT
    ADDED_TO_TB_REVIEW_LIST = "Added to TB review list"

    plan = fields.TextField(blank=True, default="")
    examination_findings = fields.TextField(
        blank=True, default=""
    )
    progress = fields.TextField(
        blank=True, default=""
    )
    infection_control = fields.TextField(
        blank=True, default=""
    )
    sent_upstream = fields.BooleanField(default=False)
    mdt_new_result = fields.BooleanField(default=False, verbose_name="New microbiology result")
    mdt_ipc        = fields.BooleanField(default=False, verbose_name="Infection control")
    mdt_management  = fields.BooleanField(default=False, verbose_name="Clinical management")
    mdt_other      = fields.BooleanField(default=False, verbose_name="Other")


class ContactDetails(PreviousMRN, models.PatientSubrecord):
    _is_singleton = True
    _advanced_searchable = False
    _icon = 'fa fa-phone'

    # telephone = fields.CharField(blank=True, null=True, max_length=50)
    # email = fields.CharField(blank=True, null=True, max_length=255)
    # address = fields.TextField(blank=True, null=True)
    details = fields.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Contact Details"
        verbose_name_plural = "Contact Details"


class NextOfKin(PreviousMRN, models.PatientSubrecord):
    _icon = 'fa fa-child'
    _advanced_searchable = False

    first_name = fields.CharField(blank=True, null=True, max_length=255)
    surname = fields.CharField(blank=True, null=True, max_length=255)
    details = fields.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Next Of Kin"
        verbose_name_plural = "Next Of Kin"


class TBSite(lookuplists.LookupList):
    pass


class TBTreatmentCentre(lookuplists.LookupList):
    pass


class LymphNodeSwellingSiteOptions(lookuplists.LookupList):
    pass


class LymphNodeSwellingSite(PreviousMRN, models.EpisodeSubrecord):
    site = ForeignKeyOrFreeText(LymphNodeSwellingSiteOptions)


class Treatment(PreviousMRN, models.Treatment):
    _angular_service = 'TreatmentRecord'
    planned_end_date = fields.DateField(blank=True, null=True)
    category = fields.CharField(blank=True, null=True, max_length=255)

    TB = "tb"
    OPAT = 'opat'


class TBHistory(PreviousMRN, models.PatientSubrecord):
    """ Used if the person has clicked that they
        have a personal history of TB in the
        initial assessment form
    """
    _icon = 'fa fa-clock-o'
    _is_singleton = True

    TB_TYPES = (
        ("Active", "Active",),
        ("Latent", "Latent",),
        ("Unknown", "Unknown",),
    )

    _is_singleton = True

    # TODO After we get sign off from the doctors the below
    # fields can be removed
    previous_tb_contact = fields.BooleanField(
        default=False,
        verbose_name="Previous TB contact"
    )
    contact_how_long_ago_years = fields.IntegerField(
        blank=True, null=True
    )
    contact_how_long_ago_months = fields.IntegerField(
        blank=True, null=True
    )
    contact_how_long_ago_days = fields.IntegerField(
        blank=True, null=True
    )
    previous_tb_contact_details = fields.TextField(default="")

    previous_tb_diagnosis = fields.BooleanField(
        default=False,
        verbose_name="Previous TB diagnosis"
    )
    diagnosis_how_long_ago_years = fields.IntegerField(
        blank=True, null=True
    )
    diagnosis_how_long_ago_months = fields.IntegerField(
        blank=True, null=True
    )
    diagnosis_how_long_ago_days = fields.IntegerField(
        blank=True, null=True
    )
    # end todo

    diagnosis_date_year = fields.IntegerField(
        blank=True, null=True
    )
    diagnosis_date_month = fields.IntegerField(
        blank=True, null=True
    )
    diagnosis_date_day = fields.IntegerField(
        blank=True, null=True
    )

    how_long_treated_years = fields.IntegerField(
        blank=True, null=True
    )
    how_long_treated_months = fields.IntegerField(
        blank=True, null=True
    )
    how_long_treated_days = fields.IntegerField(
        blank=True, null=True
    )
    tb_type = fields.CharField(
        blank=True,
        null=True,
        choices=TB_TYPES,
        max_length=256,
        verbose_name="TB Type"
    )
    site_of_tb = ForeignKeyOrFreeText(
        TBSite, verbose_name="Site of TB"
    )
    country_treated = ForeignKeyOrFreeText(models.Destination)
    treatment_centre = ForeignKeyOrFreeText(TBTreatmentCentre)
    diagnosis_details = fields.TextField(default="")

    class Meta:
        verbose_name = "History Of TB"
        verbose_name_plural = "TB Histories"


class IndexCase(PreviousMRN, models.PatientSubrecord):
    _icon = 'fa fa-chain'

    POS_NEG = (
        ("+ve", "+ve"),
        ("-ve", "-ve"),
        ("Unknown", "Unknown"),
    )

    DRUG_susceptibility = (
        ("Fully sensitive", "Fully sensitive",),
        ("Not fully sensitive", "Not fully sensitive",),
        ("Unknown", "Unknown"),
    )

    RELATIONSHIP = (
        ("Household", "Household",),
        ("Healthcare", "Healthcare",),
        (
            "Workplace (non healthcare)",
            "Workplace (non healthcare)",
        ),
        (
            "Education",
            "Education",
        ),
        (
            "Prison",
            "Prison",
        ),
    )

    ltbr_number = fields.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="LTBR Number"
    )
    hospital_number = fields.CharField(
        max_length=200,
        blank=True,
        null=True,
    )
    sputum_smear = fields.CharField(
        max_length=200,
        blank=True,
        null=True,
        choices=POS_NEG
    )
    culture = fields.CharField(
        max_length=200,
        blank=True,
        null=True,
        choices=POS_NEG
    )
    drug_susceptibility = fields.CharField(
        max_length=200,
        blank=True,
        null=True,
        choices=DRUG_susceptibility
    )

    diagnosis_year = fields.IntegerField(
        blank=True, null=True
    )

    diagnosis_month = fields.IntegerField(
        blank=True, null=True
    )

    diagnosis_day = fields.IntegerField(
        blank=True, null=True
    )

    index_case_site_of_tb = ForeignKeyOrFreeText(
        TBSite, verbose_name="Site of TB"
    )

    relationship = fields.CharField(
        max_length=200,
        blank=True,
        null=True,
        choices=RELATIONSHIP,
        verbose_name="Relationship to index case"
    )

    relationship_other = fields.CharField(
        max_length=200,
        blank=True,
        null=True,
    )

    details = fields.TextField(
        blank=True
    )


class Allergies(PreviousMRN, models.Allergies):
    pass


class Travel(PreviousMRN, models.EpisodeSubrecord):
    _icon = 'fa fa-plane'

    country = ForeignKeyOrFreeText(models.Destination)
    when = fields.CharField(max_length=255, blank=True)
    duration = fields.CharField(max_length=255, blank=True)
    reason_for_travel = ForeignKeyOrFreeText(models.Travel_reason)
    additional_exposures = fields.TextField(default="")

    class Meta:
        verbose_name = "Travel History"
        verbose_name_plural = "Travel Histories"


class TBLocation(PreviousMRN, models.EpisodeSubrecord):
    _is_singleton = True
    sites = fields.ManyToManyField(TBSite, blank=True)

    def to_dict(self, user):
        result = super(TBLocation, self).to_dict(user)
        result["sites"] = list(self.sites.values_list("name", flat=True))
        return result


class BCG(PreviousMRN, models.PatientSubrecord):
    _icon = 'fa fa-asterisk'
    _is_singleton = True

    BCG_PERIOD = (
        ('Neonatal', 'Neonatal',),
        ('School', 'School',),
        ('Adult', 'Adult',),
        ('Unsure', 'Unsure',),
        ('None', 'None',)
    )
    bcg_type = fields.CharField(
        max_length=255,
        blank=True,
        choices=BCG_PERIOD,
        verbose_name="BCG"
    )
    bcg_scar = fields.BooleanField(default=False, verbose_name="BCG Scar Seen")
    red_book_documentation_of_bcg_seen = fields.BooleanField(
        default=False, verbose_name="Red Book Documentation Of BCG Given"
    )

    class Meta:
        verbose_name = "BCG"


class MantouxTest(PreviousMRN, models.PatientSubrecord):
    _icon = "fa fa-crosshairs"

    MANTOUX_SITES = (
        ("Left Lower Arm", "Left Lower Arm",),
        ("Right Lower Arm", "Right Lower Arm",),
    )
    batch_number = fields.CharField(
        max_length=256, blank=True, default=""
    )
    date_administered = fields.DateField(blank=True, null=True)
    expiry_date = fields.DateField(blank=True, null=True)
    induration = fields.IntegerField(
        verbose_name="Induration (mm)",
        blank=True,
        null=True
    )
    site = fields.CharField(
        max_length=256, blank=True, default="", choices=MANTOUX_SITES
    )


class TBMeta(PreviousMRN, models.EpisodeSubrecord):
    _is_singleton = True
    _advanced_searchable = False

    contact_tracing_done = fields.BooleanField(default=False)
    directly_observed_therapy = fields.BooleanField(default=False)


class TBCaseManager(lookuplists.LookupList):
    pass


class TBManagement(PreviousMRN, models.EpisodeSubrecord):
    _is_singleton = True

    class Meta:
        verbose_name = "TB Management"

    case_manager = ForeignKeyOrFreeText(TBCaseManager)
    ltbr_number  = fields.CharField(
        max_length=200, blank=True, null=True,
        verbose_name = "LTBR Number"
    )


class AdverseReaction(PreviousMRN, models.EpisodeSubrecord):
    _icon = 'fa fa-stop-circle-o'
    details = fields.TextField(blank=True, default='')


class OtherInvestigation(PreviousMRN, models.EpisodeSubrecord):
    _icon = 'fa fa-crosshairs'

    name    = fields.CharField(max_length=256, blank=True, default="")
    date    = fields.DateField(blank=True, null=True)
    details = fields.TextField(blank=True, default='')


def parse_date(some_val):
    date_formats = ["%d/%m/%y", "%d/%m/%Y"]
    result = None
    for date_format in date_formats:
        try:
            dt = datetime.datetime.strptime(some_val, date_format)
            result = dt.date()
        except ValueError:
            pass
    return result


class AbstractTBObservation(fields.Model):
    """
    A TB Observation is an observation of a test that we do to see
    if a patient has TB.

    Smears and PCRs are not 100% accurate.

    Smears, AFB Cultures and the TB Ref lab are all observations
    on the same test.
    """

    # the value of Observation.observation_name
    # used by this observation
    OBSERVATION_NAMES = []
    # the lab test names that have this
    TEST_NAMES = []

    patient = fields.ForeignKey(
        models.Patient,
        on_delete=fields.CASCADE,
    )
    value = fields.TextField(blank=True, default="")
    site = fields.CharField(max_length=256, blank=True, default="")
    lab_number = fields.CharField(max_length=256, blank=True, default="")
    test_name = fields.CharField(max_length=256, blank=True, default="")
    observation_datetime = fields.DateTimeField(blank=True, null=True)
    reported_datetime = fields.DateTimeField(blank=True, null=True)
    pending = fields.BooleanField()
    positive = fields.BooleanField()

    @classmethod
    def is_positive(cls, obs):
        raise NotImplementedError("Please implement is positive")

    @classmethod
    def is_negative(cls, obs):
        raise NotImplementedError("Please implement is negative")

    @classmethod
    def populate_from_observation(cls, obs):
        new_model = cls()
        new_model.patient = obs.test.patient
        new_model.value = obs.observation_value
        if obs.test.site_code:
            new_model.site = obs.test.site_code
        new_model.lab_number = obs.test.lab_number
        new_model.test_name = obs.test.test_name
        new_model.observation_datetime = obs.observation_datetime
        new_model.reported_datetime = obs.reported_datetime
        is_positive = cls.is_positive(obs)
        is_negative = cls.is_negative(obs)
        if is_positive or is_negative:
            new_model.pending = False
        else:
            new_model.pending = True
        if is_positive:
            new_model.positive = True
        else:
            new_model.positive = False
        return new_model

    def display_value(self):
        result = "\n".join(self.value.split("~"))
        return result.strip()

    class Meta:
        abstract = True

    def to_dict(self):
        # For the purposes of TB results we care about the recent
        # TB MDT period - so if it is since the last Tuesday
        start_date = datetime.date.today()
        for i in range(1, 8):
            start_date = start_date - datetime.timedelta(i)
            if start_date.isoweekday() == 3:
                break

        if self.reported_datetime is None:
            recently = False
        else:
            recently = self.reported_datetime.date() >= start_date

            episode = self.patient.episode_set.get(category_name='TB')
            mdt_reason = models.PatientConsultationReasonForInteraction.objects.get(
                name=constants.MDT_NAME)
            mdts = episode.patientconsultation_set.filter(
                reason_for_interaction_fk=mdt_reason.pk
            )
            if mdts.exists():
                max_mdt = mdts.order_by('-when').first().when
                if self.reported_datetime < max_mdt:
                    recently = False


        return {
            'value'               : self.value,
            'site'                : self.site,
            'lab_number'          : self.lab_number,
            'test_name'           : self.test_name,
            'observation_datetime': self.observation_datetime,
            'reported_datetime'   : self.reported_datetime,
            'reported_recently'   : recently,
            'pending'             : self.pending,
            'positive'            : self.positive,
            'display_value'       : self.display_value()
        }


class AFBSmear(AbstractTBObservation):

    OBSERVATION_NAMES = [
        'AFB Smear',
        'Auramine film'
    ]

    TEST_NAMES = [
        'AFB : CULTURE',
        'AFB : EARLY MORN. URINE',
        'AFB BLOOD CULTURE',
        'AFB CULTURE',
    ]

    NEGATIVE_VALUES = [
        "AAFB not seen",
        "AFB NOT seen",
    ]

    # stored in obs name 'Date of AFB Microscopy'
    date_of_microscopy = fields.DateField(blank=True, null=True)

    @classmethod
    def is_positive(cls, obs):
        obs_value = obs.observation_value
        positive_starts_with = [
            "AAFB + Seen",
            "AAFB 2+ Seen",
            "AAFB 3+ Seen",
            "AAFB 4+ Seen",
            "AFB seen (1+)",
            "AFB seen (2+)",
            "AFB seen (3+)",
            "AFB seen (4+)",
        ]
        for psw in positive_starts_with:
            if obs_value.startswith(psw):
                return True

        return False

    @classmethod
    def is_negative(cls, obs):
        obs_value = obs.observation_value
        for val in cls.NEGATIVE_VALUES:
            if obs_value.startswith(val):
                return True
        return False

    @classmethod
    def populate_from_observation(cls, obs):
        new_model = super().populate_from_observation(obs)
        microscopy_date_obs = obs.test.observation_set.filter(
            observation_name="Date of AFB Microscopy"
        ).first()
        if microscopy_date_obs:
            microscopy_date = microscopy_date_obs.observation_value
            microscopy_date = parse_date(microscopy_date)
            if microscopy_date:
                new_model.date_of_microscopy = microscopy_date
        return new_model

    def to_dict(self):
        data = super().to_dict()
        data['date_of_microscopy'] = self.date_of_microscopy
        return data


class AFBCulture(AbstractTBObservation):

    OBSERVATION_NAMES = [
        'TB: Culture Result',
        'AFB Isolate(s)',
    ]

    TEST_NAMES = [
        'AFB : CULTURE',
        'AFB : EARLY MORN. URINE',
        'AFB BLOOD CULTURE',
        'AFB CULTURE',
        'AFB URINE',
        'MYCOBACTERIA BLOOD CULTURE'
    ]

    # what is stored in 'Date of AFB Culture Result'
    date_of_culture_result = fields.DateField(blank=True, null=True)
    # what is stored in obs name TB: Comment
    tb_comment = fields.TextField(blank=True, default="")
    # what is stored in obs name TB: Clinical Comment
    tb_clinical_comment = fields.TextField(blank=True, default="")

    @classmethod
    def is_positive(cls, obs):
        pos = ["1", "~1"]
        for val in pos:
            if obs.observation_value.startswith(val):
                return True
        return False

    @classmethod
    def is_negative(cls, obs):
        return obs.observation_value.startswith("No")

    @classmethod
    def populate_from_observation(cls, obs):
        new_model = super().populate_from_observation(obs)
        microscopy_date_obs = obs.test.observation_set.filter(
            observation_name="Date of AFB Culture Result"
        ).first()
        if microscopy_date_obs:
            microscopy_date = microscopy_date_obs.observation_value
            microscopy_date = parse_date(microscopy_date)
            if microscopy_date:
                new_model.date_of_culture_result = microscopy_date

        tb_comment = obs.test.observation_set.filter(
            observation_name="TB: Comment"
        ).first()
        if tb_comment:
            new_model.tb_comment = tb_comment

        clinical_comment = obs.test.observation_set.filter(
            observation_name="TB: Clinical Comment"
        ).first()
        if clinical_comment:
            new_model.clinical_comment = clinical_comment

        return new_model

    def has_sensitivities(self):
        return self.value.count("1)") > 1 or self.value.count("2)") > 1

    def display_value(self):
        val = super().display_value().strip()
        to_remove = "\n".join([
            'Key: Susceptibility interpretation (Note: update to I)',
            'S = susceptible using standard dosing',
            'I= susceptible at increased dosing, high dose regimen must be used (please see your local antibiotic policy or Microguide for dosing guidance)',
            'R = resistant',
        ])
        return val.replace(to_remove, "").strip()

    def to_dict(self):
        data = super().to_dict()
        data['date_of_culture_result'] = self.date_of_culture_result
        data['tb_comment'] = self.tb_comment
        data['tb_clinical_comment'] = self.tb_clinical_comment
        return data



class AFBRefLab(AbstractTBObservation):
    OBSERVATION_NAMES = ['TB Ref. Lab. Culture result']
    TEST_NAMES = [
        'AFB : CULTURE',
        'AFB : EARLY MORN. URINE',
        'AFB BLOOD CULTURE'
    ]

    date_of_ref_lab_string = fields.CharField(
        max_length=256, blank=True, default=""
    )
    comment = fields.TextField(blank=True, default="")

    @classmethod
    def is_positive(cls, obs):
        return obs.observation_value.startswith("1")

    @classmethod
    def is_negative(cls, obs):
        """
        Ref lab reports are only done after the culture has
        been resolved to be positive.
        IE they are only pending or positive.
        """
        return False

    @classmethod
    def get_ref_lab_date_observation_string(cls, obs):
        ref_lab_date_obs = obs.test.observation_set.filter(
            observation_name="Date of Ref. Lab. report"
        ).first()
        if ref_lab_date_obs:
            return ref_lab_date_obs.observation_value

    @classmethod
    def populate_from_observation(cls, obs):
        new_model = super().populate_from_observation(obs)
        ref_lab_date_str = cls.get_ref_lab_date_observation_string(obs)
        if ref_lab_date_str:
            cls.date_of_ref_lab_string = ref_lab_date_str
        comment = obs.test.observation_set.filter(
            observation_name="TB Ref. Lab. Comment"
        ).first()
        if comment:
            new_model.comment = comment
        return new_model

    def has_sensitivities(self):
        return self.value.count("1)") > 1

    def display_value(self):
        val = super().display_value().strip()
        to_remove = "\n".join([
            'Key: Susceptibility interpretation (Note: update to I)',
            'S = susceptible using standard dosing',
            'I= susceptible at increased dosing, high dose regimen must be used (please see your local antibiotic policy or Microguide for dosing guidance)',
            'R = resistant',
        ])
        return val.replace(to_remove, "").strip()

    def to_dict(self):
        data = super().to_dict()
        data['date_of_ref_lab_string'] = self.date_of_ref_lab_string
        data['comment'] = self.comment
        return data



class TBPCR(AbstractTBObservation):
    OBSERVATION_NAMES = ['TB PCR']
    TEST_NAMES = [
        'TB PCR TEST',
        'TB PCR'
    ]

    NEGATIVE_VALUES = [
        'Not Detected',
        "PCR to detect M.tuberculosis complex was~NEGATIVE",
        "PCR to detect M.tuberculosis complex was ~ NEGATIVE",
        "TB PCR (GeneXpert) Negative"
    ]

    POSITIVE_VALUES = [
        "The PCR to detect M.tuberculosis complex was~POSITIVE",
        "The PCR to detect M.tuberculosis complex was ~ POSITIVE",
        "TB PCR (GeneXpert) Positive",
        "DETECTED",
    ]

    @classmethod
    def is_negative(cls, obs):
        obs_val = obs.observation_value
        for val in cls.NEGATIVE_VALUES:
            if val == obs_val:
                return True
        return False

    @classmethod
    def is_positive(cls, obs):
        obs_val = obs.observation_value
        for val in cls.POSITIVE_VALUES:
            if val == obs_val:
                return True
        return False

    def display_value(self):
        # to_remove = "This does not exclude a diagnosis of tuberculosis."
        obs_value = self.value
        if "The PCR to detect M.tuberculosis complex was~POSITIVE" in obs_value:
            return "The PCR to detect M.tuberculosis complex was POSITIVE"
        if "The PCR to detect M.tuberculosis complex was ~ POSITIVE" in obs_value:
            return "The PCR to detect M.tuberculosis complex was POSITIVE"
        if obs_value.startswith("NOT detected."):
            return "NOT detected."
        return super().display_value()


TB_OBS = (TBPCR, AFBRefLab, AFBCulture, AFBSmear)
