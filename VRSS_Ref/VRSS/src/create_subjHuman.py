import functions_CBC as ifxn
import pandas as pd
from sys import platform
from os import path, system
import numpy as np
import cbc_functions as cbcFxn

if platform == "darwin":
    system('clear')
else:
    system('cls')


base_path='/Users/liualg/Documents/GitHub/SeroNet/VRSS_Ref/VRSS'
data_path=path.join(base_path,'data')
out_path=path.join(base_path,'xoutput')
immport_templates='/Users/liualg/Documents/GitHub/SeroNet/VRSS_Ref/xtemplates'


demographic_data = cbcFxn.obtain_data('Demographics_4.0.0','Detailed_Report',data_path)


LEN = len(demographic_data['Research_Participant_ID'])
BLANKS = ['']*LEN

OUT = pd.DataFrame(columns=cbcFxn.grab_headers('subjectHumans'))
OUT['Column Name']=BLANKS
OUT['Subject ID']=demographic_data['Research_Participant_ID']
OUT['Arm Or Cohort ID']=cbcFxn.clean_data(demographic_data['Primary_Cohort'])
OUT['Gender']=cbcFxn.clean_data(demographic_data['Sex_At_Birth'])
OUT['Min Subject Age']=demographic_data['Age']
OUT['Max Subject Age']=demographic_data['Age']
OUT['Age Unit']=['Years']*LEN
OUT['Age Event']=['Age at enrollment']*LEN
OUT['Age Event Specify']=BLANKS
OUT['Subject Phenotype']=BLANKS
OUT['Subject Location']=cbcFxn.clean_data(demographic_data['Location'])
OUT['Ethnicity']=cbcFxn.clean_data(demographic_data['Ethnicity'])
OUT['Race']=cbcFxn.clean_data(demographic_data['Race'])
OUT['Race Specify']=BLANKS
OUT['Description']=BLANKS
OUT['Result Separator Column']=BLANKS
OUT['Exposure Process Reported']=BLANKS
OUT['Exposure Material Reported']=BLANKS
OUT['Exposure Material ID']=BLANKS
OUT['Disease Reported']=BLANKS
OUT['Disease Ontology ID']=BLANKS
OUT['Disease Stage Reported']=BLANKS



cbcFxn.create_final(OUT,'subjectHumans',path.join(out_path,'vrss_subjectHuman.txt'))

# print(ELISA_OUT['Unit Reported'][0])

# NEED TO GET DATA FOR OTHER TYPES OF EXPERIMENTS 


