#!/usr/bin/env bash
# v1.1.0 => Package.zip
# v1.2.0 => Package_v1.2.zip
# v1.4.0 => hold data for PMDO

 #getting new requirements

mkdir -p ./Package

# Folders
cp -r ./dictionary ./Package/dictionary
cp -r ./template ./Package/template
cp -r ./notes ./Package/notes

# Definitions
cp ./seronetDataclass.py ./Package/seronetDataclass.py
cp ./seronetFunctions.py ./Package/seronetFunctions.py

# SeroNet
cp ./Registry2ImmPort_full.py ./Package/Registry2ImmPort_full.py
cp ./Registry2ImmPort_full.py ./Package/Registry2ImmPort_full.py
cp ./Registry2ImmPort_basic.py ./Package/Registry2ImmPort_basic.py
cp ./createTemplates.py ./Package/createTemplates.py
cp ./instructions.txt ./Package/instructions.txt
cp ./1_0000_SeroNet_Diagram-3x4.jpg ./Package/1_0000_SeroNet_Diagram-3x4.jpg
cp ./README.txt ./Package/README.txt

# JSON  
cp ./JSONcreateSuggestions.py ./Package/JSONcreateSuggestions.py
cp ./JSONparse_template.py ./Package/JSONparse_template.py
cp ./JSONparseRegistryTemplate.py ./Package/JSONparseRegistryTemplate.py


# Internal Qs
cp ./InternalQs.ipynb ./Package/InternalQs.ipynb

# This doc
cp ./createPackage.sh ./Package/createPackage.sh

pipreqs ./Package/
mv ./Package/requirements.txt ./Package/software.txt

zip -r ./Package_v1.2.7.zip ./Package
rm -r ./Package


