from dataclasses import dataclass, field
import seronetFunctions as seroFxn
# import seronetDataclass_v2 as seroClass
import datetime as dt
import numpy as np
import pandas as pd
import os
import path
import re
import logging
import sys


VARS_TO_CLEAN = ['', 'N/A', 'n/a', np.nan, None]

STATES = pd.read_csv(os.path.join("dictionary", "States.csv"),
                     header=None,
                     index_col=0,
                     squeeze=True).to_dict()


CD = os.getcwd()

if not os.path.exists(os.path.join(CD, "log")):
    os.mkdir(os.path.join(CD, "log"))

today = dt.datetime.today().strftime('%Y_%m_%d')
logging.basicConfig(filename=os.path.join(CD, "log", f"Registry_{today}.log"), level=logging.DEBUG,
                    format='%(asctime)s %(message)s', filemode='w', datefmt='%m/%d/%Y %I:%M:%S %p')


###
@dataclass
class study:
    """1 Column to the right"""
    Study_Identifier: str = None
    Study_Name: str = None
    Publication_Title: str = None
    Study_Objective: str = None
    Study_Description: str = None
    Primary_Institution_Name: str = None
    NAME: str = 'study'


@dataclass
class study_personnel:
    """1 row below, 11 Columns"""
    User_Defined_ID: list = None
    Honorific: list = None
    Last_Name: list = None
    First_Name: list = None
    Suffixes: list = None
    Organization: list = None
    ORCID_ID: list = None
    Email: list = field(default_factory=list)
    Title_In_Study: list = field(default_factory=list)
    Role_In_Study: list = field(default_factory=list)
    Site_Name: list = field(default_factory=list)
    ImmPortNAME: str = 'study_personnel'


@dataclass
class study_file:
    File_Name: list = field(default_factory=list)
    Description: list = field(default_factory=list)
    Study_File_Type: list = field(default_factory=list)
    ImmPortNAME: str = 'study_file'


@dataclass
class study_link:
    Name: list = field(default_factory=list)
    Value: list = field(default_factory=list)
    ImmPortNAME: str = 'study_link'


@dataclass
class study_categorization:
    """1 Column to the right"""
    Research_Focus: str = None
    Study_Type: str = None
    Keywords: list = None
    ImmPortNAME: str = 'study_categorization'


@dataclass
class study_design:
    """1 Column to the right"""
    Clinical_Study_Design: str = None
    in_silico_Model_Type: str = None
    ImmPortNAME: str = 'NA'


@dataclass
class protocols:
    Protocol_ID: str
    Protocol_File_Name: str
    Protocol_Name: str
    Protocol_Description: str = None
    Protocol_Type: str = None
    ImmPortNAME: str = 'study_2_protocol'


@dataclass
class condition_or_disease:
    """1 Column to the right"""
    Reported_Health_Condition: str = None
    ImmPortNAME: str = 'study_2_condition_or_disease'


@dataclass
class Intervention_Agent:
    SARS_CoV_2_Vaccine_Type: list = None
    ImmPortNAME: str = 'NA'


@dataclass
class study_details:
    Clinical_Outcome_Measure: str = None
    Enrollment_Start_Date: str = None  # dd-MMM-yy
    Enrollment_End_Date: str = None  # dd-MMM-yy
    Number_of_Study_Subjects: str = None
    Age_Unit: str = 'Years'
    Minimum_Age: int = None
    Maximum_Age: int = None
    ImmPortNAME: str = 'study'


@dataclass
class inclusion_exclusion:
    """1 row below, 3 Columns"""
    User_Defined_ID: list = None
    Criterion: list = field(default_factory=list)
    Criterion_Category: list = field(default_factory=list)
    ImmPortNAME: str = 'inclusion_exclusion'

# confused on why this doesnt work
@dataclass
class study_pubmed:
    Pubmed_ID: str = None
    DOI: int = None
    Title: str = None
    Journal: str = None
    Year: int = None
    Month: str = None
    Issue: str = None
    Pages: str = None
    Authors: str = None

    ImmPortNAME: str = 'study_pubmed'

