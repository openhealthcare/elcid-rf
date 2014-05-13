
from elcid import models
from opal import models as omodels

list_columns = [
    models.Demographics,
    models.Location,
    models.Diagnosis,
    models.PastMedicalHistory,
    models.Travel,
    models.Antimicrobial,
    models.MicrobiologyTest,
    models.GeneralNote,
    models.Todo,
]

list_columns_opat = [
    models.Demographics,
    models.Location,
    models.Diagnosis,
    models.Antimicrobial,
    models.MicrobiologyTest,
    models.Line,
    models.OPATOutstandingIssues
]

list_columns_opat_review = [
    models.Antimicrobial,
]

list_schemas = {
    'default': list_columns,
    'opat': {
        'default': list_columns_opat,
#        'opat_review': list_columns_opat_review
        }
}

detail_columns = [
    models.Demographics,
    models.ContactDetails,
    models.Carers,
    models.Location,
    models.Diagnosis,
    models.PastMedicalHistory,
    models.Antimicrobial,
    models.Allergies,
    models.MicrobiologyTest,
    models.Line,
    models.MicrobiologyInput,
    models.OPATReview,
    models.Travel,
    models.Todo,
    models.OPATOutstandingIssues,
    models.GeneralNote,
]

extract_columns = [
    omodels.Tagging,
    models.Demographics,
    models.Location,
    models.Diagnosis,
    models.Antimicrobial,
    models.Allergies,
    models.PastMedicalHistory,
    models.MicrobiologyInput,
    models.MicrobiologyTest,
    models.Travel,
    models.Todo,
    models.GeneralNote,
    ]
