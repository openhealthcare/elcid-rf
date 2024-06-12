"""
Views for the EPMA plugin
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from plugins.epma import models


class OrderDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'epma/order_detail.html'

    def get_context_data(self, *a, **k):
        context = super().get_context_data(*a, **k)

        order = models.EPMAMedOrder.objects.get(o_order_id=k['order_id'])

        context['order'] = order
        context['order_detail'] = order.epmamedorderdetail_set.all()
        return context
