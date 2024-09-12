import functions_CBC as ifxn
import pandas as pd
import re
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

autoImmune_data = cbcFxn.obtain_data('Participants_With_Autoimmune_Condition_4.0.0','Autoimmune Status',data_path)
cancer_data = cbcFxn.obtain_data('Participants_With_Cancer_4.0.0','Cancer Status at Baseline',data_path)
hiv_data = cbcFxn.obtain_data('Participants_With_HIV_4.0.0','HIV Status at Baseline',data_path)
SOTR_data = cbcFxn.obtain_data('Participants_With_Organ_Transplant_4.0.0','Transplant Status at Baseline',data_path)
all_covid_data = cbcFxn.obtain_data('Covid_History_4.0.0','Covid Test All Visit',data_path)
pos_covid_data = cbcFxn.obtain_data('Covid_History_4.0.0','Positive Covid Visits',data_path)

# neg_covid_data = all_covid_data[all_covid_data['Covid Test Summary'].str.contains(r'No Covid Event|Negative')]
# neg_covid_data.to_csv('test2.csv')
# Reported_health_data = cbcFxn.obtain_data('Reported_Health_Conditions_4.0.0',data_path)

ids=autoImmune_data['Research_Participant_ID']+cancer_data['Research_Participant_ID']+hiv_data['Research_Participant_ID']+SOTR_data['Research_Participant_ID']
cohort=autoImmune_data['Primary_Cohort']+cancer_data['Primary_Cohort']+hiv_data['Primary_Cohort']+SOTR_data['Primary_Cohort']

exposure_process=[]
exposure_material=[]
disease=[]
stage=[]

############### CHECK
'''
print("autoImmune_data: ", len(autoImmune_data['Research_Participant_ID'].drop_duplicates()))
print("cancer_data: ", len(cancer_data['Research_Participant_ID'].drop_duplicates()))
print("hiv_data: ", len(hiv_data['Research_Participant_ID'].drop_duplicates()))
print("SOTR_data: ", len(SOTR_data['Research_Participant_ID'].drop_duplicates()))
total=len(autoImmune_data['Research_Participant_ID'].drop_duplicates())+len(cancer_data['Research_Participant_ID'].drop_duplicates())+\
	len(hiv_data['Research_Participant_ID'].drop_duplicates())+len(SOTR_data['Research_Participant_ID'].drop_duplicates())
print("sum: ", total)

demographic_data = cbcFxn.obtain_data('Demographics_4.0.0','Detailed_Report',data_path)
print("demographic_data: ", len(demographic_data['Research_Participant_ID'].drop_duplicates()))
'''

###############

# This portion is adding data by cohort
vocab=['occurrence of autoimmune disease', 'occurrence of cancer', 'occurrence of infectious disease', 'solid tissue transplantation','occurrence of infectious disease']
disease=['Autoimmune_Condition','Cancer','Primary_Cohort','Organ Transplant', 'COVID_Status']
df=pd.DataFrame()

for i, cohort in enumerate([autoImmune_data, cancer_data, hiv_data, SOTR_data, pos_covid_data]):
	LEN = len(cohort['Research_Participant_ID'])
	BLANKS = ['']*LEN

	OUT = pd.DataFrame(columns=cbcFxn.grab_headers('immuneExposure'))
	OUT['Column Name']=BLANKS
	OUT['Subject ID']=cohort['Research_Participant_ID']
	OUT['Arm Or Cohort ID']=cbcFxn.clean_data(cohort['Primary_Cohort'])
	OUT['Exposure Process Reported']=[vocab[i]]*LEN
	OUT['Exposure Material Reported']=BLANKS
	OUT['Exposure Material ID']=BLANKS
	OUT['Disease Ontology ID']=BLANKS

	if i == 4:
		dr = cbcFxn.clean_data(['COVID-19 Positive']*LEN) #this vocab isnt right
		ds = cbcFxn.clean_data(cohort['Disease_Severity'])
	else:
		dr = cbcFxn.clean_data(cohort[disease[i]]) #this vocab isnt right
		ds = BLANKS
	
	OUT['Disease Reported']=dr
	OUT['Disease Stage Reported']=ds
	

	df = pd.concat([df,OUT])

