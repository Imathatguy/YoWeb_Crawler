# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 00:28:54 2018

@author: Ben Zhao
"""

import pandas as pd
import csv


# Input: pirate name
# Returns: [[crew_rank, crew, flag_rank, flag], dictionary of pirate stats]
def retrieve_pirate_info(pirate_name):
    url = (
        r'http://obsidian.puzzlepirates.com/yoweb/pirate.wm?' +
        r'classic=false&target=%s' % pirate_name
    )

    return_data = []
    puzzle_list = ['Sailing', 'Rigging', 'Carpentry', 'Patching',
                   'Bilging', 'Gunning', 'Treasure Haul', 'Navigating',
                   'Battle Navigation', 'Swordfighting', 'Rumble']

    tables = pd.read_html(url)  # Returns list of all tables on page

    # Affiliation Extraction
    affiliation = tables[0][2][0].split('  ')

    if affiliation[0] == 'Independent Pirate':
        return_data.append(affiliation[0])
    else:
        crew_rank = affiliation[0].split(' of the crew ', 1)[0].split(' and ')[0]
        crew = affiliation[0].split(' of the crew ', 1)[1]
        if ' of the flag ' not in affiliation[1]:
            flag_rank = ''
            flag = ''
        else:
            flag_rank = affiliation[1].split(' of the flag ', 1)[0]
            flag = affiliation[1].split(' of the flag ', 1)[1]
        # [crew_rank, crew, flag_rank, flag]
        return_data.append([crew_rank, crew, flag_rank, flag])

    # Statistics
    for n, row in enumerate(tables[0][0]):
        if row == row and 'Piracy Skills' in row:
            break
    stats = row.split('  ')
    ocean_stats = [stat for stat in stats if "/" in stat]
    stats_dict = {puzzle: stat for puzzle, stat in zip(puzzle_list,
                                                       ocean_stats)}
    return_data.append(stats_dict)

    return return_data


if __name__ == '__main__':
    pirate_name = 'Wazoo'
    print retrieve_pirate_info(pirate_name)

    # Select Tables of Interest
#    total_numbers_table = tables[6]
#    jobber_list_table = tables[8]
#
#    # Parse pd df into basic dict
#    # Numbers
#    total_numbers_dict = {}
#    for i, row in total_numbers_table.iterrows():
#        total_numbers_dict[row[0].strip(':')] = int(row[1])
#
#    # Users
#    jobber_list_dict = {}
#    rank = None
#    for i, row in jobber_list_table.iterrows():
#        # Ignore table row with no entries (nan)
#        if pd.isna(row).all():
#            continue
#        # Ignore table row with duplicate rank
#        if row.dropna().duplicated().any():
#            continue
#        # Check rank bracket
#        if row.dropna().values[0] in total_numbers_dict:
#            rank = row.dropna().values[0]
#            jobber_list_dict[rank] = []
#            continue
#        # Row should contain users
#        for user in row.dropna().values:
#            jobber_list_dict[rank].append(user)
#
#    return jobber_list_dict, total_numbers_dict
