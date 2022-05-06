#!/usr/bin/env bash

 #getting new requirements

mkdir -p ./Package
cp -r ./dictionary ./Package/dictionary
cp -r ./template ./Package/template
cp ./seronetDataclass_v1_1_0.py ./Package/seronetDataclass_v1_1_0.py
cp ./seronetFunctions.py ./Package/seronetFunctions.py
cp ./Registry2ImmPort_final_v1.1.0.py ./Package/Registry2ImmPort_final_v1.1.0.py
cp ./instructions.txt ./Package/instructions.txt
pipreqs ./Package/

zip -r ./Package.zip ./Package
rm -r ./Package


