"""
Models for the elCID admissions plugin
"""
import datetime

from django.db import models
from opal.models import Patient, PatientSubrecord

from plugins.admissions import logger
from plugins.admissions import constants


class PatientEncounterStatus(PatientSubrecord):
    _is_singleton = True

    has_encounters = models.BooleanField(default=False)


class Encounter(models.Model):
    """
    An Encounter at the hospital as defined by Cerner / ADT

    These are transmitted as HL7 messages and then stored in an RFH
    SQL database which we poll to populate this table.

    Here we replicate that database table closely, even though we don't
    currently use all fields.

    Our table should be the equivalent of the upstream table, filtered
    to only inlcude our elCID cohort.
    """
    # We link the upstream data to our system via a single foreign key to the
    # Patient object. In practice we take the MRN fields and match them
    # with patient.demographics().hospital_number
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='encounters')

    # Note: Field - level comments here are from the documentation provided by the integration team
    # Internal SQL Database identifier - Primary Key
    upstream_id                        = models.IntegerField(blank=True, null=True)
    # HL7 Message Datetime sent from Cerner
    msh_7                              = models.DateTimeField(blank=True, null=True)
    # Last HL7 Message update Type
    msh_9_msg_type                     = models.CharField(blank=True, null=True, max_length=4)
    evn_2_movement_date                = models.DateTimeField(blank=True, null=True)             # Cerner Event Datetime
    pid_3_mrn                          = models.CharField(blank=True, null=True, max_length=255) # Patient Hospital Number
    pid_3_nhs                          = models.CharField(blank=True, null=True, max_length=255) # Patient NHS Number
    pid_18_account_number              = models.CharField(blank=True, null=True, max_length=25)  # Encounter ID
    pv1_2_patient_class                = models.CharField(blank=True, null=True, max_length=50)
    # Cerner Facility - Not very usefull
    pv1_3_hospital                     = models.CharField(blank=True, null=True, max_length=50)
    pv1_3_ward                         = models.CharField(blank=True, null=True, max_length=50)  # Location
    pv1_3_room                         = models.CharField(blank=True, null=True, max_length=50)
    pv1_3_bed                          = models.CharField(blank=True, null=True, max_length=50)
    pv1_3_ambulatory_indicator         = models.CharField(blank=True, null=True, max_length=50)
    # Cerner building - much better for identifying by site
    pv1_3_building                     = models.CharField(blank=True, null=True, max_length=50)
    pv1_4_admission_type               = models.CharField(blank=True, null=True, max_length=50)
    pv1_6_hospital                     = models.CharField(blank=True, null=True, max_length=50)  # Previous Facility
    pv1_6_ward                         = models.CharField(blank=True, null=True, max_length=50)  # Previous Location
    pv1_6_room                         = models.CharField(blank=True, null=True, max_length=50)  # Previous Room
    pv1_6_bed                          = models.CharField(blank=True, null=True, max_length=50)  # Previous Bed
    # Encounter clinician NACS code
    pv1_7_consultant_code              = models.CharField(blank=True, null=True, max_length=50)
    consultant_name                    = models.CharField(blank=True, null=True, max_length=50)  # Encounter clinician name
    # Encounter Speciality code
    # 3 digit = National speciality
    # 5 digit = local Treat function where 1st 3 digits in the parent national speciality code
    pv1_10_speciality_code             = models.CharField(blank=True, null=True, max_length=50)
    # Encounter Speciality Description
    speciality_name                    = models.CharField(blank=True, null=True, max_length=50)
    pv1_14_admission_source            = models.CharField(blank=True, null=True, max_length=50)
    pv1_18_visit_patient_type_original = models.CharField(blank=True, null=True, max_length=50)
    pv1_18_visit_patient_type_product  = models.CharField(blank=True, null=True, max_length=50)
    # Cerner Encounter Visit ID
    pv1_19_hsn                         = models.CharField(blank=True, null=True, max_length=50)
    pv1_41_account_status              = models.CharField(blank=True, null=True, max_length=50)
    # Registered GP Practice Code
    pd1_3_practice_code                = models.CharField(blank=True, null=True, max_length=50)
    # Registered GP National Code
    pd1_4_national_code                = models.CharField(blank=True, null=True, max_length=50)
    # Cerner Encounter Admission Datetime
    pv1_44_admit_date_time             = models.DateTimeField(blank=True, null=True)
    # Cerner Encounter Discharge Datetime
    pv1_45_discharge_date_time         = models.DateTimeField(blank=True, null=True)
    pv2_2_patient_type                 = models.CharField(blank=True, null=True, max_length=50)
    fin_hsn                            = models.CharField(blank=True, null=True, max_length=50)
    # SQL database update timestamp
    last_updated                       = models.DateTimeField(blank=True, null=True)
    # SQL database insert timestamp
    insert_date                        = models.DateTimeField(blank=True, null=True)
    # MRN of parent record following a Cerner Merge
    parent_mrn                         = models.CharField(blank=True, null=True, max_length=20)
    # Comments explaining that the patient was merged
    comments                           = models.TextField(blank=True, null=True)

    UPSTREAM_FIELDS_TO_MODEL_FIELDS = {
        'ID'                                : 'upstream_id',
        'MSH_7'                             : 'msh_7',
        'MSH_9_MSG_TYPE'                    : 'msh_9_msg_type',
        'EVN_2_MOVEMENT_DATE'               : 'evn_2_movement_date',
        'PID_3_MRN'                         : 'pid_3_mrn',
        'PID_3_NHS'                         : 'pid_3_nhs',
        'PID_18_ACCOUNT_NUMBER'             : 'pid_18_account_number',
        'PV1_2_PATIENT_CLASS'               : 'pv1_2_patient_class',
        'PV1_3_HOSPITAL'                    : 'pv1_3_hospital',
        'PV1_3_WARD'                        : 'pv1_3_ward',
        'PV1_3_ROOM'                        : 'pv1_3_room',
        'PV1_3_BED'                         : 'pv1_3_bed',
        'PV1_3_AMBULATORY_INDICATOR'        : 'pv1_3_ambulatory_indicator',
        'PV1_3_BUILDING'                    : 'pv1_3_building',

        # WHAT ARE THESE CODES?
        'PV1_4_ADMISSION_TYPE'              : 'pv1_4_admission_type',

        'PV1_6_HOSPITAL'                    : 'pv1_6_hospital',
        'PV1_6_WARD'                        : 'pv1_6_ward',
        'PV1_6_ROOM'                        : 'pv1_6_room',
        'PV1_6_BED'                         : 'pv1_6_bed',
        'PV1_7_CONSULTANT_CODE'             : 'pv1_7_consultant_code',
        'CONSULTANT_NAME'                   : 'consultant_name',
        'PV1_10_SPECIALITY_CODE'            : 'pv1_10_speciality_code',
        'SPECIALITY_NAME'                   : 'speciality_name',

        # WHAT ARE THESE CODES?
        'PV1_14_ADMISSION_SOURCE'           : 'pv1_14_admission_source',

        'PV1_18_VISIT_PATIENT_TYPE_ORIGINAL': 'pv1_18_visit_patient_type_original',
        'PV1_18_VISIT_PATIENT_TYPE_PRODUCT' : 'pv1_18_visit_patient_type_product',
        'PV1_19_HSN'                        : 'pv1_19_hsn',
        'PV1_41_ACCOUNT_STATUS'             : 'pv1_41_account_status',
        'PD1_3_PRACTICE_CODE'               : 'pd1_3_practice_code',
        'PD1_4_NATIONAL_CODE'               : 'pd1_4_national_code',
        'PV1_44_ADMIT_DATE_TIME'            : 'pv1_44_admit_date_time',
        'PV1_45_DISCHARGE_DATE_TIME'        : 'pv1_45_discharge_date_time',
        'PV2_2_PATIENT_TYPE'                : 'pv2_2_patient_type',
        'FIN_HSN'                           : 'fin_hsn',
        'LAST_UPDATED'                      : 'last_updated',
        'INSERT_DATE'                       : 'insert_date',
        'PARENT_MRN'                        : 'parent_mrn',
        'COMMENTS'                          : 'comments',
    }

    # Although we maintain the upstream column names with minimal alterations,
    # there is no real utility in sending metadata about the original HL7v2 message
    # ADT format fieldnames through to the front end and using them in templates.
    #
    # Accdcordingly we re-name the fields that we will serialise via the API to
    # more usable properties to be rendered in templates
    FIELDS_TO_SERIALIZE = {
        'evn_2_movement_date'       : 'movement_date',
        'pv1_2_patient_class'       : 'patient_class',
        'pv1_3_ward'                : 'ward',
        'pv1_3_room'                : 'room',
        'pv1_3_bed'                 : 'bed',
        'consultant_name'           : 'consultant_name',
        'speciality_name'           : 'speciality_name',
        'pv1_44_admit_date_time'    : 'admit_datetime',
        'pv1_45_discharge_date_time': 'discharge_datetime',
        'pv1_3_ambulatory_indicator': 'ambulatory_indicator',
        'pid_18_account_number'     : 'spell_number',
        'fin_hsn'                   : 'fin_hsn',
    }

    def to_dict(self):
        """
        Serialise an encounter instance for use on the client
        """
        serialized =  {
            dictfield: getattr(self, modelfield)
            for modelfield, dictfield in self.FIELDS_TO_SERIALIZE.items()
        }

        if self.msh_9_msg_type:
            try:
                serialized['last_update_type'] = constants.MESSAGE_CODES[self.msh_9_msg_type]
            except KeyError:
                logger.error(f'Unknown Message Code {self.msh_9_msg_type}')
                serialized['last_update_type'] = 'UNKNOWN'

        serialized['hospital'] = constants.BUILDING_CODES.get(self.pv1_3_building, self.pv1_3_building)
        serialized['patient_id'] = self.patient_id

        return serialized


