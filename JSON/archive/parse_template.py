import pandas as pd
import json
import re
from datetime import datetime

#
# Line Number Locations in Excel File
#
STUDY_PUBMED = 13
STUDY_IDENTIFIER = 16
STUDY_NAME = 17
PUBLICATION_TITLE = 18
STUDY_OBJECTIVE = 19
STUDY_DESCRIPTION = 20
PRIMARY_INSTITUTION_NAME = 21
STUDY_PERSONNEL = 25
STUDY_FILE = 39
STUDY_LINK = 45
STUDY_CATEGORIZATION = 49
RESEARCH_FOCUS = 50
STUDY_TYPE = 51
KEYWORDS = 52
STUDY_DESIGN = 55
CLINICAL_STUDY_DESIGN = 56
IN_SILICO_MODEL_TYPE = 57
PROTOCOLS = 60
PROTOCOL_ID = 61
PROTOCOL_FILE_NAME = 62
PROTOCOL_NAME = 63
PROTOCOL_DESCRIPTION = 64
PROTOCOL_TYPE = 65
CONDITION_OR_DISEASE = 68
REPORTED_HEALTH_CONDITION = 69
INTERVENTION_AGENT = 72
SARS_COV_2_VACCINE_TYPE = 73
STUDY_DETAILS = 76
CLINICAL_OUTCOME_MEASURE = 77
ENROLLMENT_START_DATE = 78
ENROLLMENT_END_DATE = 79
NUMBER_OF_STUDY_SUBJECTS = 80
AGE_UNIT = 81
MINIMUM_AGE = 82
MAXIMUM_AGE = 83

INCLUSION_EXCLUSION = 86
INCLUSION_ID = 87
INCLUSION_CRITERION = 88
INCLUSION_CRITERION_CATEGORY = 89

HUMAN_ARM_ID = 93
HUMAN_ARM_NAME = 94
HUMAN_STUDY_POPULATION_DESCRIPTION = 95
HUMAN_ARM_TYPE = 96
HUMAN_ETHNICITY = 97
HUMAN_RACE = 98
HUMAN_RACE_SPECIFY = 99
HUMAN_DESCRIPTION = 100
HUMAN_SEX_AT_BIRTH = 101
HUMAN_AGE_EVENT = 102
HUMAN_SUBJECT_PHENOTYPE = 103
HUMAN_STUDY_LOCATION = 104
HUMAN_ASSESSMENT_NAME = 105
HUMAN_MEASURED_BEHAVIORAL_OR_PYSCHOLOGICAL_FACTOR = 106
HUMAN_MEASURED_SOCIAL_FACTOR = 107
HUMAN_SARS_COV_2_SYMPTOMS = 108
HUMAN_ASSESSMENT_CLINICAL_AND_DEMOGRAPHIC_DATA_PROVENANCE = 109
HUMAN_ASSESSMENT_DEMOGRAPHIC_DATA_TYPES_COLLECTED = 110
HUMAN_SARS_COV_2_HISTORY = 111
HUMAN_SARS_COV_2_VACCINE_TYPE = 112
HUMAN_COVID_19_DISEASE_SEVERITY = 113
HUMAN_POST_COVID_19_SYMPTOMS = 114
HUMAN_COVID_19_COMPLICATIONS = 115

MODEL_ARM_ID = 119
MODEL_ARM_NAME = 120
MODEL_STUDY_POPULATION_DESCRIPTION = 121
MODEL_ARM_TYPE = 122
MODEL_SPECIES = 123
MODEL_BIOSAMPLE_TYPE = 124
MODEL_STRAIN_CHARACTERISTICS = 125
MODEL_SEX_AT_BIRTH = 126
MODEL_AGE_EVENT = 127
MODEL_SUBJECT_PHENOTYPE = 128
MODEL_STUDY_LOCATION = 129
MODEL_SARS_COV_2_HISTORY = 130
MODEL_SARS_COV_2_VACCINE_TYPE = 131
MODEL_COVID_19_DISEASE_SEVERITY = 132
MODEL_POST_COVID_19_SYMPTOMS = 133
MODEL_COVID_19_COMPLICATIONS = 134

PLANNED_VISIT = 137
VISIT_ID = 138
VISIT_NAME = 139
VISIT_ORDER_NUMBER = 140
VISIT_MIN_START_DAY = 141
VISIT_MAX_START_DAY = 142
VISIT_START_RULE = 143

