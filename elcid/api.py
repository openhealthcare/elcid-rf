import datetime
import re
from django.conf import settings
from operator import itemgetter
from collections import defaultdict, OrderedDict
from django.utils.text import slugify
from django.http import HttpResponseBadRequest
from intrahospital_api import loader
from rest_framework import viewsets, status
from opal.core.api import OPALRouter
from opal.core.api import (
    patient_from_pk, LoginRequiredViewset, SubrecordViewSet
)
from opal.core.views import json_response
from opal.core import serialization
from elcid import models as emodels
from plugins.labtests import models as lab_test_models


_LAB_TEST_TAGS = {
    "BIOCHEMISTRY": [
        "BONE PROFILE",
        "UREA AND ELECTROLYTES",
        "LIVER PROFILE",
        "IMMUNOGLOBULINS",
        "C REACTIVE PROTEIN",
        "RENAL"

    ],
    "HAEMATOLOGY": [
        "FULL BLOOD COUNT", "HAEMATINICS", "HBA1C"
    ],
    "ENDOCRINOLOGY": [
        "CORTISOL AT 9AM", "THYROID FUNCTION TESTS"
    ],
    "URINE": [
        "OSMALITY", "PROTEIN ELECTROPHORESIS"
    ],
}

_ALWAYS_SHOW_AS_TABULAR = [
    "UREA AND ELECTROLYTES",
    "LIVER PROFILE",
    "IMMUNOGLOBULINS",
    "C REACTIVE PROTEIN",
    "RENAL",
    "RENAL PROFILE",
    "BONE PROFILE",
    "FULL BLOOD COUNT",
    "HAEMATINICS",
    "HBA1C",
    "THYROID FUNCTION TESTS",
    "ARTERIAL BLOOD GASES",
    "B12 AND FOLATE SCREEN",
    "CLOTTING SCREEN",
    "BICARBONATE",
    "CARDIAC PROFILE",
    "CHLORIDE",
    "CHOLESTEROL/TRIGLYCERIDES",
    "AFP",
    "25-OH VITAMIN D",
    "AMMONIA",
    "FLUID CA-125",
    "CARDIAC TROPONIN T",
    "BODYFLUID CALCIUM",
    "BODYFLUID GLUCOSE",
    "BODYFLUID POTASSIUM",
    "PDF PROTEIN",
    "TACROLIMUS",
    "FULL BLOOD COUNT"
]

LAB_TEST_TAGS = defaultdict(list)


for tag, test_names in _LAB_TEST_TAGS.items():
    for test_name in test_names:
        LAB_TEST_TAGS[test_name].append(tag)


def extract_observation_value(observation_value):
    """
        if an observation is numeric, return it as a float
        if its >12 return >12
        else return None
    """
    regex = r'^[-0-9][0-9.]*$'
    obs_result = observation_value.strip()
    obs_result = obs_result.split("~")[0].strip("<").strip(">").strip()
    if re.match(regex, obs_result):
        return round(float(obs_result), 3)


def get_observation_value(observation):
    return extract_observation_value(observation["observation_value"])


def clean_ref_range(ref_range):
    return ref_range.replace("]", "").replace("[", "").strip()


def get_reference_range(observation_reference_range):
    ref_range = clean_ref_range(observation_reference_range)
    if not len(ref_range.replace("-", "").strip()):
        return None
    range_min_max = ref_range.split("-")
    if len(range_min_max) > 2:
        return None
    return {"min": range_min_max[0].strip(), "max": range_min_max[1].strip()}


AEROBIC = "aerobic"
ANAEROBIC = "anaerobic"


