#!/usr/bin/env bash

 #getting new requirements

mkdir -p ./Package
cp -r ./dictionary ./Package/dictionary
cp -r ./template ./Package/template
cp ./seronetDataclass_v1_1_0.py ./Package/seronetDataclass_v1_1_0.py
cp ./seronetFunctions.py ./Package/seronetFunctions.py
cp ./Registry2ImmPort_full.py ./Package/Registry2ImmPort_full.py
cp ./Registry2ImmPort_basic.py ./Package/Registry2ImmPort_basic.py
cp ./createTemplates.py ./Package/createTemplates.py
cp ./instructions.txt ./Package/instructions.txt
cp ./1_0000_SeroNet_Diagram-3x4.jpg ./Package/1_0000_SeroNet_Diagram-3x4.jpg
pipreqs ./Package/

zip -r ./Package.zip ./Package
rm -r ./Package


