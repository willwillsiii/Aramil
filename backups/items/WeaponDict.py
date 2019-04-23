#!/usr/local/bin/python3

import re

d = {}
tableFilename = "WeaponList"
with open(tableFilename, 'r') as f:
    for line in f:
        if line[0] is '#':
            continue
        line = line.replace('\n', '').split('\t')
        if line[1][0] is '~': 
            line[1] = line[1][1:]
        line[1] = float(line[1])
        name = line[0]
        name = name.strip().title().replace(' ','')
        name = re.sub('[^A-z]', '', name)
        key,values = name, line
        d[key] = values
    print(d)
