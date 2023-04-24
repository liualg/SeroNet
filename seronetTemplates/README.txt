Date: 
Feb 13, 2023

Author/contact information:
contact - Alexander Liu
email - liualg@nih.gov | alexander.g.liu001@gmail.com

Package purpose: 
This package contains scripts, dictionaries, and templates to automate the transfer of information from SeroNet specific templates to ImmPort templates. Versions of the package reflect the most recent template

Version: 
1.3.4
- ETL: Cleans and normalizes SeroNet Registry Template data and outputs SeroNet specific templates. The script will automatically run "Registry2ImmPort_short.py", which is an abridged version. The short version will create the Basic, Protocol, Experiment, and Subject templates.

- JSON: Will create a JSON version of SeroNet Registry Template and run facet fields through spell checker. The spell checker is based on a package called "fuzzywuzzy", which uses Levenshtein Distance to calculate the differences between sequences. 

Pointer to Instructions/Requirements for configuration and installation info: 
To install packages please navigate to Instructions.txt file. 
Download the required python packages in software.txt 

Once the files and packages have downloaded, check to make sure the box path [local var = box_base] is correct in Registry2ImmmPort_full.py and Registry2ImmmPort_basic.py. 

To run the script, please type 'python createTemplates.py' and enter the PMID into the pop-up window. 


Acknowledgements: 
SeroNet Team - Elaine Freund, Renuka Vepachedu, David Abraham, Patrick Breads
ImmPort Team - Henry Schaefer, John Campbell, Ruth Monterio
National Cancer Institute (NCI)
Essential Software Inc (ESI)
