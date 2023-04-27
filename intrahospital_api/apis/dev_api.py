from intrahospital_api import constants
from intrahospital_api.apis import base_api, prod_api
from datetime import date, timedelta, datetime
from elcid.models import (
    Demographics, ContactInformation, NextOfKinDetails, GPDetails,
    MasterFileMeta
)
import random

RAW_TEST_DATA = {
    u'Abnormal_Flag': u'',
    u'Accession_number': u'73151060487',
    u'CRS_ADDRESS_LINE1': u'Jameson Centre',
    u'CRS_ADDRESS_LINE2': u'39 Windsor Terrace',
    u'CRS_ADDRESS_LINE3': u'LONDON',
    u'CRS_ADDRESS_LINE4': u'',
    u'CRS_DOB': datetime(1980, 10, 10, 0, 0),
    u'CRS_Date_of_Death': datetime(1900, 1, 1, 0, 0),
    u'CRS_Deceased_Flag': u'ALIVE',
    u'CRS_EMAIL': u'',
    u'CRS_Ethnic_Group': u'D',
    u'CRS_Forename1': u'TEST',
    u'CRS_Forename2': u'',
    u'CRS_GP_NATIONAL_CODE': u'G1005756',
    u'CRS_GP_PRACTICE_CODE': u'H85012',
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
    u'DOB': datetime(1964, 1, 1, 0, 0),
    u'Date_Last_Obs_Normal': datetime(2015, 7, 18, 16, 26),
    u'Date_of_the_Observation': datetime(2015, 7, 18, 16, 26),
    u'Department': u'9',
    u'Encounter_Consultant_Code': u'C2754019',
    u'Encounter_Consultant_Name': u'DR. M. SMITH',
    u'Encounter_Consultant_Type': u'',
    u'Encounter_Location_Code': u'6N',
    u'Encounter_Location_Name': u'RAL 6 NORTH',
    u'Encounter_Location_Type': u'IP',
    u'Event_Date': datetime(2015, 7, 18, 16, 47),
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
    u'ORC-9_Datetime_of_Transaction': datetime(2015, 7, 18, 16, 47),
    u'Observation_date': datetime(2015, 7, 18, 16, 18),
    u'Order_Number': u'',
    u'Patient_Class': u'NHS',
    u'Patient_ID_External': u'7060976728',
    u'Patient_Number': u'20552710',
    'PV1_7_C_NUMBER': '',
    'PV1_7_CONSULTANT_NAME': '',
    'PV1_3_5': None,
    'PV1_3_9': None,
    u'Relevant_Clinical_Info': u'testing',
    u'Reported_date': datetime(2015, 7, 18, 16, 26),
    u'Request_Date': datetime(2015, 7, 18, 16, 15),
    u'Requesting_Clinician': u'C4369059_Claire Jameson',
    u'Result_ID': u'0013I245895',
    u'Result_Range': u' -',
    u'Result_Units': u'',
    u'Result_Value': u'Negative',
    u'SEX': u'F',
    u'Specimen_Site': u'^&                              ^',
    u'Surname': u'ZZZTEST',
    u'Visit_Number': u'',
    u'crs_patient_masterfile_id': None,
    u'date_inserted': datetime(2015, 7, 18, 17, 0, 2, 240000),
    u'id': 5949264,
    u'last_updated': datetime(2015, 7, 18, 17, 0, 2, 240000),
    'obr_id': 2000000,
    'result_source': 'RF',
    u'visible': u'Y'
}

