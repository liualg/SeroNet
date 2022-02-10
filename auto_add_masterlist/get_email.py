import pandas as pd 
import argparse 
import re

check = 0

parser = argparse.ArgumentParser(description='PI last name')
parser.add_argument('PI', metavar='N', type=str, nargs='+',
                    help='enter the PI last name please')

args = parser.parse_args()

PI_name = args.PI[0]
print("Input:", PI_name)

masterlist_dir = "~/National Institutes of Health/NCI-FNL SeroNet Team - Curation channel/Award to curator and all contacts mapping.xlsx"
masterlist = pd.read_excel(masterlist_dir, sheet_name = 'contact&curatorGrantMapping')
# print(masterlist.columns)
try:
	df = masterlist[masterlist['PI'].astype(str).str.contains(
		PI_name, 
		flags=re.IGNORECASE, 
		regex=True)]

	print("PI:\n",
		df['PI'].reset_index(drop=True)[0].title(),"\n",
		df['PI-Email'].reset_index(drop=True)[0],"\n",
		df['Grant'].reset_index(drop=True)[0],"\n")
	print("Co-author:\n",
		df['Co-Investigator(s)'].reset_index(drop=True)[0].title(), "\n",
		df['Co-Email'].reset_index(drop=True)[0],"\n",
		df['Grant'].reset_index(drop=True)[0],"\n")
	check += 1
except:
	print(" ~~ PI does not exist, will try Co-author ~~ \n")

if check == 0:
	try:
		df = masterlist[masterlist['Co-Investigator(s)'].astype(str).str.contains(
			PI_name, 
			flags=re.IGNORECASE, 
			regex=True)]

		print("PI:\n",
			df['PI'].reset_index(drop=True)[0].title(),"\n",
			df['PI-Email'].reset_index(drop=True)[0],"\n",
			df['Grant'].reset_index(drop=True)[0],"\n")
		print("Co-author:\n",
			df['Co-Investigator(s)'].reset_index(drop=True)[0].title(),"\n", 
			df['Co-Email'].reset_index(drop=True)[0],"\n",
			df['Grant'].reset_index(drop=True)[0],"\n")
	except:
		print("\n~~ Name is not a Co-Auther. Please check or add ~~")


