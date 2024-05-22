"""
Urls for the labtests Opal plugin
"""
from django.urls import path

from plugins.labtests import views

urlpatterns = [
    # path(
    #     'templates/lab/detail-modal/<lab_number>/',
    #     views.LabDetailModal.as_view(),
    #     name='lab_detail_modal'
    # ),
    path(
        'templates/labtests/<test_name>/',
        views.LabTestListByName.as_view(),
        name="labtests-list-by-view"
    )
]
