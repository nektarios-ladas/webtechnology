

import os
import subprocess

text = str(raw_input("Enter the text you want to search for: "))

thedir = 'C:\\your\\path\\here\\'
for file in os.listdir(thedir):
    filepath = thedir + file
    for line in open(filepath):
        if text in line:
            subprocess.call(filepath, shell=True)
            break

