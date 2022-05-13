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

    def __post_init__(self):
        self.Study_Identifier = self.Study_Identifier.replace('\n', '').replace('\t', '')
        self.Study_Name = self.Study_Name.replace('\n', '').replace('\t', '')
        self.Publication_Title = self.Publication_Title.replace('\n', '').replace('\t', '')
        self.Study_Objective = self.Study_Objective.replace('\n', '').replace('\t', '')
        self.Study_Description = self.Study_Description.replace('\n', '').replace('\t', '')


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

    def __post_init__(self):
        if len(self.Role_In_Study) != len(self.User_Defined_ID) != len(self.Last_Name) != len(self.First_Name) != len(
                self.Organization) != len(self.Email) != len(self.Title_In_Study):
            logging.error("[study personnel]: Lengths of personnel is wrong")
            sys.exit("ERROR:: [study personnel]: Check Study Personnel")

        if len(set(self.User_Defined_ID)) != len(self.User_Defined_ID):
            logging.error("[study personnel]: Same Personnel ID used")
            sys.exit("ERROR:: [study personnel]: Check Study ID used")


@dataclass
class study_file:
    File_Name: list = field(default_factory=list)
    Description: list = field(default_factory=list)
    Study_File_Type: list = field(default_factory=list)
    ImmPortNAME: str = 'study_file'

    # def __bool__(self):
    #     print(len(list(self.Study_File_Type)) == len(list(set(self.Study_File_Type))))

    def __post_init__(self):
        for i, k in enumerate(self.Description):
            object.__setattr__(self, 'Description',
                               [k.replace('\n', '').replace('\t', '') for i, k in enumerate(self.Description)])
            # self.Description[i] = k.replace('\n','').replace('\t','')

        if len(list(self.File_Name)) != len(list(set(self.File_Name))):
            logging.warning("[file names]: Redudant names: file names")
            sys.exit("ERROR:: [file names]: Check file names")

        if len(self.File_Name) != len(self.Study_File_Type):
            logging.warning("[file names]: Missing value")
            sys.exit("ERROR:: [file names]: Check for missing values")


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

    def __post_init__(self):
        if self.Keywords:
            self.Keywords = self.Keywords.replace('\n', '').replace('\t', '').replace(';', ',').replace('|', ',')
        else:
            logging.error("ERROR:: [study_categorization]: Keywords missing")
            sys.exit("ERROR:: [study_categorization]: Keywords missing")


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

    def __post_init__(self):
        for i, k in enumerate(self.Reported_Health_Condition):
            object.__setattr__(self, 'Reported_Health_Condition', [k.replace('\n', '').replace('\t', '') for i, k in
                                                                   enumerate(self.Reported_Health_Condition)])
            # self.Reported_Health_Condition[i] = k.replace('|',',').replace(':',',')


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




    def __post_init__(self):
        def get_correct_datetime(date_to_check):
            if isinstance(date_to_check, str):
                return dt.datetime.strptime(date_to_check, '%m/%d/%y %H:%M').strftime('%d/%B/%y')
            else:
                return date_to_check.strftime('%d-%b-%Y')


        if self.Maximum_Age is None:
            object.__setattr__(self, 'Maximum_Age', 89)

        if self.Minimum_Age is None:
            object.__setattr__(self, 'Minimum_Age', 0)

        # Checking the Datetime Format
        if self.Enrollment_End_Date in VARS_TO_CLEAN:
            object.__setattr__(self, 'Enrollment_End_Date', '')
        else:
            object.__setattr__(self, "Enrollment_End_Date", get_correct_datetime(self.Enrollment_End_Date))

        if self.Enrollment_Start_Date in VARS_TO_CLEAN:
            object.__setattr__(self, 'Enrollment_Start_Date', '')
        else:
            object.__setattr__(self, "Enrollment_Start_Date", get_correct_datetime(self.Enrollment_Start_Date))
