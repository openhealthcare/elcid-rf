import datetime
from django.db import transaction
from plugins.appointments.models import PatientAppointmentStatus
from opal.models import Patient
from elcid.models import Demographics
from elcid import episode_categories as infection_episode_categories
from intrahospital_api.apis.prod_api import ProdApi as ProdAPI
from intrahospital_api.loader import create_rfh_patient_from_hospital_number
from plugins.tb import episode_categories, constants, logger, models, lab, views
from plugins.appointments.loader import save_or_discard_appointment_data


Q_TB_APPOINTMENTS = """
SELECT DISTINCT vPatient_Number FROM VIEW_ElCid_CRS_OUTPATIENTS
WHERE Derived_Appointment_Type = @appointment_type
"""

Q_TB_APPOINTMENTS_SINCE = """
SELECT * FROM VIEW_ElCid_CRS_OUTPATIENTS
WHERE Derived_Appointment_Type = @appointment_type
and Appointment_Start_Datetime > @since
"""


@transaction.atomic
def create_tb_episodes():
    api = ProdAPI()
    results = set()
    for appointment in constants.TB_APPOINTMENT_CODES:
        results_for_type = api.execute_hospital_query(
            Q_TB_APPOINTMENTS, params={'appointment_type': appointment}
        )
        results.update(i["vPatient_Number"] for i in results_for_type)

    existing_hospital_numbers = set(Demographics.objects.filter(
        patient__episode__category_name=episode_categories.TbEpisode.display_name
    ).values_list("hospital_number", flat=True))
    created_patients = 0
    created_episodes = 0

    results = list(results)
    for mrn in results:
        if mrn not in existing_hospital_numbers:
            patient = Patient.objects.filter(
                demographics__hospital_number=mrn
            ).first()
            if not patient:
                created_patients += 1
                patient = create_rfh_patient_from_hospital_number(
                    mrn, infection_episode_categories.InfectionService
                )
            patient.create_episode(
                category_name=episode_categories.TbEpisode.display_name
            )
            created_episodes += 1

    logger.info(f"Created {created_patients} patients")
    logger.info(f"Created {created_episodes} episodes")


def refresh_tb_patients():
    refresh_future_tb_appointments()
    refresh_future_appointment_key_investigations()


@transaction.atomic
def refresh_future_tb_appointments():
    """
    Make sure we have appointments with TB patients
    in our system for all patients with TB appointments
    in the upstream system.
    """
    api = ProdAPI()
    since = datetime.datetime.combine(
        datetime.date.today(), datetime.datetime.min.time()
    )
    upstream_appointments = []
    for appointment_type in constants.TB_APPOINTMENT_CODES:
        result = api.execute_hospital_query(
            Q_TB_APPOINTMENTS_SINCE, params={
                'appointment_type': appointment_type,
                'since': since
            }
        )
        upstream_appointments.extend(result)

    updated_hns = []
    created_patients = 0
    created_episodes = 0

    for appointment in upstream_appointments:
        mrn = appointment["vPatient_Number"]
        if not mrn:
            continue
        patient = Patient.objects.filter(
            demographics__hospital_number=mrn
        ).first()
        if not patient:
            patient = create_rfh_patient_from_hospital_number(
                mrn, infection_episode_categories.InfectionService
            )
            patient.create_episode(
                category_name=episode_categories.TbEpisode.display_name
            )
            created_patients += 1
            # new patients load in all appointments so we don't need
            # to check them again here
            continue
        if not patient.episode_set.filter(
            category_name=episode_categories.TbEpisode.display_name
        ):
            created_episodes += 1
            patient.create_episode(
                category_name=episode_categories.TbEpisode.display_name
            )
        save_or_discard_appointment_data(appointment, patient)
        updated_hns.append(mrn)
    PatientAppointmentStatus.objects.filter(
        patient__demographics__hospital_number__in=updated_hns
    ).update(
        has_appointments=True
    )
    logger.info(f"Created {created_patients} patients")
    logger.info(f"Created {created_episodes} episodes")
    logger.info(f"Updated {len(updated_hns)} patients appointments")


def refresh_future_appointment_key_investigations():
    """
    For each appointment on the TB clinic list make sure there
    is a TBPatient instance in the database that tells us when
    they first became TB positive.
    """
    appointments = views.ClinicList().get_queryset().prefetch_related(
        'patient'
    )
    patients = [i.patient for i in appointments]
    models.TBPatient.objects.exclude(
        patient__in=patients
    ).delete()
    for patient in patients:
        refresh_patients_key_investigations(patient)


@transaction.atomic
def refresh_patients_key_investigations(patient):
    tb_patient, _ = patient.tb_patient.get_or_create(
        patient=patient
    )
    tb_tests_for_patient = lab.tb_tests_for_patient(patient)
    for model_field_name, model_value in tb_tests_for_patient.items():
        setattr(tb_patient, model_field_name, model_value)
    tb_patient.save()




