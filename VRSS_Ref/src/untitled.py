import pandas as pd 
from glob import glob

file_dir='/Users/liualg/Documents/GitHub/SeroNet/VRSS_Ref/final'
files = glob(file_dir+'/*.xlsx')
out_dir='/Users/liualg/Documents/GitHub/SeroNet/VRSS_Ref/final/text'
# print(files)

for f in files:
	name = f.split('/')[-1].split('.')[0]
	print(name)
	temp = pd.read_excel(f)
	temp.to_csv(out_dir+'/'+name+'.txt',sep='\t',index=False)