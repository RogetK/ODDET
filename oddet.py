#!/usr/bin/env python3

"""
MIT License

Copyright (c) [year] [fullname]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import os, sys, argparse, yaml, logging, pandas, shutil
from liboddet import parse

from tkinter import *
from tkinter import Tk, filedialog


logging.basicConfig(format='[ODDET] [%(levelname)8s]: %(message)s', level=logging.DEBUG) 


parser = argparse.ArgumentParser(description="Tool for data extraction of the Opera dataset.")

parser.add_argument('-config', action='store_true', help="Configure directories")
parser.add_argument('-clean', action='store_true', help='Clean output directory')
parser.add_argument('-m', help = 'Modality')

parser.add_argument('-d', action='store_true', help='Descriptor to extract according to')
parser.add_argument('-e', help='Experiment number')
parser.add_argument('-f', nargs='+', help='Feature list to be extracted')

###################
global args
global dataset_cfg_dir 
global data_cfg 
global output_dir

###################
def oddet_clean():
    logging.info("Cleaning output directory")
    with open('configs/config.yml', 'r') as f:
        oddet_config = yaml.full_load(f)

    output = oddet_config["output_dir"]
    if os.path.exists(output):
        shutil.rmtree(output)
        os.mkdir(output)
    
    logging.info("Output directory cleaned. Exiting")
    exit()


def configure():
    if len(sys.argv) > 3:
        logging.error("Too many arguments, -config is standalone.")
        logging.error("Exiting.")
        exit()

    logging.info("Configuring Oddet")

    with open('configs/config.yml', 'r') as f:
        oddet_config = yaml.full_load(f)

    print("\n[1]:\tConfigure dataset directory")
    print("[2]:\tConfigure output directory\n")

    p = input(">> Select one of the numbers above: ")
    print('')

    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    if p == '1':
        logging.info("Selecting dataset location")
        dataset_directory = filedialog.askdirectory()
        if dataset_directory != '':
            oddet_config["dataset_dir"] = dataset_directory
            print(oddet_config["dataset_dir"])
            with open('configs/config.yml', 'w') as f:
                yaml.dump(oddet_config, f)
        else:
            logging.error("No directory selected. Exiting.")
            exit()

    elif p == '2':
        logging.info("Selecting output directory")
        output_directory = filedialog.askdirectory()
        if output_directory != '':
            oddet_config["output_dir"] = output_directory
            print(oddet_config["output_dir"])
            with open('configs/config.yml', 'w') as f:
                yaml.dump(oddet_config, f)
        else:
            logging.error("No directory selected. Exiting.")
            exit()

    else:
        logging.error("No directory selected. Exiting.")
        exit()
    exit()



#############################################################################

def read_config():
    global dataset_cfg_dir, output_dir

    with open('configs/config.yml', 'r') as f:
        oddet_config = yaml.full_load(f)

    dataset_cfg_dir = oddet_config["dataset_dir"]
    output_dir = oddet_config["output_dir"]

    logging.info("Looking for dataset ...")
    if os.path.isdir(dataset_cfg_dir):
        logging.info("Dataset directory: " + dataset_cfg_dir)
    else:
        logging.error('Dataset not found.')

    ### Creating output DIR
    if os.path.isdir(output_dir):
        logging.info("Output directory: " + output_dir)
    else: 
        logging.error("Output directory not found.")
        response = input("Create output directory? [y/N]: ")
        if response == ('y' or 'Y'):
            logging.info("Creating output directory")
            os.mkdir(output_dir)
            if (os.path.isdir(output_dir)):
                logging.info("Directory created")
            else: 
                logging.error("Output directory not created")
                exit()
        else:
            logging.info("Output directory not created")
            exit()


#############################################################################


def complex_retrieval_d():
    logging.info("Retrieving based on descriptor")
    return


def complex_retrieval_f():
    logging.info("Retrieving specified features")
    return


def oddet_modality_get():
    if (len(sys.argv) < 3):
        logging.error("Not enough arguments. For usage, use flag -h.")
        return
    
    global data_cfg 
    descriptor = False
    dataset_string = ""

    # Selecting modality
    if args.m is not None: 
        set_dir = dataset_cfg_dir+'/'+ args.m + '/'
        set_cfg_string = 'configs/sets/' + args.m + '.yml'
    else: 
        logging.error("No modality selected, exiting.")
        exit()

    # Finding modality config
    if os.path.isfile(set_cfg_string): 
        logging.info("Dataset config found")
        temp_cfg = open(set_cfg_string, 'r')
        data_cfg = yaml.full_load(temp_cfg)
    else:
        logging.error("No dataset config specified. Exiting.")
        exit()

    # Retrieve based on dataset descriptor
    if args.d is True:
        complex_retrieval_d()
        exit()

    # Retrieve based on experiment number
    if args.e is not None:
        dataset_string = set_dir + args.m + '_exp' + args.e + data_cfg["filetype"]
        if os.path.isfile(dataset_string):
            logging.info("Dataset found")         
        else:
            logging.error("Dataset for not found, ensure file location is correct. Exiting.")
            exit()
    else: 
        logging.info("No experiments specified")
        prompt = input ("Do you want to retrieve all sets from " + args.m + "? [y/N]: ")
        if (prompt == ('y' or 'Y')):
            logging.info("Copying set for entire modality")
            copy_dir = output_dir + '/' + args.m
            if os.path.exists(copy_dir):
                shutil.rmtree(copy_dir)
            shutil.copytree(set_dir, copy_dir)
            if os.path.exists(copy_dir):
                logging.info("Copy successful. Exiting.")
            exit() 
        else:
            logging.info("Nothing to do. Exiting.")
            exit()
        
            
    # Retrieve if only modality is selected
    # Retrieves the entire set for the modality
    if (args.f is None) and (args.d is not True) and (args.e is not None):
        logging.info("Retrieving entire set of " + args.m + '_exp' + args.e)
        prompt = input("Do you want to retrieve the whole set? [y/N]: ")
        if prompt == ('y' or 'Y'): 
            shutil.copy2(dataset_string, output_dir)
            output_file = output_dir+'/'+args.m+'_exp' + args.e + data_cfg["filetype"]
            if os.path.isfile(output_file):
                logging.info("Dataset written to " + output_file)
                logging.info("Exiting.")
        else:
            logging.info("Nothing retrieved. Exiting.")
            exit()

    elif (args.f is not  None) and (args.d is not True):
        complex_retrieval_f()

    return





####################################################################

def main():
    print("\n***** ODDET Extraction Tool *****")
    global args
    if len(sys.argv) < 2:
        parser.print_help()
        exit()

    args = parser.parse_args()

    if args.config is True:
        configure()
    
    if args.clean is True:
        oddet_clean()

    read_config()

    if args.m is not None:
        oddet_modality_get()

    oddet_get()

if __name__ == "__main__":
    main()
    exit()