@dataclass
class inclusion_exclusion:
    """1 row below, 3 Columns"""
    User_Defined_ID: list = None
    Criterion: list = field(default_factory=list)
    Criterion_Category: list = field(default_factory=list)
    ImmPortNAME: str = 'inclusion_exclusion'

    def __post_init__(self):
        if len(self.User_Defined_ID) == 1: #change n/a to other / inclusion  
            if (self.Criterion[1] in VARS_TO_CLEAN):
                object.__setattr__(self, "Criterion", "Other") 
                object.__setattr__(self, "Criterion_Category", "Inclusion")


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

    def __any__(self):
        return bool(self.Pubmed_ID)


@dataclass
class arm_or_cohort:
    User_Defined_ID: list = field(default_factory=list),
    Name: list = field(default_factory=list),
    Description: list = field(default_factory=list),
    Type_Reported: list = field(default_factory=list),
    ImmPortNAME: str = 'arm_or_cohort'

    def __post_init__(self):
        if len(self.Type_Reported) < len(self.User_Defined_ID):
            logging.error("[arm_or_cohort]: Arm type missing")
            sys.exit("ERROR:: [arm_or_cohort]: Arm type missing")

        for i, k in enumerate(self.Description):
            object.__setattr__(self, 'Description',
                               [k.replace('\n', '').replace('\t', '') for i, k in enumerate(self.Description)])
            # self.Description[i] = k.replace('\n','').replace('\t','')

        # temp = self.User_Defined_ID[0][:-1]
        # object.__setattr__(self, "User_Defined_ID", [temp+str(i+1) for i in range(len(self.User_Defined_ID))])


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

    def __bool__(self):
        if len(set(self.User_Defined_ID).intersection([None])) == 1:
            return False
        # return True
        return bool(len(self.User_Defined_ID))

    def __post_init__(self):
        if len(self.User_Defined_ID):
            # Checking to make sure everying is the same length (taking into acount that None are Empty Spaces)
            # IMMPORT_REQUIRED = ['User_Defined_ID', 'Name','Description','Type_Reported','Species','Biosample_Types',
            # 'Sex_at_Birth', 'Age_Event', 'Study_Location']

            largest_val = 0
            for field in self.__dataclass_fields__:
                if field != "ImmPortNAME":
    #                 field = [x for x in getattr(self, field) if x not in VARS_TO_CLEAN]
                    field = seroFxn.clean_array(getattr(self,field), [None])
                    
                    if len(field) != 0:
                        value = len(field)
                        if value > largest_val:
                            largest_val = value

            for field in self.__dataclass_fields__:
                # if isinstance(getattr(self,field), list): #THIS
                    
                cell = seroFxn.clean_array(getattr(self,field), [None])
                if len(cell) > 0 and field != "ImmPortNAME":
                    if len(cell) != largest_val:
        #                 logging.error("[planned visit]: check Order Numer")
                        sys.exit(f"ERROR:: Error [Subject Human]: Check {field}")

            for i, k in enumerate(self.Sex_at_Birth):
                MoF = ["male | female", "female | male", "female i male", "male i female"]
                if k is not None:
                    if k.lower().strip() == "n/a":
                        self.Sex_at_Birth[i + 1] = 'Not Specified'

                    if k.lower().strip() in MoF:
                        logging.warning("Changing male | female to other")
                        self.Sex_at_Birth[i + 1] = 'Other'

            # Cleaning out characters in Vaccine Typpe
            # self.SARS_CoV_2_Vaccine_Type = [x for x in self.SARS_CoV_2_Vaccine_Type if x not in VARS_TO_CLEAN]

            # changing SeroNet terms to ImmPort specific terms 
            for i, k in enumerate(self.Study_Location):
                k = k.split(' | ')
                if isinstance(k , list) and len(k ) > 1:
                    if len(set(k ).intersection(STATES)) < len(k ):
                        self.Study_Location[i + 1] = 'Other'
                    else:
                        self.Study_Location[i + 1] = 'United States of America'
                
                elif k[0].strip().upper() in STATES.keys():
                    self.Study_Location[i + 1] = f"US: {STATES.get(k[0].strip().upper())}"

            # if len(set(self.User_Defined_ID)) != len(self.User_Defined_ID):
            #     logging.error("[human AOC]: Check for repeat User Defined IDs")
            #     sys.exit("ERROR:: Error [human AOC]: Check User Defined ID")





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

    def __len__(self):
        if len(set(self.User_Defined_ID).intersection([None])) == 1:
            return False
        # if not self.User_Defined_ID:
        return bool(len(self.User_Defined_ID))
        # return True

    def __post_init__(self):

        if len(self.User_Defined_ID):
            # IMMPORT_REQUIRED = ['User_Defined_ID', 'Name','Description','Type_Reported',
            # 'Species','Biosample_Types', 'Sex_at_Birth', 'Age_Event', 'Study_Location']

            # Checking to make sure everying is the same length (taking into acount that None are Empty Spaces)
            largest_val = 0

            for field in self.__dataclass_fields__:
                if field != "ImmPortNAME":
                    cell = seroFxn.clean_array(getattr(self,field), [None])
                    if len(cell) != 0:
                        value = len(cell)
                        if value > largest_val:
                            largest_val = value

            for field in self.__dataclass_fields__:
                # if field in IMMPORT_REQUIRED:
                    
                cell = seroFxn.clean_array(getattr(self,field), [None])
                if len(cell) > 0 and field != "ImmPortNAME":
                    if len(cell) != largest_val:
        #                 logging.error("[planned visit]: check Order Numer")
                        sys.exit(f"ERROR:: Error [Subject organism]: Check {field}")

            # shorting vaccine type to non-hidden characters  
            # self.SARS_CoV_2_Vaccine_Type = [x for x in self.SARS_CoV_2_Vaccine_Type if x not in VARS_TO_CLEAN]

            # changing SeroNet species terms to ImmPort specific terms 
            for i, k in enumerate(self.Species):
                if k is not None:
                    if k.lower().strip() == "human":
                        self.Species[i + 1] = 'Homo sapiens'

                    if k.lower().strip() == "mice":
                        self.Species[i + 1] = "Mus musculus"

                    if k.lower().strip() == "cynomolgus macaques":
                        self.Species[i + 1] = "macaca fascicularis"

                    if k.lower().strip() == "african green monkey":
                        self.Species[i + 1] = "Chlorocebus sabaeus"
                        # Chlorocebus aethiops. Change when added to immport

                    if k.lower().strip() in ["syrian hamster", "syrian hamsters", "golden hampster", "golden syrian hampsters",
                                     "golden syrian hampster", "golden hampsters"]:
                        self.Species[i + 1] == "Mesocricetus auratus"

            #cells are n/a. Changing to Not Specified. 
            for i, k in enumerate(self.Age_Event):
                if k is not None:
                    if k.lower().strip() == "n/a":
                        self.Age_Event[i + 1] = 'Not Specified'

            #cells are n/a. Changing to Not Specified. 
            for i, k in enumerate(self.Sex_at_Birth):
                MoF = ["male | female", "female | male", "female i male", "male i female"]
                if k is not None:
                    if k.lower().strip() == "n/a":
                        self.Sex_at_Birth[i + 1] = 'Not Specified'

                    if k.lower().strip() in MoF:
                        self.Sex_at_Birth[i + 1] = 'Other'

            # changing SeroNet terms to ImmPort specific terms 
            for i, k in enumerate(self.Study_Location):
                k = k.split(' | ')
                if isinstance(k , list) and len(k ) > 1:
                    if len(set(k).intersection(STATES)) < len(k ):
                        self.Study_Location[i + 1] = 'Other'
                    else:
                        self.Study_Location[i + 1] = 'United States of America'
                
                elif k[0].strip().upper() in STATES.keys():
                    self.Study_Location[i + 1] = f"US: {STATES.get(k[0].strip().upper())}"


