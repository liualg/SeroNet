import functions_CBC as cbcFxn
import pandas as pd
from sys import platform
from os import path, system
import numpy as np
import cbc_functions as cbcFxn

import warnings

with warnings.catch_warnings():
	warnings.simplefilter("ignore")

if platform == "darwin":
    system('clear')
else:
    system('cls')

################# Set Paths #################


base_path='/Users/liualg/Documents/GitHub/SeroNet/VRSS_Ref'
data_path=path.join(base_path,'data')
immport_templates='/Users/liualg/Documents/GitHub/SeroNet/seronetTemplates/template/v.50/ImmPortTemplates.6661.2023-12-04.11-24-40/excel-templates'

map_folder = path.join(base_path,'mapping')
reference_study = path.join(data_path,'reff')
vrss_study = path.join(data_path,'vrss')
final_ref = path.join(base_path,'final')
final_txt = path.join(base_path,'final','_final')

################# Organization #################

Multiplex = [
'27_504', '27_505', '32_040'
]

lat_flow_IDs = [
'27_508'
]

total_ids = Multiplex + lat_flow_IDs

################# Pull Data #################
serology_data = cbcFxn.obtain_data('serology_results_data_2.0.0','Raw Data')

assay_data = serology_data
# assay_data = serology_data.replace(np.nan, 'aaa', regex=True)
# print(assay_data['Assay_Target_Sub_Region'])
experiment_data = cbcFxn.obtain_data('refr-experiments-v2',base_dir=final_txt)

reset_exp = experiment_data.iloc[1:,:]
reset_exp = reset_exp.rename(columns=reset_exp.iloc[0]).drop(reset_exp.index[0]).reset_index(drop=True)
ID_name_dict = dict(zip(reset_exp['User Defined ID'],reset_exp['Name']))
ID_nameNorm_dict = dict(zip(reset_exp['User Defined ID'],reset_exp['Measurement Technique']))
ID_nameNorm_des = dict(zip(reset_exp['User Defined ID'],reset_exp['Description']))

biosample_data = cbcFxn.obtain_data('refr_bioSample',base_dir=final_txt)

reset_bio = biosample_data.iloc[1:,:]
reset_bio = reset_bio.rename(columns=reset_bio.iloc[0]).drop(reset_bio.index[0]).reset_index(drop=True)


################# Build Data Frame #################
subject_id = [x.strip() for x in reset_bio['Subject ID']]
bioid = [x.strip() for x in reset_bio['User Defined ID']]
bioIdMap=dict(zip(subject_id, bioid)) # This connects User ID to  biosample ID


assay_data = assay_data[assay_data['Assay_ID'].isin(total_ids)]


# Getting Derived Resul
derived_result = []
for x in assay_data['Derived_Result']:

    if pd.isnull(x):
        derived_result.append('NA') 
    else:
        derived_result.append(x)

derived_result_unit = []
for x in assay_data['Derived_Result_Units']:
    if pd.isnull(x):
        derived_result_unit.append('Not Specified') 
    else:
        derived_result_unit.append(x)

print(assay_data['Assay_ID'])

LEN = len(assay_data['Assay_ID'])
BLANKS = ['']*LEN

# print(TOP)
OUT = pd.DataFrame(columns=cbcFxn.grab_headers('experimentSamples.ELISA'))
OUT['Column Name']=BLANKS
OUT['Expsample ID']=[f'refr-multi_lat-{str(x)}' for x in range(LEN)]
OUT['Biosample ID']=[bioIdMap.get(x) for x in assay_data['# Research_Participant_ID']]
OUT['Experiment ID']=[x for x in assay_data['Assay_ID']]
OUT['Reagent ID(s)']=['refr-no_reagents']*LEN
OUT['Treatment ID(s)']=['refr-no_treatments']*LEN
OUT['Expsample Name']=BLANKS
OUT['Expsample Description']=BLANKS
OUT['Additional Result File Names']=BLANKS
OUT['Study ID']=['SeroNet_Reference_Study']*LEN
OUT['Protocol ID(s)']=['refr_Protocol']*LEN
OUT['Subject ID']=assay_data['# Research_Participant_ID']
OUT['Planned Visit ID']=['SeroNet_Reference_Study_visit-01']*LEN
OUT['Type'] = BLANKS #
OUT['Subtype']=BLANKS #[ATSB.get(x) for x in assay_data['Assay_ID']]
OUT['Biosample Name']=BLANKS
OUT['Biosample Description']=BLANKS
OUT['Study Time Collected']=BLANKS
OUT['Study Time Collected Unit']=BLANKS
OUT['Study Time T0 Event']=BLANKS
OUT['Study Time T0 Event Specify']=BLANKS
OUT['Experiment Name']=[ID_name_dict.get(x) for x in assay_data['Assay_ID']]
OUT['Experiment Description']=[ID_nameNorm_des.get(x) for x in assay_data['Assay_ID']]
OUT['Measurement Technique']=[ID_nameNorm_dict.get(x) for x in assay_data['Assay_ID']]
OUT['Result Separator Column']=BLANKS
OUT['Analyte Reported']=[x for x in assay_data['Measurand_Antibody']]
OUT['Value Reported']=derived_result
OUT['Unit Reported']=derived_result_unit
OUT['Comments']=assay_data['Interperation Group']


cbcFxn.create_final(OUT,'experimentSamples.ELISA', 'refr_experimentSamples.MPLF.txt')



