#!/usr/bin/env python

import pandas as pd 
import sys, yaml

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askdirectory, askopenfilenames

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing

if len(sys.argv) > 1 and sys.argv[1] == 'config':
     output_dir = askdirectory() + '/'
     compress_config["output_dir"] = output_dir
     with open('compress_config.yml', 'w') as f:
             yaml.dump(compress_config, f)
             print("Output selected")
             exit()


files = askopenfilenames() # show an "Open" dialog box and return the path to the selected file
file_list = list(files)
# print(file_list)

print("Compressing the following: ")
for fp in file_list:
        filename = fp.split('/')[-1]
        print(filename)

        with open('compress_config.yml', 'r') as f:
                compress_config = yaml.full_load(f)

        output_name = compress_config["output_dir"] + filename + '.gz'
        print(output_name)
        output_file = pd.read_csv(fp)
        output_file.to_csv(output_name, compression='gzip')

