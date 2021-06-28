# ODDET - Opera Dataset Data Extraction Tool
## Description
Data Extraction Tool for the Opera multi modality dataset for Wireless Sensing

## Features

## Todo

### File Naming
- Proposed file naming for files

- Proposed CSV layout:
```
[modality]_exp{number}.csv

e.g.
uwb1_exp001.csv
wificsi_exp013.csv
```

### Usage 

- Take in 3 main arguments
- Dataset descriptors are help in /sets
    -   These are stored as YAML files with separate sections for identifiers and feature listings
        This should make integration of new data quicker as little/no code needs to be used to 
        retrieve the data.
-   Right now YAML file is for bulk retrieval for specified data. So the '-f' flag is only used for 
    retrieving a small number of select features. However by using the YAML configuration you can 
    specify large groups of features to output with specific identifiers. This way you can prune out 
    features from sets that are not needed.

- Flags currently include:
    - -config: configure the dataset directory and the output directory via a selector
    - -clean: clears the entire output folder

    - -m: modalities 
    - -e: experiment numbers
    - -f: features
    - -d: descriptor usage

```
oddet.py -m [modality] -e [experiment_no]
oddet.py -m [modality] -e [experiment_no] -f [features] 
```

- Output - file.csv