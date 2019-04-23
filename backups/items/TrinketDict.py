

d = {}
tableFilename = "Trinkets"
with open(tableFilename, 'r') as f:
    for line in f:
        if line[0] is '#':
            continue
        line = line.replace('\n', '').split('\t')
        line[0] = int(line[0])
        name = line[0]
        key, values = name, line
        d[key] = values
    print(d)