EXPERIMENTS = 147
ASSOCIATED_ARM_IDS = 148
ASSOCIATED_FIRST_PLANNED_VISIT_ID = 149
ASSAY_TYPE = 150
EXPERIMENT_NAME = 151
EXPERIMENT_RESULTS_FILE_NAME = 152
BIOSPECIMEN_TYPE = 153
BIOSPECIMEN_COLLECTION_POINT = 154
SARS_COV_2_ANTIGEN = 155
ASSAY_USE = 156
MANUFACTURER = 157
CATALOG_NUMBER = 158
VIRUS_TARGET = 159
ANTIBODY_ISOTYPE = 160
REPORTING_UNITS = 161
ASSAY_REPORTING_FORMAT = 162

#
# Remove characters or escape characters that corrupt JSON
#
def cleanData(s):
    #print(str, type(s))
    if pd.isna(s):
        return ""
    else:
        if isinstance(s, str):
            r1 = re.compile("\n|\t|\r")
            r2 = re.compile('"')
            s = r1.sub(" ", s)
            s = r2.sub('\\"', s)
            s = s.strip()
        elif isinstance(s, datetime):
            s = s.strftime('%Y-%m-%d')
        else:
            pass
        return s

def parse_sv(df, line_number, index):
    return list(df.loc[line_number])[index]

def parse_clean_sv(df, line_number, index):
    return cleanData(list(df.loc[line_number])[index])

def parse_clean_mv_split(df, line_number, index):
    if pd.isna(df.loc[line_number][index]):
        return []
    else:
        return [cleanData(item) for item in re.split(" \| ", df.loc[line_number][index])]

def parse_clean_mv_split_I(df, line_number, index):
    return [cleanData(item) for item in re.split(" I ", df.loc[line_number][index])]

def parse_registry_template(df, template):
    parse_pubmed(df, template)
    parse_study(df, template)
    parse_study_personnel(df, template)
    parse_study_file(df, template)
    parse_study_link(df, template)
    parse_study_categorization(df, template)
    parse_study_design(df, template)
    parse_protocol(df, template)
    parse_condition_or_disease(df, template)
    parse_intervention(df, template)
    parse_study_details(df, template)
    parse_subject_human(df, template)
    parse_model_organism(df, template)
    parse_planned_visit(df, template)
    parse_experiment(df, template)
    parse_inclusion_exclusion(df, template)

def parse_pubmed(df, template):
    template['pubmed_id'] = parse_sv(df, STUDY_PUBMED, 2)

def parse_study(df, template):
    template['study_identifier'] = parse_clean_sv(df, STUDY_IDENTIFIER, 2)
    template['study_name'] = parse_clean_sv(df, STUDY_NAME, 2)
    template['publication_title'] = parse_clean_sv(df, PUBLICATION_TITLE, 2)
    template['study_objective'] = parse_clean_sv(df, STUDY_OBJECTIVE, 2)
    template['study_description'] = parse_clean_sv(df, STUDY_DESCRIPTION, 2)
    template['primary_institution_name'] = parse_clean_sv(df, PRIMARY_INSTITUTION_NAME, 2)

def parse_study_personnel(df, template):
    studyPersonnel = []
    personnel = list(df.loc[STUDY_PERSONNEL])
    for idx, val in enumerate(personnel[2:], start=2):
        if not pd.isna(val):
            obj = {
                "personnel_id": val,
                "honorific": parse_clean_sv(df, STUDY_PERSONNEL + 1, idx),
                "last_name": parse_clean_sv(df, STUDY_PERSONNEL + 2, idx),
                "first_name": parse_clean_sv(df, STUDY_PERSONNEL + 3, idx),
                "suffixes": parse_clean_sv(df, STUDY_PERSONNEL + 4, idx),
                "organization": parse_clean_sv(df, STUDY_PERSONNEL + 5, idx),
                "orchid_id": parse_clean_sv(df, STUDY_PERSONNEL + 6, idx),
                "email": parse_clean_sv(df, STUDY_PERSONNEL + 7, idx),
                "seronet_title_in_study":  parse_clean_sv(df, STUDY_PERSONNEL + 8, idx),
                "role_in_study": parse_clean_sv(df, STUDY_PERSONNEL + 9, idx),
                "site_name": parse_clean_sv(df, STUDY_PERSONNEL + 10, idx)
            }
            studyPersonnel.append(obj)
        else:
            pass
    
    template['study_personnel'] = studyPersonnel

