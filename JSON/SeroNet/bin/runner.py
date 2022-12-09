import os 
import shutil
from glob import glob 
import seronetFunctions as seroFxn
import pandas as pd 
from tqdm import tqdm

data_release = 'DR46'

one_drive = '/Users/liualg/Library/CloudStorage/OneDrive-SharedLibraries-NationalInstitutesofHealth/NCI-FNL SeroNet Team - Curation channel/ImmPort Uploads/'
immport_uploads = os.path.join(one_drive,f'Immport-{data_release}*.xlsx')
PMIDS = pd.read_excel(glob(immport_uploads)[0], sheet_name = 'November - Deadline').iloc[1:, 1]



def create_json(PMIDS_INPUTS):

	# for pmid in tqdm(PMIDS):
	for pmid in PMIDS:
		pmid = str(pmid).strip()
		print(pmid)
		try:
			box_dir = os.path.join('~','Library','CloudStorage','Box-Box','SeroNet Public Data')
			grant_dir = seroFxn.get_box_dir(box_dir, pmid)
			input_file = glob(os.path.join(grant_dir, 'templated_data','PMID*.xlsm'))[0]
			file_name = os.path.basename(input_file)

			shutil.copy(input_file, os.path.join('..','SampleTemplates'))


			output_file = f'../SampleJson/{pmid}_test.orig'



			os.system(f"python parseRegistryTemplate.py --excel_file ../SampleTemplates/{file_name} --output_file {output_file}")
		except:
			print(f"{pmid} no idea")

create_json(PMIDS)

print("##### adding new PMIDS #####")
PMIDS = pd.read_excel(glob(immport_uploads)[0], sheet_name = 'Retro - Add data').iloc[1:, 1]
create_json(PMIDS)