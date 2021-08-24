#!/usr/bin/env python

import pandas as pd
import os

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename

Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file

new = os.path.splitext(filename)[0]

print(new)
input = pd.read_csv(filename, compression='gzip')
input.to_csv(new)