def parse_study_file(df, template):
    studyFile = []
    study_files = list(df.loc[STUDY_FILE])
    for idx, val in enumerate(study_files[2:], start=2): 
        if not pd.isna(val):
            obj = {
               "study_file_name": val,
               "study_file_description": parse_clean_sv(df, STUDY_FILE + 1, idx),
               "study_file_type": parse_clean_sv(df, STUDY_FILE + 2, idx)
            }
            studyFile.append(obj)
        else:
            pass
    template['study_file'] = studyFile
    
def parse_study_link(df, template):
    studyLink = []
    study_links = list(df.loc[STUDY_LINK])
    for idx, val in enumerate(study_links[2:], start=2): 
        if not pd.isna(val):
            obj = {
               "link_name": val,
               "value": parse_clean_sv(df, STUDY_LINK +1, idx)
            }
            studyLink.append(obj)
        else:
            pass
    template['study_link'] = studyLink

def parse_study_categorization(df, template):
    #
    # Research Focus
    #
    template['research_focus'] = parse_clean_sv(df, RESEARCH_FOCUS, 2)


    #
    # Study Type
    #
    template['study_type'] = parse_clean_sv(df, STUDY_TYPE, 2)

    #
    # Keywords 
    #
    keyword = []
    keywords = (list(df.loc[KEYWORDS])[2]).split(",")
    for k in keywords:
        keyword.append(k.strip())
    template['keyword'] = keyword

def parse_study_design(df, template):
    template['clinical_study_design'] = parse_clean_sv(df, CLINICAL_STUDY_DESIGN, 2)
    template['in_silico_model_type'] = parse_clean_sv(df, IN_SILICO_MODEL_TYPE, 2)

def parse_protocol(df, template):
    # Protocol 
    protocol = {}
    protocol['protocol_id'] = parse_clean_sv(df, PROTOCOL_ID, 2)
    protocol['protocol_file_name'] = parse_clean_sv(df, PROTOCOL_FILE_NAME, 2)
    protocol['protocol_name'] = parse_clean_sv(df, PROTOCOL_NAME, 2)
    protocol['protocol_description'] = parse_clean_sv(df, PROTOCOL_DESCRIPTION, 2)
    protocol['protocol_type'] = parse_clean_sv(df, PROTOCOL_TYPE, 2)
    
    template['protocol'] = protocol

def parse_condition_or_disease(df, template):
    values = re.split(" I ", list(df.loc[REPORTED_HEALTH_CONDITION])[2])
    reported_health_condition = []
    for c in values:
        reported_health_condition.append(cleanData(c))
    template['reported_health_condition'] = reported_health_condition

def parse_intervention(df, template):
    values = parse_clean_mv_split(df, SARS_COV_2_VACCINE_TYPE, 2)
    vaccine_types = []
    for v in values:
        vaccine_types.append(cleanData(v))
    template['sars_cov_2_vaccine_type'] = vaccine_types

def parse_study_details(df, template):
    template['clinical_outcome_measure'] = parse_clean_sv(df, CLINICAL_OUTCOME_MEASURE, 2)
    template['enrollment_start_date'] = parse_clean_sv(df, ENROLLMENT_START_DATE, 2)
    template['enrollment_end_date'] = parse_clean_sv(df, ENROLLMENT_END_DATE, 2)
    template['number_of_study_subjects'] = parse_clean_sv(df, NUMBER_OF_STUDY_SUBJECTS, 2)
    template['age_unit'] = parse_clean_sv(df, AGE_UNIT, 2)
    template['minimum_age'] = parse_clean_sv(df, MINIMUM_AGE, 2)
    template['maximum_age'] = parse_clean_sv(df, MAXIMUM_AGE, 2)

