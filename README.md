# socrata_method

*socrata_method* is a short Python script for regularly downloading datasets from online data portals as CSV files to check for differences over time.

## Overview

The script is intended to be run regularly, and compares newly downloaded datasets against existing (local) ones to detect changes since prior executions of the script. On detection of recent changes, a full copy of the newly downloaded dataset is saved in a timestamped CSV file in the directory in which the script was executed, and a plaintext MD5 hash file of the newly downloaded dataset (with the same timestamp) is saved separately in the same directory. This MD5 hash file is then used for efficient comparison with future CSV files. 

## Recommended Usage

Because the script compares lines from the previous downloaded dataset to the newly downloaded dataset from the end of the file going backward, it is recommended to run the script once every 2-3 days in order to avoid missing incremental published updates to the dataset (as only the most recent new line will trigger retention). On Unix-like systems, it may be useful to set up a cron job to automate this process.

## Dependencies

*socrata_method* is written to function with Python 3 (tested using Python 3.6.8). Python 2.7 compliance will require alteration.

The following Python modules are required for the script to function.
- argparse
- configparser
- csv
- datetime
- fnmatch
- hashlib
- os
- pandas
- shlex
- sodapy

## Caveats and Future Development

By default, the *socrata_methods* script downloads the Contracts database from the City of Chicago's open data portal, but offers the option to download from other City of Chicago databases as defined in its accompanying *dataset_ids.csv* file. For those wishing to employ the script for databases not included in this file, review the target database's documentation to confirm compatibility with database access tools provided in *pandas*, follow the appropriate instructions, and add the database ID string and database name to the local copy of *dataset_ids.csv*. 

NOTE: Passing the ID string directly along with the "-d" flag will throw an error, as the script only accepts database ID strings contained within the first column of the *dataset_id.csv* file.

The script also iteratively check datasets line-by-line from the end of the file going backward until a change is detected. This line comparison is performed using hashed copies of the database for faster analysis. In order to archive historical states of published datasets and avoid missing incremental changes to these datasets over time, it is recommended to run the script every 2-3 days. 

At present, the script is designed to track changes in a single database at a time, and as such does not accommodate different file naming schemes for differentiating multiple databases. This may be addressed in future versions of the script, but for now, users who wish to use the script to monitor several databases are encouraged to run the script for different databases in separate directories, respectively.
