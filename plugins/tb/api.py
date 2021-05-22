"""
Specific API endpoints for the TB module
"""
from django.utils import timezone
from opal.core.views import json_response
from opal.core.api import patient_from_pk, LoginRequiredViewset

from plugins.tb.utils import get_tb_summary_information


class TbTestSummary(LoginRequiredViewset):
    base_name = 'tb_test_summary'
    """"
    Example payload

    return [
        {
            name: 'C REACTIVE PROTEIN',
            date: '',
            result: '1'
        },
        {
            name: 'ALT',
            date: '',
            result: '1'
        }
    ]
    """
    @patient_from_pk
    def retrieve(self, request, patient):
        tb_summary_information = get_tb_summary_information(patient)
        recent_results = []
        for obs_name, summary in tb_summary_information.items():
            recent_results.append({
                "name": obs_name,
                "date": summary["observation_datetime"],
                "result": summary["observation_value"]
            })

        return json_response(dict(recent_results=recent_results))