# cbcFxn.create_final(df,'immuneExposure',path.join(out_path,'vrss_immuneExposure.txt'))
# cbcFxn.create_final(df.drop_duplicates(),'immuneExposure',path.join(out_path,'vrss_immuneExposure-nodup.txt'))



#### Are things counted twice??

columns_of_interest = [
'Diabetes', 'Hypertension', 'Obesity', 'Cardiovascular_Disease', 'Chronic_Lung_Disease', 
'Chronic_Kidney_Disease', 'Chronic_Liver_Disease', 'Acute_Liver_Disease', 'Immunosuppressive_Condition', 
'Autoimmune_Disorder', 'Chronic_Neurological_Condition', 'Chronic_Oxygen_Requirement', 
'Inflammatory_Disease', 'Viral_Infection', 'Bacterial_Infection', 'Cancer', 'Substance_Abuse_Disorder', 
'Organ_Transplant_Recipient'
]


# # This portion is adding data by reported health conditions
r_h_d = cbcFxn.obtain_data('Reported_Health_Conditions_4.0.0','Brief_Report',data_path)
for i in columns_of_interest:
	reported = r_h_d[r_h_d[i].str.contains(r'Yes|Obesity|Over')]

	LEN = len(reported['Research_Participant_ID'])
	BLANKS = ['']*LEN

	OUT = pd.DataFrame(columns=cbcFxn.grab_headers('immuneExposure'))
	OUT['Column Name']=BLANKS
	OUT['Subject ID']=reported['Research_Participant_ID']
	OUT['Arm Or Cohort ID']=cbcFxn.clean_data(reported['Primary_Cohort'])
	OUT['Exposure Process Reported']=['occurrence of disease']*LEN
	OUT['Exposure Material Reported']=BLANKS
	OUT['Exposure Material ID']=BLANKS
	OUT['Disease Reported']=cbcFxn.clean_data([i]*LEN) #this vocab isnt right
	OUT['Disease Ontology ID']=BLANKS
	if i == 4:
		ds = cbcFxn.clean_data(cohort['Disease_Severity'])
	else:
		ds = BLANKS
	OUT['Disease Stage Reported']=ds

	df = pd.concat([df,OUT])


cbcFxn.create_final(df,'immuneExposure',path.join(out_path,'vrss_immuneExposure2.txt'))
cbcFxn.create_final(df.drop_duplicates(),'immuneExposure',path.join(out_path,'vrss_immuneExposure-nodup2.txt'))

print("created: immuneExposure templates")
# Reported_health_data['Obesity'] =[re.sub('.*Obesity.*','obesity ; DOID:9970', x) for x in Reported_health_data['Obesity']]
# print(Reported_health_data.iloc[:, 4:])



#.notnull()
'''
vocab=['Condition Not Described', 'Not Reported']

for i, cohort in enumerate([autoImmune_data, cancer_data, hiv_data, SOTR_data]):
	LEN = len(cohort['Research_Participant_ID'])
	BLANKS = ['']*LEN

	OUT = pd.DataFrame(columns=cbcFxn.grab_headers('immuneExposure'))
	OUT['Column Name']=BLANKS
	OUT['Subject ID']=cohort['Research_Participant_ID']
	OUT['Arm Or Cohort ID']=cbcFxn.clean_data(cohort['Primary_Cohort'])
	OUT['Exposure Process Reported']=[vocab[i]]*LEN
	OUT['Exposure Material Reported']=BLANKS
	OUT['Exposure Material ID']=BLANKS
	OUT['Disease Reported']=cbcFxn.clean_data(cohort[disease[i]]) #this vocab isnt right
	OUT['Disease Ontology ID']=BLANKS
	OUT['Disease Stage Reported']=BLANKS

	df = pd.concat([df,OUT])

cbcFxn.create_final(df,'immuneExposure',path.join(out_path,'vrss_immuneExposure.txt'))
cbcFxn.create_final(df.drop_duplicates(),'immuneExposure',path.join(out_path,'vrss_immuneExposure-nodup.txt'))

'''



