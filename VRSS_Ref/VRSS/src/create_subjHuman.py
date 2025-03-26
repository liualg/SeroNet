# import cbc_functions as ifxn
import pandas as pd
from sys import platform
from os import path, system
import numpy as np
import cbc_functions as cbcFxn

if platform == "darwin":
    system('clear')
else:
    system('cls')


base_path='/Users/liualg/Documents/GitHub/SeroNet/VRSS_Ref'
data_path=path.join(base_path,'data')
immport_templates='/Users/liualg/Documents/GitHub/SeroNet/seronetTemplates/template/v.50/ImmPortTemplates.6661.2023-12-04.11-24-40/excel-templates'


map_folder = path.join(base_path,'mapping')
reference_study = path.join(data_path,'reff')
vrss_study = path.join(data_path,'VRSS')
final_ref = path.join(base_path,'final')

demographic_data = cbcFxn.obtain_data('/Users/liualg/Documents/GitHub/SeroNet/VRSS_Ref/VRSS/data/Release_4.1_with_Corrections/Demographics_4.1.0','Detailed_Report')
l1 = ['ARM10729', 'ARM10730', 'ARM10548', 'ARM10731','ARM10732','ARM10733']
l2 = ['Healthy Cohort', 'Comorbidity Cohort', 'Cancer', 'HIV', 'IBD', 'Transplant']
name2id = dict(zip(l2,l1))
#finding a mapping of sometjing 


## Get locations
states = pd.read_csv("./States.csv")
sdict = dict(zip(states['Abv'],states['Full']))
location=[]
for x in demographic_data['Location']:
	x = x.strip()
	if x != 'Northeast':
		location.append(f"US: {sdict.get(x)}")
	else:
		location.append('US: Northeast')

cohorts=[]
for x in demographic_data['SeroNet_Cohort']:
	x = x.strip()
	cohorts.append(name2id.get(x))

ethi=[]
for x in demographic_data['Ethnicity']:
	x = x.strip()
	if x in ('Not Reported','Unknown'):
		ethi.append('Not Specified')
	else:
		ethi.append(x)

# Not Reported

vaccination_data = cbcFxn.obtain_data('/Users/liualg/Documents/GitHub/SeroNet/VRSS_Ref/VRSS/data/Release_4.1_with_Corrections/Vaccination_Data_4.1.0','Visit Vacc and Side Effects')
novac = vaccination_data[vaccination_data['Last Vaccine Received']=='No vaccination event reported']
novacc_people = list(set(novac['Research_Participant_ID']))

vacc_status = []
for i in demographic_data['Research_Participant_ID']:
	if i in novacc_people:
		vacc_status.append('Not Vaccinated')
	else:
		vacc_status.append('Vaccinated')
# 

LEN = len(demographic_data['Research_Participant_ID'])
# print(LEN)
BLANKS = ['']*LEN

OUT = pd.DataFrame(columns=cbcFxn.grab_headers('subjectHumans'))
OUT['Column Name']=BLANKS
OUT['Subject ID']=cbcFxn.clean_data(demographic_data['Research_Participant_ID'])
#[f"vrss_v4-{x}" for x in demographic_data['Research_Participant_ID']]
OUT['Arm Or Cohort ID']=cohorts
OUT['Gender']=cbcFxn.clean_data(demographic_data['Sex_At_Birth'])
OUT['Min Subject Age']=demographic_data['Age']
OUT['Max Subject Age']=demographic_data['Age']
OUT['Age Unit']=['Years']*LEN
OUT['Age Event']=['Age at enrollment']*LEN
OUT['Age Event Specify']=BLANKS
OUT['Subject Phenotype']=BLANKS
OUT['Subject Location']=location
OUT['Ethnicity']=ethi
OUT['Race']=cbcFxn.clean_data(demographic_data['Race'])
OUT['Race Specify']=BLANKS
OUT['Description']=BLANKS
OUT['Result Separator Column']=BLANKS
OUT['Exposure Process Reported']=vacc_status
OUT['Exposure Material Reported']=BLANKS
OUT['Exposure Material ID']=BLANKS
OUT['Disease Reported']=BLANKS
OUT['Disease Ontology ID']=BLANKS
OUT['Disease Stage Reported']=BLANKS


### REMOVING PEOPLE IN QUESTION
rmv_pls=[
'41_100015', '41_100057', '41_100063', '41_100124', '41_100209', 
'41_100495', '41_100637', '41_100711', '41_100712', '41_100740', 
'41_100744', '41_100756', '41_100770', '41_100776', 
'41_100779', '41_100804'
]

OUT2 = OUT[~OUT['Subject ID'].isin(rmv_pls)]
# print(len(OUT))
# print(len(OUT2))
# print(len(OUT)-len(OUT2))

##



cbcFxn.create_final(OUT2,'subjectHumans','refr_subjectHuman.txt')

# print(ELISA_OUT['Unit Reported'][0])

# NEED TO GET DATA FOR OTHER TYPES OF EXPERIMENTS 


