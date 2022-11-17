#!/usr/bin/env python
'''Generate JSON object from SeroNet Registry Excel Sheet
'''

import sys
import os
import json
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

from argparse import ArgumentParser

import parse_template as pt

if __name__ == "__main__":
    parser = ArgumentParser(
             prog="parseRegistryTemplate",
             description="Parse a SeroNet registry template into JSON")

    parser.add_argument(
        '--excel_file',
        dest="excel_file",
        required=True,
        help="Specify the path to the excel file"
    )

    parser.add_argument(
        '--output_file',
        dest="output_file",
        required=True,
        help="Specify the path to the output file"
    )

    args = parser.parse_args()

    df = pd.read_excel(args.excel_file, sheet_name = 0, header=None)
    #
    # Start the Index at 1 to Match Excel Line Numbers
    #
    df.index += 1

    #
    # Initialize Empty Template Dictionary
    #
    template = {}

    pt.parse_registry_template(df, template)
    #print(json.dumps(template, indent=4))

    f = open(args.output_file, "w")
    print(json.dumps(template, indent=4), file = f)
    f.close()