class LabTestResultsView(LoginRequiredViewset):
    """ The Api view of the the results view in the patient detail
        We want to show everything grouped by test, then observation, then
        date.
    """
    base_name = 'lab_test_results_view'

    def aggregate_observations_by_lab_test(self, lab_tests):
        by_test = defaultdict(list)
        # lab tests are sorted by lab test type
        # this is either the lab test type if its a lab test we've
        # defined or its what is in the profile description
        # if its an HL7 jobby
        for lab_test in lab_tests:
            observations = lab_test.observation_set.all()
            lab_test_type = lab_test.test_name

            for observation in observations:
                obs_dict = {
                    "observation_name": observation.observation_name,
                    "observation_datetime": observation.observation_datetime,
                    "observation_number": observation.observation_number,
                    "units": observation.units,
                    "last_updated": serialization.serialize_datetime(observation.last_updated),
                }
                obs_result = extract_observation_value(observation.observation_value)
                if obs_result:
                    obs_dict["observation_value"] = obs_result
                else:
                    obs_dict["observation_value"] = observation.observation_value

                obs_dict["reference_range"] = observation.reference_range.replace("]", "").replace("[", "")

                if not len(obs_dict["reference_range"].replace("-", "").strip()):
                    obs_dict["reference_range"] = None
                else:
                    range_min_max = obs_dict["reference_range"].split("-")
                    if not range_min_max[0].strip():
                        obs_dict["reference_range"] = None
                    else:
                        if not len(range_min_max) == 2:
                            obs_dict["reference_range"] = None
                            # raise ValueError("unable to properly judge the range")
                        else:
                            obs_dict["reference_range"] = dict(
                                min=float(range_min_max[0].strip()),
                                max=float(range_min_max[1].strip())
                            )

                obs_dict["datetime_ordered"] = lab_test.datetime_ordered
                by_test[lab_test_type].append(obs_dict)

        return by_test

    def is_empty_value(self, observation_value):
        """ we don't care about empty strings or
            ' - ' or ' # '
        """
        if isinstance(observation_value, str):
            return not observation_value.strip().strip("-").strip("#").strip()
        else:
            return observation_value is None

    @patient_from_pk
    def retrieve(self, request, patient):

        # so what I want to return is all observations to lab test desplay
        # name with the lab test properties on the observation

        a_year_ago = datetime.date.today() - datetime.timedelta(365)
        lab_tests = patient.lab_tests.all().prefetch_related('observation_set')
        lab_tests = lab_tests.filter(datetime_ordered__gte=a_year_ago)
        by_test = self.aggregate_observations_by_lab_test(lab_tests)
        serialised_tests = []

        # within the lab test observations should be sorted by test name
        # and within the if we have a date range we want to be exposing
        # them as part of a time series, ie adding in blanks if they
        # aren't populated
        for lab_test_type, observations in by_test.items():
            if lab_test_type.strip().upper() in set([
                'UNPROCESSED SAMPLE COMT', 'COMMENT', 'SAMPLE COMMENT'
            ]):
                continue

            observations = sorted(observations, key=lambda x: x["datetime_ordered"])
            observations = sorted(observations, key=lambda x: x["observation_name"])


            # observation_time_series = defaultdict(list)
            by_observations = defaultdict(list)
            timeseries = {}

            observation_metadata = {}
            observation_date_range = {
                observation["observation_datetime"].date() for observation in observations
            }
            observation_date_range = sorted(list(observation_date_range))
            long_form = False

            for observation in observations:
                test_name = observation["observation_name"]

                if test_name.strip() == "Haem Lab Comment":
                    # skip these for the time being, we may not even
                    # have to bring them in
                    continue

                if test_name.strip() == "Sample Comment":
                    continue

                if lab_test_type in _ALWAYS_SHOW_AS_TABULAR:
                    pass
                else:
                    if isinstance(observation["observation_value"], str):
                        if extract_observation_value(observation["observation_value"].strip(">").strip("<")) is None:
                            long_form = True

                if test_name not in by_observations:

                    # we don't serializer dictionary keys as part of the serializer so we need to do it ourselves
                    obs_for_test_name = {
                        serialization.serialize_date(i["observation_datetime"].date()): i for i in observations if i["observation_name"] == test_name
                    }
                    # if its all None's for a certain observation name lets skip it
                    # ie if WBC is all None, lets not waste the users' screen space
                    # sometimes they just have '-' so lets skip these too
                    if not all(i for i in obs_for_test_name.values() if self.is_empty_value(i)):
                        continue
                    by_observations[test_name] = obs_for_test_name

                if test_name not in observation_metadata:
                    observation_metadata[test_name] = dict(
                        units=observation["units"],
                        reference_range=observation["reference_range"],
                        api_name=slugify(observation["observation_name"])
                    )

            if long_form:
                # when we are showing in long form the user sees tests as a
                # list so show the most recent test first
                observation_date_range.reverse()
            else:
                # if we're not in long form ie we're displaying results
                # in a tabular timeline, we only want to display
                # the 7 most recent results.
                observation_date_range = observation_date_range[-7:]

            serialised_lab_test = dict(
                long_form=long_form,
                timeseries=timeseries,
                api_name=slugify(lab_test_type),
                observation_metadata=observation_metadata,
                lab_test_type=lab_test_type,
                observations=observations,
                observation_date_range=observation_date_range,
                # observation_time_series=observation_time_series,
                by_observations=by_observations,
                observation_names=sorted(by_observations.keys()),
                tags=LAB_TEST_TAGS.get(lab_test_type, [])
            )
            serialised_tests.append(serialised_lab_test)

        serialised_tests = sorted(
            serialised_tests, key=itemgetter("lab_test_type")
        )

        # ordered by most recent observations first please
        serialised_tests = sorted(
            serialised_tests, key=lambda t: -t["observation_date_range"][-1].toordinal()
        )

        all_tags = list(_LAB_TEST_TAGS.keys())

        return json_response(
            dict(
                tags=all_tags,
                tests=serialised_tests
            )
        )


