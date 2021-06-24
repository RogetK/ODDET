import os
import sys
import argparse
import yaml
import logging

with open('config.yml', 'r') as f:
    config = yaml.full_load(f)


logging.basicConfig(format='[ODDET] [%(levelname)8s]: %(message)s', level=logging.DEBUG) 
oddet_parser = argparse.ArgumentParser(description="Tool for data extraction of the Opera dataset.")


oddet_parser.add_argument('get', nargs='+', help = 'Find and output specified set')

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
    if (len(args.get) < 2):
        logging.error("Not enough arguments.")
        logging.error("This function takes: oddet.py get [modality] [experiment] [feature 1] ... ")
    else:
        pass
    

        return









####################################################################

def main():
    print("***** ODDET Extraction Tool *****")
    global args
    if len(sys.argv) < 2:
        oddet_parser.print_help()
        exit()
    parse_config()
    args = oddet_parser.parse_args()

    if args.get:
        logging.info("ODDET Getting data:")
        oddet_get()

if __name__ == "__main__":
    main()
    print('')
    exit()