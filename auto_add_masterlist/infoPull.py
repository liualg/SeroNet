import pandas as pd 
import urllib3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import os
from datetime import datetime
from tqdm import tqdm
from datetime import date
import itertools

import argparse

import warnings
warnings = 0

######### taking in inputs ##############

parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test", help="testing only, nothing is saved",
                    action="store_true")
args = parser.parse_args()
if args.test:
    print("Testing function...")

import tkinter as tk
from tkinter import simpledialog

ROOT = tk.Tk()

ROOT.withdraw()
# the input dialog
USER_INP = simpledialog.askstring(title="Test",
                                  prompt="What's your Name?:")
email_list = USER_INP.split('\n')
r = re.compile("[\d]{8}")
PMID_list = list(filter(r.match, email_list)) # Read Note below

if len(PMID_list) < 1:
    print('Please enter PMIDS seperated by rows')
    exit()
else:
    print(PMID_list)


######### Functions ##############

def convert_date(d):
    try:
        date = datetime.strptime(d, '%Y %b %d').strftime('%Y-%m-%d')
    except:
        date = datetime.strptime(d, '%Y %b').strftime('%Y-%m')
    return date

def clean_carriages(array):
    try:
        array = [line.replace('\r', '') for line in array]
    except:
        print('no return carriages')
    
    try:
        array = [line.replace('\n', '') for line in array]
    except:
        print('no newline carriages')
    
    return(array)


def get_PI(grantDict, grantNumber):
    a = []
    for grants in grantNumber:
        a.append(
            grantDict.loc[grantDict['Grant'] == grants].reset_index().PI[0].split(",")[0]
        )

    return(a)

    
def get_df_info(pubmed_url, ids, grant_names_1):
    url = pubmed_url + ids
    
    
    page = urlopen(url)
    html_doc = page.read()
    html = html_doc.decode("utf-8")

    # parse html content
    soup = BeautifulSoup( html_doc , 'html.parser')
    # =============================================== #
    # preprint or not:
    if (len(re.findall('preprint\s', str(soup))) < 1):
        print_type = ''
    else:
        print_type = 'preprint'
    
    # =============================================== #
    # Citation (since im lazy)
    try:
        citation = soup.find("div", {"class": "article-citation"}).text.replace('\r', '').replace('\n', '')
        citation = re.findall("(^.*?)(?:doi)", citation)[0].strip()
    except:
        citation = ''
    
    # =============================================== #
    # Finding by class name (title)
    title = soup.find(class_ = "heading-title")
    try:
        title = str(clean_carriages(title)[0]).strip()
    except:
        title = str(title)
        title = title.replace('\n', '').replace('<h1 class="heading-title">','').replace('</h1>','')
        try:
            title = title.replace('<i>', '').replace('</i>','').strip()

        except:
            print("no italics")
    
    # =============================================== #
    # Finding by class name (authors)
    author = soup.find_all(class_ = "authors-list-item")
    author_name = re.findall("data-ga-label=\"(.+?)\"", str(author))
    
    # =============================================== #
    # Finding date of publication (cit)
#     DOP = soup.find(class_ = "cit").string
#     try:
#         date = convert_date(DOP.split(';')[0])
#     except:
#         date = convert_date(DOP.split('.')[0])
    
    # =============================================== #
    # Finding the correct grant
    # parse html content
    soup = BeautifulSoup( html_doc , 'html.parser')
    grant = soup.find_all(class_ = "grant-item")
    grant = re.findall("data-ga-label=\"(.+?)\"", str(grant))

    str_grants = ', '.join(grant)
    # print(str_grants)
    
    # =============================================== #
    # clean out grants that are not in the right format:
    # bgrants = re.findall('(\w{3} \d{2}X\d{3})|(CA\d{6})', ' '.join(grant))
    bgrants = re.findall('(\w{3} CA\d{6})|(\w{3} \d{2}X\d{3})|(CA\d{6}|(\d{2}\w\d{5}\w\d{5}))', ' '.join(grant))
    out = list(filter(None,itertools.chain(*bgrants)))
    
    for i in out:
        base_grant = ''
        seroNet_grant = ''

        try:
            grant = i.split(' ')[1]
        except:
            grant = i

#         print(grant)

        try:
            if grant in grant_names_1:
                base_grant = grant
                seroNet_grant = grant
                break
        except:
            print('error')
    
    # Finding publishing journal 
    soup = BeautifulSoup(html_doc, 'lxml', from_encoding='utf-8')
    journal = re.findall('(?:meta content=\")(.*?)(?:name=\"citation_journal_title)',str(soup))[0][:-2]
    
    
    return title, author_name, journal, seroNet_grant, base_grant, print_type, citation

######### main script ############


PUBMED_SEARCH = 'https://pubmed.ncbi.nlm.nih.gov/?term=CA260508+OR+CA260476+OR+CA260539+OR+CA' \
'60584+OR+CA260507+OR+CA260469+OR+CA260526+OR+CA260588+OR+CA260513+OR+CA260541+OR+CA260462'\
'+OR+CA261276+OR+CA261277+OR+CA260582+OR+CA260543+OR+CA260492+OR+CA260591+OR+CA260581+OR+' \
'CA260517+OR+CA260563+OR+CA260560+OR+21X089+OR+21X090+OR+21X091+OR+21X092%5BGrant+Number%5'\
'D&format=pubmed&sort=date&size=200'