class InfectionServiceTestSummaryApi(LoginRequiredViewset):
    base_name = 'infection_service_summary_api'
    RELEVANT_TESTS = OrderedDict((
        ("FULL BLOOD COUNT", ["WBC", "Lymphocytes", "Neutrophils"],),
        ("CLOTTING SCREEN", ["INR"],),
        ("C REACTIVE PROTEIN", ["C Reactive Protein"]),
        ("LIVER PROFILE", ["ALT", "AST", "Alkaline Phosphatase"]),
    ),)

    NUM_RESULTS = 5

    def get_recent_dates_to_observations(self, qs):
        """
        We are looking for the last 5 dates
        where we have any observation that
        can be cast to a number.

        If a patient has multiple observations
        on the same date take the most recent
        that can be cast into a number
        """
        date_to_observation = {}
        # this should never be the case, but
        # we don't create the data so cater for it
        qs = qs.exclude(observation_datetime=None)
        for i in qs.order_by("-observation_datetime"):
            if i.value_numeric is not None:
                dt = i.observation_datetime
                obs_date = dt.date()
                if obs_date in date_to_observation:
                    if date_to_observation[obs_date].observation_datetime < dt:
                        date_to_observation[obs_date] = i
                else:
                    date_to_observation[obs_date] = i
            if len(date_to_observation.keys()) == self.NUM_RESULTS:
                break

        return date_to_observation

    def get_obs_queryset(self, patient, lab_test_name, observation_name):
        return lab_test_models.Observation.objects.filter(
            test__patient=patient
        ).filter(
            test__test_name=lab_test_name
        ).filter(
            observation_name=observation_name
        )

    def serialize_observations(self, observations):
        latest_results = {
            serialization.serialize_date(i.observation_datetime.date()): i.value_numeric
            for i in observations
        }
        return dict(
            name=observations[0].observation_name,
            units=observations[0].units,
            reference_range=get_reference_range(
                observations[0].reference_range
            ),
            latest_results=latest_results
        )

    def serialise_lab_tests(self, patient):
        obs = []
        date_set = set()

        for test_name, observation_names in self.RELEVANT_TESTS.items():
            for obs_name in observation_names:
                qs = self.get_obs_queryset(patient, test_name, obs_name)
                if qs:
                    date_to_obs = self.get_recent_dates_to_observations(qs)
                    if date_to_obs:
                        date_set.update(date_to_obs.keys())
                        obs.append(list(date_to_obs.values()))

        all_dates = list(date_set)
        all_dates.sort()
        recent_dates = all_dates[-self.NUM_RESULTS:]

        # flush out the recent dates with nulls if
        # the patient does not have a lot of results
        while len(recent_dates) < self.NUM_RESULTS:
            recent_dates.append(None)
        obs_values = []

        for obs_set in obs:
            obs_values.append(self.serialize_observations(obs_set))
        return dict(
            obs_values=obs_values,
            recent_dates=recent_dates
        )

    @patient_from_pk
    def retrieve(self, request, patient):
        result = self.serialise_lab_tests(patient)
        return json_response(result)


