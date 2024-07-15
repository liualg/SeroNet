'''
Common Functions used in porting CBC data 


'''
import functions_CBC as ifxn
import pandas as pd
from sys import platform
from os import path, system
import numpy as np

## Paths ##

base_path='/Users/liualg/Documents/GitHub/SeroNet/VRSS_Ref'
data_path=path.join(base_path,'data')
immport_templates='/Users/liualg/Documents/GitHub/SeroNet/seronetTemplates/template/v.50/ImmPortTemplates.6661.2023-12-04.11-24-40/excel-templates'

map_folder = path.join(base_path,'mapping')
reference_study = path.join(data_path,'reff')
vrss_study = path.join(data_path,'vrss')
final_ref = path.join(base_path,'final','updates')



## FXNS XX

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

def build_subset(*files, ids):
	ELISA = pd.DataFrame()
	for f in files:
		try:
			ELISA = pd.concat([ELISA, get_assay(f,ids)])
		except:
			pass

	return(ELISA)

def clean_data(field):
	out =[]
	for x in field:
		if x == 'Native Hawaiian or Not Specified Pacific Islander':
			out.append('Native Hawaiian or Other Pacific Islander')
		elif x =='Unknown':
			out.append('Not Specified')
		elif x == 'Not Reported':
			out.append('Not Specified')
		elif x == 'Multirace':
			out.append('Multiracial')
		elif x == 'Other':
			out.append('Not Specified')
		else :
			out.append(x)
	return out

def get_set_data(data, column, group_index):
	OUT = data.groupby(group_index, dropna=False)[column].apply(','.join).reset_index()
	OUT[column] = [','.join(list(set(x.split(',')))) for x in OUT[column]]
	OUT[column] = [x.strip() for x in OUT[column]]
	OUT[column] = OUT[column].replace('aaa', np.nan, regex=True)
	return(dict(zip(OUT[group_index], OUT[column])))


def create_final(data, in_file, out_file):
	# print(type(grab_headers('experimentSamples.ELISA')))
	TOP = grab_top(in_file)
	headers = grab_headers(in_file)
	np_TOP = np.append(TOP.to_numpy(), headers)
	np_template = np.append(np_TOP,data.to_numpy())

	rows = int(len(np_template)/len(headers))
	col = int(len(headers))
	np_template = np.reshape(np_template,(rows, col))
	immport_template=pd.DataFrame(np_template, columns=None)
	immport_template.to_csv(path.join(final_ref,out_file),
		header=False, index=False, sep='\t')