# @dataclass
# class immuneExposure:
#     SARS_CoV2_History: list = field(default_factory=list)
#         # SARS-CoV2 Historys
#     SARS_CoV_2_Vaccine_Type: list = field(default_factory=list)
#         # SARS-CoV-2 Vaccine Type
#     COVID_19_Disease_Severity: list = field(default_factory=list)
#         # COVID-19 Disease Severity

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

    def __post_init__(self):

        if len(set(self.User_Defined_ID)) != len(self.User_Defined_ID):
            logging.error("[planned visit]: check user defined ID")
            sys.exit("ERROR:: [planned visit]: check user defined ID")

            # Script to auto change user defined ID. Not sure if this is smart to have
            # temp = self.User_Defined_ID[1][:-1]
            # object.__setattr__(self, "User_Defined_ID", [temp+str(i+1) for i in range(len(self.User_Defined_ID))])

        if len(set(self.Order_Number)) != len(self.Order_Number):
            logging.error("[planned visit]: check Order Numer")
            sys.exit("ERROR:: Same order number used more than once")


@dataclass
class study_experiment_samples:
    Expt_Sample_User_Defined_ID: list = field(default_factory=list)
    Expt_Sample_Biospecimen_Type: list = field(default_factory=list)
    Expt_Sample_Biospecimen_Collection_Point: list = field(default_factory=list)

    def __post_init__(self):
        temp = self.Expt_Sample_User_Defined_ID[1][:-1]
        object.__setattr__(self, "Expt_Sample_User_Defined_ID",
                           [temp + str(i + 1) for i in range(len(self.Expt_Sample_User_Defined_ID))])


