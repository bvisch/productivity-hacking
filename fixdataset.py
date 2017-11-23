import sys
import csv
import json

filename = sys.argv[1]

dataset = []
with open(filename + '.csv', 'r') as openfile:
    reader = csv.reader(openfile)
    for line in reader:
        row = []
        for datapoint in line:
            datapoint = json.loads(datapoint)
            row.append(datapoint[0])

        dataset.append(row)

with open(filename + '2.csv', 'w') as savefile:
    wr = csv.writer(savefile)
    wr.writerows(dataset)
