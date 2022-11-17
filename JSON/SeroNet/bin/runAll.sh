#!/bin/bash

# FOR DEMONSTRATION ONLY

files=(
../SampleTemplates/SDY2012/PMID35504289_v1.2.2.xlsm
../SampleTemplates/SDY2024/PMID35455241_v1.2.3.xlsm
../SampleTemplates/SDY2026/PMID35589681_v1.2.4.xlsm
../SampleTemplates/SDY2033/PMID35427477_v1.2.5.xlsm
../SampleTemplates/SDY2034/PMID35348368_v1.2.3.xlsm
../SampleTemplates/SDY2035/PMID35143473_v1.2.3.xlsm
../SampleTemplates/SDY2036/PMID35129576_v1.2.4.xlsm
../SampleTemplates/SDY2037/PMID35013325_v1.2.3.xlsm
../SampleTemplates/SDY2038/PMID35040666_v1.2.3.xlsm
../SampleTemplates/SDY2039/PMID35025672_v1.2.3.xlsm
../SampleTemplates/SDY2040/PMID34260834_v1.2.3.xlsm
../SampleTemplates/SDY2041/PMID34107529_v1.2.3.xlsm
../SampleTemplates/SDY2042/PMID35289637_v1.2.3.xlsm
../SampleTemplates/SDY2043/PMID34001652_v1.2.3.xlsm
../SampleTemplates/SDY2044/PMID34250512_v1.2.4.xlsm
../SampleTemplates/SDY2045/PMID35764643_v1.2.4.xlsm
../SampleTemplates/SDY2047/PMID34523968_v1.2.3.xlsm
../SampleTemplates/SDY2053/PMID35148837_v1.2.5.xlsm
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
    parseRegistryTemplate.py --excel_file ${files[i]} --output_file ../SampleJson/${studies[i]}.orig
done
