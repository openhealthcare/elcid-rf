"""
Handles updating demographics pulled in by the loader
"""
import traceback

from django.db import transaction
from opal.models import Patient
from opal.core.serialization import deserialize_date

from intrahospital_api import logger
from intrahospital_api import get_api
from intrahospital_api.constants import EXTERNAL_SYSTEM
from elcid.utils import timing

api = get_api()


def update_external_demographics(
    external_demographics,
    demographics_dict,
):
    external_demographics_fields = [
        "hospital_number",
        "nhs_number",
        "surname",
        "first_name",
        "title",
        "date_of_birth",
        "sex",
        "ethnicity",
        "death_indicator",
        "date_of_death"
    ]

    external_demographics_dict = {}
    for field in external_demographics_fields:
        result = demographics_dict.get(field)
        if result:
            external_demographics_dict[field] = result

    external_demographics.update_from_dict(
        external_demographics_dict, api.user, force=True
    )


@timing
def reconcile_all_demographics():
    """
        Look at all patients who have not been reconciled with the upstream
        demographics, ie there demographics external system is not
        EXTERNAL_SYSTEM.

        Take a look upstream, can we reconcile them by getting a match
        on a few different criteria.

        If not stick them on the reconcile list.
    """
    patients = Patient.objects.exclude(
        demographics__external_system=EXTERNAL_SYSTEM
    )

    for patient in patients:
        reconcile_patient_demographics(patient)


@transaction.atomic
def reconcile_patient_demographics(patient):
    """ for a patient,
    """
    demographics = patient.demographics_set.get()
    external_demographics_dict = api.demographics(
        demographics.hospital_number
    )
    if not external_demographics_dict:
        logger.info("unable to find {}".format(
            demographics.hospital_number
        ))
        return
    if is_reconcilable(patient, external_demographics_dict):
        demographics = patient.demographics_set.first()
        demographics.update_from_dict(
            external_demographics_dict, api.user, force=True
        )
    else:
        external_demographics = patient.externaldemographics_set.get()
        update_external_demographics(
            external_demographics, external_demographics_dict
        )


def is_reconcilable(patient, external_demographics_dict):
    # TODO, are we allowed to reconcile even if
    # the values are None?
    dob = external_demographics_dict["date_of_birth"]
    if dob:
        dob = deserialize_date(dob)
    return patient.demographics_set.filter(
        first_name__iexact=external_demographics_dict["first_name"],
        surname__iexact=external_demographics_dict["surname"],
        date_of_birth=dob,
        hospital_number=external_demographics_dict["hospital_number"]
    ).exists()


def have_demographics_changed(
    upstream_demographics, our_demographics_model
):
    """ checks to see i the demographics have changed
        if they haven't, don't bother updating

        only compares keys that are coming from the
        upstream dict
    """
    as_dict = our_demographics_model.to_dict(api.user)
    relevent_keys = set(upstream_demographics.keys())
    our_dict = {i: v for i, v in as_dict.items() if i in relevent_keys}
    return not upstream_demographics == our_dict


def update_patient_demographics(patient, upstream_demographics_dict=None):
    """
    Updates a patient with the upstream demographics, if they have changed.
    """
    if upstream_demographics_dict is None:
        upstream_demographics_dict = api.demographics(
            patient.demographics_set.first().hospital_number
        )
        # this should never really happen but has..
        # It happens in the case of a patient who has previously
        # matched with WinPath but who's hospital_number has
        # then been changed by the admin.
        if upstream_demographics_dict is None:
            return

    demographics = patient.demographics_set.get()
    if have_demographics_changed(
        upstream_demographics_dict, demographics
    ):
        demographics.update_from_dict(
            upstream_demographics_dict, api.user, force=True
        )


def update_all_demographics():
    """
    Runs update_patient_demographics for all_patients.

    Called by the management command sync_demographics which runs periodically
    """
    for patient in Patient.objects.all():
        try:
            update_patient_demographics(patient)
        except:
            msg = 'Exception syncing upstream demographics \n {}'
            logger.error(msg.format(traceback.format_exc()))
