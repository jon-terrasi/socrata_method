#!/usr/bin/python
# NOTE: can run this script in ipython3 for easy setup with...
# [1]: %run chicago_contracts_downloader.py

import os, datetime, fnmatch, csv, hashlib
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

# set current working directory, and pattern_csv to timestamped CSV files
files_list = os.listdir(os.getcwd())
pattern_csv = '*contracts.csv'
pattern_txt = '*.txt'

# create list of CSV files in directory
csv_list = []
for entry in files_list:
    if fnmatch.fnmatch(entry, pattern_csv):
        csv_list += entry.split('\n')

txt_list = []
for entry in files_list:
    if fnmatch.fnmatch(entry, pattern_txt):
        txt_list += entry.split('\n')

# in case of no pre-existing database, download current copy and exit
if len(csv_list) == 0 and len(txt_list) == 0:
    print('No pre-existing CSV databases or hash files found.')
    now_csv = open('now.csv', 'r')
    now = now_csv.readlines()
    now_hash = []
    for line in now:
        result = hashlib.md5(line.encode()).digest()
        now_hash.append(result)
    f = open(ts + '_hash.txt', 'w')
    for element in now_hash:
        f.write("%s\n" % element)
    f.close()
    now_csv.close()
    os.rename('now.csv', ts + '_contracts.csv')
    quit()

# sort by modify time and save latest to "prev_csv"
txt_list = sorted(txt_list, key=os.path.getmtime)
prev_txt = txt_list[-1]

# limit total number of CSV files to archive_int 
archive_int = 10
if len(csv_list) > archive_int:
    print('More than', archive_int, 'copies of prev database.')
    os.remove(csv_list[0:-(archive_int + 1)])

# open previous txt hash file, create txt hash file for now.csv
prev_hashfile = open(prev_txt, 'r')
now_csv = open('now.csv', 'r')

prev = prev_hashfile.readlines()
now = now_csv.readlines()

prev_hash = []
for line in prev:
    prev_hash.append(line)

now_hash = []
for line in now:
    result = hashlib.md5(line.encode()).digest()
    now_hash.append(result)

# compare "now" to "prev" in reverse order, break loop at first new line 
for line in reversed(now_hash):
    if line not in reversed(prev_hash):
        print('Chicago Contracts database updated since last execution.')
        now_csv.close()
        f = open(ts + '_hash.txt', 'w')
        for element in now_hash:
            f.write("%s\n" % element)
        f.close()
        prev_hashfile.close()
        os.rename('now.csv', ts + '_contracts.csv')
        quit()

print('No change to database since last execution.')
os.remove('now.csv')
now_csv.close()
prev_hashfile.close()
