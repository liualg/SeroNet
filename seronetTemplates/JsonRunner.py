import pandas as pd
import seronetFunctions as serofxn
import JSONparse_template as pt
import json
from glob import glob
import os
from tqdm import tqdm
import shutil

box_dir = '/Users/liualg/Library/CloudStorage/Box-Box/SeroNet Curation/SeroNet Public Data'
out_dir = './archive/JSON/'
file_type = 'json'
PMID_LIST = [
    34664987
]

#need to run later [35932763, 35090596, 33688034,35061630 ]


for PMID in PMID_LIST:
    PMID = str(PMID)
    print(PMID)
    file_output_name = f'PMID{PMID}_JSON.{file_type}'
    
    BASE_DIR = serofxn.get_box_dir(box_dir, PMID)
    df_path = glob(os.path.join(BASE_DIR,'templated_data',f'PMID{PMID}*.xlsm'))[0]

    output_file = os.path.join(BASE_DIR, 'ImmPort_templates_DR49', file_output_name)
    df = pd.read_excel(df_path, sheet_name = 0, header=None)
    df.index += 1
    template = {}
    pt.parse_registry_template(df, template)

    f = open(output_file, "w")
    print(json.dumps(template, indent=4), file = f)
    f.close()

    shutil.copyfile(output_file, os.path.join('/Users/liualg/Library/CloudStorage/OneDrive-NationalInstitutesofHealth/Curation channel/ImmPort Uploads/Data Release Updates_/DR49/JSON-updates/',file_output_name))