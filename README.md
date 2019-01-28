# socrata_method

*socrata_method* is a short Python script for regularly downloading datasets from online data portals as CSV files.

## Overview

The script is intended to be run regularly, and compares newly downloaded datasets against existing (local) ones to detect changes since prior executions of the script. On detection of recent changes, a full copy of the newly downloaded dataset is saved in a timestamped CSV file in the directory in which the script was executed, and the altered/new lines from that new dataset are saved in a separate timestamped CSV in the same directory. 

## Recommended Usage

Because the script compares the last 100 lines of the most recent pre-existing copy of a dataset and the newly downloaded one, it is recommended to run the script once every 3-4 days. On Unix-like systems, it may be useful to set up a cron job to automate this process.

## Dependencies

The following Python modules are required for the script to function.
- datetime
- csv
- fnmatch
- os
- pandas
- sodapy

## Caveats and Future Development

At present, the primary *socrata_methods* Python script downloads exclusively from the Contracts database from the City of Chicago's open data portal. For those wishing to employ the script for other databases, review the target database's documentation to confirm compatibility with database access tools provided in *pandas* and follow the appropriate instructions. Future development plans will include functionality for specifying different City of Chicago datasets. 

The script also currently only checks the last 100 lines of CSV files being compared. If you wish to query the Contracts database with less than the recommended frequency (every 2-3 days), it is suggested that you edit the script to check more lines, though this will increase the execution time for the script. In the future, the script will be re-worked to iteratively check lines from the end of the file going backward until a change is detected for increased efficiency and flexibility. 
