"""
Helpers for working with Covid 19 testing
"""
from plugins.labtests import models as lab_test_models


class CovidTest(object):
    TEST_NAME        = None # Name of the test (human readable & used to filter)
    OBSERVATION_NAME = None # Observation field that contains result value
    SPECIMEN_NAME    = None # Observation field that contains specimen details
    TEST_CODE        = None # Used by lab & micro to refer to the test
    POSITIVE_RESULTS = []
    NEGATIVE_RESULTS = []

    @classmethod
    def resulted_values(klass):
        values = []
        values += klass.POSITIVE_RESULTS
        values += klass.NEGATIVE_RESULTS
        return values


class Coronavirus2019Test(CovidTest):
    TEST_NAME        = '2019 NOVEL CORONAVIRUS'
    OBSERVATION_NAME = '2019 nCoV'
    SPECIMEN_NAME    = '2019 nCoV Specimen Type'
    TEST_CODE        = 'NCOV'

    POSITIVE_RESULTS = [
        '*****Amended Result*****~Detected',
        'DETECTED',
        'Detected',
        'POSITIVE',
        'POSITIVE~SARS CoV-2 RNA DETECTED. Please maintain~appropriate Infection Prevention and Control~Measures in line with PHE Guidance.',
        'detected',
        'detected~result from ref lab',
    ]

    NEGATIVE_RESULTS = [
        'NOT detected ~ SARS CoV-2 RNA NOT Detected. ~ Please note that the testing of upper respiratory ~ tract specimens alone may not exclude SARS CoV-2 ~ infection. ~ If there is a high clinical index of suspicion, ~ please send a lower respiratory specimen (sputum, ~ BAL, EndoTracheal aspirate) to exclude SARS CoV-2 ~ where possible.',
        'Undetected~results from ref lab',
        'NOT detected~',
        'Undetected - result from ref lab',
        'Undetected~results form ref lab',
        'SARS CoV-2 not detected - result from PHE',
        'Undetetced',
        'NOT detected',
        'Not detected- PHE Ref Lab report (14/03/2020)',
        'Undetectd',
        'Undetected - results from ref lab',
        'NOT detected~SARS CoV-2 RNA NOT Detected.~Please note that the testing of upper respiratory~tract specimens alone may not exclude SARS CoV-2~infection.~If there is a high clinical index of suspicion,~please send a lower respiratory specimen (sputum,~BAL, EndoTracheal aspirate) to exclude SARS CoV-2~where possible.',
        'Undetected',
        'NOT detected ~ *****Amended Result*****',
        'NOT detected~result from ref lab'
    ]


class CrickInstituteTest(CovidTest):
    TEST_NAME        = 'CORONAVIRUS CRICK INST'
    OBSERVATION_NAME = 'SARS CoV-2 RNA'

    POSITIVE_RESULTS = [
        'POSITIVE'
    ]

    NEGATIVE_RESULTS = [
        'NOT detected'
    ]


class ReferenceLabTest(CovidTest):
    TEST_NAME        = 'CORONAVIRUS REF LAB'
    OBSERVATION_NAME = 'SARS CoV-2 RNA'
    TEST_CODE        = 'RCOV'
    SPECIMEN_NAME    = 'Specimen type'

    POSITIVE_RESULTS = [
        'Detected~2019 nCoV ORF1ab Detected (Ct value: >30)~Please note, the Ct values for detection of SARS~CoV-2 viral RNA are indicative of the viral load~in the sample, but are not quantitative PCR~values. The Ct values obtained should therefore be~interpreted with caution.~SARS CoV-2 Detected in this sample',
        '*****Amended Result***** 08/06/20~Detected',
        'Detected~ ~2019 nCoV ORF1ab Detected (Ct value: 20-30)~Please note, the Ct value for detection of SARS~CoV-2 viral RNA are indicative of the viral load~in the sample, but are not quantitative PCR~values. The Ct values obtained should therefore be~interpreted with caution.~SARS CoV-2 Detected in this sample',
        '2019 nCoV RdRp Detected',
        '2019 nCoV RdRp gene Detected',
        'POSITIVE',
        'Detected'
    ]

    NEGATIVE_RESULTS = [
        'NOT detected',
        'Undetected~ ~2019 nCoV ORF1ab Undetected~SARS CoV-2 Not detected in this sample',
        'Undetected~SARS CoV-2 NOT detected in this sample',
        '2019 nCoV ORF1ab undetected',
        'Undetected~ ~2019 nCoV ORF1ab Undetected~SARS CoV-2 Undetected in this sample',
        'Undetected',
        'Undetected~ ~2019 nCoV ORF1ab Undetected~SARS Co-2 Not detected in this sample',
        'Undetected~2019 nCoV ORF1ab Undetected~SARS CoV-2 NOT detected in this sample~Please note that the result from testing the~respiratory sample from this patient is pending',
        'Undetected~2019 nCoV ORF1ab Undetected~SARS CoV-2 NOT detected in this sample',
        '2019 nCoV RdRp gene Undetected'
    ]