# this data may not be representative of upstream data
RAW_MASTER_FILE_DATA = {
    "ID": 1,
    "CRS_GP_MASTERFILE_ID": 2,
    "PATIENT_NUMBER": "123",
    "NHS_NUMBER": "456",
    "TITLE": "Mrs",
    "FORENAME1": "Gemima",
    "FORENAME2": "Philipa",
    "SURNAME": "Rogers",
    "DOB": datetime(2015, 7, 18, 16, 26),
    "ADDRESS_LINE1": "1 Church rd",
    "ADDRESS_LINE2": "Whittington",
    "ADDRESS_LINE3": "West Weybridge",
    "ADDRESS_LINE4": "East Anglia",
    "POSTCODE": "N12 5BC",
    "GP_NATIONAL_CODE": "234",
    "GP_PRACTICE_CODE": "345",
    "HOME_TELEPHONE": "0970 123 5467",
    "WORK_TELEPHONE": "0170 123 5467",
    "MOBILE_TELEPHONE": "0870 123 5467",
    "EMAIL": "rogers@gmail.com",
    "SEX": "F",
    "RELIGION": "Agnostic",
    "ETHNIC_GROUP": "G",
    "MAIN_LANGUAGE": "Spanish",
    "NATIONALITY": "",
    "MARITAL_STATUS": "",
    "DEATH_FLAG": "",
    "DATE_OF_DEATH": "",
    "NOK_TYPE": "UNKNOWN",
    "NOK_SURNAME": "WILSON",
    "NOK_FORENAME1": "JOSHUA",
    "NOK_FORENAME2": "MAXIMILLIAN",
    "NOK_relationship": "FATHER",
    "NOK_address1": "1 Station Rd",
    "NOK_address2": "Whistable",
    "NOK_address3": "Kent",
    "NOK_address4": "UK",
    "NOK_Postcode": "CT5",
    "nok_home_telephone": "0204 456 6780",
    "nok_work_telephone": "0205 567 890",
    "ACTIVE_INACTIVE": "",
    "MERGED": "",
    "MERGE_COMMENTS": "",
    "LAST_UPDATED": None,
    "INSERT_DATE": None,
    "gp_title": "DR",
    "GP_INITIALS": "S",
    "GP_SURNAME": "PATEL",
    "GP_ADDRESS1": "12 HABOUR WALK",
    "GP_ADDRESS2": "EASTLY",
    "GP_ADDRESS3": "",
    "GP_ADDRESS4": "",
    "GP_POSTCODE": "EA19 4BJ",
    "GP_TELEPHONE": "",
}


MALE_FIRST_NAMES = [
    "Oliver",
    "George",
    "Harry",
    "Jack",
    "Jacob",
    "Noah",
    "Charlie",
    "Muhammad",
    "Thomas",
    "Oscar",
]

FEMALE_FIRST_NAMES = [
    "Olivia",
    "Amelia",
    "Isla",
    "Ava",
    "Emily",
    "Isabella",
    "Mia",
    "Poppy",
    "Ella",
    "Lily",
]

LAST_NAMES = [
    "Smith",
    "Jones",
    "Patel",
    "Brown",
    "Singh",
    "Williams",
    "Taylor",
    "Wilson",
    "Davies",
    "Evans",
]

