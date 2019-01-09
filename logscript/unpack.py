# -*- coding: UTF-8 -*-

import sys
import os
from subprocess import call
import csv
import time
import numpy
import pandas as pd

def parse_time(t):
    t = t.split(':')
    return int(t[0])#*60+int(t[1])

def is_int(s):
    check = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    for i in range (len(s)):
        if s[i] not in check:
            return 0
    return 1

dates_count = []
avarege = numpy.zeros(24)
avarege_name = []

def parse (filename):
    infotable = [['time', 'counter']]
    f = open(filename, 'r')
    stat = [0 for i in range (24)]
    for line in f:
        pline = line.split()
        if len(pline) != 0:
            if pline[2 % len(pline)] == 'INFO':
                if infotable == [['time', 'counter']]:
                    out_file = 'out_csv/'+pline[0]+'.csv'
                if is_int(pline[-1]) == 1:
                    infotable.append([parse_time(pline[1]), pline[-1]])
                    stat[int(parse_time(pline[1]))] += 1
    if len(infotable) != 1:
        with open(out_file, "w") as file:
            writer = csv.writer(file)
            writer.writerows(infotable)
        name_condidate = out_file[8:-4].split('-')
        avarege_name.append(name_condidate[0]+name_condidate[1]+name_condidate[2])

    if filename[7:17] != '.txt':
        dates_count.append([filename[7:17], len(infotable)-1])
    return numpy.array(stat)


dates = ''

if __name__ == "__main__":
    i = 0
    rc = call("./newdirs.sh")
    for directory in sys.argv:
        if i != 0:
            files = os.listdir(directory)
            for filename in files:
                os.environ["FILENAME"] = directory+'/'+filename
                os.environ["NEWFILE"] = filename[15:25]
                rc = call("./unpack.sh")
        i += 1
    files = os.listdir('output')
    j = 0
    for filename in files:
        j += 1
        avarege += parse('output/'+filename)
    dates_count.sort()
    dates_count = [['date', 'count']] + dates_count
    dates = min(avarege_name)+'-'+max(avarege_name)
    with open(dates + '_dates_count.csv', "w") as file:
        writer = csv.writer(file)
        writer.writerows(dates_count)
    
    avarege = avarege / j
    a = [['time' , 'count']]
    for i in range(24):
        a.append([i, avarege[i]])
    with open(dates + '_avarege.csv', "w") as file:
        writer = csv.writer(file)
        writer.writerows(a)


import numpy as np
import matplotlib.pyplot as plt
import os

files = os.listdir('out_csv')
res = plt.figure()
i = 0
ax = res.gca()
ax.grid(True)
plt.ylim((0,550))
plt.xlabel('time')
plt.ylabel('message (1000)')
ax.set_xticks(numpy.arange(0, 24, 1))
ax.set_yticks(numpy.arange(0, 550, 50))
ax.grid(True)
step = 0.024/len(files)
for f in files:
    i += step
    if f[0]!='.':
        frame = pd.read_csv('out_csv/'+f, header=0, sep=',')
        n, bins, patches = plt.hist(frame['time'], range=(0, 24), bins=24,
                                    color='red',  alpha=i)
i = 0.025
for f in files:
    i = i - step
    if f[0]!='.':
        frame = pd.read_csv('out_csv/'+f, header=0, sep=',')
        n, bins, patches = plt.hist(frame['time'], range=(0, 24), bins=24,
                                    color='blue',  alpha=i)

res.savefig(dates + "_combine.pdf", bbox_inches='tight')




from matplotlib.backends.backend_pdf import PdfPages
files = os.listdir('out_csv')
for f in files:
    res = plt.figure(dpi = 160)
    if f[0]!='.':
        ax = res.gca()
        ax.grid(True)
        plt.ylim((0,800))
        plt.xlabel('time')
        plt.ylabel('message (1000)')
        ax.set_xticks(numpy.arange(0, 24, 1))
        ax.set_yticks(numpy.arange(0, 850, 50))
        ax.grid(True)
        frame = pd.read_csv('out_csv/'+f, header=0, sep=',')
        n, bins, patches = plt.hist(frame['time'], range=(0, 24), bins=24, width = 0.7,
                                    color='orange',  alpha=0.6, label=f[:10])
        plt.legend(loc='upper right')
    res.savefig('out_pdf/'+f[:len(f)-4]+".pdf", bbox_inches='tight')




frame = pd.read_csv(dates + '_avarege.csv', header=0, sep=',')
dpi = 80
res = plt.figure(dpi = 160 )
plt.title('Average')
ax = res.gca()
plt.xlabel('time')
ax.set_xticks(numpy.arange(0, 24, 1))
ax.grid(True)
plt.ylabel('message (1000)')
plt.bar(frame['time'], frame['count'],
        width = 0.7, color = 'orange', alpha = 0.7, label = '2018',
        zorder = 1)
plt.legend(loc='upper right')

res.savefig(dates + "_avarege.pdf", bbox_inches='tight')

frame = pd.read_csv(dates + '_dates_count.csv', header=0, sep=',')
res = plt.figure(dpi = 200)
import datetime
d =[]
for u in frame['date']:
    if u != '.txt':
        ss = u.split('-')
        d.append(datetime.date(int(ss[0]), int(ss[1]), int(ss[2])))
ax = res.gca()
ax.grid(True)
plt.ylabel('message (1000)')
plt.xlabel('date')
plt.rcParams.update({'font.size': 5})
plt.legend(loc='upper right')
plt.bar(d, frame['count'], width = 0.8, color = 'orange', alpha = 0.7, label = '2018')
res.savefig(dates + "_count.pdf", bbox_inches='tight')

