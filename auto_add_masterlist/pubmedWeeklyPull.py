import pandas as pd 
import numpy as np
import urllib3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from datetime import datetime
from tqdm import tqdm
import warnings
warnings = 0

preprint_url = 'https://pubmed.ncbi.nlm.nih.gov/?term=CA260508+OR+CA260476+OR+CA260539'  \
'+OR+CA260584+OR+CA260507+OR+CA260469+OR+CA260526+OR+CA260588+OR+CA260513+OR+CA260541+OR'\
'+CA260462+OR+CA261276+OR+CA261277+OR+CA260582+OR+CA260543+OR+CA260492+OR+CA260591+OR+CA'\
'260581+OR+CA260517+OR+CA260563+OR+CA260560%5BGrant+Number%5D&filter=pubt.preprint&format=pubmed&size=200'

pmids_url = 'https://pubmed.ncbi.nlm.nih.gov/?term=CA260508+OR+CA260476+OR+CA260539+OR+CA' \
'60584+OR+CA260507+OR+CA260469+OR+CA260526+OR+CA260588+OR+CA260513+OR+CA260541+OR+CA260462'\
'+OR+CA261276+OR+CA261277+OR+CA260582+OR+CA260543+OR+CA260492+OR+CA260591+OR+CA260581+OR+' \
'CA260517+OR+CA260563+OR+CA260560+OR+21X089+OR+21X090+OR+21X091+OR+21X092%5BGrant+Number%5'\
'D&format=pubmed&sort=date&size=200'

PMID_input = '34469363 34485950 34521836 34523968 34546094 33119738 33292895 33798476 34081540 34086877 34250518 34253053'
PMID_list = PMID_input.split(' ')
search_url= 'https://pubmed.ncbi.nlm.nih.gov/34485950/'



grant_names = re.findall('(CA\d{6})', pmids_url)
grant_names += re.findall('(\d{2}X\d{3})', pmids_url)

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

# might be able to use soup.stripped_strings:

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


def get_df_info(pubmed_url, ids):
    url = pubmed_url + ids
    
    
    page = urlopen(url)
    html_doc = page.read()
    html = html_doc.decode("utf-8")

    # parse html content
    soup = BeautifulSoup( html_doc , 'html.parser')

    # =============================================== #
    # Finding by class name (title)
    title = soup.find(class_ = "heading-title")
    title = str(clean_carriages(title)[0]).strip()

    # Finding by class name (authors)
    author = soup.find_all(class_ = "authors-list-item")
    author_name = re.findall("data-ga-label=\"(.+?)\"", str(author))
    
    # Finding date of publication (cit)
    DOP = soup.find(class_ = "cit").string
    date = convert_date(DOP.split(';')[0])

    # Finding the correct grant
    try:
        grant = soup.find_all(class_ = "grant-item")
        grant = re.findall("data-ga-label=\"(.+?)\"", str(grant))
        grant = ''.join(re.findall('(\w{3} CA\d{6})|(\w{3} \d{2}X\d{3})', ' '.join(grant))[0])
        base_grant = grant.replace(' ','')
        seroNet_grant = grant.split(' ')[1]
    except:
        seroNet_grant = ''
        base_grant = ''
    
    # Finding publishing journal 
    soup = BeautifulSoup(html_doc, 'lxml', from_encoding='utf-8')
    journal = re.findall('(?:meta content=\")(.*?)(?:name=\"citation_journal_title)',str(soup))[0][:-2]
    
    return title, author_name, journal, date, seroNet_grant, base_grant
    # # Finding by class name (title)
    # title = soup.find(class_ = "heading-title")
    # title = str(clean_carriages(title)[0]).strip()


search_url= 'https://pubmed.ncbi.nlm.nih.gov/34485950/'
page = urlopen(search_url)
html_doc = page.read()
html = html_doc.decode("utf-8")

# parse html content
soup = BeautifulSoup( html_doc , 'html.parser')
grant = soup.find_all(class_ = "grant-item")
grant = re.findall("data-ga-label=\"(.+?)\"", str(grant))
grant = ''.join(re.findall('(\w{3} CA\d{6})|(\w{3} \d{2}X\d{3})', ' '.join(grant))[0])
base_grant = grant.replace(' ','')
seroNet_grant = grant.split(' ')[1]
seroNet_grant


PMID = []
title_list = []
author_list = []
journal_list = []
date_list = []
grant_list = []
base_list = []

for ids in tqdm(PMID_list):
    title, author_name, journal, date_str, seroNet_grant, base_grant = get_df_info(search_url, ids)
    
    PMID.append(ids)
    title_list.append(title)
    author_list.append(str(author_name))
    journal_list.append(journal)
    date_list.append(date_str)
    grant_list.append(seroNet_grant)
    base_list.append(base_grant)



empty = ['']*len(PMID)
updating_fields = {
    'Base_Project':base_list,
    'Base_Project.1':grant_list, 
    'PMID':PMID, 
    'Folder name':empty,
    'PubMed_ID link':PMID,
    'Publication_Title':title_list, 
    'Journal':journal_list,
#     'Author(s)':author_list,
    'Pub Date':date_list,
    'PI':empty
}

temp = pd.DataFrame(updating_fields)
# temp['Author(s)'] = temp['Author(s)'].str.replace('\'','')
# temp['Author(s)'] = temp['Author(s)'].str.replace('[','')
# temp['Author(s)'] = temp['Author(s)'].str.replace(']','')
# temp.to_csv('/Users/liualg/Desktop/delete/October-1.csv')

today = date.today()
today = today.strftime("%y-%m-%d")
temp.to_csv(f'/Users/liualg/Desktop/delete/data_pull_{today}.csv')
print(temp.head())