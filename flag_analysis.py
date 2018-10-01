# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 23:23:30 2018

@author: Ben Zhao
"""

from datetime import datetime
import time
import csv
import os
from yoweb import base

other_holder = []
cis_holder = []
index = []

start_minute = 0

destination = "./MEL_TRIPLEDROP/"

ocean = base.Ocean('Obsidian')

with open("%sLB_job.csv"%destination, 'r') as csvfile:
    crew_reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    for row in crew_reader:
        if int(row[1]) < start_minute:
            continue

        if len(row) > 3:
            other_holder.append(row[3:])
        else:
            other_holder.append([])

with open("%sCiS_job.csv"%destination, 'r') as csvfile:
    crew_reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    for row in crew_reader:
        if int(row[1]) < start_minute:
            continue

        if len(row) > 3:
            cis_holder.append(row[3:])
        else:
            cis_holder.append([])
        index.append(int(row[1]))


other_jobbers = []
for t_jobbers in other_holder:
    other_jobbers.extend(t_jobbers)
cis_jobbers = []
for t_jobbers in cis_holder:
    cis_jobbers.extend(t_jobbers)

cis_jobbers = set(cis_jobbers)
other_jobbers = set(other_jobbers)


cis_only = cis_jobbers.difference(other_jobbers)
both = cis_jobbers.intersection(other_jobbers)
other_only = other_jobbers.difference(cis_jobbers)
total = cis_jobbers.union(other_jobbers)

print("CIS Only: %s"% str(len(cis_only)))
print("Both: %s" % len(both))
print("LB Only: %s" % len(cis_only))

# Don't repeat spam yoweb
if 'pirate_data_holder' not in globals():
    pirate_data_holder = {}

# Only request pirates not in our dictionary
for n, pirate_name in enumerate(total):
    if pirate_name in pirate_data_holder:
        continue
    else:

        pirate_stats = ocean.getpirate(pirate_name)
        pirate_data_holder[pirate_name] = pirate_stats


cis_only_flags_numbers = {}
cis_only_flags_jobbers = {}
for pirate_name in cis_only:
    pirate_data = pirate_data_holder[pirate_name]
    flag = pirate_data.affiliations.flag.name

    cis_only_flags_numbers[flag] = cis_only_flags_numbers.get(flag, 0) + 1
    if flag not in cis_only_flags_jobbers:
        cis_only_flags_jobbers[flag] = []
    cis_only_flags_jobbers[flag].append(pirate_name)


both_flags_numbers = {}
both_flags_jobbers = {}
for pirate_name in both:
    pirate_data = pirate_data_holder[pirate_name]
    flag = pirate_data.affiliations.flag.name

    both_flags_numbers[flag] = both_flags_numbers.get(flag, 0) + 1
    if flag not in both_flags_jobbers:
        both_flags_jobbers[flag] = []
    both_flags_jobbers[flag].append(pirate_name)


other_only_flags_numbers = {}
other_only_flags_jobbers = {}
for pirate_name in other_only:
    pirate_data = pirate_data_holder[pirate_name]
    flag = pirate_data.affiliations.flag.name

    other_only_flags_numbers[flag] = other_only_flags_numbers.get(flag, 0) + 1
    if flag not in other_only_flags_jobbers:
        other_only_flags_jobbers[flag] = []
    other_only_flags_jobbers[flag].append(pirate_name)


full_results = {'LB': {'numbers': other_only_flags_numbers, 'jobbers': other_only_flags_jobbers},
                'CIS': {'numbers': cis_only_flags_numbers, 'jobbers': cis_only_flags_jobbers},
                'BOTH': {'numbers': both_flags_numbers, 'jobbers': both_flags_jobbers}}

print(full_results)

import Pickle
Pickle.dump(full_results, open("full_results.pickle", "w"))