class UpstreamLocation(models.Model):
    """
    For ease of querying, and to prevent multiple occupancy,
    we de-normalize the upstream location data.

    Two patients cannot occupy the same bed.
    """
    patient   = models.ForeignKey(Patient, blank=True, null=True, on_delete=models.SET_NULL, related_name='upstreamlocation')
    encounter = models.ForeignKey(Encounter, blank=True, null=True, on_delete=models.SET_NULL, related_name='encounter')
    hospital  = models.CharField(blank=True, null=True, max_length=50)
    building  = models.CharField(blank=True, null=True, max_length=50)
    ward      = models.CharField(blank=True, null=True, max_length=50)
    room      = models.CharField(blank=True, null=True, max_length=50)
    bed       = models.CharField(blank=True, null=True, max_length=50)
    admitted  = models.DateTimeField(blank=True, null=True)


class TransferHistory(models.Model):
    """
    A Transfer history sequence as defined by Cerner
    Obtained via the data warehousing team

    Here we replicate the upstream view closely.
    """
    # This is the timestamp we create this model in elcid
    created_in_elcid                = models.DateTimeField(auto_now_add=True)
    patient                         = models.ForeignKey(
                                        Patient,
                                        blank=True,
                                        null=True,
                                        on_delete=models.SET_NULL
                                    )

    update_datetime                 = models.DateTimeField(blank=True, null=True)
    # Boolean field as 0/1
    active_transfer                 = models.IntegerField(blank=True, null=True)
    # Boolean field as 0/1
    active_spell                    = models.IntegerField(blank=True, null=True)
    # What is this?
    encounter_id                    = models.IntegerField(blank=True, null=True)
    # What is this?
    encounter_slice_id              = models.BigIntegerField(blank=True, null=True)
    spell_number                    = models.CharField(blank=True, null=True, max_length=255)
    mrn                             = models.CharField(blank=True, null=True, max_length=255)
    transfer_sequence_number        = models.IntegerField(blank=True, null=True)
    transfer_start_datetime         = models.DateTimeField(blank=True, null=True)
    transfer_end_datetime           = models.DateTimeField(blank=True, null=True)
    # Numeric code for a location in the hospital
    transfer_location_code          = models.IntegerField(blank=True, null=True)
    # What are these?
    site_code                       = models.CharField(blank=True, null=True, max_length=255)
    # Ward
    unit                            = models.CharField(blank=True, null=True, max_length=255)
    room                            = models.CharField(blank=True, null=True, max_length=255)
    bed                             = models.CharField(blank=True, null=True, max_length=255)
    transfer_reason                 = models.CharField(blank=True, null=True, max_length=255)
    updated_datetime                = models.DateTimeField(blank=True, null=True)
    trans_updated                   = models.DateTimeField(blank=True, null=True)
    trans_created                   = models.DateTimeField(blank=True, null=True)
    spell_created                   = models.DateTimeField(blank=True, null=True)
    spell_updated                   = models.DateTimeField(blank=True, null=True)

    # What are these ?
    trf_inp_th_encntr_updt_dt_tm           = models.DateTimeField(blank=True, null=True)
    trf_inp_th_encntr_slice_updt_dt_tm     = models.DateTimeField(blank=True, null=True)
    trf_inp_th_encntr_alias_updt_dt_tm     = models.DateTimeField(blank=True, null=True)
    trf_inp_th_encntr_slice_act_updt_dt_tm = models.DateTimeField(blank=True, null=True)


    class Meta:
        ordering = ['transfer_sequence_number']

    # We ingore SOURCE because it does not contain useful data
    # We ignore In_Spells and In_TransHist because if either
    # of these is 0 we delete the row.
    UPSTREAM_FIELDS_TO_MODEL_FIELDS = {
        'UPDT_DT_TM'                            : 'update_datetime',
        'ACTIVE_TRANSFER'                       : 'active_transfer',
        'ACTIVE_SPELL'                          : 'active_spell',
        'ENCNTR_ID'                             : 'encounter_id',
        'ENCNTR_SLICE_ID'                       : 'encounter_slice_id',
        'SPELL_NUMBER'                          : 'spell_number',
        'LOCAL_PATIENT_IDENTIFIER'              : 'mrn',
        'TRANS_HIST_SEQ_NBR'                    : 'transfer_sequence_number',
        'TRANS_HIST_START_DT_TM'                : 'transfer_start_datetime',
        'TRANS_HIST_END_DT_TM'                  : 'transfer_end_datetime',
        'TRANS_HIST_LOCATION_DETAIL_CD'         : 'transfer_location_code',
        'SITE_CODE'                             : 'site_code',
        'UNIT'                                  : 'unit',
        'ROOM'                                  : 'room',
        'BED'                                   : 'bed',
        'TRANS_HIST_TRANSFER_REASON'            : 'transfer_reason',
        'UPDATED_DATE'                          : 'updated_datetime',
        'TRANS_UPDATED'                         : 'trans_updated',
        'TRANS_CREATED'                         : 'trans_created',
        'SPELL_CREATED'                         : 'spell_created',
        'SPELL_UPDATED'                         : 'spell_updated',
        'TRF_INP_TH_ENCNTR_UPDT_DT_TM'          : 'trf_inp_th_encntr_updt_dt_tm',
        'TRF_INP_TH_ENCNTR_SLICE_UPDT_DT_TM'    : 'trf_inp_th_encntr_slice_updt_dt_tm',
        'TRF_INP_TH_ENCNTR_ALIAS_UPDT_DT_TM'    : 'trf_inp_th_encntr_alias_updt_dt_tm',
        'TRF_INP_TH_ENCNTR_SLICE_ACT_UPDT_DT_TM': 'trf_inp_th_encntr_slice_act_updt_dt_tm',
    }

    def location(self):
        return " ".join([self.site_code, self.unit, self.room, self.bed])

