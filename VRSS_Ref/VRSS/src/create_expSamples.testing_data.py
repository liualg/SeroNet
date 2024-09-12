# import functions_CBC as cbcFxn
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


base_path='/Users/liualg/Documents/GitHub/SeroNet/VRSS_Ref/VRSS'
data_path=path.join(base_path,'data')
out_path=path.join(base_path,'xoutput')
immport_templates='/Users/liualg/Documents/GitHub/SeroNet/VRSS_Ref/xtemplates'


map_folder = path.join(base_path,'mapping')
reference_study = path.join(data_path,'reff')
vrss_study = path.join(data_path,'vrss')
final_ref = path.join(base_path,'final')

################# Organization #################


# lat_flow_IDs=['27_508']

total_ids = [
'27_502','27_503','41_488','12_102','14_020','41_483',
'32_048','14_010','32_047','41_481','12_101', '12_104',
'41_491','41_487','27_501','12_103']

################# Pull Data #################
biosample_testing_data = cbcFxn.obtain_data('Biospecimen_Test_Results_4.0.0','Biospecimen Test Results')
assay_data = cbcFxn.obtain_data('Assay_Data_4.0.0','Assay_MetaData')
assay_data = assay_data.replace(np.nan, 'aaa', regex=True)
# print(assay_data['Assay_Target_Sub_Region'])

biosample_data = cbcFxn.obtain_data('vrss_bioSample',base_dir=out_path)

reset_bio = biosample_data.iloc[1:,:]
reset_bio = reset_bio.rename(columns=reset_bio.iloc[0]).drop(reset_bio.index[0]).reset_index(drop=True)




################# Build Data Frame #################
subject_id = [x.strip() for x in reset_bio['Subject ID']]
bioid = [x.strip() for x in reset_bio['User Defined ID']]
bioIdMap=dict(zip(subject_id, bioid)) # This connects User ID to  biosample ID

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
OUT['Experiment Name']=[ID_name_dict.get(x) for x in three_tests['Assay ID']]
OUT['Experiment Description']=[ID_nameNorm_des.get(x) for x in three_tests['Assay ID']]
OUT['Measurement Technique']=[ID_nameNorm_dict.get(x) for x in three_tests['Assay ID']]
OUT['Result Separator Column']=BLANKS
OUT['Analyte Reported']=[MAT.get(x) for x in three_tests['Assay ID']]
OUT['Value Reported']=derived_result
OUT['Unit Reported']=derived_result_unit
OUT['Comments']=[f'Interpretation: {x}' for x in three_tests['Interpretation']]


cbcFxn.create_final(OUT,'experimentSamples.ELISA', 'refr_experimentSamples.testing_data.v3.txt')




