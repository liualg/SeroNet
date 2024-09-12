import cbc_functions as cbcFxn
import pandas as pd
from sys import platform
from os import path, system
import numpy as np

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
final_ref = path.join(base_path,'final','updates')

# Open file
def obtain_data(file,sname,base_dir=reference_study):
	return pd.read_excel(path.join(base_dir,file+'.xlsx'),sheet_name=sname)

# Get ImmPort Template headers
def grab_headers(file,base_dir=immport_templates):
	return pd.read_excel(path.join(base_dir,file+'.xlsx'),header=None).iloc[[2]].values.flatten().tolist()

def grab_top(file,base_dir=immport_templates):
	return pd.read_excel(path.join(base_dir,file+'.xlsx'),header=None).iloc[[0,1]].values.flatten().tolist()



demographic_data = obtain_data('demographics_2.0.0','Demographic_Data')
symptom_data = obtain_data('symptomatic_data_2.0.0','Symptom Data')
comorb_data = obtain_data('comorbidity_or_infections_2.0.0','Comorbidity_Data')
# serology_data = obtain_data('serology_results_data_2.0.0','Serology Results')
serology_data = obtain_data('serology_results_data_2.1.0','Serology Results')
PCR_data = obtain_data('Prior_PCR_Testing_2.0.0','PCR_Test_Data')
# assay_data = assay_data.replace(np.nan, 'aaa', regex=True)
# print(assay_data['Assay_Target_Sub_Region'])

def get_set_data(data, column, group_index):
	OUT = data.groupby(group_index, dropna=False)[column].apply(','.join).reset_index()
	OUT[column] = [','.join(list(set(x.split(',')))) for x in OUT[column]]
	OUT[column] = [x.strip() for x in OUT[column]]
	OUT[column] = OUT[column].replace('aaa', np.nan, regex=True)
	return(dict(zip(OUT[group_index], OUT[column])))

#ARU = get_set_data(assay_data,'Assay_Result_Unit','# Assay_ID')

# Get locations
def get_locations(column_name):
	location=[]
	for x in column_name:
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
	return location

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
				stage.append(temp['Covid_Disease_Severity'])
		else:
			exposure_process.append('no exposure')
			exposure_material.append('')
			disease.append('')
			stage.append('')
	else:
		print('asdadasds')
		exposure_process.append('no exposure')


'''
compenents = [
'refr-COVID19_Symptom_Status','refr-Physical_Exam',
'refr-Coinfection','refr-COVID19_History','refr-Comorbidity'
]
'''

# ######## Comorbidity ######### #
DATA = comorb_data
LEN = len(DATA['# Research_Participant_ID'])
BLANKS = ['']*LEN
value=[]
for i in DATA['Cormobidity_is_Present']:
	if str(i) == '1':
		value.append('Yes')
	else:
		value.append('No')

compenent = 'refr-Comorbidity'
# compenent = compenent.split('-')[1]
OUT = pd.DataFrame(columns=grab_headers('assessmentcomponent'))
OUT['Column Name']=BLANKS
OUT['User Defined ID']=[f'refr-symp_status-Comorbidity-{x}' for x in range(LEN)]
OUT['Assessment Panel ID']=[compenent]*LEN
OUT['Subject ID']=[x.strip() for x in DATA['# Research_Participant_ID']]
OUT['Planned Visit ID']=['SeroNet_Reference_Study_visit-01']*LEN
OUT['Name Reported']=DATA['Comorbidity_Name']
OUT['Study Day']=['0']*LEN
OUT['Result Value Reported']=value
OUT['Result Unit Reported']=['Yes/No/Unknown']*LEN
OUT['Result Value Category']=BLANKS
OUT['Age At Onset Reported']=BLANKS
OUT['Age At Onset Unit Reported']=BLANKS
OUT['Is Clinically Significant']=BLANKS
OUT['Location Of Finding Reported']=get_locations(DATA['Submission_CBC'])
OUT['Organ Or Body System Reported']=BLANKS
OUT['Subject Position Reported']=BLANKS
OUT['Time Of Day']=BLANKS
OUT['Verbatim Question']=BLANKS
OUT['Who Is Assessed']=BLANKS


# print(OUT)
# OUT.to_csv(path.join(final_ref,'refr-component-comorbidity.txt'), sep='\t')
#cbcFxn.create_final(OUT,'assessmentcomponent', 'refr-component-comorbidity.txt')


# ######## COVID19_Symptom_Status ######### #
DATA = symptom_data
LEN = len(DATA['# Research_Participant_ID'])
BLANKS = ['']*LEN
value=[]
for i in DATA['Is_Symptomatic']:
	if i == '':
		value.append('Unknown')
	else:
		value.append(i)