class IsolatedBed(models.Model):
    """
    Beds marked by users as now in isolation.
    """
    hospital_site_code             = models.CharField(blank=True, null=True, max_length=255)
    ward_name                      = models.CharField(blank=True, null=True, max_length=255)
    room                           = models.CharField(blank=True, null=True, max_length=255)
    bed                            = models.CharField(blank=True, null=True, max_length=255)


class BedStatus(models.Model):
    """
    A snapshot of current bed status
    Obtained via the data warehousing team

    Here we replicate the upstream table closely
    """
    # We link the upstream data to our system via a single foreign key to the
    # Patient object. In practice we take the MRN fields and match them
    # with patient.demographics().hospital_number
    patient                        = models.ForeignKey(Patient, on_delete=models.CASCADE,
                                                       related_name='bedstatus',
                                                       blank=True, null=True)
    facility                       = models.CharField(blank=True, null=True, max_length=255)
    building                       = models.CharField(blank=True, null=True, max_length=255)
    hospital_site_code             = models.CharField(blank=True, null=True, max_length=255)
    hospital_site_description      = models.CharField(blank=True, null=True, max_length=255)
    ward_name                      = models.CharField(blank=True, null=True, max_length=255)
    room                           = models.CharField(blank=True, null=True, max_length=255)
    room_gender                    = models.CharField(blank=True, null=True, max_length=255)
    bed                            = models.CharField(blank=True, null=True, max_length=255)
    bed_status                     = models.CharField(blank=True, null=True, max_length=255)
    isolation_description          = models.CharField(blank=True, null=True, max_length=255)
    encounter_id                   = models.CharField(blank=True, null=True, max_length=255)
    encounter_type_description     = models.CharField(blank=True, null=True, max_length=255)
    person_id                      = models.CharField(blank=True, null=True, max_length=255)
    spell_number                   = models.CharField(blank=True, null=True, max_length=255)
    local_patient_identifier       = models.CharField(blank=True, null=True, max_length=255)
    nhs_number                     = models.CharField(blank=True, null=True, max_length=255)
    patient_name                   = models.CharField(blank=True, null=True, max_length=255)
    date_of_birth                  = models.CharField(blank=True, null=True, max_length=255)
    gender                         = models.CharField(blank=True, null=True, max_length=255)
    admission_date_time            = models.CharField(blank=True, null=True, max_length=255)
    admission_method_code          = models.CharField(blank=True, null=True, max_length=255)
    admission_method_description   = models.CharField(blank=True, null=True, max_length=255)
    patient_classification_code    = models.CharField(blank=True, null=True, max_length=255)
    main_specialty_code            = models.CharField(blank=True, null=True, max_length=255)
    main_specialty_description     = models.CharField(blank=True, null=True, max_length=255)
    treatment_function_code        = models.CharField(blank=True, null=True, max_length=255)
    treatment_function_description = models.CharField(blank=True, null=True, max_length=255)
    pod                            = models.CharField(blank=True, null=True, max_length=255)
    pod_description                = models.CharField(blank=True, null=True, max_length=255)
    division_patient               = models.CharField(blank=True, null=True, max_length=255)
    division_ward                  = models.CharField(blank=True, null=True, max_length=255)
    covid19_flag                   = models.CharField(blank=True, null=True, max_length=255)
    side_room_flag                 = models.CharField(blank=True, null=True, max_length=255)
    updated_date                   = models.DateTimeField(blank=True, null=True)
    source                         = models.CharField(blank=True, null=True, max_length=255)

    @property
    def isolated_bed(self):
        return IsolatedBed.objects.filter(
            hospital_site_code=self.hospital_site_code,
            ward_name=self.ward_name,
            room=self.room,
            bed=self.bed
        ).first()

    @property
    def is_side_room(self):
        return self.room.startwith('SR')

    def to_location_str(self):
            """
            A human readable location,

            returns f"{hospital_site_description} {ward_name} {room} {bed}"
            removing fields that are empty or None
            """
            result = []
            for field in [
                "hospital_site_description", "ward_name", "room", "bed"
            ]:
                field_str = getattr(self, field)
                if field_str is not None and len(field_str):
                    result.append(field_str)
            return " ".join(result)


    UPSTREAM_FIELDS_TO_MODEL_FIELDS = {
        'Facility'                      : 'facility',
        'Building'                      : 'building',
        'Hospital_Site_Code'            : 'hospital_site_code',
        'Hospital_Site_Description'     : 'hospital_site_description',
        'Ward_Name'                     : 'ward_name',
        'Room'                          : 'room',
        'Room_Gender'                   : 'room_gender',
        'Bed'                           : 'bed',
        'Bed_status'                    : 'bed_status',
        'Isolation_Description'         : 'isolation_description',
        'Encounter_ID'                  : 'encounter_id',
        'Encounter_Type_Description'    : 'encounter_type_description',
        'Person_ID'                     : 'person_id',
        'Spell_Number'                  : 'spell_number',
        'Local_Patient_Identifier'      : 'local_patient_identifier',
        'NHS_Number'                    : 'nhs_number',
        'Patient_Name'                  : 'patient_name',
        'Date_Of_Birth'                 : 'date_of_birth',
        'Gender'                        : 'gender',
        'Admission_Date_Time'           : 'admission_date_time',
        'Admission_Method_Code'         : 'admission_method_code',
        'Admission_Method_Description'  : 'admission_method_description',
        'Patient_Classification_Code'   : 'patient_classification_code',
        'Main_Specialty_Code'           : 'main_specialty_code',
        'Main_Specialty_Description'    : 'main_specialty_description',
        'Treatment_Function_Code'       : 'treatment_function_code',
        'Treatment_Function_Description': 'treatment_function_description',
        'POD'                           : 'pod',
        'POD_Description'               : 'pod_description',
        'Division_Patient'              : 'division_patient',
        'Division_Ward'                 : 'division_ward',
        'COVID19_Flag'                  : 'covid19_flag',
        'Side_Room_Flag'                : 'side_room_flag',
        'Updated_Date'                  : 'updated_date',
        'SOURCE'                        : 'source',
    }

    #
    # Although we maintain consistency with the upstream
    # data with minimal alterations, there is no real
    # utility in serializing much of this to the front end
    # on every patient/episode serialization.
    #
    FIELDS_TO_SERIALIZE = {
        'hospital_site_description': 'hospital',
        'ward_name'                : 'ward',
        'room'                     : 'room',
        'bed'                      : 'bed',
        'hospital_site_code'       : 'site_code', # Links sometimes use this
        'side_room_flag'           : 'side_room_flag' # tell the front room it's an extra sideroom
    }

    def to_dict(self):
        """
        Pluck out the fields relevant to serialization in the context of
        being a patient subrecord
        """
        result =  {v: getattr(self, k) for k, v in self.FIELDS_TO_SERIALIZE.items()}

        if 'hospital' in result and result['hospital']: # null entries introduced upstream Nov '24
            if result['hospital'].endswith(' HOSPITAL'):
                result['hospital'] = result['hospital'][:-9]

        if self.admission_date_time:
            try:
                result['admission_date_time'] = datetime.datetime.strptime(
                    self.admission_date_time, '%Y-%m-%d %H:%M:%S'
                )
            except ValueError:
                result['admission_date_time'] = None
        return result

    def to_location_str(self):
        """
        A human readable location
        """
        return ' '.join([
            self.hospital_site_description, self.ward_name,
            self.room, self.bed
        ])

    def get_admitted_as_dt(self):
        """
        We store admission_date_time as a char - this breaks Angular display.
        Return either None or a datetime
        """
        if not self.admission_date_time:
            return self.admission_date_time

        return datetime.datetime.strptime(
            self.admission_date_time, "%Y-%m-%d %H:%M:%S")
