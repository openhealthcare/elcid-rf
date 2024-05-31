"""
ICU specific urls
"""
from django.urls import path
from django.conf.urls import url

from plugins.icu import views

urlpatterns = [
    url(
        'templates/icu/dashboard.html',
        views.ICUDashboardView.as_view(),
        name='icu_dashboard'
    ),
    path(
        'templates/icu/activity/<year>/',
        views.ICUActivityView.as_view(),
        name='icu_activity'
    )
]
