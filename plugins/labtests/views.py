"""
Views for the labtests Opal Plugin
"""
import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from plugins.labtests import models


class LabTestListByName(LoginRequiredMixin, TemplateView):
    template_name = 'labtests/list_by_name.html'

    def get_context_data(self, *a, **k):
        context = super().get_context_data(*a, **k)

        time_ago = datetime.datetime.now() - datetime.timedelta(days=31*6)
        tests = models.LabTest.objects.filter(
            test_name=k['test_name'],
            datetime_ordered__gte=time_ago
        )
        count = tests.count()

        context['test_name'] = k['test_name']
        context['tests'] = tests
        context['count'] = count
        return context
