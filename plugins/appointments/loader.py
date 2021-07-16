"""
Load Appointments from upstream
"""
import datetime
import time
from django.db import transaction
from collections import defaultdict
from opal.core import serialization
from django.db.models import DateTimeField
from django.utils import timezone
from elcid.models import Demographics

from intrahospital_api.apis.prod_api import ProdApi as ProdAPI

from plugins.appointments.models import Appointment, PatientAppointmentStatus
from plugins.appointments import logger


Q_GET_ALL_PATIENT_APPOINTMENTS = """
SELECT *
FROM VIEW_ElCid_CRS_OUTPATIENTS
WHERE vPatient_Number = @mrn
"""

Q_GET_APPOINTMENTS_SINCE = """
SELECT *
FROM VIEW_ElCid_CRS_OUTPATIENTS
WHERE last_updated > @last_updated
OR insert_date > @last_updated
"""


def cast_to_instance(patient, upstream_dict):
    our_appointment = Appointment(patient=patient)
    for k, v in upstream_dict.items():
        if v:  # Ignore empty values
            fieldtype = type(
                Appointment._meta.get_field(Appointment.UPSTREAM_FIELDS_TO_MODEL_FIELDS[k])
            )
            if fieldtype == DateTimeField:
                v = timezone.make_aware(v)
            setattr(
                our_appointment, Appointment.UPSTREAM_FIELDS_TO_MODEL_FIELDS[k], v
            )
    return our_appointment


def load_appointments_since(last_updated):
    """
    Loads appointments from the upstream table that have
    been reported since last_updated.

    Returns the created appointment models
    """
    api = ProdAPI()
    query_start = time.time()
    upstream_rows = api.execute_hospital_query(
        Q_GET_APPOINTMENTS_SINCE,
        params={'last_updated': last_updated}
    )
    query_end = time.time()
    logger.info(f"Appointments: queries {len(upstream_rows)} rows in {query_end - query_start}s")
    created = update_appointments_from_query_result(upstream_rows)
    load_end = time.time()
    logger.info(f'Appointments: created {len(created)} in {load_end - query_end}')
    return created


def get_changed_appointment_fields(old_instance, appointment_dict):
    changed = {}
    for their_label, our_field in old_instance.UPSTREAM_FIELDS_TO_MODEL_FIELDS.items():
        new_val = appointment_dict[their_label]
        old_val = getattr(old_instance, our_field)
        fieldtype = type(
            Appointment._meta.get_field(our_field)
        )
        if fieldtype == DateTimeField and new_val:
            new_val = timezone.make_aware(new_val)
        if not new_val == old_val:
            if new_val is None and old_val == "":
                continue
            if old_val is None and new_val == "":
                continue

            changed[our_field] = {
                "old_val": serialization._temporal_thing_to_string(old_val),
                "new_val": serialization._temporal_thing_to_string(new_val),
            }
    return changed


@transaction.atomic
def update_appointments_from_query_result(upstream_rows):
    """
    Takes in the result from a db query.
    Ignores the rows where we don't need to update.
    Deletes old rows where we do need to update.

    Creates new rows, including rows with updates.

    Returns the created new rows.
    """
    existing_appointment = Appointment.objects.filter(
        sqlserver_id__in=[i["id"] for i in upstream_rows],
    )
    sql_id_to_existing_appointments = {
        ea.sqlserver_id: ea for ea in existing_appointment
    }
    to_create = []
    to_delete = []
    hospital_numbers = {row["vPatient_Number"].strip() for row in upstream_rows}
    demographics = Demographics.objects.filter(
        hospital_number__in=hospital_numbers
    ).select_related('patient')
    hospital_number_to_patients = defaultdict(list)
    for demo in demographics:
        hospital_number_to_patients[demo.hospital_number].append(
            demo.patient
        )
    for row in upstream_rows:
        hn = row["vPatient_Number"].strip()
        # if hn is empty, skip it
        if hn == "":
            continue
        if hn not in hospital_number_to_patients:
            continue
        for patient in hospital_number_to_patients[hn]:
            sql_id = row["id"]
            # If it's a new appointment, add it to the to_create list
            if sql_id not in sql_id_to_existing_appointments:
                new_instance = cast_to_instance(patient, row)
                to_create.append(new_instance)
            else:
                existing_appointment = sql_id_to_existing_appointments[sql_id]
                # If it's an existing appointment and it needds updating
                # delete the existing and create a new one,
                # logging the difference between them.
                last_updated = None
                if row["last_updated"]:
                    last_updated = timezone.make_aware(row["last_updated"])
                insert_date = None
                if row["insert_date"]:
                    insert_date = timezone.make_aware(row["insert_date"])
                existing_updated = existing_appointment.last_updated
                existing_insert_date = existing_appointment.insert_date

                changed = False

                # We update if...
                # 1. Our insert_date is after the existing insert_date and neither has been updated
                #    (Should never happen but does in the case of duplicate appointment ids)
                #    If there is also an update date we use that though
                # 2. Upstream has a last_updated timestamp and we don't
                # 3. Upstream has a higher last updated timestamp than us

                if not last_updated and not existing_updated:
                    if insert_date > existing_insert_date:
                        changed = True

                if last_updated and not existing_updated:
                    changed = True

                if last_updated and existing_updated:
                    if last_updated > existing_updated:
                        changed = True

                if changed:
                    patient_id = existing_appointment.patient_id
                    logger.info(
                        f"Appointments: checking for patient id {patient_id} sql id {sql_id}"
                    )
                    changed_fields = get_changed_appointment_fields(
                        existing_appointment, row
                    )
                    for k, v in changed_fields.items():
                        logger.info(
                            f'Appointments: updating {k} was {v["old_val"]} now {v["new_val"]}'
                        )
                    to_delete.append(existing_appointment)
                    new_instance = cast_to_instance(patient, row)
                    to_create.append(new_instance)
    Appointment.objects.filter(
        id__in=[i.id for i in to_delete]
    ).delete()
    Appointment.objects.bulk_create(to_create)
    PatientAppointmentStatus.objects.filter(
        patient_id__in=set([i.patient_id for i in to_create])
    ).update(
        has_appointments=True
    )
    return to_create


def load_appointments(patient):
    """
    Load any upstream appointment data we may not have for PATIENT
    """
    api = ProdAPI()
    demographic = patient.demographics()
    appointments = api.execute_hospital_query(
        Q_GET_ALL_PATIENT_APPOINTMENTS,
        params={'mrn': demographic.hospital_number}
    )
    update_appointments_from_query_result(appointments)
