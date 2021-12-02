import pandas as pd
import numpy as np
import datetime
import dateutil.tz
from glob import glob
# import args 
import os 
import re

import warnings
# warnings.simplefilter("ignore")

file_sep = os.path.sep
eastern = dateutil.tz.gettz("US/Eastern")
validation_date = datetime.datetime.now(tz=eastern).strftime("%Y-%m-%d")

os.getlogin()
user_dir = os.getcwd()

## ========================= excel doc ===================== ##
jenns_file = pd.read_excel("new_paper_1.xlsx")
master_list = pd.read_excel("Master-List-copy.xlsx")
gov_df = pd.read_excel('gov_side.xlsx', 'Full Publication List')

file_sep = os.path.sep
box_dir = file_sep + 'Users' + file_sep + os.getlogin() + file_sep + 'Box'
sero_net = box_dir + file_sep + 'SeroNet Public Data' 

## ========================= functions ===================== ##
# Finding new papers 
def new_paper_list(gov, master):
    new_papers_PMID = list(set(gov.PMID)- set(master.PMID))
    return(gov[gov['PMID'].isin(new_papers_PMID)])

# Find repeated things in 2 lists (intersection)
def find_repeat(list1, list2):
    return(set(list1).intersection(set(list2)))

# Getting PI names from BOX 
def get_PI_name(jenn, master):
    pi = []
    grant_number = [e[3:] for e in jenn.Base_Project]
    for i in grant_number:
        name = glob(sero_net + file_sep + i + '*')[0].split('_')[1]
        matching = [s for s in np.unique(master.PI) if name.lower() in s.lower()]
        pi.append(matching[0])
    return(pi)

# Changing to correct format to merge to master list 
#changing to correct format to merge to master list 
def to_master_format(new_papers, master):
    data_dic = {}
    empty = ['']*len(new_papers.PubMed_ID)
    updating_fields = {
        'Base_Project':list(new_papers['Base_Project']),
        'Base_Project.1':[e[3:] for e in new_papers.Base_Project], 
        'PMID':list(new_papers['PubMed_ID']), 
        'Folder name':list(['PMID_'+str(e) for e in new_papers.PubMed_ID]),
        'PubMed_ID link':list(new_papers['PubMed_ID']),
        'Publication_Title':list(new_papers['Publication_Title']), 
        'Journal':list(new_papers['Journal']),
        'Author(s)':list(new_papers['Author(s)']),
        'Pub Date':list(new_papers['Pub Date']),
        'PI':get_PI_name(new_papers, master_list)
    }

    for col_name in master_list.columns:
        if (col_name in updating_fields.keys()):
            data_dic[col_name] = updating_fields[col_name]
        else:
            data_dic[col_name] = empty

    return(pd.DataFrame(data_dic))

# Finding repteate in the two lists 
def repeates(list1, list2):
    return(set(list1).intersection(set(list2)))

## ========================= main ===================== ##
if __name__ == '__main__':
	# finding new papers 
	new_papers = new_paper_list(gov_df, master_list)
	# creating df to concat to master list
	add_on = to_master_format(new_papers, master_list)
	new_master_list = pd.concat([master_list, add_on])
	new_master_list = new_master_list.replace(np.nan, '', regex=True).reset_index(drop=True)
	new_master_list.head()

	print(len(add_on.PMID))
	print(new_master_list)
	new_master_list.to_excel('~/Desktop/temp.xlsx', nindex=False)