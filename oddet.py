import os
import sys
import argparse
import yaml
import logging

from liboddet import parse

with open('config.yml', 'r') as f:
    config = yaml.full_load(f)


logging.basicConfig(format='[ODDET] [%(levelname)8s]: %(message)s', level=logging.DEBUG) 


parser = argparse.ArgumentParser(description="Tool for data extraction of the Opera dataset.")
parser.add_argument('-m', help = 'Modality')
parser.add_argument('-e', type=int, help='Experiment number')
parser.add_argument('-f', nargs='+', help='Feature list to be extracted')
parser.add_argument('-a', help='Activity to be searched')

###################
global args
global dataset_dir
global output_dir

###################

def parse_config():
    global dataset_dir, output_dir
    dataset_dir = config["dataset_dir"]
    output_dir = config["output_dir"]

    logging.info("Looking for dataset ...")
    if os.path.isdir(dataset_dir):
        logging.info("Dataset directory: " + dataset_dir)
    else:
        logging.error('Dataset not found.')

    if os.path.isdir(output_dir):
        logging.info("Output directory: " + output_dir)
    else: 
        logging.error("Output directory not found.")
        response = input("Create output directory? [y/N]")
        print(response)
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




def oddet_get():
    set_dir = dataset_dir+'/'+ args.m
    set_string = 'sets/'+ args.m +'.yml'
    print(set_dir)
    print(set_string)

    if (len(sys.argv) < 3):
        logging.error("Not enough arguments. For usage, use flag -h.")
        return

    logging.info("Finding " + args.m[1] + " dataset")
    if os.path.isfile(set_string): 
        logging.info("Dataset descriptor found and loading info ...")
        dataset = open(set_string, 'r')
        data = yaml.full_load(dataset)



             

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