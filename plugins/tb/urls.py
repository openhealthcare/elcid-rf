"""
Urls for the tb Opal plugin
"""
from django.conf.urls import url

from plugins.tb import views

urlpatterns = [
    url(
        r'^tb/clinical_advice/(?P<pk>\d+)/?$',
        views.ClinicalAdvicePrintView.as_view()
    ),
    url(
        r'^tb/initial_assessment/(?P<pk>\d+)/?$',
        views.InitialAssessment.as_view()
    ),
    url(
        r'^tb/followup_assessment/(?P<pk>\d+)/?$',
        views.FollowUp.as_view()
    ),
    url(
        r'^tb/nurse_letter/(?P<pk>\d+)/?$',
        views.NurseLetter.as_view(),
        name="nurse_letter"
    ),
    url(
        r'^tb/primary_diagnosis/$',
        views.PrimaryDiagnosisModal.as_view(),
        name="primary_diagnosis_modal"
    ),
    url(
        r'^tb/co_morbidities/$',
        views.SecondaryDiagnosisModal.as_view(),
        name="secondary_diagnosis_modal"
    ),
    url(
        r'^tb/tb_medication/$',
        views.TbMedicationModal.as_view(),
        name="tb_medication_modal"
    ),
    url(
        r'^tb/other_medication/$',
        views.OtherMedicationModal.as_view(),
        name="other_medication_modal"
    ),
    url(
        r'^templates/tb/clinic_list/$',
        views.ClinicList.as_view(),
        name="tb_clinic_list"
    ),
    url(
        r'^templates/tb/clinic_list/(?P<date_stamp>[0-9A-Za-z]+)/$',
        views.ClinicListForDate.as_view(),
        name="tb_clinic_list_for_date"
    ),
    url(
        r'^templates/tb/last_30_days.html$',
        views.Last30Days.as_view(),
        name="last_30_days"
    ),
    url(
        r'^tb/patient_consultation_print/(?P<pk>\d+)/?$',
        views.PrintConsultation.as_view()
    ),
    url(
        r'^tb/mdt/(?P<site>[a-z_\-]+)/$',
        views.MDTList.as_view(),
        name="tb_mdt"
    ),
    url(
        r'^templates/tb/outstanding_mdt_list/$',
        views.OutstandingActionsMDT.as_view(),
        name="outstanding_mdt_list"
    ),
    url(
        r'tb/clinic_activity/$',
        views.ClinicActivity.as_view(),
        name="clinic_activity"
    )
]
