"""
Views for the labtests Opal Plugin
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from plugins.labtests import models


class LabTestListByName(LoginRequiredMixin, TemplateView):
    template_name = 'labtests/list_by_name.html'

    def get_context_data(self, *a, **k):
        context = super().get_context_data(*a, **k)
        context['test_name'] = k['test_name']
        context['tests'] = models.LabTest.objects.filter(test_name=k['test_name'])[:100]
        return context
