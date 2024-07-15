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
serum_data = cbcFxn.obtain_data('biospecimen_data_2.0.0','Serum')
pbmc_data = cbcFxn.obtain_data('biospecimen_data_2.0.0','PBMC')


from itertools import chain
def flatten_chain(matrix):
	return list(chain.from_iterable(matrix))

combine_IDs = flatten_chain([serum_data['# Biospecimen_ID'], pbmc_data['# Biospecimen_ID']])
combine_type= flatten_chain([['Serum']*len(serum_data['# Biospecimen_ID']), ['PBMC']*len(pbmc_data['# Biospecimen_ID'])])
combine_years=flatten_chain([serum_data['Biospecimen_Collection_Year'], pbmc_data['Biospecimen_Collection_Year']])

LEN = len(combine_IDs)
BLANKS = ['']*LEN

OUT = pd.DataFrame(columns=cbcFxn.grab_headers('bioSamples'))
OUT['Column Name']=BLANKS
OUT['User Defined ID']=combine_IDs
OUT['Type']=combine_type
OUT['Subtype']=BLANKS
OUT['Name']=BLANKS
OUT['Description']=BLANKS
OUT['Subject ID']=[x[:-4] for x in combine_IDs]
OUT['Study ID']=['SeroNet_Reference_Study']*LEN
OUT['Planned Visit ID']=['SeroNet_Reference_Study_visit-01']*LEN
OUT['Treatment ID(s)']=BLANKS
OUT['Study Time Collected']=combine_years
OUT['Study Time Collected Unit']=['Years']*LEN
OUT['Study Time T0 Event']=['Time of enrollment']*LEN
OUT['Study Time T0 Event Specify']=BLANKS

cbcFxn.create_final(OUT,'bioSamples', 'refr_bioSample.txt')


