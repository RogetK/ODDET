# ODDET - Opera Dataset Data Extraction Tool
## Description
Opera Dataset Data Extraction Tool

## Features

## Todo

### File Naming
- Proposed file naming 

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
```
oddet.py -m [modality] -e [experiment_no] -f [features] 
```

- Output - file.csv