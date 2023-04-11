import pandas as pd
import seronetFunctions as serofxn
import JSONparse_template as pt
import json
from glob import glob
import os
from tqdm import tqdm

box_dir = '/Users/liualg/Library/CloudStorage/Box-Box/SeroNet Public Data'
out_dir = './archive/DR48-JSON'
file_type = 'json'
PMID_LIST = [
    35289637, 35040666, 34523968, 33704352, 35504289, 35427477, 35148837, 
    35013325, 35025672, 35455241, 34250512, 35348368, 34107529, 35143473, 
    35589681, 35764643, 34001652, 35129576, 35756977, 34260834, 34095338, 
    33276369, 33408181, 34877479, 34794169, 33142304, 33622794, 34835131,
    33479118, 34921308, 34687893, 34086877, 33065030, 33830946, 33993265, 
    35132398, 34161961, 33846272, 33666169, 34759001, 34452006, 34003112, 
    33472939, 34130883, 34652783, 33440148, 33035201, 34910927, 33961839, 
    34696403, 34353890, 33743211, 34151306, 33521695, 34802457, 33169014, 
    34145263, 33478949, 33571162, 34730254, 34937699, 33160316, 33602725, 
    33727353, 34150933, 34250518, 34308390, 34320281, 34368647, 34383889,
    34546094, 35081612, 35085183, 35180044, 35284808, 35390296, 35483404,
    35576468, 35704428, 35756977, 35839768, 35881005, 35881010, 33688034,
    33915337, 34047304, 34253053, 34706273, 35932763, 35090596, 35061630, 
    35092678, 35289114, 35632708, 35795812, 35877413, 35915094, 36058184, 34952892
]
# PMID_LIST = [33479118, 33035201]
print(len(PMID_LIST))

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