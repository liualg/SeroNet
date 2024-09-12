import functions_CBC as ifxn
import pandas as pd
from sys import platform
from os import path, system
import numpy as np

if platform == "darwin":
    system('clear')
else:
    system('cls')

immportFile='subjectHumans'
h=ifxn.grab_headers(immportFile)

print(h)