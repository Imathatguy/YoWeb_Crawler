# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 23:23:30 2018

@author: Ben Zhao
"""

import csv
import time
from yoweb_piratepage import retrieve_pirate_info


gw_holder = []
cis_holder = []
index = []

start_minute = 90

with open('GW_job.csv', 'rb') as csvfile:
    crew_reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    for row in crew_reader:
        if row[1] < start_minute:
            continue

        if len(row) > 3:
            gw_holder.append(row[3:])
        else:
            gw_holder.append([])

with open('CIS_job.csv', 'rb') as csvfile:
    crew_reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    for row in crew_reader:
        if row[1] < start_minute:
            continue

        if len(row) > 3:
            cis_holder.append(row[3:])
        else:
            cis_holder.append([])
        index.append(int(row[1]))


gw_jobbers = []
for t_jobbers in gw_holder:
    gw_jobbers.extend(t_jobbers)
cis_jobbers = []
for t_jobbers in cis_holder:
    cis_jobbers.extend(t_jobbers)

cis_jobbers = set(cis_jobbers)
gw_jobbers = set(gw_jobbers)


cis_only = cis_jobbers.difference(gw_jobbers)
both = cis_jobbers.intersection(gw_jobbers)
gw_only = gw_jobbers.difference(cis_jobbers)
total = cis_jobbers.union(gw_jobbers)

print "CIS Only: %s" % len(cis_only)
print "Both: %s" % len(both)
print "GW Only: %s" % len(cis_only)

# Don't repeat spam yoweb
if 'pirate_data_holder' not in globals():
    pirate_data_holder = {}

# Only request pirates not in our dictionary
for n, pirate_name in enumerate(total):
    # print "%s/%s %s" % (n, len(total)-1, pirate_name)
    if pirate_name in pirate_data_holder:
        continue
    else:
        pirate_stats = retrieve_pirate_info(pirate_name)
        pirate_data_holder[pirate_name] = pirate_stats


cis_only_flags_numbers = {}
cis_only_flags_jobbers = {}
for pirate_name in cis_only:
    pirate_data = pirate_data_holder[pirate_name]
    if pirate_data[0] == 'Independent Pirate':
        flag = pirate_data[0]
    else:
        flag = pirate_data[0][3]

    cis_only_flags_numbers[flag] = cis_only_flags_numbers.get(flag, 0) + 1
    if flag not in cis_only_flags_jobbers:
        cis_only_flags_jobbers[flag] = []
    cis_only_flags_jobbers[flag].append(pirate_name)


both_flags_numbers = {}
both_flags_jobbers = {}
for pirate_name in both:
    pirate_data = pirate_data_holder[pirate_name]
    if pirate_data[0] == 'Independent Pirate':
        flag = pirate_data[0]
    else:
        flag = pirate_data[0][3]

    both_flags_numbers[flag] = both_flags_numbers.get(flag, 0) + 1
    if flag not in both_flags_jobbers:
        both_flags_jobbers[flag] = []
    both_flags_jobbers[flag].append(pirate_name)


gw_only_flags_numbers = {}
gw_only_flags_jobbers = {}
for pirate_name in gw_only:
    pirate_data = pirate_data_holder[pirate_name]
    if pirate_data[0] == 'Independent Pirate':
        flag = pirate_data[0]
    else:
        flag = pirate_data[0][3]

    gw_only_flags_numbers[flag] = gw_only_flags_numbers.get(flag, 0) + 1
    if flag not in gw_only_flags_jobbers:
        gw_only_flags_jobbers[flag] = []
    gw_only_flags_jobbers[flag].append(pirate_name)


full_results = {'GW': {'numbers': gw_only_flags_numbers, 'jobbers': gw_only_flags_jobbers},
                'CIS': {'numbers': cis_only_flags_numbers, 'jobbers': cis_only_flags_jobbers},
                'BOTH': {'numbers': both_flags_numbers, 'jobbers': both_flags_jobbers}}
