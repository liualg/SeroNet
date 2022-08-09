import os 
import shutil
from glob import glob
import seronetFunctions as seroFxn


dr44_list = [
'33035201','33065030','33142304','33160316','33169014',
'33276369','33408181','33440148','33472939','33478949',
'33479118','33521695','33571162','33602725','33622794',
'33666169','33727353','33743211','33830946','33846272',
'33961839','33993265','34003112','34086877','34095338',
'34130883','34145263','34151306','34161961','34353890',
'34452006','34652783','34687893','34696403','34730254',
'34759001','34794169','34802457','34835131','34877479',
'34910927','34921308','34952892','35132398','34937699']

box_base = "~/Library/CloudStorage/Box-Box/SeroNet Public Data"
out_path = "/Users/liualg/Library/CloudStorage/Box-Box/ImmPort Data"

# print(glob(out_path))

for PMID in dr44_list:
	print(PMID)
	BASE_DIR = seroFxn.get_box_dir(box_base,PMID)


	try:
		df_path = glob(os.path.join(BASE_DIR,'templated_data',f'PMID{PMID}_v1.2.5_reviewed.xlsm'))[0]
	except FileNotFoundError:
		sys.exit("ERROR:: Incorrect Template format. Cannot Find File")

	# print(os.path.exists(out_path))
	if os.path.exists(df_path):
		shutil.copy(df_path, os.path.join(out_path,f'PMID{PMID}_v1.2.5_reviewed.xlsm'))