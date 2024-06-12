"""
Urls for the EPMA plugin
"""
from django.urls import path

from plugins.epma import views

urlpatterns = [
    path(
        'templates/epma/order/<order_id>/',
        views.OrderDetailView.as_view(),
        name="epmaorder-detail-view"
    )
]
