# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 08:09:30 2018

@author: Ben Zhao
"""

import csv
import matplotlib.pyplot as plt


gw_holder = []
cis_holder = []
index = []

with open('GW_job.csv', 'rb') as csvfile:
    crew_reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    for row in crew_reader:
        gw_holder.append(int(row[2]))

with open('CIS_job.csv', 'rb') as csvfile:
    crew_reader = csv.reader(csvfile, delimiter=',', quotechar='\"')
    for row in crew_reader:
        cis_holder.append(int(row[2]))
        index.append(int(row[1]))

plt.figure()
plt.plot(index, gw_holder, label="GW")
plt.plot(index, cis_holder, label="CIS")

plt.legend()
plt.title('Melanaster III')
plt.ylabel('Jobbers')
plt.xlabel('Minutes')

plt.savefig("cis_gw.pdf")
plt.savefig("cis_gw.png")
plt.show()
