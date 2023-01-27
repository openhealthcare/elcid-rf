import datetime
import copy
from unittest import mock
from django.utils import timezone
from opal.core.test import OpalTestCase
from plugins.labtests import models as lab_test_models
from plugins.labtests import loader


FAKE_PATHOLOGY_DATA = {
    u'Abnormal_Flag': u'',
    u'Accession_number': u'73151060487',
    u'CRS_ADDRESS_LINE1': u'James Centre',
    u'CRS_ADDRESS_LINE2': u'39 Winston Terrace',
    u'CRS_ADDRESS_LINE3': u'LONDON',
    u'CRS_ADDRESS_LINE4': u'',
    u'CRS_DOB': datetime.datetime(1980, 10, 10, 0, 0),
    u'CRS_Date_of_Death': datetime.datetime(1900, 1, 1, 0, 0),
    u'CRS_Deceased_Flag': u'ALIVE',
    u'CRS_EMAIL': u'',
    u'CRS_Ethnic_Group': u'D',
    u'CRS_Forename1': u'TEST',
    u'CRS_Forename2': u'',
    u'CRS_GP_NATIONAL_CODE': u'G1004756',
    u'CRS_GP_PRACTICE_CODE': u'H84012',
    u'CRS_HOME_TELEPHONE': u'0111111111',
    u'CRS_MAIN_LANGUAGE': u'',
    u'CRS_MARITAL_STATUS': u'',
    u'CRS_MOBILE_TELEPHONE': u'',
    u'CRS_NATIONALITY': u'GBR',
    u'CRS_NHS_Number': u'',
    u'CRS_NOK_ADDRESS1': u'',
    u'CRS_NOK_ADDRESS2': u'',
    u'CRS_NOK_ADDRESS3': u'',
    u'CRS_NOK_ADDRESS4': u'',
    u'CRS_NOK_FORENAME1': u'',
    u'CRS_NOK_FORENAME2': u'',
    u'CRS_NOK_HOME_TELEPHONE': u'',
    u'CRS_NOK_MOBILE_TELEPHONE': u'',
    u'CRS_NOK_POST_CODE': u'',
    u'CRS_NOK_RELATIONSHIP': u'',
    u'CRS_NOK_SURNAME': u'',
    u'CRS_NOK_TYPE': u'',
    u'CRS_NOK_WORK_TELEPHONE': u'',
    u'CRS_Postcode': u'N6 P12',
    u'CRS_Religion': u'',
    u'CRS_SEX': u'F',
    u'CRS_Surname': u'ZZZTEST',
    u'CRS_Title': u'',
    u'CRS_WORK_TELEPHONE': u'',
    u'DOB': datetime.datetime(1964, 1, 1, 0, 0),
    u'Date_Last_Obs_Normal': datetime.datetime(2015, 7, 18, 16, 26),
    u'Date_of_the_Observation': datetime.datetime(2015, 7, 18, 16, 26),
    u'Department': u'9',
    u'Encounter_Consultant_Code': u'C2754019',
    u'Encounter_Consultant_Name': u'DR. M. SMITH',
    u'Encounter_Consultant_Type': u'',
    u'Encounter_Location_Code': u'6N',
    u'Encounter_Location_Name': u'RAL 6 NORTH',
    u'Encounter_Location_Type': u'IP',
    u'Event_Date': datetime.datetime(2015, 7, 18, 16, 47),
    u'Firstname': u'TEST',
    u'MSH_Control_ID': u'18498139',
    u'OBR-5_Priority': u'N',
    u'OBR_Sequence_ID': u'2',
    u'OBR_Status': u'F',
    u'OBR_exam_code_ID': u'ANNR',
    u'OBR_exam_code_Text': u'ANTI NEURONAL AB REFERRAL',
    u'OBX_Sequence_ID': u'11',
    u'OBX_Status': u'F',
    u'OBX_exam_code_ID': u'AN12',
    u'OBX_exam_code_Text': u'Anti-CV2 (CRMP-5) antibodies',
    u'OBX_id': 20334311,
    u'ORC-9_Datetime_of_Transaction': datetime.datetime(2015, 7, 18, 16, 47),
    u'Observation_date': datetime.datetime(2015, 7, 18, 16, 18),
    u'Order_Number': u'',
    u'Patient_Class': u'NHS',
    u'Patient_ID_External': u'7060976728',
    u'Patient_Number': u'20552710',
    u'Relevant_Clinical_Info': u'testing',
    u'Reported_date': datetime.datetime(2015, 7, 18, 16, 26),
    u'Request_Date': datetime.datetime(2015, 7, 18, 16, 15),
    u'Requesting_Clinician': u'C4369059_Chee Ronnie',
    u'Result_ID': u'0013I245895',
    u'Result_Range': u' -',
    u'Result_Units': u'',
    u'Result_Value': u'Negative',
    u'SEX': u'F',
    u'Specimen_Site': u'^&                              ^',
    u'Surname': u'ZZZTEST',
    u'Visit_Number': u'',
    u'crs_patient_masterfile_id': None,
    u'date_inserted': datetime.datetime(2015, 7, 18, 17, 0, 2, 240000),
    u'id': 5949264,
    u'last_updated': datetime.datetime(2015, 7, 18, 17, 0, 2, 240000),
    u'visible': u'Y'
}


class LoadLabTestsTestCase(OpalTestCase):
    @mock.patch('plugins.labtests.loader.results_for_hospital_number')
    def test_load_lab_tests(self, results_for_hospital_number):
        results_for_hospital_number.return_value = [FAKE_PATHOLOGY_DATA]
        patient, _ = self.new_patient_and_episode_please()
        patient.demographics_set.update(
            hospital_number=FAKE_PATHOLOGY_DATA["Patient_Number"]
        )
        loader.load_lab_tests(patient)
        lab_test = patient.lab_tests.get()
        self.assertEqual(
            lab_test.lab_number,
            FAKE_PATHOLOGY_DATA["Result_ID"]
        )
        self.assertEqual(
            lab_test.test_name,
            FAKE_PATHOLOGY_DATA["OBR_exam_code_Text"]
        )
        observation = lab_test.observation_set.get()
        self.assertEqual(
            observation.observation_name,
            FAKE_PATHOLOGY_DATA["OBX_exam_code_Text"]
        )
        self.assertEqual(
            observation.observation_value,
            FAKE_PATHOLOGY_DATA["Result_Value"]
        )
