#!/usr/bin/env python

import pandas as pd 
import sys, yaml

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askdirectory, askopenfilename

with open('compress_config.yml', 'r') as f:
        compress_config = yaml.full_load(f)

if len(sys.argv) > 1 and sys.argv[1] == 'config':
# if sys.argv > 1 and sys.argv[1] == 'config':
     output_dir = askdirectory() + '/'
     print(output_dir)

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
filename = filename.split('/')[-1]
print(filename)

output = output_dir + filename + '.gz'
print(output)
# input = pd.read_csv(filename)
# input.to_csv(filename + '.gz', compression='gzip')