class UpstreamBloodCultureApi(viewsets.ViewSet):
    """
        for every upstream blood culture, return them grouped by

        datetimes_ordered as a date,
        lab_number
        observation name
    """
    base_name = "upstream_blood_culture_results"

    def no_growth_observations(self, observations):
        """
            We are looking for observations that looks like the below.
            Its not necessarily 5 days, sometimes its e.g. 48 hours.
            Otherwise they always look like the below.

            Aerobic bottle culture: No growth after 5 days of incubation
            Anaerobic bottle culture: No growth after 5 days of incubation

            The are always of the type [Anaerobic/Aerobic] bottle culture
        """
        obs_names = ["Aerobic bottle culture", "Anaerobic bottle culture"]

        bottles = [
            o for o in observations if o["observation_name"] in obs_names
        ]

        return len(bottles) == 2

    @patient_from_pk
    def retrieve(self, request, patient):
        """
            returns any observations with Aerobic or Anaerobic in their name
        """
        lab_tests = patient.labtest_set.filter(
            lab_test_type=emodels.UpstreamBloodCulture.get_display_name()
        ).order_by("external_identifier").order_by("-datetime_ordered")
        lab_tests = [i.dict_for_view(request.user) for i in lab_tests]
        for lab_test in lab_tests:
            observations = []
            lab_test["no_growth"] = self.no_growth_observations(
                lab_test["observations"]
            )

            for observation in lab_test["observations"]:
                ob_name = observation["observation_name"].lower()

                if "aerobic" in ob_name:
                    observations.append(observation)

            lab_test["observations"] = sorted(
                observations, key=lambda x: x["observation_name"]
            )
            if lab_test["extras"]["clinical_info"]:
                lab_test["extras"]["clinical_info"] = "{}{}".format(
                    lab_test["extras"]["clinical_info"][0].upper(),
                    lab_test["extras"]["clinical_info"][1:]
                )

        return json_response(dict(
            lab_tests=lab_tests
        ))


