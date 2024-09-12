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

vacc_data = cbcFxn.obtain_data('Vaccination_Data_4.0.0','Detailed_Report',data_path)

## Clean up the data bit  ##
# remove all the 'Unvaccinated' from Vaccination_Status
clean_data = vacc_data[vacc_data['Vaccination_Status'] != 'Unvaccinated'].reset_index()

# combine Vaccination_Status + : + SARS-CoV-2_Vaccine_Type
clean_data['compound_name_reported'] = clean_data['Vaccination_Status']+ [' : ']*len(clean_data['SARS-CoV-2_Vaccine_Type']) + clean_data['SARS-CoV-2_Vaccine_Type']

###############

LEN = len(clean_data['Research_Participant_ID'])
BLANKS = ['']*LEN

OUT = pd.DataFrame(columns=cbcFxn.grab_headers('interventions'))
OUT['Column Name']=BLANKS
OUT['User Defined ID']=[f'vrss_interventions-{x}' for x in range(LEN)]
OUT['Subject ID']=clean_data['Research_Participant_ID']
OUT['Study ID']=['SeroNet-VRSS']*LEN
OUT['Name Reported']=clean_data['SARS-CoV-2_Vaccine_Type'] # This needs to be updated to have the correct thing 
OUT['Compound Name Reported']=clean_data['compound_name_reported']
OUT['Compound Role']=['Intervention']*LEN
OUT['Dose Reported']=clean_data['Vaccination_Status']
OUT['Start Day']=[str(x)[:-9] for x in clean_data['Date of Vaccination']] #removing the 00:00:00 from date
OUT['End Day']=[str(x)[:-9] for x in clean_data['Date_Of_Blood_Draw']] #removing the 00:00:00 from date
OUT['Status']=['Duration btwn vacc rcvd and blood draw']*LEN
OUT['Reported Indication']=BLANKS
OUT['Formulation']=BLANKS
OUT['Dose']=BLANKS
OUT['Dose Units']=BLANKS
OUT['Dose Freq Per Interval']=BLANKS
OUT['Route Of Admin Reported']= [' ']*LEN
OUT['Is Ongoing']=BLANKS
OUT['Start Time']=BLANKS
OUT['End Time']=BLANKS
OUT['Duration']=clean_data['Duration_Between_Vaccine_and_Visit']
OUT['Duration Unit']=['Days']*LEN

OUT.replace(' 00:00:00', '')
cbcFxn.create_final(OUT,'interventions',path.join(out_path,'vrss_interventions.txt'))
cbcFxn.create_final(OUT.drop_duplicates(),'interventions',path.join(out_path,'vrss_interventions-nodup.txt'))

