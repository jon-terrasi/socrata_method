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
query = client.get("b6tt-rgti", limit=query_int)

# [see sodapy .get() for more useful options]

# convert to DataFrame object
query_df = pd.DataFrame.from_records(query)

# export DataFrame to CSV file
query_df.to_csv(r'current.csv')

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
    current_csv = open('current.csv', 'r')
    current = current_csv.readlines()
    current_hash = []
    for line in current:
        result = hashlib.md5(line.encode()).digest()
        current_hash.append(result)
    f = open(ts + '_hash.txt', 'w')
    for element in current_hash:
        f.write("%s\n" % element)
    f.close()
    current_csv.close()
    os.rename('current.csv', ts + '_contracts.csv')
    quit()

# sort hash text files by modify time and assign latest to "previous_txt"
txt_list = sorted(txt_list, key=os.path.getmtime)
previous_txt = txt_list[-1]

# limit total number of CSV files to archive_int 
archive_int = 10
if len(csv_list) > archive_int:
    print('More than', archive_int, 'copies of previous database.')
    os.remove(csv_list[0:-(archive_int + 1)])

# open previous txt hash file, create txt hash file for current.csv
previous_hashfile = open(previous_txt, 'r')
current_csv = open('current.csv', 'r')

previous = previous_hashfile.readlines()
current = current_csv.readlines()

previous_hash = []
for line in previous:
    previous_hash.append(line)

current_hash = []
for line in current:
    result = hashlib.md5(line.encode()).digest()
    current_hash.append(result)

# compare "current" to "previous" in reverse order, break loop first new line 
for line in reversed(current_hash):
    if line not in reversed(previous_hash):
        print('Chicago Contracts database updated since last execution.')
        current_csv.close()
        f = open(ts + '_hash.txt', 'w')
        for element in current_hash:
            f.write("%s\n" % element)
        f.close()
        previous_hashfile.close()
        os.rename('current.csv', ts + '_contracts.csv')
        quit()

print('No change to database since last execution.')
os.remove('current.csv')
current_csv.close()
previous_hashfile.close()
