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

# set current working directory, and pattern1_str to timestamped CSV files
files_list = os.listdir(os.getcwd())
pattern1_str = '*contracts.csv'

# create list of CSV files in directory
csv_list = []
for entry in files_list:
    if fnmatch.fnmatch(entry, pattern1_str):
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

# open updates.csv for writing
updates_csv = open('updates.csv', 'w')
updates_csv.write(now[0])

# write non-matching lines to "updates.csv"
compare_int = 100
for line in now[-compare_int:]:
    if line not in prev[-compare_int:]:
        updates_csv.write(line)

# close and reopen updates.csv for reading
updates_csv.close()
updates_csv = open('updates.csv', 'r')

# if "updates.csv" contains updated records, close and rename with timestamp
# else, remove "updates.csv" and "now.csv" temporary file
if len(updates_csv.readlines()) > 1:
    print('Chicago Contracts database updated since last execution.')
    updates_csv.close()
    os.rename('updates.csv', ts + '_updates.csv')
    prev_csv.close()
    now_csv.close()
    os.rename('now.csv', ts + '_contracts.csv')
else:
    print('No change to database since last execution.')
    updates_csv.close()
    os.remove('updates.csv')
    os.remove('now.csv')
    prev_csv.close()
    now_csv.close()

# limit total number of *updates.csv files to archive_int
pattern2_str = '*updates.csv'
update_list = []
for entry in files_list:
    if fnmatch.fnmatch(entry, pattern2_str):
        update_list += entry.split('\n')

if len(update_list) > archive_int:
    print('More than', archive_int, 'archived *updates.csv files.')
    os.remove(update_list[0:-(archive_int)])