class CepheidTest(CovidTest):
    TEST_NAME        = 'CORONAVIRUS CEPHEID'
    OBSERVATION_NAME = 'SARS CoV-2 RNA'
    TEST_CODE        = 'XCOV'

    POSITIVE_RESULTS = [
        'POSITIVE'
    ]

    NEGATIVE_RESULTS = [
        'NOT detected',
        'NOT Detected'
    ]


class AbbotTest(CovidTest):
    TEST_NAME        = 'CORONAVIRUS ABBOTT'
    OBSERVATION_NAME = 'SARS CoV-2 RNA'
    TEST_CODE        = 'ACOV'
    SPECIMEN_NAME    = 'Specimen Type'

    POSITIVE_RESULTS = [
        'POSITIVE'
    ]

    NEGATIVE_RESULTS = [
        'NOT Detected'
    ]


class RapidCovidAndRespiratory(CovidTest):
    TEST_NAME        = 'RAPID COVID + RESPIRATORY'
    OBSERVATION_NAME = 'SARS CoV-2 RNA'
    TEST_CODE        = 'XCOV'

    POSITIVE_RESULTS = [
        'POSITIVE'
    ]

    NEGATIVE_RESULTS = [
        'NOT detected',
        'Negative'
    ]



COVID_19_TESTS = [
    Coronavirus2019Test,
    CrickInstituteTest,
    ReferenceLabTest,
    CepheidTest,
    AbbotTest,
    RapidCovidAndRespiratory
]
COVID_19_TEST_NAMES = [t.TEST_NAME for t in COVID_19_TESTS]


def _get_covid_test(test):
    """
    Given the plugins.labtests.models.LabTest instance TEST, return
    the CovidTest subclass related to it.
    """
    for t in COVID_19_TESTS:
        if t.TEST_NAME == test.test_name:
            return t


def get_specimen_type(test):
    """
    Given the plugins.labgests.models.LabTest instance TEST which is a
    COVID 19 test, return the value of the relevant specemin type, or None
    """
    covid_test = _get_covid_test(test)
    if covid_test.SPECIMEN_NAME:
        observations = test.observation_set.filter(
            observation_name=covid_test.SPECIMEN_NAME
        )
        if observations.count() > 0:
            return observations[0].observation_value

    clean_site = test.cleaned_site
    if clean_site == 'Nasopharygeal swab':
        clean_site = 'NPS'

    return clean_site


def get_result(test):
    """
    Given the plugins.labtests.models.LabTest instance TEST, which is a
    COVID 19 test, return the value of the relevant observation result
    field.
    """
    covid_test = _get_covid_test(test)
    observations = test.observation_set.filter(
        observation_name=covid_test.OBSERVATION_NAME
    )
    if observations.count() == 0:
        return
    return observations[0].observation_value


def get_resulted_datetime(test):
    """
    Given the plugins.labtests.models.LabTest instance TEST, which is a
    COVID 19 test, return the datetime of the relevant observation
    """
    covid_test = _get_covid_test(test)
    observations = test.observation_set.filter(
        observation_name=covid_test.OBSERVATION_NAME
    )
    return observations[0].observation_datetime


def get_resulted_date(test):
    """
    Given the plugins.labtests.models.LabTest instance TEST, which is a
    COVID 19 test, return the date of the relevant observation
    """
    return get_resulted_datetime(test).date()


def resulted(test):
    """
    Predicate function to determine whether the plugins.labtests.models.LabTest
    instance TEST has returned a positive or negative result.
    """
    covid_test = _get_covid_test(test)
    result = get_result(test)
    return result in covid_test.resulted_values()


def positive(test):
    """
    Predicate function to determine whether the plugins.labtests.models.LabTest
    instance TEST is positive
    """
    covid_test = _get_covid_test(test)
    result = get_result(test)
    return result in covid_test.POSITIVE_RESULTS


def get_covid_result_ticker(patient):
    """
    Given a PATIENT, return a list of dictionaries representing the last
    3 results for each test type, with a timestamp, result string, and test name.
    """
    ticker = []

    for test in COVID_19_TESTS:
        data = []

        tests = lab_test_models.LabTest.objects.filter(
            test_name=test.TEST_NAME, patient=patient
        ).order_by('-datetime_ordered')

        for test in tests:
            if len(data) > 2:
                continue

            if not resulted(test):
                continue

            timestamp = get_resulted_datetime(test)
            value     = get_result(test)
            specimen  = get_specimen_type(test)

            result_string = "{}".format(value)

            if specimen:
                result_string += " ({})".format(specimen)

            data.append(
                {
                    'date_str' : timestamp.strftime('%d/%m/%Y %H:%M'),
                    'timestamp': timestamp,
                    'name'     : _get_covid_test(test).OBSERVATION_NAME,
                    'value'    : result_string
                }
            )

        ticker += data

    ticker = list(reversed(sorted(ticker, key=lambda i: i['timestamp'])))

    return ticker
