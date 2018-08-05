# -*- coding: utf-8 -*-
"""
Created on Wed Aug  1 01:44:21 2018

@author: Ben Zhao
"""
from datetime import datetime
import time
import csv
import os
from yoweb import base


if __name__ == '__main__':
    tracker_list = {5001832: ("Consider it Drunk", "CiD"),
                    5000435: ("The Southsea Bandits", "TSB"),
                    5001990: ("The Organization", "TO")}

    destination = "./MEL_IV/"
    if not os.path.exists(destination):
        os.makedirs(destination)

    n = 0
    ocean = base.Ocean('Obsidian')

    while True:
        now_time = datetime.utcnow().strftime('%d/%m/%y-%H:%M:%S')

        for (crew_id, (crew_name, crew_short)) in tracker_list.items():

            print(crew_id, crew_name, crew_short)
            with open("%s%s_job.csv" % (destination, crew_short), "a") as crew_file:
                writer = csv.writer(crew_file, delimiter=',', quotechar="\"",
                                    lineterminator="\n",
                                    quoting=csv.QUOTE_NONNUMERIC)
                crew_base = ocean.getcrew(crew_id)
                line = [now_time, n]
                
                # Jobber Numbers
                try:
                    line.append(crew_base.active_mates.jobbing_pirate)
                except:
                    line.append(0)
                # Jobber List
                try:
                    line.extend(crew_base.members.jobbing_pirate)
                except:
                    pass
                    
                writer.writerow(line)

        #sleeptime = 60 - datetime.utcnow().second
        #time.sleep(sleeptime)

        n += 1
        
        break