@dataclass
class arm_or_cohort:
    User_Defined_ID: list = field(default_factory=list),
    Name: list = field(default_factory=list),
    Description: list = field(default_factory=list),
    Type_Reported: list = field(default_factory=list),
    ImmPortNAME: str = 'arm_or_cohort'


@dataclass
class subject_type_human:
    User_Defined_ID: list = field(default_factory=list) # might need to change
    Name: list = None  # arm
    Description: list = None  # arm
    Type_Reported: list = None  # arm type
    Ethnicity: list = field(default_factory=list)
    Race: list = field(default_factory=list)
    Race_Specify: list = field(default_factory=list)
    Subject_Description: list = field(default_factory=list)
    Sex_at_Birth: list = field(default_factory=list)
    Age_Event: list = field(default_factory=list)
    Subject_Phenotype: list = field(default_factory=list)
    Study_Location: list = field(default_factory=list)  # Add something to make north west or check?
    Assessment_Name: list = field(default_factory=list)
    Measured_Behavioral_or_Psychological_Factor: list = field(default_factory=list)
    Measured_Social_Factor: list = field(default_factory=list)
    SARS_CoV_2_Symptoms: list = field(default_factory=list)
    Assessment_Clinical_and_Demographic_Data_Provenance: list = field(default_factory=list)
    Assessment_Demographic_Data_Types_Collected: list = field(default_factory=list)
    SARS_CoV2_History: list = field(default_factory=list)
    SARS_CoV_2_Vaccine_Type: list = field(default_factory=list)
    COVID_19_Disease_Severity: list = field(default_factory=list)
    Post_COVID_19_Symptoms: list = field(default_factory=list)
    COVID_19_Complications: list = field(default_factory=list)
    ImmPortNAME: str = 'n/a'


@dataclass
class subject_type_mode_organism:
    User_Defined_ID: list = field(default_factory=list)  # might need to change
    Name: list = None
    Description: list = None
    Type_Reported: list = None
    Species: list = field(default_factory=list)
    Biosample_Types: list = field(default_factory=list)
    Strain_Characteristics: list = field(default_factory=list)
    Sex_at_Birth: list = field(default_factory=list)
    Age_Event: list = field(default_factory=list)
    Subject_Phenotype: list = field(default_factory=list)
    Study_Location: list = field(default_factory=list)
    # SARS_CoV_2_Symptoms: list = field(default_factory=list)
    SARS_CoV2_History: list = field(default_factory=list)
    SARS_CoV_2_Vaccine_Type: list = field(default_factory=list)
    COVID_19_Disease_Severity: list = field(default_factory=list)
    Post_COVID_19_Symptoms: list = field(default_factory=list)
    COVID_19_Complications: list = field(default_factory=list)
    ImmPortNAME: str = 'n/a'


@dataclass
class planned_visit:
    """1 row below, 7 Columns"""
    User_Defined_ID: list = field(default_factory=list)
    Name: list = field(default_factory=list)
    Order_Number: list = field(default_factory=list)
    Min_Start_Day: list = field(default_factory=list)
    Max_Start_Day: list = None
    Start_Rule: list = None
    ImmPortNAME: str = 'planned_visit'


@dataclass
class study_experiment_samples:
    Expt_Sample_User_Defined_ID: list = field(default_factory=list)
    Expt_Sample_Biospecimen_Type: list = field(default_factory=list)
    Expt_Sample_Biospecimen_Collection_Point: list = field(default_factory=list)


@dataclass
class study_experiment:
    Experiment_ID: str = None
    Experiment_Name: list = field(default_factory=list)
    Experiment_Assay_Type: list = field(default_factory=list)
    Experiment_Results_File_Name: str = None

@dataclass
class reagent_per_experiment:
    Reagent_ID: list = field(default_factory=list)
    SARS_CoV_2_Antigen: list = field(default_factory=list)
    Assay_Use: list = field(default_factory=list)
    Manufacturer: list = field(default_factory=list)
    Catalog: list = field(default_factory=list)



@dataclass
class results:
    Results_Virus_Target: list = field(default_factory=list)
    Results_Antibody_Isotype: list = field(default_factory=list)
    Results_Reporting_Units: list = field(default_factory=list)
    Results_Reporting_Format: list = field(default_factory=list)