def parse_inclusion_exclusion(df, template):
    inclusion_exclusion = []
    ids = list(df.loc[INCLUSION_ID])

    for idx, val in enumerate(ids[2:], start=2):
        if not pd.isna(val):
            obj = {
               "inclusion_exculusion_id": val,
               "inclusion_criterion": parse_clean_sv(df, INCLUSION_CRITERION, idx),
               "inclusion_criterion_category": parse_clean_sv(df, INCLUSION_CRITERION_CATEGORY, idx)
            }
            inclusion_exclusion.append(obj)
            
            if ( obj['inclusion_criterion'] == "Geriatric Subjects"
                 and obj['inclusion_criterion_category'] == "inclusion") :
                 template['geriatric_subjects'] = "Y"
            else: 
                 template['geriatric_subjects'] = "N"
                
            if ( obj['inclusion_criterion'] == "Pediatric Subjects"
                 and obj['inclusion_criterion_category'] == "inclusion") :
                 template['pediatric_subjects'] = "Y"
            else: 
                 template['pediartric_subjects'] = "N"

            if ( obj['inclusion_criterion'] == "Pregnant subjects"
                 and obj['inclusion_criterion_category'] == "inclusion") :
                 template['pregnant_subjects'] = "Y"
            else: 
                 template['pregnant_subjects'] = "N"

            if ( obj['inclusion_criterion'] == "SARS-CoV-2 Antibodies Measured"
                 and obj['inclusion_criterion_category'] == "inclusion") :
                 template['SARS_CoV2_antibodies_measured'] = "Y"
            else: 
                 template['SARS_CoV2_antibodies_measured'] = "N"


                
        else:
            pass
    
    template['inclusion_exclusion'] = inclusion_exclusion

def parse_subject_human(df, template):
    human_cohort = []
    chorts = list(df.loc[HUMAN_ARM_ID])
    for idx, val in enumerate(chorts[2:], start=2): 
        if not pd.isna(val):
            obj = {
               "arm_id": val,
               "arm_name": parse_clean_sv(df, HUMAN_ARM_NAME, idx),
               "study_population_description": parse_clean_sv(df, HUMAN_STUDY_POPULATION_DESCRIPTION, idx),
               "arm_type": parse_clean_sv(df, HUMAN_ARM_TYPE, idx),
               "ethnicity": parse_clean_mv_split(df, HUMAN_ETHNICITY, idx),
               "race": parse_clean_mv_split(df, HUMAN_RACE, idx),
               "race_specify": parse_clean_mv_split(df, HUMAN_RACE_SPECIFY, idx),
               "description": parse_clean_sv(df, HUMAN_DESCRIPTION, idx),
               "sex_at_birth": parse_clean_mv_split(df, HUMAN_SEX_AT_BIRTH, idx),
               "age_event": parse_clean_sv(df, HUMAN_AGE_EVENT, idx),
               "subject_phenotype": parse_clean_mv_split(df, HUMAN_SUBJECT_PHENOTYPE,idx),
               "assessment_name": parse_clean_sv(df, HUMAN_ASSESSMENT_NAME, idx),
               "study_location": parse_clean_mv_split(df, HUMAN_STUDY_LOCATION, idx),
               "measured_behavioral_or_pyschological_factor": parse_clean_mv_split(df, HUMAN_MEASURED_BEHAVIORAL_OR_PYSCHOLOGICAL_FACTOR, idx),
               "measured_social_factor": parse_clean_mv_split(df, HUMAN_MEASURED_SOCIAL_FACTOR, idx),
               "sars_cov_2_symptoms": parse_clean_mv_split(df, HUMAN_SARS_COV_2_SYMPTOMS, idx),
               "assessment_clinical_and_demographic_data_provenance": parse_clean_mv_split(df, HUMAN_ASSESSMENT_CLINICAL_AND_DEMOGRAPHIC_DATA_PROVENANCE, idx),
               "assessment_demographic_data_types_collected": parse_clean_mv_split(df, HUMAN_ASSESSMENT_DEMOGRAPHIC_DATA_TYPES_COLLECTED, idx),
               "sars_cov_2_history": parse_clean_mv_split(df, HUMAN_SARS_COV_2_HISTORY, idx),
               "sars_cov_2_vaccine_type": parse_clean_mv_split(df, HUMAN_SARS_COV_2_VACCINE_TYPE, idx),
               "covid_19_disease_severity": parse_clean_mv_split(df, HUMAN_COVID_19_DISEASE_SEVERITY, idx),
               "post_covid_19_symptoms": parse_clean_mv_split(df, HUMAN_POST_COVID_19_SYMPTOMS, idx),
               "covid_19_complications": parse_clean_mv_split(df, HUMAN_COVID_19_COMPLICATIONS, idx)
            }
            human_cohort.append(obj)
        else:
            pass
    
    template['study_human_cohort'] = human_cohort

