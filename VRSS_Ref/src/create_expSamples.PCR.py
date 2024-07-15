import functions_CBC as ifxn
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

################# Organization #################


################# Pull Data #################
PCR_data = cbcFxn.obtain_data('Prior_PCR_Testing_2.0.0','PCR_Test_Data')
#assay_data = cbcFxn.obtain_data('assay_data_2.0.0','Assay_Metadata')
#assay_data = assay_data.replace(np.nan, 'aaa', regex=True)
# print(assay_data['Assay_Target_Sub_Region'])

# biosample_data = cbcFxn.obtain_data('refr_bioSample',base_dir=final_ref)

# reset_bio = biosample_data.iloc[1:,:]
# reset_bio = reset_bio.rename(columns=reset_bio.iloc[0]).drop(reset_bio.index[0]).reset_index(drop=True)


################# Build Data Frame #################
# # subject_id = [x.strip() for x in PCR_data['Subject ID']]
# bioid = [x.strip() for x in PCR_data['# Research_Participant_ID']]
# bioIdMap=dict(zip(subject_id, bioid)) # This connects User ID to  biosample ID


# PCR_data = cbcFxn.build_ELISA(PCR_data,FNL_assay_data,IDK_assay_data, ids=total_ids)
# PCR_data = PCR_data.reset_index(drop=True)
# PCR_data.to_csv("./3est.csv")

# Getting Derived Resul
# derived_result = []
# for x in PCR_data['Derived_Result']:

#     if pd.isnull(x):
#         derived_result.append('NA') 
#     else:
#         derived_result.append(x)

# derived_result_unit = []
# for x in PCR_data['Derived_Result_Units']:
#     if pd.isnull(x):
#         derived_result_unit.append('Not Specified') 
#     else:
#         derived_result_unit.append(x)
# print(PCR_data.columns)
LEN = len(PCR_data['# Research_Participant_ID'])
BLANKS = ['']*LEN

# print(TOP)
OUT = pd.DataFrame(columns=cbcFxn.grab_headers('experimentSamples.ELISA'))
OUT['Column Name']=BLANKS
OUT['Expsample ID']=[f'refr-pcr-{str(x)}' for x in range(LEN)]#[f'refr-PCR-{str(x)}' for x in range(LEN)]
OUT['Biosample ID']=['PCR-bio']*LEN #Do all these need to be different per person?
OUT['Experiment ID']=[f'{x}-PCR' for x in PCR_data['# Research_Participant_ID']]
OUT['Reagent ID(s)']=['refr-no_reagents']*LEN
OUT['Treatment ID(s)']=['refr-no_treatments']*LEN
OUT['Expsample Name']=BLANKS
OUT['Expsample Description']=BLANKS
OUT['Additional Result File Names']=BLANKS
OUT['Study ID']=['SeroNet_Reference_Study']*LEN #['SeroNet_Reference_Study']*LEN
OUT['Protocol ID(s)']=['refr_Protocol']*LEN
OUT['Subject ID']=PCR_data['# Research_Participant_ID']
OUT['Planned Visit ID']=['SeroNet_Reference_Study_visit-01']*LEN
OUT['Type'] = ['Nasal Swab']*LEN #
OUT['Subtype']=BLANKS #[ATSB.get(x) for x in PCR_data['Assay ID']]
OUT['Biosample Name']=['Nasal Swab']*LEN
OUT['Biosample Description']=BLANKS
OUT['Study Time Collected']=['0']*LEN
OUT['Study Time Collected Unit']=['Days']*LEN
OUT['Study Time T0 Event']=['Other']*LEN
OUT['Study Time T0 Event Specify']=['Result recorded at enrollment']*LEN
OUT['Experiment Name']=['Prior visit PCR test']*LEN
OUT['Experiment Description']=BLANKS
OUT['Measurement Technique']=['PCR']*LEN
OUT['Result Separator Column']=BLANKS
OUT['Analyte Reported']=['SARS-CoV-2 spike or mucleocapsid']*LEN
OUT['Value Reported']=PCR_data['Test_Result']
OUT['Unit Reported']=['Positive | Negative']*LEN
OUT['Comments']=PCR_data['Test_Result_Provenance']

print(OUT)

cbcFxn.create_final(OUT,'experimentSamples.ELISA', 'refr_experimentSamples.PCR.txt')



