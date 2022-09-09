#!/usr/bin/env bash
# v1.1.0 => Package.zip
# v1.2.0 => Package_v1.2.zip
 #getting new requirements

mkdir -p ./Package
cp -r ./dictionary ./Package/dictionary
cp -r ./template ./Package/template
cp ./seronetDataclass.py ./Package/seronetDataclass.py
cp ./seronetFunctions.py ./Package/seronetFunctions.py

# SeroNET
cp ./Registry2ImmPort_full.py ./Package/Registry2ImmPort_full.py
cp ./Registry2ImmPort_full.py ./Package/Registry2ImmPort_full.py
cp ./Registry2ImmPort_basic.py ./Package/Registry2ImmPort_basic.py
cp ./createTemplates.py ./Package/createTemplates.py
cp ./instructions.txt ./Package/instructions.txt
cp ./1_0000_SeroNet_Diagram-3x4.jpg ./Package/1_0000_SeroNet_Diagram-3x4.jpg
cp ./README.txt ./Package/README.txt
pipreqs ./Package/
mv ./Package/requirements.txt ./Package/software.txt

zip -r ./Package_v1.3.zip ./Package
rm -r ./Package


