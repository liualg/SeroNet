import pandas as pd
from sys import platform
from os import path, system
import numpy as np

base_path='/Users/liualg/Documents/GitHub/SeroNet/VRSS_Ref'
data_path=path.join(base_path,'data')
immport_templates='/Users/liualg/Documents/GitHub/SeroNet/seronetTemplates/template/v.50/ImmPortTemplates.6661.2023-12-04.11-24-40/excel-templates'

map_folder = path.join(base_path,'mapping')
reference_study = path.join(data_path,'reff')
vrss_study = path.join(data_path,'vrss')

def grab_headers(file,base_dir=immport_templates):
	return pd.read_excel(path.join(base_dir,file+'.xlsx'),header=None).iloc[[2]].values.flatten().tolist()