# So this is basic meta information about some tests that come through
# we will then use this to create mock results
TEST_BASES = {
    "B12 AND FOLATE SCREEN": {
        "Vitamin B12": {
            "reference_range": "160 - 925",
            "units": "ng/L"
        },
        "Folate": {
            "reference_range": "3.9 - 26.8",
            "units": "ng/L"
        }
    },
    "C REACTIVE PROTEIN": {
        "C Reactive Protein": {
            "units": "mg/L",
            "reference_range": "0 - 5"
        }
    },
    "FULL BLOOD COUNT": {
        "Hb": {
            "units": "g/l",
            "reference_range": "110 - 150"
        },
        "WBC": {
            "units": "g/l",
            "reference_range": "3.5 - 11"
        },
        "Platelets": {
            "units": "10",
            "reference_range": "140 - 400"
        },
        "RBC": {
            "units": "10",
            "reference_range": "3.8 - 5.4"
        },
        "HCT": {
            "units": "%",
            "reference_range": "11 - 16"
        },
        "Lymphocytes": {
            "units": "10",
            "reference_range": "1 - 4"
        },
        "Neutrophils": {
            "units": "10",
            "reference_range": "1.7 - 7.5"
        }
    },
    "CLOTTING SCREEN": {
        "INR": {
            "units": "Ratio",
            "reference_range": "0.9 - 1.12"
        }
    },
    "LIVER PROFILE": {
        "ALT": {
            "units": "U/L",
            "reference_range": "10 - 35"
        },
        "AST": {
            "units": "U/L",
            "reference_range": "0 - 31"
        },
        "Alkaline Phosphatase": {
            "units": "U/L",
            "reference_range": "0 - 129"
        },
        "Total Bilirubin": {
            "units": "umol/L",
            "reference_range": '0 - 21'
        }
    },
    "QUANTIFERON TB GOLD IT": {
        "QFT IFN gamma result (TB1)": {
            "units": "IU/mL",
            "reference_range": " -",
            "observation_value": "0.00"

        },
        "QFT IFN gamme result (TB2)": {
            "units": "IU/mL",
            "reference_range": " -",
            "observation_value": "0.00"

        },
        "QFT TB interpretation": {
             "units": "",
             "reference_range": " -",
             "observation_value": "INDETERMINATE"
        },

    },
    "25-OH Vitamin D": {
        "25-OH Vitamin D": {
            "units": "nmol/L",
            "reference_range": "",
            "observation_value": "".join([
                "43~Deficient if < 25 nmol/L~Insufficent if 25 - 75 nmol/L~",
                "Possible Toxicity if > 250 nmol/L~Note assay change to ",
                "Roche Gen II from 26/2/18.~Results >75 nmol/L average approx ",
                "20% lower"
            ])
        }
    },
    "HEPATITIS B SURFACE AG": {
        "Hepatitis B 's'Antigen........": {
            "units": "",
            "reference_range": " -",
            "observation_value": "Negative"
        }
    },
    "HEPATITIS C ANTIBODY": {
        "Hepatitis C IgG Antibody......": {
            "units": "",
            "reference_range": " -",
            "observation_value": "Negative"
        }
    },
    "HIV 1 + 2 ANTIBODIES": {
        "HIV 1 + 2 Antibodies..........": {
            "units": "",
            "reference_range": " -",
            "observation_value": "Negative"
        }
    }
}


