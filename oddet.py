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
from typing import final
from liboddet import parse

from tkinter import *
from tkinter import Tk, filedialog

import h5py
import numpy as np



logging.basicConfig(format='[ODDET] [%(levelname)8s]: %(message)s', level=logging.DEBUG) 


parser = argparse.ArgumentParser(description="Tool for data extraction of the Opera dataset.")

parser.add_argument('-config', action='store_true', help="Configure directories")
parser.add_argument('-clean', action='store_true', help='Clean output directory')

parser.add_argument('-m', nargs='+', help = 'Modality')
parser.add_argument('-d', action='store_true', help='Descriptor to extract according to')
parser.add_argument('-e', nargs='+', help='Experiment number')
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

'''
Gets all data for specified modalities
'''

def oddet_m():
    global data_cfg

    for m in args.m: 
        set_dir = dataset_cfg_dir+'/'+ m + '/'
        set_cfg_string = 'configs/sets/' + m + '.yml'

        if os.path.isfile(set_cfg_string) and os.path.exists(set_dir): 
            logging.info("Modality config and dataset found for " + m)
            temp_cfg = open(set_cfg_string, 'r')
            data_cfg = yaml.full_load(temp_cfg)
        else:
            logging.info("Modality " + m + " not found, skipping")
            continue


        final_output_dir = output_dir + '/' + m
        if os.path.isdir(final_output_dir):
            shutil.rmtree(final_output_dir)
        shutil.copytree(set_dir, final_output_dir)

        logging.info("Finished copying modality data")

    return
        
'''
Gets all experiments for specified modalities
'''

def oddet_m_e():
    global data_cfg

    for m in args.m:
        set_dir = dataset_cfg_dir+'/'+ m + '/'
        set_cfg_string = 'configs/sets/' + m + '.yml'

        if os.path.isfile(set_cfg_string) and os.path.exists(set_dir): 
            logging.info("Modality config and dataset found for " + m)
            temp_cfg = open(set_cfg_string, 'r')
            data_cfg = yaml.full_load(temp_cfg)
        else:
            logging.info("Modality " + m + " not found, skipping")
            continue

        for e in args.e:
            dataset_string = set_dir + m +'_exp' + e + data_cfg["filetype"]
            print(dataset_string)
            if os.path.isfile(dataset_string):
                logging.info("Dataset found for " + dataset_string)
            else:
                logging.info("Dataset not found, skipping")
                continue
            
            final_ouput_dir = output_dir + '/' + 'exp' + e
            logging.info("Generating final output")
            if os.path.isdir(final_ouput_dir):
                shutil.rmtree(final_ouput_dir)
            else:
                os.path.os.mkdir(final_ouput_dir)
                shutil.copy2(dataset_string, final_ouput_dir)

        logging.info("Sets copied for " + m)
    return


'''
Generates output based on provided descriptors for specified modality
'''

def oddet_m_d():
    logging.info("Retrieving based on descriptors")
    global data_cfg

    for m in args.m:
        set_dir = dataset_cfg_dir+'/'+ m + '/'
        set_cfg_string = 'configs/sets/' + m + '.yml'

        if os.path.isfile(set_cfg_string) and os.path.exists(set_dir): 
            logging.info("Modality config and dataset found for " + m)
            temp_cfg = open(set_cfg_string, 'r')
            data_cfg = yaml.full_load(temp_cfg)
        else:
            logging.info("Modality " + m + " not found, skipping")
            continue

        descriptor_path = 'descriptors/' + m + '.yml'
        descriptor = None
        if os.path.isfile(descriptor_path):
            logging.info("Descriptor found for " + m)
            with open(descriptor_path, 'r') as des:
                descriptor = yaml.full_load(des)
        else:
            logging.info("No descriptor found. Skipping.")
            continue

        final_output_dir = output_dir + '/' + m +"_descriptor"
        if os.path.isdir(final_output_dir):
            shutil.rmtree(final_output_dir)
        os.mkdir(final_output_dir)

        if data_cfg["filetype"] == '.csv':
            for file in os.listdir(set_dir):
                newfile = os.path.splitext(file)[0] + "_descriptor" + data_cfg["filetype"]
                processed = pandas.read_csv(set_dir + '/' + file, 
                    usecols= descriptor["identifiers"] + descriptor["features"], low_memory=True)
                final_output = final_output_dir + '/' + newfile
                processed.to_csv(final_output)
                logging.info("Wrote successfully to " + final_output)

    return

