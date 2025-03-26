from sys import platform
import os
import seronetFunctions as sfxn
from argparse import ArgumentParser
import subprocess


parser = ArgumentParser(
             prog="Find PMID folder in Share Point",
             description="Traverse through Share Point, check to see if the folder exists."\
             "If it does, open up the current folder for the PMID")

parser.add_argument(
        '--PMID',
        '-p',
        required=True,
        help="Please enter a 8 digit PMID to find the folder in share point"
    )
args = parser.parse_args()
pmid =  args.PMID.strip()

if platform == "darwin":
	drive = "/Users/liualg/Library/CloudStorage/OneDrive-SharedLibraries-NationalInstitutesofHealth"
	share_point = os.path.join(drive,"NCI-SeroNet - SeroNet Public Data Curation RESTRICTED")
else: 
	print("User has windows")
	share_point = os.path.join("Users",os.getlogin(), "OneDrive-SharedLibraries-NationalInstitutesofHealth", "NCI-SeroNet - SeroNet Public Data Curation RESTRICTED")

#File Paths
cloud_drive = share_point

if os.path.isdir(cloud_drive):
	try:
		BASE_DIR = sfxn.traverse_dir(cloud_drive, pmid)
	except FileNotFoundError:
		sys.exit("ERROR:: Incorrect Template format. Cannot Find File")

subprocess.Popen(["open", BASE_DIR])
