# -*- coding: utf-8 -*-
"""
Created on Sun Jul 22 23:45:56 2018

@author: Imathatguy

For Crew page crawling of data.

This script is a sample to crawl the webpages of yoweb.

TODO: > Avoid getting banned by OMs for botting
TODO: - check with OMs what the web request limitation is.
TODO: > Expand beyond crew information
TODO: - grab per user details from pirate pages
TODO: - support list of crews
TODO: - loop over specified time delay
TODO: - plotting of statistics over time.
"""
import pandas as pd
from datetime import datetime
import time
import csv

def retrieve_crew_info(crew_id):
    url = (
        r'http://obsidian.puzzlepirates.com/yoweb/crew/info.wm'
        r'?crewid=%s&classic=false' % crew_id
    )
    tables = pd.read_html(url)  # Returns list of all tables on page

    # Select Tables of Interest
    total_numbers_table = tables[6]
    jobber_list_table = tables[8]

    # Parse pd df into basic dict
    # Numbers
    total_numbers_dict = {}
    for i, row in total_numbers_table.iterrows():
        total_numbers_dict[row[0].strip(':')] = int(row[1])

    # Users
    jobber_list_dict = {}
    rank = None
    for i, row in jobber_list_table.iterrows():
        # Ignore table row with no entries (nan)
        if pd.isna(row).all():
            continue
        # Ignore table row with duplicate rank
        if row.dropna().duplicated().any():
            continue
        # Check rank bracket
        if row.dropna().values[0] in total_numbers_dict:
            rank = row.dropna().values[0]
            jobber_list_dict[rank] = []
            continue
        # Row should contain users
        for user in row.dropna().values:
            jobber_list_dict[rank].append(user)

    return jobber_list_dict, total_numbers_dict


if __name__ == '__main__':
    # crew_id = 5001832  # Consider it Drunk
    # crew_id = 5000435  # The Southsea Bandits
    # crew_id = 5001990  # The Organization
    n = 0
    while True:

        now_time = datetime.utcnow().strftime('%d/%m/%y-%H:%M:%S')

        with open("bandits_job.csv", "ab") as crew_file:
            writer = csv.writer(crew_file, delimiter=',', quotechar="\"",
                                quoting=csv.QUOTE_NONNUMERIC)
            job_list, tot_num = retrieve_crew_info(5000435)
            line = [now_time, n]
            line.append(tot_num.get("Jobbing Pirate", 0))
            line.extend(job_list.get("Jobbing Pirate", ""))
            writer.writerow(line)

        with open("CIS_job.csv", "ab") as crew_file:
            writer = csv.writer(crew_file, delimiter=',', quotechar="\"",
                                quoting=csv.QUOTE_NONNUMERIC)
            job_list, tot_num = retrieve_crew_info(5001832)
            line = [now_time, n]
            line.append(tot_num.get("Jobbing Pirate", 0))
            line.extend(job_list.get("Jobbing Pirate", ""))
            writer.writerow(line)

        with open("GW_job.csv", "ab") as crew_file:
            writer = csv.writer(crew_file, delimiter=',', quotechar="\"",
                                quoting=csv.QUOTE_NONNUMERIC)
            job_list, tot_num = retrieve_crew_info(5001990)
            line = [now_time, n]
            line.append(tot_num.get("Jobbing Pirate", 0))
            line.extend(job_list.get("Jobbing Pirate", ""))
            writer.writerow(line)

        sleeptime = 60 - datetime.utcnow().second
        time.sleep(sleeptime)

        n += 1