class BloodCultureResultApi(viewsets.ViewSet):
    base_name = 'blood_culture_results'

    BLOOD_CULTURES = [
        emodels.GramStain.get_display_name(),
        emodels.QuickFISH.get_display_name(),
        emodels.GPCStaph.get_display_name(),
        emodels.GPCStrep.get_display_name(),
        emodels.GNR.get_display_name(),
        emodels.BloodCultureOrganism.get_display_name()
    ]

    def sort_by_date_ordered_and_lab_number(self, some_keys):
        """ takes in a tuple of (date, lab number)
            both date or lab number will be "" if empty

            it sorts them by most recent and lowest lab number
        """
        def comparator(some_key):
            dt = some_key[0]
            if not dt:
                dt = datetime.date.max
            return (dt, some_key[1],)
        return sorted(some_keys, key=comparator, reverse=True)

    def sort_by_lab_test_order(self, some_results):
        """
            results should be sorted by the order of the blood culture
            list
        """
        return sorted(
            some_results, key=lambda x: self.BLOOD_CULTURES.index(
                x["lab_test_type"]
            )
        )

    def translate_date_to_string(self, some_date):
        if not some_date:
            return ""

        dt = datetime.datetime(
            some_date.year, some_date.month, some_date.day
        )
        return dt.strftime(
            settings.DATE_INPUT_FORMATS[0]
        )

    @patient_from_pk
    def retrieve(self, request, patient):
        lab_tests = patient.labtest_set.filter(
            lab_test_type__in=self.BLOOD_CULTURES
        )
        lab_tests = lab_tests.order_by("datetime_ordered")
        cultures = defaultdict(lambda: defaultdict(dict))
        culture_order = set()

        for lab_test in lab_tests:
            lab_number = lab_test.extras.get("lab_number", "")
            # if lab number is None or "", group it together
            if not lab_number:
                lab_number = ""
            if lab_test.datetime_ordered:
                date_ordered = self.translate_date_to_string(
                    lab_test.datetime_ordered.date()
                )

                culture_order.add((
                    lab_test.datetime_ordered.date(), lab_number,
                ))
            else:
                date_ordered = ""
                culture_order.add(("", lab_number,))

            if lab_number not in cultures[date_ordered]:
                cultures[date_ordered][lab_number][AEROBIC] = defaultdict(list)
                cultures[date_ordered][lab_number][ANAEROBIC] = defaultdict(
                    list
                )

            isolate = lab_test.extras["isolate"]

            if lab_test.extras[AEROBIC]:
                cultures[date_ordered][lab_number][AEROBIC][isolate].append(
                    lab_test.to_dict(self.request.user)
                )
            else:
                cultures[date_ordered][lab_number][ANAEROBIC][isolate].append(
                    lab_test.to_dict(request.user)
                )

        culture_order = self.sort_by_date_ordered_and_lab_number(culture_order)

        for dt, lab_number in culture_order:
            dt_string = self.translate_date_to_string(dt)
            by_date_lab_number = cultures[dt_string][lab_number]
            for robic in [AEROBIC, ANAEROBIC]:
                for isolate in by_date_lab_number[robic].keys():
                    by_date_lab_number[robic][isolate] = self.sort_by_lab_test_order(
                        by_date_lab_number[robic][isolate]
                    )

        return json_response(dict(
            cultures=cultures,
            culture_order=culture_order
        ))


class DemographicsSearch(LoginRequiredViewset):
    base_name = 'demographics_search'
    PATIENT_FOUND_IN_ELCID = "patient_found_in_elcid"
    PATIENT_FOUND_UPSTREAM = "patient_found_upstream"
    PATIENT_NOT_FOUND = "patient_not_found"

    def list(self, request, *args, **kwargs):
        hospital_number = request.query_params.get("hospital_number")
        if not hospital_number:
            return HttpResponseBadRequest("Please pass in a hospital number")
        demographics = emodels.Demographics.objects.filter(
            hospital_number=hospital_number
        ).last()

        # the patient is in elcid
        if demographics:
            return json_response(dict(
                patient=demographics.patient.to_dict(request.user),
                status=self.PATIENT_FOUND_IN_ELCID
            ))
        else:
            if settings.USE_UPSTREAM_DEMOGRAPHICS:
                demographics = loader.load_demographics(hospital_number)

                if demographics:
                    return json_response(dict(
                        patient=dict(demographics=[demographics]),
                        status=self.PATIENT_FOUND_UPSTREAM
                    ))
        return json_response(dict(status=self.PATIENT_NOT_FOUND))


class BloodCultureIsolateApi(SubrecordViewSet):
    model = emodels.BloodCultureIsolate
    base_name = emodels.BloodCultureIsolate.get_api_name()

    def create(self, request):
        bc = self.model()
        bc.update_from_dict(request.data, request.user)
        return json_response(
            bc.to_dict(request.user),
            status_code=status.HTTP_201_CREATED
        )


elcid_router = OPALRouter()
elcid_router.register(BloodCultureResultApi.base_name, BloodCultureResultApi)
elcid_router.register(
    UpstreamBloodCultureApi.base_name, UpstreamBloodCultureApi
)
elcid_router.register(DemographicsSearch.base_name, DemographicsSearch)
elcid_router.register(BloodCultureIsolateApi.base_name, BloodCultureIsolateApi)

lab_test_router = OPALRouter()
lab_test_router.register(
    'infection_service_summary_api', InfectionServiceTestSummaryApi
)
lab_test_router.register('lab_test_results_view', LabTestResultsView)
