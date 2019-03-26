#!/usr/bin/python
# NOTE: can run this script in ipython3 for easy setup with...
# [1]: %run chicago_contracts_downloader.py

# TODO
# -> compare "prev" and "now" CSVs from end to beginning (i.e. backwards)
# -> compare lines using md5 hashing

import os, datetime, fnmatch, csv
import pandas as pd
from sodapy import Socrata

# create client object, with "None" for no authentication (public data only)
client = Socrata("data.cityofchicago.org", None)

# must set query_int to at least dataset size or only 1000 records returned
query_int = 200000
results = client.get("b6tt-rgti", limit=query_int)

# [see sodapy .get() for more useful options]

# convert to DataFrame object
results_df = pd.DataFrame.from_records(results)

# change NaN to 0
#results_df = results_df.fillna(0)

# export DataFrame to CSV file
results_df.to_csv(r'now.csv')

# create timestamp for file naming
ts = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

# set current working directory, and pattern_str to timestamped CSV files
files_list = os.listdir(os.getcwd())
pattern_str = '*contracts.csv'

# create list of CSV files in directory
csv_list = []
for entry in files_list:
    if fnmatch.fnmatch(entry, pattern_str):
        csv_list += entry.split('\n')

# in case of no pre-existing database, download current copy and exit
if len(csv_list) == 0:
    print('No pre-existing CSV databases found.')
    os.rename('now.csv', ts + '_contracts.csv')
    quit()

# sort by modify time and save latest to "prev_csv"
csv_list = sorted(csv_list, key=os.path.getmtime)
prev_csv = csv_list[-1]

# limit total number of CSV files to archive_int 
archive_int = 10
if len(csv_list) > archive_int:
    print('More than', archive_int, 'copies of prev database.')
    os.remove(csv_list[0:-(archive_int + 1)])

# open newest preexisting local copy ("prev_csv"), downloaded copy ("now_csv")
prev_csv = open(prev_csv, 'r')
now_csv = open('now.csv', 'r')

# read in old and new CSV files
prev = prev_csv.readlines()
now = now_csv.readlines()

# compare "now" to "prev" in reverse order, break loop at first new line 
for line in reversed(now):
    if line not in reversed(prev):
        print('Chicago Contracts database updated since last execution.')
        prev_csv.close()
        now_csv.close()
        os.rename('now.csv', ts + '_contracts.csv')
        quit()

print('No change to database since last execution.')
os.remove('now.csv')
prev_csv.close()
now_csv.close()
