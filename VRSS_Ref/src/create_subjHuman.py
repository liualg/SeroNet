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


base_path='/Users/liualg/Documents/GitHub/SeroNet/VRSS_Ref'
data_path=path.join(base_path,'data')
immport_templates='/Users/liualg/Documents/GitHub/SeroNet/seronetTemplates/template/v.50/ImmPortTemplates.6661.2023-12-04.11-24-40/excel-templates'


map_folder = path.join(base_path,'mapping')
reference_study = path.join(data_path,'reff')
vrss_study = path.join(data_path,'vrss')
final_ref = path.join(base_path,'final')

demographic_data = cbcFxn.obtain_data('demographics_2.0.0','Demographic_Data')
symptom_data = cbcFxn.obtain_data('symptomatic_data_2.0.0','Symptom Data')

# Get locations
location=[]
for x in demographic_data['Submission_CBC']:
	x = str(x)
	if x == '14':
		y='US: New York' #Mt. Sinai
	elif x == '41':
		y='US: New York' # 'Feinstein'
	elif x == '27':
		y='US: Minnesota' #y= 'UMN'
	elif x == '32':
		y= 'US: Arizona'
	else:
		y=''
	location.append(y)

#Get exposure and disease 

exposure_process=[]
exposure_material=[]
disease=[]
stage=[]

for x in demographic_data['# Research_Participant_ID']:
	if symptom_data['# Research_Participant_ID'].str.contains(x).any():
		temp = symptom_data[symptom_data['# Research_Participant_ID'] == x].reset_index(drop=True)
		# print(temp)
		if temp['Is_Symptomatic'][0] == 'Yes':
			exposure_process.append('occurrence of infectious disease')
			exposure_material.append('SARS-CoV-2 ; NCBITaxon:2697049')
			disease.append('COVID-19 ; DOID:0080600')
			if temp['Symptoms_Resolved'][0] == 'Yes':
				stage.append('Post')
			else:
				stage.append(temp['Covid_Disease_Severity'][0])
		else:
			exposure_process.append('no exposure')
			exposure_material.append('')
			disease.append('')
			stage.append('')
	else:
		print('asdadasds')
		exposure_process.append('no exposure')


LEN = len(demographic_data['# Research_Participant_ID'])
BLANKS = ['']*LEN

OUT = pd.DataFrame(columns=cbcFxn.grab_headers('subjectHumans'))
OUT['Column Name']=BLANKS
OUT['Subject ID']=demographic_data['# Research_Participant_ID']
OUT['Arm Or Cohort ID']=['SeroNet_Reference_Study_human_subject-01']*LEN
OUT['Gender']=cbcFxn.clean_data(demographic_data['Gender'])
OUT['Min Subject Age']=demographic_data['Age']
OUT['Max Subject Age']=demographic_data['Age']
OUT['Age Unit']=['Years']*LEN
OUT['Age Event']=['Age at enrollment']*LEN
OUT['Age Event Specify']=BLANKS
OUT['Subject Phenotype']=BLANKS
OUT['Subject Location']=location
OUT['Ethnicity']=cbcFxn.clean_data(demographic_data['Ethnicity'])
OUT['Race']=cbcFxn.clean_data(demographic_data['Race'])
OUT['Race Specify']=BLANKS
OUT['Description']=BLANKS
OUT['Result Separator Column']=BLANKS
OUT['Exposure Process Reported']=exposure_process
OUT['Exposure Material Reported']=exposure_material
OUT['Exposure Material ID']=BLANKS
OUT['Disease Reported']=disease
OUT['Disease Ontology ID']=BLANKS
OUT['Disease Stage Reported']=stage



cbcFxn.create_final(OUT,'subjectHumans','refr_subjectHuman.txt')

# print(ELISA_OUT['Unit Reported'][0])

# NEED TO GET DATA FOR OTHER TYPES OF EXPERIMENTS 


