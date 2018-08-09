# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 00:06:14 2018

@author: Ben Zhao
"""

from bs4 import BeautifulSoup
import urllib2
from xml.etree import ElementTree as ET



page = urllib2.urlopen("http://obsidian.puzzlepirates.com/yoweb/crew/info.wm?crewid=5001832&classic=$classic")

soup = BeautifulSoup(page, 'html.parser')

# Parse this text
table_text = soup.body.contents[1]



table = ET.XML(str(list(list(list(table_text.children)[5].children)[5].children)[1]))

#trs = soup.find('table').find_all('tr')
#trs = [tr for tr in trs if len(tr.find_all('td')) == 2]
#results = []
#for tr in trs:
#    tds = tr.find_all('td')
#    d = {
#        'tdb': tds[0].b.text,
#        'tdHidden': tds[0].b.next_sibling,
#        'tdSecond': tds[1].text
#    }
#    results.append(d)