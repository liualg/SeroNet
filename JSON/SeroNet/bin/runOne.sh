#!/bin/bash

# FOR DEMONSTRATION ONLY

files=(
../SeroNetDR45/SDY2044/PMID34250512_v1.2.4.xlsm
)

studies=(
    SDY2012
    SDY2024
    SDY2026
    SDY2033
    SDY2034
    SDY2035
    SDY2036
    SDY2037
    SDY2038
    SDY2039
    SDY2040
    SDY2041
    SDY2042
    SDY2043
    SDY2044
    SDY2045
    SDY2047
    SDY2053
)

for (( i = 0; i < ${#files[@]}; ++i )); do
    echo "File: ${files[i]}"
    echo "Study: ${studies[i]}"
    parseRegistryTemplate.py --excel_file ${files[i]} --output_file ../SeroNetSearch/studies/${studies[i]}.json
done

#parseRegistryTemplate.py --excel_file ../SeroNetDR45/SDY2036/PMID35129576_v1.2.4.xlsm --output_file ../SeroNetJSON/SDY3036.json
