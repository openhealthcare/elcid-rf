"""
Load ICU Handover records from upstream
"""
from django.db import transaction
from opal.models import Patient

from elcid.models import Demographics
from elcid.episode_categories import InfectionService
from intrahospital_api import get_api
from intrahospital_api.loader import create_rfh_patient_from_hospital_number

from plugins.icu import logger
from plugins.icu.models import ICUHandover, ICUHandoverLocation, parse_icu_location
from plugins.icu.episode_categories import ICUHandoverEpisode


Q_GET_ICU_HANDOVER = """
SELECT *
FROM VIEW_ElCid_ITU_Handover
WHERE discharged = 'No'
"""

Q_GET_ICU_MRNS = """
SELECT *
FROM VIEW_ElCid_ITU_Handover
WHERE discharged = 'No'
"""

def get_upstream_data():
    """
    Fetch the upstream handover snapshot data
    """
    api = get_api()

    return api.execute_hospital_query(Q_GET_ICU_HANDOVER)


def get_upstream_mrns():
    """
    Return a list of MRNs of patients currently undischarged on
    the ICU Handover database
    """
    api = get_api()

    return [p['Patient_MRN'] for p in api.execute_hospital_query(Q_GET_ICU_MRNS)]


@transaction.atomic
def load_icu_handover():
    """
    Load a snapshot of data from the upstream appointment database
    """
    results = get_upstream_data()

    ICUHandoverLocation.objects.all().delete()

    for result in results:

        mrn = result['Patient_MRN']

        if not Demographics.objects.filter(hospital_number=mrn).exists():
            create_rfh_patient_from_hospital_number(mrn, InfectionService)

            logger.info('Created patient for {}'.format(mrn))

        patient = Patient.objects.get(demographics__hospital_number=mrn)

        if not patient.episode_set.filter(
                category_name=ICUHandoverEpisode.display_name).exists():
            patient.create_episode(category_name=ICUHandoverEpisode.display_name)

        our_handover, _ = ICUHandover.objects.get_or_create(patient=patient)

        for k, v in result.items():
            setattr(
                our_handover,
                ICUHandover.UPSTREAM_FIELDS_TO_MODEL_FIELDS[k],
                v
            )

        our_handover.save()

        handover_location, _ = ICUHandoverLocation.objects.get_or_create(
            patient=patient
        )
        hospital, ward, bed        = parse_icu_location(result['Location'])

        handover_location.hospital = hospital
        handover_location.ward     = ward
        handover_location.bed      = bed
        handover_location.admitted = result['Date_ITU_Admission'].date()
        handover_location.save()

        logger.info('Stored ICU Handover record for {}'.format(mrn))
