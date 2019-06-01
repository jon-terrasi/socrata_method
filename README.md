# socrata_method

*socrata_method* is a short Python script for regularly downloading datasets from online data portals as CSV files.

## Overview

The script is intended to be run regularly, and compares newly downloaded datasets against existing (local) ones to detect changes since prior executions of the script. On detection of recent changes, a full copy of the newly downloaded dataset is saved in a timestamped CSV file in the directory in which the script was executed, and the altered/new lines from that new dataset are saved in a separate timestamped CSV in the same directory.

## Recommended Usage

Because the script compares lines from the previous downloaded dataset to the newly downloaded dataset from the end of the file going backward, it is recommended to run the script once every 2-3 days in order to avoid missing incremental published updates to the dataset (as only the most recent new line will trigger retention). On Unix-like systems, it may be useful to set up a cron job to automate this process.

## Dependencies

The following Python modules are required for the script to function.
- datetime
- csv
- fnmatch
- hashlib
- os
- pandas
- sodapy

## Caveats and Future Development

At present, the primary *socrata_methods* Python script downloads exclusively from the Contracts database from the City of Chicago's open data portal. For those wishing to employ the script for other databases, review the target database's documentation to confirm compatibility with database access tools provided in *pandas* and follow the appropriate instructions. Future development plans will include functionality for specifying different City of Chicago datasets using their respective "dataset IDs" as listed in the Chicago Data Portal API Documentation pages.

The script also iteratively check datasets line-by-line from the end of the file going backward until a change is detected. This line comparison is performed using hashed copies of the database for faster analysis. In order to archive historical states of published datasets and avoid missing incremental changes to these datasets over time, it is recommended to run the script every 2-3 days. In future versions of this script, flags will allow users to set the number of previously downloaded copies of the dataset to archive.