compenent = 'refr-COVID19_Symptom_Status'
# compenent = compenent.split('-')[1]
OUT = pd.DataFrame(columns=grab_headers('assessmentcomponent'))
OUT['Column Name']=BLANKS
OUT['User Defined ID']=[f'refr-COVID19_Symptom_Status-{x}' for x in range(LEN)]
OUT['Assessment Panel ID']=[compenent]*LEN
OUT['Subject ID']=[x.strip() for x in DATA['# Research_Participant_ID']]
OUT['Planned Visit ID']=['SeroNet_Reference_Study_visit-01']*LEN
OUT['Name Reported']=['Is_Symptomatic']*LEN
OUT['Study Day']=['0']*LEN
OUT['Result Value Reported']=value
OUT['Result Unit Reported']=['Yes/No/Unknown']*LEN
OUT['Result Value Category']=BLANKS
OUT['Age At Onset Reported']=BLANKS
OUT['Age At Onset Unit Reported']=BLANKS
OUT['Is Clinically Significant']=BLANKS
OUT['Location Of Finding Reported']=get_locations(DATA['Submission_CBC'])
OUT['Organ Or Body System Reported']=BLANKS
OUT['Subject Position Reported']=BLANKS
OUT['Time Of Day']=BLANKS
OUT['Verbatim Question']=BLANKS
OUT['Who Is Assessed']=BLANKS


# print(OUT)
# OUT.to_csv(path.join(final_ref,'refr-component-symptom_status.txt'), sep='\t')
# cbcFxn.create_final(OUT,'assessmentcomponent', 'refr-component-symptom_status.txt')


# ######## refr-COVID19_History ######### # 
DATA = serology_data
LEN = len(DATA['# Research_Participant_ID'])
BLANKS = ['']*LEN
value=[]
for i in DATA['sars positive']:
	if int(i)> 0:
		value.append('Yes')
	else:
		value.append('No')

compenent = 'refr-COVID19_History'
# compenent = compenent.split('-')[1]
OUT = pd.DataFrame(columns=grab_headers('assessmentcomponent'))
OUT['Column Name']=BLANKS
OUT['User Defined ID']=[f'refr-COVID19_History-x{x}' for x in range(LEN)]
OUT['Assessment Panel ID']=[compenent]*LEN
OUT['Subject ID']=[x.strip() for x in DATA['# Research_Participant_ID']]
OUT['Planned Visit ID']=['SeroNet_Reference_Study_visit-01']*LEN
OUT['Name Reported']=['SARS-CoV-2 Positive']*LEN
OUT['Study Day']=['0']*LEN
OUT['Result Value Reported']=value
OUT['Result Unit Reported']=['Yes/No/Unknown']*LEN
OUT['Result Value Category']=BLANKS
OUT['Age At Onset Reported']=BLANKS
OUT['Age At Onset Unit Reported']=BLANKS
OUT['Is Clinically Significant']=BLANKS
OUT['Location Of Finding Reported']=get_locations(DATA['CBC'])
OUT['Organ Or Body System Reported']=BLANKS
OUT['Subject Position Reported']=BLANKS
OUT['Time Of Day']=BLANKS
OUT['Verbatim Question']=BLANKS
OUT['Who Is Assessed']=BLANKS


# print(OUT)
# OUT.to_csv(path.join(final_ref,'refr-component-COVID19_History.txt'), sep='\t')
cbcFxn.create_final(OUT,'assessmentcomponent', 'refr-component-COVID19_History-2.txt')


# ######## refr-PCR test ######### # 
DATA = PCR_data
LEN = len(DATA['# Research_Participant_ID'])
BLANKS = ['']*LEN
value=[]
# for i in DATA['sars positive']:
# 	if int(i)> 0:
# 		value.append('Yes')
# 	else:
# 		value.append('No')

compenent = 'refr-Prior_PCR'
# compenent = compenent.split('-')[1]
OUT = pd.DataFrame(columns=grab_headers('assessmentcomponent'))
OUT['Column Name']=BLANKS
OUT['User Defined ID']=[f'refr-COVID19_History-{x}' for x in range(LEN)]
OUT['Assessment Panel ID']=[compenent]*LEN
OUT['Subject ID']=[x.strip() for x in DATA['# Research_Participant_ID']]
OUT['Planned Visit ID']=['SeroNet_Reference_Study_visit-01']*LEN
OUT['Name Reported']=['Prior PCR test result']*LEN
OUT['Study Day']=['0']*LEN
OUT['Result Value Reported']=DATA['Test_Result']
OUT['Result Unit Reported']=['Positive/Negative']*LEN
OUT['Result Value Category']=BLANKS
OUT['Age At Onset Reported']=BLANKS
OUT['Age At Onset Unit Reported']=BLANKS
OUT['Is Clinically Significant']=BLANKS
OUT['Location Of Finding Reported']=get_locations(DATA['Submission_CBC'])
OUT['Organ Or Body System Reported']=BLANKS
OUT['Subject Position Reported']=BLANKS
OUT['Time Of Day']=BLANKS
OUT['Verbatim Question']=BLANKS
OUT['Who Is Assessed']=BLANKS


# print(OUT)
# cbcFxn.create_final(OUT,'assessmentcomponent', 'refr-component-Prior_PCR.txt')
# OUT.to_csv(path.join(final_ref,'refr-component-Prior_PCR.txt'), sep='\t')



