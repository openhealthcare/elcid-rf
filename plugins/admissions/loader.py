"""
Load admissions from upsteam
"""
import datetime

from django.db.models import DateTimeField
from django.utils import timezone

from intrahospital_api import get_api

from plugins.admissions.models import Encounter
from plugins.admissions import logger


Q_GET_ALL_PATIENT_ENCOUNTERS = """
SELECT *
FROM CRS_ENCOUNTERS
WHERE PID_3_MRN = @mrn
AND insert_date > @insert_date
"""


def save_encounter(encounter, patient):
    """
    Given a dictionary of ENCOUNTER data from the upstream database,
    and the PATIENT for whom it concerns, save it.
    """
    our_encounter = Encounter(patient=patient)
    for k, v in encounter.items():

        if v: # Ignore for empty / nullvalues
            # Empty is actually more complicated than pythonic truthiness.
            # Many admissions have the string '""' as the contents of room/bed
            if v == '""':
                continue

            fieldtype = type(
                Encounter._meta.get_field(Encounter.UPSTREAM_FIELDS_TO_MODEL_FIELDS[k])
            )
            if fieldtype == DateTimeField:
                try:
                    v = timezone.make_aware(v)
                except AttributeError:
                    # Only some of the "DateTime" fields from upstream
                    # are actually typed datetimes.
                    # Sometimes (when they were data in the originating HL7v2 message),
                    # they're strings. Make them datetimes.
                    v = datetime.datetime.strptime(v, '%Y%m%d%H%M%S')
                    v = timezone.make_aware(v)

            setattr(
                our_encounter,
                Encounter.UPSTREAM_FIELDS_TO_MODEL_FIELDS[k], v
            )

    our_encounter.save()
    logger.info('Saved encounter {}'.format(our_encounter.pk))
    return


def load_encounters(patient):
    """
    Load any upstream admission data we may not have for PATIENT
    """
    api = get_api()

    demographic = patient.demographics()

    encounter_count = patient.encounters.count()

    if encounter_count > 0:
        insert_date = patient.encounters.all().order_by('insert_date').last().insert_date
    else:
        insert_date = datetime.datetime(1971, 1, 1, 1, 1, 1)

    encounters = api.execute_hospital_query(
        Q_GET_ALL_PATIENT_ENCOUNTERS,
        params={'mrn': demographic.hospital_number, 'insert_date': insert_date}
    )
    for encounter in encounters:
        save_encounter(encounter, patient)

    if encounter_count == 0:
        if patient.encounters.count() > 0:
            # We've stored the first encounter for this patient
            status = patient.patientencounterstatus_set.get()
            status.has_encounters = True
            status.save()
