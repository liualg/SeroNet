import os
from glob import escape, glob
from sys import platform
import seronetFunctions as sfxn
import getpass
from pathlib import Path

def find_onedrive():
	USER=getpass.getuser()
	print(USER)

	if platform == "linux" or platform == "linux2":
		print("NOT SUPPORTED. Please edit PATH_SETUP.py as you see fit")

	elif platform == "darwin":
		ONEDRIVE = os.path.join("Users",USER,"Library","CloudStorage","OneDrive-SharedLibraries-NationalInstitutesofHealth")
		CURATION =os.path.join(ONEDRIVE,"NCI-FNL SeroNet Team - Curation channel")
		DATA = os.path.join(ONEDRIVE,"NCI-SeroNet - SeroNet Public Data Curation RESTRICTED")

		# print(find_onedrive(ONEDRIVE,'ONEDRIVE'))
		print("ere")

	elif platform == "win32":
		ONEDRIVE =os.path.join("c:/", "Users",USER,"OneDrive - National Institutes of Health")
		CURATION =os.path.join(ONEDRIVE,"Curation channel")
		DATA = os.path.join(ONEDRIVE,"SeroNet Public Data Curation RESTRICTED")

	else:
		sys.exit("ERROR:: What OS are you using?")

	return ONEDRIVE, CURATION, DATA