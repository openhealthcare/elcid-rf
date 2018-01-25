"""
Admin for elcid fields
"""
from django.contrib import admin
from reversion import models as rmodels
from django.utils.html import format_html
from opal import models as omodels
from elcid import models as emodels
from opal.admin import PatientAdmin as OldPatientAdmin
from django.core.urlresolvers import reverse


class TaggingListFilter(admin.SimpleListFilter):
    title = 'team'
    parameter_name = 'team'

    def lookups(self, request, model_admin):
        tags = omodels.Tagging.objects.values_list(
            'value', flat=True
        ).distinct()
        result = []
        for i in tags:
            current_name = "{} - current".format(i)
            old_name = "{} - previously".format(i)
            result.append((current_name.replace(" ", ""), current_name,))
            result.append((old_name.replace(" ", ""), old_name,))

        return result

    def queryset(self, request, queryset):
        """
        Returns the filtered queryset based on the value
        provided in the query string and retrievable via
        `self.value()`.
        """
        # Compare the requested value (either '80s' or '90s')
        # to decide how to filter the queryset.
        value = self.value()
        if value:
            if value.endswith("-current"):
                value = value.replace("-current", "")
                tagging_qs = omodels.Tagging.objects.filter(
                    value=value, archived=False
                )
                return omodels.Patient.objects.filter(
                    episode__tagging__in=tagging_qs
                )
            else:
                value = value.replace("-previously", "")
                tagging_qs = omodels.Tagging.objects.filter(
                    value=value, archived=True
                )
                return omodels.Patient.objects.filter(
                    episode__tagging__in=tagging_qs
                )
        return omodels.Patient.objects.all()


class PatientAdmin(OldPatientAdmin):
    actions = ["refresh_lab_tests"]
    list_filter = (TaggingListFilter,)
    list_display = (
        '__str__',
        'patient_detail_link',
        'upstream_lab_results',
        'upstream_blood_culture_results',
    )

    def refresh_lab_tests(self, request, queryset):
        for patient in queryset:
            emodels.refresh_upstream_lab_tests(patient, request.user)

    def upstream_lab_results(self, obj):
        hospital_number = obj.demographics_set.first().hospital_number
        url = reverse(
            'raw_results', kwargs=dict(hospital_number=hospital_number)
        )
        return format_html("<a href='{url}'>{url}</a>", url=url)

    def upstream_blood_culture_results(self, obj):
        hospital_number = obj.demographics_set.first().hospital_number
        url = reverse(
            'raw_results', kwargs=dict(
                hospital_number=hospital_number, test_type="BLOOD CULTURE"
            )
        )
        return format_html("<a href='{url}'>{url}</a>", url=url)


    refresh_lab_tests.short_description = "Load in lab tests from upstream"


admin.site.register(rmodels.Version, admin.ModelAdmin)
admin.site.register(rmodels.Revision, admin.ModelAdmin)
admin.site.unregister(omodels.Patient)
admin.site.register(omodels.Patient, PatientAdmin)