def parse_model_organism(df, template):
    model_cohort = []
    chorts = list(df.loc[MODEL_ARM_ID])
    for idx, val in enumerate(chorts[2:], start=2): 
        if not pd.isna(val):
            obj = {
               "arm_id": val,
               "arm_name": parse_clean_sv(df, MODEL_ARM_NAME, idx),
               "study_population_description": parse_clean_sv(df, MODEL_STUDY_POPULATION_DESCRIPTION, idx),
               "arm_type": parse_clean_sv(df, MODEL_ARM_TYPE, idx),
               "species": parse_clean_mv_split(df, MODEL_SPECIES, idx),
               "biosample_type": parse_clean_mv_split(df, MODEL_BIOSAMPLE_TYPE, idx),
               "strain_characteristics": parse_clean_mv_split(df, MODEL_STRAIN_CHARACTERISTICS, idx),
               "sex_at_birth": parse_clean_mv_split(df, MODEL_SEX_AT_BIRTH, idx),
               "age_event": parse_clean_sv(df, MODEL_AGE_EVENT, idx),
               "subject_phenotype": parse_clean_sv(df, MODEL_SUBJECT_PHENOTYPE, idx),
               "study_location": parse_clean_mv_split(df, MODEL_STUDY_LOCATION, idx),
               "sars_cov_2_history": parse_clean_mv_split(df, MODEL_SARS_COV_2_HISTORY, idx),
               "sars_cov_2_vaccine_type": parse_clean_mv_split(df, MODEL_SARS_COV_2_VACCINE_TYPE, idx),
               "covid_19_disease_severity": parse_clean_mv_split(df, MODEL_COVID_19_DISEASE_SEVERITY, idx),
               "post_covid_19_symptons": parse_clean_mv_split(df, MODEL_POST_COVID_19_SYMPTOMS, idx),
               "covid_19_complications": parse_clean_mv_split(df, MODEL_COVID_19_COMPLICATIONS, idx)
            }
            model_cohort.append(obj)
        else:
            pass
    

    template['study_model_cohort'] = model_cohort

def parse_planned_visit(df, template):
    plannedVisit = []
    visits = list(df.loc[VISIT_ID])
    for idx, val in enumerate(visits[2:], start=2):  
        if not pd.isna(val):
            obj = {
               "visit_id": val,
               "visit_name": parse_clean_sv(df, VISIT_NAME, idx),
               "visit_order_number": parse_sv(df, VISIT_ORDER_NUMBER, idx),
               "visit_min_start_day": parse_clean_sv(df, VISIT_MIN_START_DAY, idx),
               "visit_max_start_day": parse_clean_sv(df, VISIT_MAX_START_DAY, idx),
               "visit_start_rule": parse_clean_sv(df, VISIT_START_RULE, idx)
            }
            plannedVisit.append(obj)
        else:
            pass
    template['planned_visit'] = plannedVisit

def parse_experiment(df, template):
    experiment = []
    experiments = list(df.loc[ASSOCIATED_ARM_IDS])
    for idx, val in enumerate(experiments[2:], start=2): 
        if not pd.isna(val):
            obj = {
               "arm_id": [cleanData(item) for item in re.split(" I ",val)],
               "associated_first_planned_visit_id": [cleanData(item) for item in re.split(" I ", df.loc[ASSOCIATED_FIRST_PLANNED_VISIT_ID][idx])],
               "assay_type": parse_clean_mv_split(df, ASSAY_TYPE, idx),
               "experiment_name": parse_clean_mv_split(df, EXPERIMENT_NAME, idx),
               "experiment_results_file_name": parse_clean_mv_split(df, EXPERIMENT_RESULTS_FILE_NAME, idx),
               "biospecimen_type": parse_clean_mv_split(df, BIOSPECIMEN_TYPE, idx),
               "sars_cov_2_antigen": parse_clean_mv_split(df, SARS_COV_2_ANTIGEN, idx),
               "assay_use": parse_clean_mv_split(df, ASSAY_USE, idx),
               "manufacture": parse_clean_mv_split(df, MANUFACTURER, idx),
               "catalog_number": parse_clean_mv_split(df, CATALOG_NUMBER, idx),
               "virus_target": parse_clean_mv_split(df, VIRUS_TARGET, idx),
               "antibody_isotype": parse_clean_mv_split(df, ANTIBODY_ISOTYPE, idx),
               "reporting_units": parse_clean_mv_split(df, REPORTING_UNITS, idx),
               "assay_reporting_format": parse_clean_mv_split(df, ASSAY_REPORTING_FORMAT, idx)
            }
            experiment.append(obj)
        else:
            pass
                                                                                 
    template['experiment'] = experiment