'''
Gets features requested from experiments for specified modalities
'''
def oddet_m_e_f():
    global data_cfg

    for m in args.m: 
        set_dir = dataset_cfg_dir+'/'+ m + '/'
        set_cfg_string = 'configs/sets/' + m + '.yml'

        if os.path.isfile(set_cfg_string) and os.path.exists(set_dir): 
            logging.info("Modality config and dataset found for " + m)
            temp_cfg = open(set_cfg_string, 'r')
            data_cfg = yaml.full_load(temp_cfg)
        else:
            logging.info("Modality " + m + " not found, skipping")
            continue

        final_output_dir = output_dir + '/' + m + "_exp_features"
        if os.path.isdir(final_output_dir):
            shutil.rmtree(final_output_dir)
        os.mkdir(final_output_dir)

        for e in args.e:
            dataset_string = set_dir + m +'_exp' + e + data_cfg["filetype"]
            if os.path.isfile(dataset_string):
                logging.info("Dataset found for " + dataset_string)
            else:
                logging.info("Dataset not found, skipping")
                continue
           
            # if data_cfg["filetype"] == '.csv':
            #     filename = m + '_exp' + e + data_cfg["filetype"]
            #     final_output = final_output_dir + '/' + filename
            #     processed_ef = pandas.read_csv(dataset_string, usecols=data_cfg["identifiers"] + args.f, low_memory=True)
            #     processed_ef.to_csv(final_output)
            #     logging.info("Wrote successfully to " + final_output)

            if data_cfg["filetype"] == '.csv.gz':
                logging.info("Compressed CSV")
            if data_cfg["filetype"] == '.csv':
                logging.info("CSV file format")

            filename = m + '_exp' + e + data_cfg["filetype"]
            final_output = final_output_dir + '/' + os.path.splitext(filename)[0]
            logging.info("Generating output, please wait")
            processed_ef = pandas.read_csv(dataset_string, usecols=data_cfg["identifiers"] + args.f, compression='gzip', low_memory=True)
            processed_ef.to_csv(final_output)
            logging.info("Written successfully, exiting.")

    return



def oddet_m_f():
    for m in args.m: 
        set_dir = dataset_cfg_dir+'/'+ m + '/'
        set_cfg_string = 'configs/sets/' + m + '.yml'

        if os.path.isfile(set_cfg_string) and os.path.exists(set_dir): 
            logging.info("Modality config and dataset found for " + m)
            temp_cfg = open(set_cfg_string, 'r')
            data_cfg = yaml.full_load(temp_cfg)
        else:
            logging.info("Modality " + m + " not found, skipping")
            continue

        final_output_dir = output_dir + '/' + m + "_features"
        if os.path.isdir(final_output_dir):
            shutil.rmtree(final_output_dir)
        os.mkdir(final_output_dir)

        if data_cfg["filetype"] == '.csv':
            for file in os.listdir(set_dir):
                newfile = os.path.splitext(file)[0] + '_features' + data_cfg["filetype"]
                final_output = final_output_dir + '/' + newfile
                processed = pandas.read_csv(set_dir + '/' + file, usecols=data_cfg["identifiers"] + args.f, low_memory=True)
                processed.to_csv(final_output)
                logging.info("Wrote successfully to " + final_output)
    return


'''
General modality retrieval function calls the above functions
'''
 
def oddet_modality_get():
    if (len(sys.argv) < 3):
        logging.error("Not enough arguments. For usage, use flag -h.")
        return
    
    global data_cfg 
    descriptor = False
    dataset_string = ""

    if args.m is None:
        logging.info("No modality selected")
        return
    
    if (args.e is None) and (args.d is not True) and (args.f is None):
        logging.info("Only modality selected")
        input_char = input("Do you want to retrieve all set from " + str(args.m) + " ? [y/N]: ")
        if input_char == ('y' or 'Y'):
            oddet_m()
            return
        else:
            logging.info("Nothing to do. Exiting")
            return


    if (args.m is not None) and (args.e is not None) and (args.d is not True) and (args.f is None):
        input_char = input("Do you want to retrieve all sets from " + str(args.m) + " from experiments " + str(args.e) + " ? [y/N]: ")
        if input_char == ('y' or 'Y'):
            oddet_m_e()
        else:
            logging.info("Nothing to do. Exiting")
            return

    if (args.d is True):
        input_char = input("Do you want to retrieve from " + str(args.m) + " from descriptors? [y/N]: ")
        if input_char == ('y' or 'Y'):
            oddet_m_d()
        else:
            logging.info("Nothing to do. Exiting")
            return    
    
    if (args.d is not True) and (args.e is not None) and (args.f is not None):
        input_char = input("Retrieve features for modalities " + str(args.m) + " from experiments " + str(args.e) + " ? [y/N]: ")
        if input_char == ('y' or 'Y'):
            oddet_m_e_f()
        else:
            logging.info("Nothing to do. Exiting")
            return
    
    if (args.d is not True) and (args.e is None) and (args.f is not None):
        input_char = input("Retrieve features for all data for " + str(args.m) + " ? [y/N]: ")
        if input_char == ('y' or 'Y'):
            oddet_m_f()
        else:
            logging.info("Nothing to do. Exiting.")
            return
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


if __name__ == "__main__":
    main()
    exit()