CURATION_DIR = '~/National Institutes of Health/NCI-FNL SeroNet Team - Curation channel/'
FILE_NAME = 'Award to curator and all contacts mapping.xlsx'
grant_map = pd.read_excel(os.path.join(CURATION_DIR, FILE_NAME))

# grant_names
grant_names = re.findall('(CA\d{6})', PUBMED_SEARCH)
grant_names += re.findall('(\d{2}X\d{3})', PUBMED_SEARCH)
grant_names.append('75N91019D00024')

today = date.today()
today = today.strftime("%y-%m-%d")

# Input
# PMID_input = '34253053 33798476 34584899 34951746 34424479 34767812'
# PMID_list = PMID_input.split(' ')

search_url = 'https://pubmed.ncbi.nlm.nih.gov/'

# Output
BASE = "/Users/liualg/Documents/GitHub/SeroNet/auto_add_masterlist"
OUT_DIR = f'{BASE}/new_pmids/data_pull_{today}.csv'
JENN_OUT_DIR = f'{BASE}/for_jenn/data_pull_{today}.csv'

PMID = []
title_list = []
author_list = []
journal_list = []
grant_list = []
base_list = []
paperType_list = []
paper_citation = []
curator = []

for ids in tqdm(PMID_list):
    title, author_name, journal, seroNet_grant, base_grant, print_type, citation = get_df_info(search_url, ids, grant_names)
    
    PMID.append(ids)
    title_list.append(title)
    author_list.append(str(author_name))
    journal_list.append(journal)
#     date_list.append(date_str)
    grant_list.append(seroNet_grant)
    base_list.append(base_grant)
    
    if journal in ['ArXiv']:
         paperType_list.append('preprint')
    else:
        paperType_list.append(print_type)
    paper_citation.append(citation)
    
print("\n")  
grantCuratorDic = dict(zip(grant_map['Grant'], grant_map['primaryCurator']))

curator = [*map(grantCuratorDic.get,grant_list)]

# replacing 75N91019D00024 with 75N91019D00024, Task Order No. 75N91020F00003
base_list = [sub.replace('75N91019D00024',
                         '75N91019D00024, Task Order No. 75N91020F00003') for sub in base_list]


empty = ['']*len(PMID)
OWNER = 'Publication Owner'
EPIC_NUMBER = 'JIRA Epic #'
BASE_PROJ = 'Base_Project'
STATUS = 'Status/ImmPort Study ID'
BASE_PROJ_1 = 'Base_Project.1'
NUMBER = 'PMID'
PMID_NUMBER = 'PMID_N'
URL = 'PMID_link'
TITLE = 'Publication_Title'
JOURNAL = 'Journal'
AUTHOR = 'Author(s)'
DATE = 'Pub Date'
SERONET_PI = 'PI'
PRE_PRINT = 'print_type'
CITE = 'citation'


updating_fields = {
    OWNER: curator,
    EPIC_NUMBER: empty,
    BASE_PROJ: base_list,
    STATUS: empty,
    BASE_PROJ_1: grant_list, 
    NUMBER: PMID,
    PMID_NUMBER: ['PMID_'+str(x) for x in PMID],
    URL: [search_url+str(x) for x in PMID],
    TITLE: title_list, 
    JOURNAL:journal_list,
    AUTHOR:author_list,
    DATE:empty,
    SERONET_PI:empty,
    PRE_PRINT: paperType_list,
    CITE: paper_citation
}

temp = pd.DataFrame(updating_fields)
# display(temp)
temp[AUTHOR] = temp[AUTHOR].str.replace('\'','',regex=True)
temp[AUTHOR] = temp[AUTHOR].str.replace('[','',regex=True)
temp[AUTHOR] = temp[AUTHOR].str.replace(']','',regex=True)

temp[SERONET_PI] = get_PI(grant_map, temp[BASE_PROJ_1])

if args.test != True:
    temp.to_csv(OUT_DIR)
    temp[['PMID','Publication_Title']].to_csv(JENN_OUT_DIR)
    print(f"output is located at: {OUT_DIR}")
    print("\n")

# temp.head()

for i,o in enumerate(temp.PMID):
    if args.test == True:
        print(f"CURATOR: {temp[OWNER][i]}")
        print(f"Title: {temp[TITLE][i]}")
        print(f"Journal: {temp[JOURNAL][i]}")
        print(f"Pubmed: {temp[URL][i]}")
        print(temp[PMID_NUMBER][i])
        print(temp[SERONET_PI][i].capitalize())
        print(temp[BASE_PROJ_1][i])
        print("\n")
    else:
        if temp[PRE_PRINT][i] != 'preprint':
            print(f"CURATOR: {temp[OWNER][i]}")
            print(temp[PMID_NUMBER][i])
            print(f"*Title*: {temp[TITLE][i]}")
            print(f"*Journal*: {temp[JOURNAL][i]}")
            print(f"*Pubmed*: {temp[URL][i]}")
            print(f"CURATOR: {temp[OWNER][i]}")
            print(temp[PMID_NUMBER][i])
            print(temp[SERONET_PI][i].capitalize())
            print(temp[BASE_PROJ_1][i])
            print("\n")

if args.test != True:
    print("\n")
    print("These are the new publications for this week:")
    for i,o in enumerate(temp.PMID):
        
        if temp[OWNER][i] == 'Mani' or temp[OWNER][i] == 'Liu / Mani':
            print(temp[PMID_NUMBER][i])
    print("\n")