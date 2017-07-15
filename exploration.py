import matplotlib.pyplot as plt
import numpy as np
import sys
import csv
import json


baseline_data = []
with open('baseline.csv', 'r') as baseline_csv:
    reader = csv.reader(baseline_csv)
    for row in reader:
        baseline_data.append([item for sublist in row for item in json.loads(sublist)])

concentration_data = []
with open('concentration.csv', 'r') as concentration_csv:
    reader = csv.reader(concentration_csv)
    for row in reader:
        concentration_data.append([item for sublist in row for item in json.loads(sublist)])

baseline = np.array(baseline_data).T
concentration = np.array(concentration_data).T

baseline = np.flip(baseline, axis=0)
concentration = np.flip(concentration, axis=0)

comparison = np.append(baseline[:, 5000:6000], concentration[:, 5000:6000], axis=0)

plt.set_cmap('magma') #https://matplotlib.org/examples/color/colormaps_reference.html
import pdb; pdb.set_trace()
