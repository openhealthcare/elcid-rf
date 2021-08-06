"""
Specific API endpoints for the TB module
"""
import datetime
from collections import defaultdict
from opal.core.views import json_response
from opal.core.api import patient_from_pk, LoginRequiredViewset
from plugins.tb.utils import get_tb_summary_information
from plugins.tb import models
from plugins.tb import constants
from plugins.appointments import models as appointment_models


class TbTestSummary(LoginRequiredViewset):
    base_name = 'tb_test_summary'
    """"
    Example payload

    return [
        {
            name: 'C REACTIVE PROTEIN',
            date: '',
            result: '1'
        },
        {
            name: 'ALT',
            date: '',
            result: '1'
        }
    ]
    """
    @patient_from_pk
    def retrieve(self, request, patient):
        tb_summary_information = get_tb_summary_information(patient)
        result = []
        for obs_name, summary in tb_summary_information.items():
            result.append({
                "name": obs_name,
                "date": summary["observation_datetime"],
                "result": summary["observation_value"]
            })

        return json_response(dict(results=result))


class TbTests(LoginRequiredViewset):
    base_name = 'tb_tests'

    @patient_from_pk
    def retrieve(self, request, patient):
        smears = list(models.AFBSmear.objects.filter(
            patient=patient, pending=False
        ))
        cultures = list(models.AFBCulture.objects.filter(
            patient=patient, pending=False
        ))
        ref_labs = list(models.AFBRefLab.objects.filter(
            patient=patient, pending=False
        ))
        culture_tests = smears + cultures + ref_labs
        cultures_by_lab_number = defaultdict(list)
        for culture_test in culture_tests:
            cultures_by_lab_number[culture_test.lab_number].append(culture_test)

        cultures_by_reported = sorted(
            list(cultures_by_lab_number.values()),
            key=lambda x: x[0].observation_datetime,
            reverse=True
        )

        cultures_result = []

        for cultures in cultures_by_reported:
            culture_lines = []
            lab_number = cultures[0].lab_number
            obs_dt = cultures[0].observation_datetime.strftime('%d/%m/%Y %H:%M')
            site = cultures[0].site
            culture_lines.append(
                f"{lab_number} {obs_dt} {site}"
            )
            positive = False
            for culture in cultures:
                # Don't show pending cultures/ref lab reports
                if not isinstance(culture, models.AFBSmear):
                    if culture.pending:
                        continue
                if culture.positive:
                    positive = True
                display_value = culture.display_value()
                if isinstance(culture, models.AFBCulture):
                    if any([i for i in ref_labs if i.lab_number == culture.lab_number]):
                        # cultures when sent to the ref lab have this as a suffix
                        # if we already have the ref lab report, strip it.
                        display_value = display_value.rstrip(
                            "Sent to Ref Lab for confirmation."
                        )
                culture_lines.append(
                    f"{culture.OBSERVATION_NAME} {display_value}"
                )
            cultures_result.append({
                "text": culture_lines,
                "positive": positive
            })

        pcrs = models.TBPCR.objects.filter(patient=patient, pending=False)
        pcrs = pcrs.order_by('-observation_datetime')

        pcr_result = []
        for pcr in pcrs:
            pcr_lines = []
            lab_number = pcr.lab_number
            obs_dt = pcr.observation_datetime.strftime('%d/%m/%Y %H:%M')
            site = pcr.site
            pcr_lines.append(
                f"{lab_number} {obs_dt} {site}"
            )
            pcr_lines.append(
                pcr.display_value()
            )
            pcr_result.append({
                "text": pcr_lines,
                "positive": pcr.positive
            })

        return json_response({'cultures': cultures_result[:5], 'pcrs': pcr_result[:5]})


class TBAppointments(LoginRequiredViewset):
    base_name = "tb_appointments"

    @patient_from_pk
    def retrieve(self, request, patient):
        appointment_fields = [
            "start_datetime",
            "status_code",
            "derived_appointment_type",
            "derived_clinic_resource"
        ]
        appointments = appointment_models.Appointment.objects.filter(
            patient=patient
        ).filter(
            derived_appointment_type__in=constants.TB_APPOINTMENT_CODES
        )
        todays_appointments = list(appointments.filter(
            start_datetime__date=datetime.date.today()
        ).values(*appointment_fields))
        next_appointment = appointments.filter(
            start_datetime__date__gt=datetime.date.today(),
        ).exclude(
            status_code__in=["Rescheduled", "Canceled"]
        ).values(*appointment_fields).order_by('start_datetime').first()
        last_appointments_qs = appointments.filter(
            start_datetime__date__lt=datetime.date.today()
        ).values(*appointment_fields).order_by('-start_datetime')
        last_appointments = []
        for appointment in last_appointments_qs:
            last_appointments.append(appointment)
            if appointment["status_code"] in ['Checked In', 'Checked Out']:
                break
        return json_response({
            "todays_appointments": todays_appointments,
            "next_appointment": next_appointment,
            "last_appointments": last_appointments,
        })