@dataclass
class study_experiment:
    Experiment_ID: str = None
    Experiment_Name: list = field(default_factory=list)
    Experiment_Assay_Type: list = field(default_factory=list)
    Experiment_Results_File_Name: str = None

    def __bool__(self):
        return (len(list(self.Experiment_Results_File_Name)) == len(list(set(self.Experiment_Results_File_Name))))

    def __post_init__(self):
        temp = self.Experiment_ID[1][:-1]
        object.__setattr__(self, "Experiment_ID", [temp + str(i + 1) for i in range(len(self.Experiment_ID))])


@dataclass
class reagent_per_experiment:
    Reagent_ID: list = field(default_factory=list)
    SARS_CoV_2_Antigen: list = field(default_factory=list)
    Assay_Use: list = field(default_factory=list)
    Manufacturer: list = field(default_factory=list)
    Catalog: list = field(default_factory=list)

    # def __bool__(self):
    # if self.Reagent_ID == ""

    def __post_init__(self):
        if len(self.Reagent_ID):
            largest_val = 0

            for field in self.__dataclass_fields__:
                if field != "ImmPortNAME":
                    cell = seroFxn.clean_array(getattr(self,field), [None])
                    if len(cell) != 0:
                        value = len(cell)
                        if value > largest_val:
                            largest_val = value

            for field in self.__dataclass_fields__:
                # if field in IMMPORT_REQUIRED:
                    
                cell = seroFxn.clean_array(getattr(self,field), [None])
                if len(cell) > 0 and field != "ImmPortNAME":
                    if len(cell) != largest_val:
        #                 logging.error("[planned visit]: check Order Numer")
                        sys.exit(f"ERROR:: Error [Reagent]: Check {field}")

            if not len(self.Manufacturer):
                object.__setattr__(self, 'Manufacturer', 0)

            
            if len(self.Reagent_ID):
                if self.Reagent_ID[1] not in VARS_TO_CLEAN:
                    temp = self.Reagent_ID[1][:-1]
                    object.__setattr__(self, "Reagent_ID", [temp + str(i + 1) for i in range(len(self.Reagent_ID))])

                    for IDS in self.Reagent_ID:
                        if not re.match('pmid[\d]{8}_\w*?-[\d]{2}', IDS, re.IGNORECASE):
                            logging.error("[Reagent]: Reagent_ID is wrong")
                else:
                    sys.exit(f"ERROR:: Error [Reagent_ID]: Missing value in Reagent ID")


@dataclass
class results:
    Results_Virus_Target: list = field(default_factory=list)
    Results_Antibody_Isotype: list = field(default_factory=list)
    Results_Reporting_Units: list = field(default_factory=list)
    Results_Reporting_Format: list = field(default_factory=list)
