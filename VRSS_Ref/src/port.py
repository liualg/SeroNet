import functions_CBC as ifxn
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


# Open file
def obtain_data(file,sname,base_dir=reference_study):
	return pd.read_excel(path.join(base_dir,file+'.xlsx'),sheet_name=sname)

#def get_col_data(file_name,sheet_name)



def parse_dict(tmap):
	s = tmap.split(':')
	s_file=s[0].split('/')[0].strip() # FILE NAME
	s_sheet=s[0].split('/')[1].strip() # SHEET(s) NAME
	if '^' not in tmap:
		s_header=s[1].replace('^','').strip()
	else:
		s_header=s[1].split('^')[0].split('>')[0].replace('*','').strip()

	d_file = obtain_data(file=s_file,sname=s_sheet)

	return d_file[s_header]


def get_subject_id(col):
	temp = col.split('_')
	return ''.join(temp[0],temp[1])

def get_condition(tmap):
	s = tmap.split(':')[1]
	if '^' not in tmap:
		s_header=s[1].replace('^','').strip()
	else:
		p = s.split('^')
		p10 = p[0].split('>')[0].strip()
		p11 = p[0].split('>')[1].strip()
		p20 = p[1].split('>')[0].strip()
		p21 = p[1].split('>')[1].strip()

	return p10, p11, p20, p21

# Create dict of 2 columns
def make_dict(Qcolumn, file):
	temp = pd.read_csv(path.join(map_folder,file))
	c1 = temp.columns.get_loc(Qcolumn)
	
	return dict(zip(temp.iloc[:,c1], temp.iloc[:,c1+1]))

## SeroNet Things ## 
def grab_headers(file,base_dir=immport_templates):
	return pd.read_excel(path.join(base_dir,file+'.xlsx'),header=None).iloc[[2]].values.flatten().tolist()

# Reformat into ImmPort Templates 
def create_template(nextRows,file_name,base_dir=immport_templates):
	dfin = pd.read_excel(path.join(base_dir,file_name+'.xlsx'),header=None)

	nextRows.loc[0] = dfin.iloc[[0]].values.flatten().tolist()
	nextRows.loc[1] = dfin.iloc[[1]].values.flatten().tolist()
	nextRows.loc[2] = nextRows.columns.values.flatten().tolist()
	nextRows.columns = range(nextRows.shape[1])

	return nextRows

def get_ids_onCondition(ref_df):
	con1,con1_test,con2,con2_test = get_condition(ref_df)
	s = ref_df.split(':')
	s_file=s[0].split('/')[0].strip() 
	s_sheet=s[0].split('/')[1].strip()
	df = obtain_data(s_file, s_sheet)
	print(con2,con2_test)
	print(np.where(df[con1]==con2))
	fdf = np.where((df[con1]==con1_test) & (df[con2]==con2_test))
	if not fdf:
		out = np.nan
	else:
		out = df.loc[fdf]['# Research_Participant_ID'].values.flatten().tolist()

	# ids = df['# Research_Participant_ID'][df[con1]==con1_test & df[con2]==con2_test]
	return out

def match_(field):
	if field == 

## Reference Study Data ##
# testing
testing_data_CBC = obtain_data(file='testing_data_1.0.0',sname='Primary_Testing_Resutls( CBC)')
testing_data_FNL = obtain_data(file='testing_data_1.0.0',sname='Secondary_Testing_Results(FNL)')
testing_data_FNL = obtain_data(file='testing_data_1.0.0',sname='Tertitary_Testing_Results')
# symptom data
symptomatic_data = obtain_data(file='symptomatic_data_1.0.0',sname='Symptom Data')
# demographics
demographics_data = obtain_data(file='demographics_1.0.0',sname='Demographic_Data')
# comorbidity_or_infections
comorbidity_data = obtain_data(file='comorbidity_or_infections_1.0.0',sname='Comorbidity_Data')
infection_data = obtain_data(file='comorbidity_or_infections_1.0.0',sname='Infection_Data')
# biospecimen
serum_data = obtain_data(file='biospecimen_data_1.0.0',sname='Serum')
PMBC_data = obtain_data(file='biospecimen_data_1.0.0',sname='PBMC')
# assay
assay_data = obtain_data(file='assay_data_1.0.0',sname='Assay_Metadata')

## External Mapping to keep code cleaner
immportFile='subjectHumans'
h=grab_headers(immportFile)

d_file = demographics_data
ref_map = make_dict('subject','reference-map.csv')
temp = pd.DataFrame(columns=h)
# print(temp)
matcher=[]
for c in h:
	test = ref_map.get(c)
	if not pd.isnull(test):
		if '^' in test:
			matcher.append((c,test))

		elif ':' in test:
			if '*' in test:
				add = parse_dict(test)
			else:
				add = parse_dict(test)

		elif '-' in test:
			s1 = test.split('-')[1].strip()
			add = [s1]*len(d_file)

		elif 'code' in test:
			add = match_(c)
		else:
			add=['']*len(d_file)

	else:
		add=['']*len(d_file)

#	print(c,len(add))
	temp[c] = add
#print(temp)
out= create_template(nextRows=temp, file_name=immportFile)
# print(temp.shape)
print(out)
# if matcher:
# 	for i in range(len(matcher)):
# 		print(matcher[i][1])
# 		matchings_ids = get_ids_onCondition(matcher[i][1])
# 		print(matchings_ids)
# 		if not matchings_ids:
# 			print('is empty')
# 			pass
# 		else:
# 			print('adding to data frame')
	
# 	if '|' in sheet_name:
# 		sheet_name = s_sheet.split('|')
# 	else:
# 		sheet_name = [s_sheet]

