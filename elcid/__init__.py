"""
elCID Royal Free Hospital implementation
"""

from opal.core import application
from opal.core import menus
from plugins.ipc.constants import IPC_ROLE
from elcid import episode_categories


class StandardAddPatientMenuItem(menus.MenuItem):
    def for_user(self, user):
        if not user:
            return False

        if not user.is_authenticated:
            return False

        from opal.models import UserProfile
        if user and user.is_superuser:
            return True

        profile = UserProfile.objects.get(user=user)
        if profile.readonly:
            return False
        return True


standard_add_patient_menu_item = StandardAddPatientMenuItem(
    href='/pathway/#/add_patient',
    display='Add Patient',
    icon='fa fa-plus',
    activepattern='/pathway/#/add_patient'
)


class Application(application.OpalApplication):
    schema_module = 'elcid.schema'
    javascripts = [
        'js/elcid/routes.js',
        'js/elcid/filters.js',
        'js/elcid/directives.js',
        'js/elcid/controllers/discharge.js',
        'js/elcid/controllers/clinical_timeline.js',
        'js/elcid/controllers/welcome.js',
        'js/elcid/controllers/lab_test_json_dump_view.js',
        'js/elcid/controllers/result_view.js',
        'js/elcid/controllers/rfh_find_patient.js',
        'js/elcid/controllers/blood_culture_panel.js',
        'js/elcid/controllers/general_edit.js',
        'js/elcid/controllers/general_delete.js',
        'js/elcid/controllers/remove_patient_step.js',
        'js/elcid/controllers/add_to_service.js',
        'js/elcid/services/demographics_search.js',
        'js/elcid/controllers/tagging_step.js',
        'js/elcid/controllers/investigations.js',
        'js/elcid/controllers/add_antifungal_patients.js',

        'js/elcid/services/blood_culture_isolate.js',
        'js/elcid/services/clinical_advice.js',
        'js/elcid/services/blood_culture_loader.js',
        'js/elcid/services/lab_test_results.js',
        'js/elcid/services/demographics_search.js',
        'js/elcid/services/lab_test_summary_loader.js',
        'js/elcid/services/lab_test_json_dump.js',
        'js/elcid/services/episode_added_comparator.js',
    ]

    styles = [
        "css/elcid.css"
    ]

    patient_view_forms = {
        "General Consultation": "inline_forms/clinical_advice.html",
    }

    default_episode_category = episode_categories.InfectionService.display_name

    @classmethod
    def get_menu_items(cls, user):
        if not user or not user.is_authenticated:
            return []

        menu_items = super(Application, cls).get_menu_items(user)

        for item in menu_items:
            if item.href == '/#/list/':
                item.href = '/#/list/bacteraemia'

        if standard_add_patient_menu_item.for_user(user):
            menu_items.append(standard_add_patient_menu_item)

        if user.is_superuser:
            menu_items.append(
                menus.MenuItem(
                    href='/#/beta/',
                    display='Beta',
                    icon='fa fa-bath',
                    activepattern='beta'
                )
            )

        from opal.models import UserProfile
        profile = UserProfile.objects.get(user=user)

        if profile.roles.filter(name=IPC_ROLE).exists():
            menu_items.append(
                menus.MenuItem(
                    href='/#/ipc/',
                    display='IPC',
                    icon='fa fa-warning',
                    activepattern='ipc'
                )
            )

        return menu_items
