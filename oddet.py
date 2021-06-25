#!/usr/bin/env python3

import os, sys, argparse, yaml, logging, pandas, shutil
from liboddet import parse

with open('configs/config.yml', 'r') as f:
    oddet_config = yaml.full_load(f)


logging.basicConfig(format='[ODDET] [%(levelname)8s]: %(message)s', level=logging.DEBUG) 


parser = argparse.ArgumentParser(description="Tool for data extraction of the Opera dataset.")
parser.add_argument('-m', help = 'Modality')
parser.add_argument('-e', help='Experiment number')
parser.add_argument('-f', nargs='+', help='Feature list to be extracted')
parser.add_argument('-d', help='Descriptor to extract according to')
parser.add_argument('-a', help='Activity to be searched')
parser.add_argument('-o', help='Specify output directory')

###################
global args
global dataset_cfg_dir, data_cfg
global output_dir
global dataset_extension

###################

def parse_config():
    global dataset_cfg_dir, output_dir
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
                return
        else:
            logging.info("Output directory not created")
            return


#############################################################################


def oddet_get():
    if (len(sys.argv) < 3):
        logging.error("Not enough arguments. For usage, use flag -h.")
        return
    
    global data_cfg
    descriptor = False
    dataset_string = ""

    if not (args.m == None): 
        set_dir = dataset_cfg_dir+'/'+ args.m + '/'
        set_cfg_string = 'configs/sets/' + args.m + '.yml'
    else: 
        logging.error("No modality listed, exiting.")
        return

    if os.path.isfile(set_cfg_string): 
        logging.info("Dataset config found")
        temp_cfg = open(set_cfg_string, 'r')
        data_cfg = yaml.full_load(temp_cfg)
    else:
        logging.error("No dataset config specified. Exiting.")
        return

    if not (args.e == None):
        dataset_string = set_dir + args.m + '_exp' + args.e +'.csv'
        if os.path.isfile(dataset_string):
            logging.info("Dataset found")         
        else:
            logging.error("Dataset for not found, ensure file location is correct. Exiting.")
            return

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
            return
            

    if (args.f == None) and (args.d == None):
        logging.info("Retrieving entire set of " + args.m + '_exp' + args.e)
        prompt = input("Do you want to retrieve the whole set? [y/N]: ")
        if prompt == ('y' or 'Y'): 
            shutil.copy2(dataset_string, output_dir)
            print(output_dir+'/'+args.m+'_exp' + args.e +'.csv')
            if os.path.isfile(output_dir+'/'+args.m+'_exp' + args.e + '.csv'):
                logging.info("Dataset written to " + output_dir +". Exiting.")
        else:
            logging.info("Nothing retrieved. Exiting.")
            return

    elif (args.f != None):
        logging.info("Retrieving set of features")

    return









####################################################################

def main():
    print("***** ODDET Extraction Tool *****")
    global args
    if len(sys.argv) < 2:
        parser.print_help()
        exit()
    parse_config()
    args = parser.parse_args()

    logging.info("ODDET Getting data:")
    oddet_get()

if __name__ == "__main__":
    main()
    print('')
    exit()