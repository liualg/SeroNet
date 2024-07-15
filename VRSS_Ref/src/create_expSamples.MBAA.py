import functions_CBC as ifxn
import pandas as pd
from sys import platform
from os import path, system
import numpy as np

import warnings

with warnings.catch_warnings():
	warnings.simplefilter("ignore")

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

# Open file
def obtain_data(file,sname='',base_dir=reference_study):
	try:
		out =pd.read_excel(path.join(base_dir,file+'.xlsx'),sheet_name=sname)
	except:
		out = pd.read_csv(path.join(base_dir,file+'.txt'),sep='\t')
	return out

# Get ImmPort Template headers
def grab_headers(file,base_dir=immport_templates):
	return pd.read_excel(path.join(base_dir,file+'.xlsx'),header=None).iloc[[2]].values.flatten().tolist()

def grab_top(file,base_dir=immport_templates):
	return pd.read_excel(path.join(base_dir,file+'.xlsx'),header=None).iloc[[0,1]]

def get_assay(file, assay_list):
	return(file[file['Assay ID'].isin(assay_list)])

def build_MBAA(*files):
	MBAA = pd.DataFrame()
	for f in files:
		try:
			MBAA = pd.concat([MBAA, get_assay(f,total_ids)])
		except:
			pass

	return(MBAA)

MBAA_IDs = [
'27_504',
'27_505',
'32_040'
]


total_ids = MBAA_IDs

CBC_assay_data = obtain_data('testing_data_1.1.0','Primary_Testing_Resutls( CBC)')
FNL_assay_data = obtain_data('testing_data_1.1.0','Secondary_Testing_Results(FNL)')
IDK_assay_data = obtain_data('testing_data_1.1.0','Tertitary_Testing_Results')
assay_data = obtain_data('assay_data_1.0.0','Assay_Metadata')
assay_data = assay_data.replace(np.nan, 'aaa', regex=True)
# print(assay_data['Assay_Target_Sub_Region'])

def get_set_data(data, column, group_index):
	OUT = data.groupby(group_index, dropna=False)[column].apply(','.join).reset_index()
	OUT[column] = [','.join(list(set(x.split(',')))) for x in OUT[column]]
	OUT[column] = [x.strip() for x in OUT[column]]
	OUT[column] = OUT[column].replace('aaa', np.nan, regex=True)
	return(dict(zip(OUT[group_index], OUT[column])))


MAT = get_set_data(assay_data,'Measurand_Antibody_Type','# Assay_ID')
ATSB = get_set_data(assay_data,'Assay_Target_Sub_Region','# Assay_ID')
ART = get_set_data(assay_data,'Assay_Result_Type','# Assay_ID')
ARU = get_set_data(assay_data,'Assay_Result_Unit','# Assay_ID')

biosample_data = obtain_data('refr_bioSample',base_dir=final_ref)


# reset_bio = biosample_data.iloc[1:,:]
# reset_bio = reset_bio.rename(columns=reset_bio.iloc[0]).drop(reset_bio.index[0]).reset_index(drop=True)

bioIdMap=dict(zip(biosample_data['Subject ID'], biosample_data['User Defined ID'])) # This connects User ID to  biosample ID


three_tests = build_MBAA(CBC_assay_data,FNL_assay_data,IDK_assay_data)
three_tests = three_tests.reset_index(drop=True)
# for i in range(len(three_tests)):
# 	print(three_tests.iloc[[i]])
# comp_type in ['symptomatic']

LEN = len(three_tests['Assay ID'])
BLANKS = ['']*LEN

TOP = grab_top('experimentSamples.MBAA')
# print(TOP)
OUT = pd.DataFrame(columns=grab_headers('experimentSamples.MBAA'))
OUT['Column Name']=BLANKS
OUT['Expsample ID']=[f'refr-assay-{str(x)}' for x in range(LEN)]
OUT['Biosample ID']=[bioIdMap.get(x) for x in three_tests['Research_Participant_ID']]
OUT['Experiment ID']=three_tests['Assay ID']
OUT['Reagent ID(s)']=BLANKS
OUT['Treatment ID(s)']=BLANKS
OUT['Expsample Name']=BLANKS
OUT['Expsample Description']=BLANKS
OUT['Additional Result File Names']=BLANKS
OUT['Study ID']=['Reference_Study']*LEN
OUT['Protocol ID(s)']=['refr_Protocol']*LEN
OUT['Subject ID']=three_tests['Research_Participant_ID']
OUT['Planned Visit ID']=['refr-planned_visit-01']*LEN
OUT['Type'] = BLANKS #
OUT['Subtype']=BLANKS #[ATSB.get(x) for x in three_tests['Assay ID']]
OUT['Biosample Name']=BLANKS
OUT['Biosample Description']=BLANKS
OUT['Study Time Collected']=BLANKS
OUT['Study Time Collected Unit']=BLANKS
OUT['Study Time T0 Event']=BLANKS
OUT['Study Time T0 Event Specify']=BLANKS
OUT['Experiment Name']=BLANKS
OUT['Experiment Description']=BLANKS
OUT['Measurement Technique']=BLANKS
OUT['Result Separator Column']=BLANKS
OUT['Analyte Reported']=[MAT.get(x) for x in three_tests['Assay ID']]
OUT['Value Reported']=three_tests ['Derived_Result']
OUT['Unit Reported']=three_tests ['Derived_Result_Units']
OUT['Comments']=BLANKS

# print(type(grab_headers('experimentSamples.MBAA')))
headers = grab_headers('experimentSamples.MBAA')
np_TOP = np.append(TOP.to_numpy(), headers)
np_template = np.append(np_TOP,OUT.to_numpy())

rows = int(len(np_template)/len(headers))
col = int(len(headers))
np_template = np.reshape(np_template,(rows, col))
immport_template=pd.DataFrame(np_template, columns=None)
immport_template.to_csv(path.join(final_ref,'refr_experimentSamples.MBAA.txt'),
	header=False, index=False, sep='\t')
# print(OUT['Unit Reported'][0])

# NEED TO GET DATA FOR OTHER TYPES OF EXPERIMENTS 


