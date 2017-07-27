from mock import patch, MagicMock
from copy import copy
import json

from django.test import override_settings

from opal.core.test import OpalTestCase
from opal.core.search import queries
from opal import models as omodels


@patch("elcid.gloss_api.requests.get")
class SearchTestCase(OpalTestCase):
    returned_gloss_result = {
        'demographics': [{
            'first_name': 'Jane',
            'surname': 'Smith',
            'middle_name': None,
            'title': 'Ms',
            'gp_practice_code': None,
            'post_code': None,
            'ethnicity': None,
            'sex': None,
            'marital_status': None,
            'death_indicator': False,
            'date_of_birth': '12/12/1983',
            'date_of_death': None,
        }],
        'duplicate_patient': []
    }

    criteria = [{
        "queryType": "Equals",
        "query": "1231111",
        "field": "Hospital Number",
        'combine': 'and',
        'column': u'demographics',
    }]

    @override_settings(
        OPAL_SEARCH_BACKEND="elcid.search.GlossQuery",
        GLOSS_URL_BASE="http://0.0.0.0:6767"
    )
    def test_gloss_query_flow(self, requests_mock):
        requests_mock.return_value = MagicMock()
        requests_mock.return_value.content = json.dumps({
            "status": "success",
            "messages": self.returned_gloss_result
        })
        requests_mock.return_value.status_code = 200
        self.assertFalse(omodels.Patient.objects.exists())
        query = queries.create_query(self.user, self.criteria)

        result = query.patients_as_json()[0]

        expected = copy(self.returned_gloss_result)
        expected["demographics"][0]["hospital_number"] = "1231111"
        expected["demographics"][0]["external_system"] = "Carecast"
        self.assertEqual(result, expected)
        requests_mock.assert_called_once_with(
            "http://0.0.0.0:6767/api/patient/1231111"
        )

    def test_database_flow(self, requests_mock):
        patient = omodels.Patient.objects.create()
        patient.create_episode()
        demographics = patient.demographics_set.first()
        demographics.hospital_number = "1231111"
        demographics.first_name = "Sue"
        demographics.save()
        query = queries.create_query(self.user, self.criteria)
        result = query.patients_as_json()[0]
        self.assertEqual(result["demographics"][0]["first_name"], "Sue")
        self.assertFalse(requests_mock.called)
