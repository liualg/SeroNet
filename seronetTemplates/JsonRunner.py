import pandas as pd
import seronetFunctions as serofxn
import JSONparse_template as pt
import json
from glob import glob
import os
from tqdm import tqdm

box_dir = '/Users/liualg/Library/CloudStorage/Box-Box/SeroNet Public Data'
out_dir = './archive/JSON/'
file_type = 'json'
PMID_LIST = [
    35180044, 35390296, 34368647, 35284808, 35483404, 34546094, 34250518, 34320281, 35085183, 35704428, 35756977, 34150933, 35839768, 35081612, 34383889, 36058184, 35576468, 34308390, 35881010, 35881005
]

#need to run later [35932763, 35090596, 33688034,35061630 ]


for PMID in PMID_LIST:
    PMID = str(PMID)
    print(PMID)
    
    BASE_DIR = serofxn.get_box_dir(box_dir, PMID)
    df_path = glob(os.path.join(BASE_DIR,'templated_data',f'PMID{PMID}*.xlsm'))[0]

    output_file = os.path.join(out_dir, f'PMID{PMID}_JSON.{file_type}')
    df = pd.read_excel(df_path, sheet_name = 0, header=None)
    df.index += 1
    template = {}
    pt.parse_registry_template(df, template)

    f = open(output_file, "w")
    print(json.dumps(template, indent=4), file = f)
    f.close()