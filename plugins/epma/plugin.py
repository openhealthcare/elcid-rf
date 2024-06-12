"""
Opal Plugin definition for the EPMA plugin
"""
from opal.core import plugins

from plugins.epma import api
from plugins.epma.urls import urlpatterns

class EPMAPlugin(plugins.OpalPlugin):
    urls = urlpatterns

    apis = [
        (api.EPMAViewSet.basename, api.EPMAViewSet)
    ]
