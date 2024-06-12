"""
Custom detail view for upstream meds
"""
from opal.core import detail


class EPMADetailView(detail.PatientDetailView):
    display_name = "EPMA"
    order        = 50
    template     = "detail/epma.html"
