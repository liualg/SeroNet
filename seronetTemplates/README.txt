Date: 
June 23, 2022

Author/contact information:
contact - Alexander Liu
email - liualg@nih.gov | alexander.g.liu001@gmail.com

Package purpose: 
This package contains scripts, dictionaries, and templates to automate the transfer of information from SeroNet specific templates to ImmPort templates. Versions of the package reflect the most recent template

Version: 
1.2.6
- ETL: Cleans and normalizes SeroNet Registry Template data and outputs SeroNet specific templates 
- JSON: Will create a JSON version of SeroNet Registry Template and run facet fields through spell checker.

Pointer to Instructions/Requirements for configuration and installation info: 
To install packages please navigate to Instructions.txt file. 
Download the required packages in requirements.txt 

Once the files and packages have downloaded, check to make sure the box path [local var = box_base] is correct in Registry2ImmmPort_full.py and Registry2ImmmPort_basic.py. 

To run the script, please type 'python createTemplates.py' and enter the PMID into the pop-up window. 


Acknowledgements: 
SeroNet Team - Elaine Freund, Renuka Vepachedu, David Abraham, Patrick Breads
ImmPort Team - Henry Schaefer
National Cancer Institute (NCI)
Essential Software Inc (ESI)