class DevApi(base_api.BaseApi):
    def get_date_of_birth(self):
        some_date = date.today() - timedelta(random.randint(1, 365 * 70))
        some_dt = datetime.combine(
            some_date, datetime.min.time()
        )
        return some_dt.strftime('%d/%m/%Y')

    def patient_masterfile(self, hospital_number):
        demographics_dict = prod_api.MainDemographicsRow(
            RAW_MASTER_FILE_DATA
        ).get_demographics_dict()
        demographics_dict.update(self.demographics(hospital_number))
        return {
            Demographics.get_api_name(): demographics_dict,
            ContactInformation.get_api_name(): prod_api.get_contact_information(RAW_MASTER_FILE_DATA),
            NextOfKinDetails.get_api_name(): prod_api.get_next_of_kin_details(RAW_MASTER_FILE_DATA),
            GPDetails.get_api_name(): prod_api.get_gp_details(RAW_MASTER_FILE_DATA),
            MasterFileMeta.get_api_name(): prod_api.get_master_file_meta(RAW_MASTER_FILE_DATA),
        }

    def demographics(self, hospital_number):
        # will always be found unless you prefix it with 'x'
        if hospital_number.startswith('x'):
            return

        sex = random.choice(["Male", "Female"])
        if sex == "Male":
            first_name = random.choice(MALE_FIRST_NAMES)
            title = random.choice(["Dr", "Mr", "Not Specified"])
        else:
            first_name = random.choice(FEMALE_FIRST_NAMES)
            title = random.choice(["Dr", "Ms", "Mrs", "Not Specified"])

        return dict(
            date_of_birth=self.get_date_of_birth(),
            ethnicity="Other",
            external_system=constants.EXTERNAL_SYSTEM,
            first_name=first_name,
            hospital_number=hospital_number,
            nhs_number=self.get_external_identifier(),
            sex=sex,
            surname=random.choice(LAST_NAMES),
            title=title
        )

    def get_external_identifier(self):
        random_str = str(random.randint(0, 100000000))
        return "{}{}".format("0" * (9-len(random_str)), random_str)

    def get_observation_value(self, reference_range):
        """
            splits the reference range, casts it to an integer
            returns a result around those boundaries
        """
        min_result, max_result = [
            float(i.strip()) for i in reference_range.split("-")
        ]
        acceptable_range = max_result - min_result
        random_result = round(random.uniform(min_result, acceptable_range), 1)
        deviation = round(random.uniform(acceptable_range/3, acceptable_range))
        plus_minus = random.randint(0, 1)

        if plus_minus:
            return random_result + deviation
        else:
            return random_result - deviation

    def create_observation_dict(
        self,
        test_base_observation_name,
        test_base_observation_value,
        base_datetime=None
    ):
        """
        should return something like...
        {
            "last_updated": "18 Jul 2019, 4:18 p.m.",
            "observation_datetime": "18 Jul 2015, 4:18 p.m."
            "observation_name": "Aerobic bottle culture",
            "observation_number": "12312",
            "reference_range": "3.5 - 11",
            "units": "g"
        }

        """
        if base_datetime is None:
            base_datetime = datetime.now()

        if "observation_value" in test_base_observation_value:
            obvs_value = test_base_observation_value["observation_value"]
        else:
            obvs_value = str(self.get_observation_value(
                test_base_observation_value["reference_range"]
            ))

        return dict(
            last_updated=(base_datetime - timedelta(minutes=20)).strftime(
                '%d/%m/%Y %H:%M:%S'
            ),
            observation_datetime=(base_datetime - timedelta(1)).strftime(
                '%d/%m/%Y %H:%M:%S'
            ),
            observation_name=test_base_observation_name,
            observation_number=self.get_external_identifier(),
            observation_value=obvs_value,
            reference_range=test_base_observation_value["reference_range"],
            units=test_base_observation_value["units"],
        )

    def results_for_hospital_number(self, hospital_number, **filter_kwargs):
        """ We expect a return of something like
            {
                clinical_info:  u'testing',
                datetime_ordered: "18/07/2015 04:15",
                external_identifier: "1111",
                site: u'^&                              ^',
                status: "Sucess",
                test_code: "AN12"
                test_name: "Anti-CV2 (CRMP-5) antibodies",
                observations: [{
                    "last_updated": "18/07/2015 04:15",
                    "observation_datetime": "18/07/2015 04:15"
                    "observation_name": "Aerobic bottle culture",
                    "observation_number": "12312",
                    "reference_range": "3.5 - 11",
                    "units": "g"
                }]
            }
        """
        result = []
        for i, v in TEST_BASES.items():
            for date_t in range(10):
                base_datetime = datetime.now() - timedelta(date_t)
                result.append(dict(
                    clinical_info=u'testing',
                    datetime_ordered=base_datetime.strftime(
                        '%d/%m/%Y %H:%M:%S'
                    ),
                    external_identifier=self.get_external_identifier(),
                    external_system=constants.EXTERNAL_SYSTEM,
                    status="complete",
                    site=u'^&                              ^',
                    test_code=i.lower().replace(" ", "_"),
                    test_name=i,
                    observations=[
                        self.create_observation_dict(
                            o, y, base_datetime=base_datetime
                        ) for o, y in v.items()
                    ]
                ))

        return result

    def raw_data(self, hospital_number, **filter_kwargs):
        return [RAW_TEST_DATA]

    def data_deltas(self, some_datetime):
        return []
