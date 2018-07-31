# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 01:44:21 2018

@author: Ben Zhao
"""
from datetime import datetime
import time
import csv
from yoweb_crewpage import retrieve_crew_info


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