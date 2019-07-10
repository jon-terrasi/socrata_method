#!/usr/bin/python
# NOTE: can run this script in ipython3 for easy setup with...
# [1]: %run socrata_method.py

import os, datetime, fnmatch, csv, hashlib
import argparse, shlex
from configparser import ConfigParser
import pandas as pd
from sodapy import Socrata

query_int = 200000
archive_int = 10
database = 'rsxa-ify5'

datasets = pd.read_csv('dataset_ids.csv', names=['ID', 'Name'])
db_name = datasets.Name.tolist()
db_code = datasets.ID.tolist() 
db_listing = dict(zip(db_code, db_name))

# flag and argument handling
parser = argparse.ArgumentParser(add_help=True, description='Welcome to socrata_method, a script for downloading, archiving, and comparing Chicago Data Portal datasets.')
parser.add_argument('-v', action='store_true', default=False, help='Display version information.')
parser.add_argument('-l', action='store_true', default=False, help='List available databases.')
parser.add_argument('-d', nargs=1, type=str, help='Specify remote database to query.', choices=db_code)
parser.add_argument('-n', nargs=1, type=int, help='Specify number of records to query.')
parser.add_argument('-k', nargs=1, type=int, help='Specify number of past dataset versions to archive.')
parser.add_argument('-w', action='store_true', default=False, help='Write arguments to config file.')
parser.add_argument('-c', action='store_true', default=False, help='Reads in config file for CLI flags/arguments.')
args = parser.parse_args()

version = '0.9'

if args.v:
    print(version)
    quit()

if args.l:
    print(db_listing)
    quit()

if args.n:
    query_int = args.n

if args.d:
    database = args.d 

if args.k:
    archive_int = args.k

passed = vars(args)
if args.w:
    print('Current CLI flags/arguments saved to .socrata config file. Pass "-c" to read from config.')
    f = open('.socrata', 'w')
    f.write('[cli]')
    f.write('\n')
    f.write('options = ')
    for k in passed:
        if passed[k] == True and k != 'w' and k != 'c':
            f.write('-')
            f.write(str(k))
            f.write(' ')
        if passed[k] != True and passed[k] != False:
            f.write('-')
            f.write(str(k))
            f.write(' ')
            f.write(str(passed[k]))
            f.write(' ')
    f.close()

if args.c:
    config = ConfigParser()
    config.read('.socrata')
    config_value = config.get('cli', 'options')

    argument_list = shlex.split(config_value)
    parser.parse_args(argument_list)

# create client object, with "None" for no authentication (public data only)
client = Socrata("data.cityofchicago.org", None)

# must set query_int to at least dataset size or only 1000 records returned
query = client.get(database, limit=query_int)

# [see sodapy .get() for more useful options]

# convert to DataFrame object
query_df = pd.DataFrame.from_records(query)

# export DataFrame to CSV file
query_df.to_csv(r'current.csv')

# create timestamp for file naming
ts = datetime.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')

# set current working directory, and pattern_csv to timestamped CSV files
files_list = os.listdir(os.getcwd())
pattern_csv = '*dataset.csv'
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
    os.rename('current.csv', ts + '_dataset.csv')
    quit()

# sort hash text files by modify time and assign latest to "previous_txt"
txt_list = sorted(txt_list, key=os.path.getmtime)
previous_txt = txt_list[-1]

# limit total number of CSV files to archive_int 
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
        os.rename('current.csv', ts + '_dataset.csv')
        quit()

print('No change to database since last execution.')
os.remove('current.csv')
current_csv.close()
previous_hashfile.close()
