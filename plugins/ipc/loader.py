"""
Load utilities for the IPC module
"""
from elcid.models import Demographics, MergedMRN
from elcid.episode_categories import InfectionService
from intrahospital_api.apis.prod_api import ProdApi as ProdAPI
from intrahospital_api.loader import create_rfh_patient_from_hospital_number

from plugins.ipc import lab


Q_GET_DISTINCT_MRNS_FOR_TEST =  """
SELECT DISTINCT Patient_Number FROM tQuest.Pathology_Result_view
WHERE OBR_exam_code_Text = @TEST_NAME
"""

def load_all_extra_ipc_patients():
    """
    Load historic patients who have had IPC tests
    """
    api = ProdAPI()
    all_tested_mrns = set()

    for test in lab.IPC_TESTS:
        tested_mrns = api.execute_trust_query(
            Q_GET_DISTINCT_MRNS_FOR_TEST,
            params={'test_name': test.TEST_NAME}
        )
        # elcid does not use zero prefixed MRNs but the lab test
        # system does so strip off any zeros.
        all_tested_mrns.update([
            r['Patient_Number'].lstrip('0') for r in tested_mrns
        ])

    demographics_mrns = list(
        Demographics.objects.values_list('hospital_number', flat=True)
    )

    merged_mrns = list(
        MergedMRN.objects.values_list('mrn', flat=True)
    )

    all_mrns = set(demographics_mrns + merged_mrns)
    new_mrns = all_tested_mrns.difference(all_mrns)
    num_new = len(new_mrns)
    print(f"{num_new} New MRNs")

    i = 0
    for mrn in new_mrns:
        if i > 5000:
            return

        create_rfh_patient_from_hospital_number(mrn, InfectionService)

        i += 1
