from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from intrahospital_api.apis import get_api
from collections import defaultdict
from opal.core.views import json_response


class StaffRequiredMixin(object):
    @method_decorator(staff_member_required)
    def dispatch(self, *args, **kwargs):
        return super(StaffRequiredMixin, self).dispatch(*args, **kwargs)


def pivot_data(raw_lab_tests):
    # pivot the row data to make it easy to read
    row_data_dict = defaultdict(list)

    for row in raw_lab_tests:
        for key, value in row.items():
            row_data_dict[key].append(value)

    for key, row in row_data_dict.items():
        row.insert(0, key)
    return row_data_dict.values()


class PivottedData(StaffRequiredMixin, TemplateView):
    template_name = "intrahospital_api/table_view.html"
    api_method = ""
    title = ""

    def get_context_data(self, *args, **kwargs):
        api = get_api()
        ctx = super(PivottedData, self).get_context_data(
            *args, **kwargs
        )
        raw_lab_tests = getattr(api, self.api_method)(kwargs["hospital_number"])
        row_data = pivot_data(raw_lab_tests)
        row_data.sort(key=lambda x: x[0])
        ctx["row_data"] = row_data
        ctx["title"] = self.title
        return ctx


class IntrahospitalRawLabTestView(PivottedData):
    api_method = "raw_lab_tests"
    title = "Raw Lab Test View"


class IntrahospitalCookedLabTestView(PivottedData):
    api_method = "cooked_lab_tests"
    title = "Cooked Lab Test View"


class IntrahospitalCookedAppointmentsView(PivottedData):
    api_method = "tb_appointments_for_hospital_number"
    title = "TB Appointments"


class IntrahospitalRawAppointmentsView(PivottedData):
    api_method = "raw_appointments_for_hospital_number"
    title = "Raw Appointments"


@staff_member_required
def results_as_json(request, *args, **kwargs):
    api = get_api()
    results = api.lab_tests_for_hospital_number(
        kwargs["hospital_number"], **request.GET
    )
    return json_response(results)
