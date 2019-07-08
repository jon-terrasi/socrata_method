# socrata_method

*socrata_method* is a short Python script for regularly downloading datasets from online data portals as CSV files.

## Overview

The script is intended to be run regularly, and compares newly downloaded datasets against existing (local) ones to detect changes since prior executions of the script. On detection of recent changes, a full copy of the newly downloaded dataset is saved in a timestamped CSV file in the directory in which the script was executed, and the altered/new lines from that new dataset are saved in a separate timestamped CSV in the same directory.

## Recommended Usage

Because the script compares lines from the previous downloaded dataset to the newly downloaded dataset from the end of the file going backward, it is recommended to run the script once every 2-3 days in order to avoid missing incremental published updates to the dataset (as only the most recent new line will trigger retention). On Unix-like systems, it may be useful to set up a cron job to automate this process.

## Dependencies

The following Python modules are required for the script to function.
- argparse
- configparser
- datetime
- csv
- fnmatch
- hashlib
- os
- pandas
- shlex
- sodapy

## Caveats and Future Development

By default, the *socrata_methods* Python script downloads the Contracts database from the City of Chicago's open data portal, but offers the option to download from other City of Chicago databases as defined in its accompanying *dataset_ids.csv* file. For those wishing to employ the script for databases not included in this file, review the target database's documentation to confirm compatibility with database access tools provided in *pandas*, follow the appropriate instructions, and add the database ID string and database name to the local copy of *dataset_ids.csv*. Users are also free to pass the ID string directly along with the "-d" flag, but this is not recommended.

The script also iteratively check datasets line-by-line from the end of the file going backward until a change is detected. This line comparison is performed using hashed copies of the database for faster analysis. In order to archive historical states of published datasets and avoid missing incremental changes to these datasets over time, it is recommended to run the script every 2-3 days. 

At present, the script is designed to track changes in a single database, and as such does not accommodate different file naming schemes for differentiating multiple databases. This may be addressed in future versions of the script, but for now, users who wish to use the script to monitor several databases are encouraged to manually change filenames, or to run the script for different databases in separate directories, respectively.
