from dataclasses import dataclass, field

# Creating a class for each part in the Excel Doc. 
# have a defult NA
# Check for PMIDXXXX
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
        
@dataclass
class study_file:
    File_Name: list = field(default_factory=list)
    Description: list = field(default_factory=list)
    Study_File_Type: list = field(default_factory=list)
    ImmPortNAME : str = 'study_file'

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
    	self.Keywords = self.Keywords.replace('\n','').replace('\t','')

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
    Reported_Health_Condition: list = None
    ImmPortNAME : str = 'study_2_condition_or_disease'
        
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

@dataclass
class arm_or_cohort: #these can be a list, or we can do multiple ones 
    """1 row below, 4 Columns"""
    User_Defined_ID: list = None
    Name: list = None
    Description: list = None
    Type_Reported: list = None
    ImmPortNAME : str = 'arm_or_cohort'


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

    # def __post__init__(self):
    #     for i in range(len(self.User_Defined_ID)):
    #         if self.Max_Start_Day[i] == None or np.isnan(self.Max_Start_Day[i]):
    #             self.Max_Start_Day[i] = 

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
class subject:
    Subject_ID: list = field(default_factory=list)
    Sex_at_Birth: list = field(default_factory=list)
    Age_Event: list = field(default_factory=list)
    Subject_Phenotype: list = field(default_factory=list)
    Study_Location: list = field(default_factory=list)

    def __len__(self):
    	return len(self.Subject_ID) + len(self.Subject_Phenotype)
 
        
@dataclass
class subject_type_human:
    Ethnicity: list = field(default_factory=list)
    Race: list = field(default_factory=list)
    Race_Specify: list = field(default_factory=list)
    Description: list = field(default_factory=list)
    ImmPortNAME: str = 'n/a'

    def __post_init__(self):
        for i in self.Race:
            if i == 'Not Specified':
                object.__setattr__(self, 'Race', 'Unknown')

    def __len__(self):
        return len(self.Ethnicity) + len(self.Race) + len(self.Race_Specify) + len(self.Description)
        
@dataclass
class subject_type_mode_organism:
    Species: list = field(default_factory=list)
    Biosample_Types: list = field(default_factory=list)
    Strain_Characteristics: list = field(default_factory=list)
    ImmPortNAME: str = 'n/a'

    def __len__(self):
        return len(self.Species) + len(self.Biosample_Types) + len(self.Strain_Characteristics)
        
@dataclass
class immuneExposure:
    SARS_CoV2_History: list = field(default_factory=list)
        # SARS-CoV2 Historys
    SARS_CoV_2_Vaccine_Type: list = field(default_factory=list)
        # SARS-CoV-2 Vaccine Type
    COVID_19_Disease_Severity: list = field(default_factory=list)
        # COVID-19 Disease Severity
        
@dataclass
class assessment:
    Assessment_ID: list = field(default_factory=list)
    Assessment_Name: list = field(default_factory=list)
    Measured_Behavioral_or_Psychological_Factor: list = field(default_factory=list)
    Measured_Social_Factor: list = field(default_factory=list)
    SARS_CoV_2_Symptoms: list = field(default_factory=list)
    Assessment_Clinical_and_Demographic_Data_Provenance: list = field(default_factory=list)
    Assessment_Demographic_Data_Types_Collected: list = field(default_factory=list)
        
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
        
        
