from dataclasses import dataclass, field
import seronetDataclass_v2 as seroClass
import datetime as dt 
import numpy as np
import pandas as pd
import os 

####
'''
https://docs.python.org/3/library/logging.html
'''

VARS_TO_CLEAN = ['', 'N/A', 'n/a', np.nan, None]

STATES = pd.read_csv(os.path.join("dictionary","States.csv"),
    header=None,
    index_col=0,
    squeeze=True).to_dict()
###

# Creating a class for each part in the Excel Doc. 
# have a defult NA
# Check for PMIDXXXX
###
# ERROR LOGS
import logging
today = dt.datetime.today().strftime('%Y_%m_%d')
logging.basicConfig(filename=f'./log/Registry_{today}.log', level=logging.DEBUG,
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
    NAME : str = 'study'

    def __post_init__(self):

    	self.Study_Identifier = self.Study_Identifier.replace('\n','').replace('\t','')
    	self.Study_Name = self.Study_Name.replace('\n','').replace('\t','')
    	self.Publication_Title = self.Publication_Title.replace('\n','').replace('\t','')
    	self.Study_Objective = self.Study_Objective.replace('\n','').replace('\t','')
    	self.Study_Description = self.Study_Description.replace('\n','').replace('\t','')


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
    ImmPortNAME : str = 'study_personnel'

    def __post_init__(self):
        if len(self.Role_In_Study) != len(self.User_Defined_ID) != len(self.Last_Name) != len(self.First_Name) != len(self.Organization) != len(self.Email) != len(self.Title_In_Study):
            logging.error("[study personnel]: Lengths of personnel is wrong")
            print("[study personnel]: Check Study Personnel")

        
@dataclass
class study_file:
    File_Name: list = field(default_factory=list)
    Description: list = field(default_factory=list)
    Study_File_Type: list = field(default_factory=list)
    ImmPortNAME : str = 'study_file'

    # def __bool__(self):
    #     print(len(list(self.Study_File_Type)) == len(list(set(self.Study_File_Type))))


    def __post_init__(self):
        for i, k in enumerate(self.Description):
            object.__setattr__(self, 'Description', [k.replace('\n','').replace('\t','') for i, k in enumerate(self.Description)])
            # self.Description[i] = k.replace('\n','').replace('\t','')

        if len(list(self.File_Name)) != len(list(set(self.File_Name))):
            logging.warning("[file names]: Redudant names: file names")
            print("[file names]: Check file names")

        if len(self.File_Name) != len(self.Study_File_Type):
            logging.warning("[file names]: Missing value")
            print("[file names]: Check for missing values")

@dataclass
class study_link:
    Name: list = field(default_factory=list)
    Value: list = field(default_factory=list)
    ImmPortNAME : str = 'study_link'        
        

@dataclass
class study_categorization:
    """1 Column to the right"""
    Research_Focus: str = None
    Study_Type: str = None
    Keywords: list = None
    ImmPortNAME : str = 'study_categorization'

    def __post_init__(self):
    	self.Keywords = self.Keywords.replace('\n','').replace('\t','').replace(';',',').replace('|',',')

@dataclass
class study_design:
    """1 Column to the right"""
    Clinical_Study_Design: str = None
    in_silico_Model_Type: str = None 
    ImmPortNAME : str = 'NA'
        
@dataclass
class protocols:
    Protocol_ID: str
    Protocol_File_Name: str
    Protocol_Name: str
    Protocol_Description: str = None
    Protocol_Type: str = None
    ImmPortNAME : str = 'study_2_protocol'
        
@dataclass
class condition_or_disease:
    """1 Column to the right"""
    Reported_Health_Condition: str = None
    ImmPortNAME : str = 'study_2_condition_or_disease'

    def __post_init__(self):
        for i, k in enumerate(self.Reported_Health_Condition):
            object.__setattr__(self, 'Reported_Health_Condition', [k.replace('\n','').replace('\t','') for i, k in enumerate(self.Reported_Health_Condition)])
            # self.Reported_Health_Condition[i] = k.replace('|',',').replace(':',',')
        
@dataclass
class Intervention_Agent:
    SARS_CoV_2_Vaccine_Type: list = None
    ImmPortNAME : str = 'NA'
        
@dataclass
class study_details:
    Clinical_Outcome_Measure: str = None
    Enrollment_Start_Date: str = None #this is a datetime object
    Enrollment_End_Date: str = None #this is a datetime object
    Number_of_Study_Subjects: str = None    
    Age_Unit: str = 'Years'
    Minimum_Age: int = None
    Maximum_Age: int = None
    ImmPortNAME : str = 'study'

    def __post_init__(self):
        if self.Maximum_Age is None:
            object.__setattr__(self, 'Maximum_Age', 89)
            
        if self.Minimum_Age is None:
            object.__setattr__(self, 'Minimum_Age', 0)

        if self.Enrollment_End_Date in VARS_TO_CLEAN:
            object.__setattr__(self, 'Enrollment_Start_Date', '')


@dataclass
class inclusion_exclusion:
    """1 row below, 3 Columns"""
    User_Defined_ID: list = None
    Criterion: list = field(default_factory=list)
    Criterion_Category: list = field(default_factory=list)
    ImmPortNAME : str = 'inclusion_exclusion'

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

    ImmPortNAME : str = 'study_pubmed'

    def __any__(self):
    	return bool(self.Pubmed_ID)
 
@dataclass
class arm_or_cohort:
    User_Defined_ID: list = field(default_factory=list),
    Name:  list = field(default_factory=list),
    Description:  list = field(default_factory=list),
    Type_Reported:  list = field(default_factory=list),
    ImmPortNAME: str  = 'arm_or_cohort'

    def __post_init__(self):
        for i, k in enumerate(self.Description):
            object.__setattr__(self, 'Description', [k.replace('\n','').replace('\t','') for i, k in enumerate(self.Description)])
            # self.Description[i] = k.replace('\n','').replace('\t','')


        # temp = self.User_Defined_ID[0][:-1]
        # object.__setattr__(self, "User_Defined_ID", [temp+str(i+1) for i in range(len(self.User_Defined_ID))])

@dataclass
class subject_type_human:
    User_Defined_ID: list = None # might need to change
    Name: list = None #arm
    Description: list = None #arm
    Type_Reported: list = None #arm type
    Ethnicity: list = field(default_factory=list)
    Race: list = field(default_factory=list)
    Race_Specify: list = field(default_factory=list)
    Subject_Description: list = field(default_factory=list)
    Sex_at_Birth: list = field(default_factory=list)
    Age_Event: list = field(default_factory=list)
    Subject_Phenotype: list = field(default_factory=list)
    Study_Location: list = field(default_factory=list) # Add something to make north west or check?
    Assessment_Name: list = field(default_factory=list)
    Measured_Behavioral_or_Psychological_Factor: list = field(default_factory=list)
    Measured_Social_Factor: list = field(default_factory=list)
    SARS_CoV_2_Symptoms: list = field(default_factory=list)
    Assessment_Clinical_and_Demographic_Data_Provenance: list = field(default_factory=list)
    Assessment_Demographic_Data_Types_Collected: list = field(default_factory=list)
    SARS_CoV2_History: list = field(default_factory=list)
    SARS_CoV_2_Vaccine_Type: list = field(default_factory=list)
    COVID_19_Disease_Severity: list = field(default_factory=list)
    ImmPortNAME: str = 'n/a'

    def __bool__(self):
        if len(set(self.User_Defined_ID).intersection([None])) == 1:
            return False
        else:
            return True

    def __post_init__(self):
        self.SARS_CoV_2_Vaccine_Type = [x for x in self.SARS_CoV_2_Vaccine_Type if x not in VARS_TO_CLEAN]

        # changing SeroNet terms to ImmPort specific terms 
        for i, k in enumerate(self.Study_Location):
            if isinstance(k, list) and len():
                if len(set(k).intersection(STATES)) < len(k):
                    self.Study_Location[i+1] = 'Other'
                else:
                    self.Study_Location[i+1] = 'United States of America'


            elif k in STATES:
                self.Study_Location[i+1] = f"US: {STATES.get(k)}"

        if len(set(self.User_Defined_ID)) != len(self.User_Defined_ID):
            logging.error("[human AOC]: Check for repeat User Defined IDs")
            print("Error [human AOC]: Check User Defined ID")



@dataclass
class subject_type_mode_organism:
    User_Defined_ID: list = None #might need to change
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
    ImmPortNAME: str = 'n/a'

    def __bool__(self):
        if len(set(self.User_Defined_ID).intersection([None])) == 1:
            return False
        else:
            return True

    def __post_init__(self):

        if len(self.User_Defined_ID):
            # shorting vaccine type to non-hidden characters  
            self.SARS_CoV_2_Vaccine_Type = [x for x in self.SARS_CoV_2_Vaccine_Type if x not in VARS_TO_CLEAN]
            
            # changing SeroNet species terms to ImmPort specific terms 
            for i, k in enumerate(self.Species):
                if k is not None:
                    if k.lower() == "human":
                        self.Species[i+1] = 'Homo Sapiens'

                    if k.lower() in ["syrian hamster", "syrian hamsters", "golden hampster", "golden syrian hampsters","golden syrian hampster", "golden hampsters"]:
                        self.Species[i+1] == "Mesocricetus auratus"


            # changing SeroNet terms to ImmPort specific terms 
            for i, k in enumerate(self.Study_Location):
                if isinstance(k, list) and len():
                    if len(set(k).intersection(STATES)) < len(k):
                        self.Study_Location[i+1] = 'Other'
                    else:
                        self.Study_Location[i+1] = 'United States of America'


                elif k in STATES:
                    self.Study_Location[i+1] = f"US: {STATES.get(k)}"

        if len(set(self.User_Defined_ID)) != len(self.User_Defined_ID):
            logging.error("[organism AOC]: Check for repeat User Defined IDs")
            print("Error [organism AOC]: Check User Defined ID")


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
    ImmPortNAME : str = 'planned_visit'

    def __post_init__(self):

        if len(set(self.User_Defined_ID)) != len(self.User_Defined_ID):
            logging.error("[planned visit]: check user defined ID")
            print("[planned visit]: check user defined ID")

            # Script to auto change user defined ID. Not sure if this is smart to have
            # temp = self.User_Defined_ID[1][:-1]
            # object.__setattr__(self, "User_Defined_ID", [temp+str(i+1) for i in range(len(self.User_Defined_ID))])

        if len(set(self.Order_Number)) != len(self.Order_Number):
            logging.error("[planned visit]: check Order Numer")
            print("Same order number used more than once")



@dataclass
class study_experiment_samples:
    Expt_Sample_User_Defined_ID: list = field(default_factory=list)
    Expt_Sample_Biospecimen_Type: list = field(default_factory=list)
    Expt_Sample_Biospecimen_Collection_Point: list = field(default_factory=list)

    def __post_init__(self):
        temp = self.Expt_Sample_User_Defined_ID[1][:-1]
        object.__setattr__(self, "Expt_Sample_User_Defined_ID", [temp+str(i+1) for i in range(len(self.Expt_Sample_User_Defined_ID))])

@dataclass
class study_experiment:
    Experiment_ID: str = None
    Experiment_Name: list = field(default_factory=list)
    Experiment_Assay_Type: list = field(default_factory=list)
    Experiment_Results_File_Name: str = None

    def __bool__(self):
        return(len(list(self.Experiment_Results_File_Name)) == len(list(set(self.Experiment_Results_File_Name))))

    def __post_init__(self):
        temp = self.Experiment_ID[1][:-1]
        object.__setattr__(self, "Experiment_ID", [temp+str(i+1) for i in range(len(self.Experiment_ID))])



        
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
        if not len(self.Manufacturer):
            object.__setattr__(self, 'Manufacturer', 0)

        temp = self.Reagent_ID[1][:-1]
        object.__setattr__(self, "Reagent_ID", [temp+str(i+1) for i in range(len(self.Reagent_ID))])

  
@dataclass 
class results:
    Results_Virus_Target: list = field(default_factory=list)
    Results_Antibody_Isotype: list = field(default_factory=list)
    Results_Reporting_Units: list = field(default_factory=list)
    Results_Reporting_Format: list = field(default_factory=list)
        
        
