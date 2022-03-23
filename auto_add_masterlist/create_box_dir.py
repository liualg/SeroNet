import os 
import glob

def get_box_dir(box_dir, grant,PI):
    box_base = os.path.abspath(os.path.expanduser(os.path.expandvars(box_dir)))
    depth = 0

    for dirpath, dirnames, filenames in os.walk(box_base):
    	print(dirnames)
		# if dirpath[len(box_base):].count(os.sep) < depth:
		#     if grant+"_"+PI in dirnames:
		#         return(os.path.join(dirpath, grant+"_"+PI))


box_base = "/Users/liualg/Library/CloudStorage/Box-Box/SeroNet Public Data"
grants = 'CA260543'
pi = 'Baric'
PMID = '00001'

file = box_base+f"/{grants}_*"
PI_PATH = glob.glob(file)[0]
os.makedirs(os.path.join(PI_PATH,f"PMID_{PMID}","submitted_data"))
os.makedirs(os.path.join(PI_PATH,f"PMID_{PMID}","templated_data"))
