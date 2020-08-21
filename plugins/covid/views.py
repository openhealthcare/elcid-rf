"""
Views for our covid plugin
"""
import csv
import datetime
from django.utils import timezone
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.http import HttpResponse
from django.views.generic import (
    TemplateView, View, DetailView, ListView
)
from opal import models as opal_models
from elcid import patient_lists

from plugins.covid import models, constants, episode_categories
from plugins.appointments.models import Appointment


class CovidDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'covid/dashboard.html'

    def get_context_data(self, *a, **k):
        context = super(CovidDashboardView, self).get_context_data(*a, **k)

        context['dashboard'] = models.CovidDashboard.objects.first()

        sum_fields = [
            'tests_ordered', 'tests_resulted',
            'patients_resulted', 'patients_positive',
            'deaths'
        ]
        for sum_field in sum_fields:
            context[sum_field] = models.CovidReportingDay.objects.all(
            ).aggregate(Sum(sum_field))['{}__sum'.format(sum_field)]

        yesterday = models.CovidReportingDay.objects.get(date = datetime.date.today() - datetime.timedelta(days=1))
        context['yesterday'] = yesterday

        positive_timeseries = ['Positive Tests']
        positive_ticks      = ['x']

        deaths_timeseries   = ['Deaths']
        deaths_ticks        = ['x']

        ordered_timeseries  = ['Tests ordered']
        ordered_ticks       = ['x']

        patients_timeseries = ['Patients tested']
        patients_ticks      = ['x']

        for day in models.CovidReportingDay.objects.all().order_by('date'):
            day_string = day.date.strftime('%Y-%m-%d')

            if day.patients_positive:
                positive_ticks.append(day_string)
                positive_timeseries.append(day.patients_positive)

            if day.deaths:
                deaths_ticks.append(day_string)
                deaths_timeseries.append(day.deaths)

            if day.tests_ordered:
                ordered_ticks.append(day_string)
                ordered_timeseries.append(day.tests_ordered)

            if day.patients_resulted:
                patients_ticks.append(day_string)
                patients_timeseries.append(day.patients_resulted)


        context['positive_data'] = [positive_ticks, positive_timeseries]
        context['deaths_data']   = [deaths_ticks, deaths_timeseries]
        context['orders_data']   = [ordered_ticks, ordered_timeseries]
        context['patients_data'] = [patients_ticks, patients_timeseries]

        context['can_download'] = self.request.user.username in constants.DOWNLOAD_USERS

        return context


class CovidCohortDownloadView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="covid.cohort.csv"'

        writer = csv.writer(response)
        writer.writerow(['elcid_id', 'MRN', 'Name', 'date_first_positive'])

        if self.request.user.username in constants.DOWNLOAD_USERS:
            for patient in models.CovidPatient.objects.all():
                demographics = patient.patient.demographics()
                writer.writerow([
                    patient.patient_id,
                    demographics.hospital_number,
                    demographics.name,
                    str(patient.date_first_positive)
                ])

        return response


class CovidLetter(LoginRequiredMixin, DetailView):
    # accessed at /letters/#/covid/letter/10/
    model         = models.CovidFollowUpCall
    template_name = 'covid/letters/covid.html'

    def get_context_data(self, *a, **k):
        ctx = super().get_context_data(*a, **k)
        ctx['today'] = datetime.date.today()
        return ctx


class CovidFollowupLetter(LoginRequiredMixin, DetailView):
    # accessed at /letters/#/covid-followup/letter/10/
    model         = models.CovidFollowUpCallFollowUpCall
    template_name = 'covid/letters/covid_followup.html'


class CovidUpcomingFollowups(LoginRequiredMixin, ListView):
    template_name = "covid/covid_upcoming_followups.html"

    def get_queryset(self, *args, **kwargs):
        now = timezone.now()
        appointment_types = constants.COVID_FOLLOWUP_APPOINTMENT_TYPES
        return Appointment.objects.filter(
            derived_appointment_type__in=appointment_types
        ).filter(
            start_datetime__gte=now
        ).order_by("start_datetime")

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        ctx["admission_and_episode"] = []

        for admission in ctx["object_list"]:
            episode = admission.patient.episode_set.filter(
                category_name=episode_categories.CovidEpisode.display_name
            ).first()

            # There should always be an episode but if there is not, skip it.
            if episode:
                ctx["admission_and_episode"].append(
                    (admission, episode,)
                )
        return ctx
