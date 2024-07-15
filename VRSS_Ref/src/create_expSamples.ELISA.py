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

################# Organization #################

elisa_IDs = [
'12_101', '12_102', '12_103', '12_104', '14_010', '14_090', 
'27_502', '27_503', '27_511', '32_060', '32_065', '32_070', 
'32_075', '41_486'
]

chemi_IDS = [
'14_020', '14_050', '14_070', '14_080', '27_501', '27_506',
'27_507', '27_509', '27_510', '32_035', '32_047', '41_476',
'32_048', '41_468', '41_470', '41_472', '41_474', '41_488',
'41_481', '41_483', '41_485', '41_487'
]

lat_flow_IDs=['27_508']

total_ids = elisa_IDs + chemi_IDS + lat_flow_IDs

################# Pull Data #################
CBC_assay_data = cbcFxn.obtain_data('testing_data_2.0.0','Primary_Testing_Resutls( CBC)')
FNL_assay_data = cbcFxn.obtain_data('testing_data_2.0.0','Secondary_Testing_Results(FNL)')
IDK_assay_data = cbcFxn.obtain_data('testing_data_2.0.0','Tertitary_Testing_Results')
assay_data = cbcFxn.obtain_data('assay_data_2.0.0','Assay_Metadata')
assay_data = assay_data.replace(np.nan, 'aaa', regex=True)
# print(assay_data['Assay_Target_Sub_Region'])


MAT = cbcFxn.get_set_data(assay_data,'Measurand_Antibody_Type','# Assay_ID')
ATSB = cbcFxn.get_set_data(assay_data,'Assay_Target_Sub_Region','# Assay_ID')
ART = cbcFxn.get_set_data(assay_data,'Assay_Result_Type','# Assay_ID')
ARU = cbcFxn.get_set_data(assay_data,'Assay_Result_Unit','# Assay_ID')

biosample_data = cbcFxn.obtain_data('refr_bioSample',base_dir=final_ref)

reset_bio = biosample_data.iloc[1:,:]
reset_bio = reset_bio.rename(columns=reset_bio.iloc[0]).drop(reset_bio.index[0]).reset_index(drop=True)


################# Build Data Frame #################
subject_id = [x.strip() for x in reset_bio['Subject ID']]
bioid = [x.strip() for x in reset_bio['User Defined ID']]
bioIdMap=dict(zip(subject_id, bioid)) # This connects User ID to  biosample ID


three_tests = cbcFxn.build_subset(CBC_assay_data,FNL_assay_data,IDK_assay_data, ids=total_ids)
three_tests = three_tests.reset_index(drop=True)
three_tests.to_csv("./3est.csv")

# Getting Derived Resul
derived_result = []
for x in three_tests['Derived_Result']:

    if pd.isnull(x):
        derived_result.append('NA') 
    else:
        derived_result.append(x)

derived_result_unit = []
for x in three_tests['Derived_Result_Units']:
    if pd.isnull(x):
        derived_result_unit.append('Not Specified') 
    else:
        derived_result_unit.append(x)
# print(three_tests.columns)
LEN = len(three_tests['Assay ID'])
BLANKS = ['']*LEN

# print(TOP)
OUT = pd.DataFrame(columns=cbcFxn.grab_headers('experimentSamples.ELISA'))
OUT['Column Name']=BLANKS
OUT['Expsample ID']=[f'refr-assay-{str(x)}' for x in range(LEN)]
OUT['Biosample ID']=[bioIdMap.get(x) for x in three_tests['Research_Participant_ID']]
OUT['Experiment ID']=three_tests['Assay ID']
OUT['Reagent ID(s)']=['refr-no_reagents']*LEN
OUT['Treatment ID(s)']=['refr-no_treatments']*LEN
OUT['Expsample Name']=BLANKS
OUT['Expsample Description']=BLANKS
OUT['Additional Result File Names']=BLANKS
OUT['Study ID']=['SeroNet_Reference_Study']*LEN
OUT['Protocol ID(s)']=['refr_Protocol']*LEN
OUT['Subject ID']=three_tests['Research_Participant_ID']
OUT['Planned Visit ID']=['SeroNet_Reference_Study_visit-01']*LEN
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
OUT['Value Reported']=derived_result
OUT['Unit Reported']=derived_result_unit
OUT['Comments']=three_tests['Interpretation']


cbcFxn.create_final(OUT,'experimentSamples.ELISA', 'refr_experimentSamples.ELISA.txt')



