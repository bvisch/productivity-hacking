Profrom liblo import *

import sys
import select
import time
import json
import csv
from sklearn import neural_network, preprocessing
import numpy as np

classifier = neural_network.MLPClassifier(solver='adam', activation='relu', max_iter=1000, warm_start=True)
scaler = preprocessing.MaxAbsScaler()
class MuseServer(ServerThread):
    #listen for messages on port 5000
    def __init__(self):
        ServerThread.__init__(self, 5000)
        self.fresh_data = []

    #receive fft data
    @make_method('/muse/elements/raw_fft0', 'f'*129)
    def fft0_callback(self, path, args):
        self.fresh_data.extend(args)

    @make_method('/muse/elements/raw_fft1', 'f'*129)
    def fft1_callback(self, path, args):
        self.fresh_data.extend(args)

    @make_method('/muse/elements/raw_fft2', 'f'*129)
    def fft2_callback(self, path, args):
        self.fresh_data.extend(args)

    @make_method('/muse/elements/raw_fft3', 'f'*129)
    def fft3_callback(self, path, args):
        self.fresh_data.extend(args)
        print(classifier.predict(scaler.transform([self.fresh_data])))
        self.fresh_data = []


filename = 'baseline' #sys.argv[1]
train_baseline = []
with open(filename + '.csv', 'r') as datafile:
    reader = csv.reader(datafile)
    for row in reader:
        train_baseline.append([item for sublist in row for item in json.loads(sublist)])

filename = 'concentration' #sys.argv[2]
train_concentration = []
with open(filename + '.csv', 'r') as datafile:
    reader = csv.reader(datafile)
    for row in reader:
        train_concentration.append([item for sublist in row for item in json.loads(sublist)])

print('Training')
scaler.partial_fit(train_baseline)
scaler.partial_fit(train_concentration)
train_baseline = scaler.transform(train_baseline)
train_concentration = scaler.transform(train_concentration)

# classifier.partial_fit(train_baseline, np.zeros(len(train_baseline)), classes=[0,1])
# classifier.partial_fit(train_concentration, np.ones(len(train_concentration)))
classifier.fit(np.append(train_concentration, train_baseline, axis=0), np.append(np.ones(len(train_concentration)), np.zeros(len(train_baseline))))

try:
    server = MuseServer()
except ServerError as err:
    print(str(err))
    sys.exit()

print('Predicting')
server.start()

if __name__ == "__main__":
    while 1:
        time.sleep(1)
