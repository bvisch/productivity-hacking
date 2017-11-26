from liblo import *

import time
import json
import csv
from sklearn import neural_network, preprocessing, model_selection, neighbors, tree
from sklearn.pipeline import Pipeline
from sklearn.feature_selection import SelectPercentile, chi2
import numpy as np
import matplotlib.pyplot as plt

import os
from datetime import datetime
import threading


data = []
predict = False
lock = threading.Lock()
classifier = neural_network.MLPClassifier(hidden_layer_sizes=(100,),
                                          solver='adam',
                                          activation='identity',
                                          alpha=0.0001,
                                          tol=0.01,
                                          early_stopping=False,
                                          warm_start=False,
                                          verbose=True)

class MuseServer(ServerThread):
    #listen for messages on port 5000
    def __init__(self):
        ServerThread.__init__(self, 5000)
        self.fresh_data = []
        self.last_message = datetime.now()
        self.run_count = 0

    #receive fft data
    @make_method('/muse/elements/raw_fft0', 'f'*129)
    def fft0_callback(self, path, args):
        global lock
        lock.acquire()
        self.fresh_data.extend(args)
        lock.release()

    @make_method('/muse/elements/raw_fft1', 'f'*129)
    def fft1_callback(self, path, args):
        global lock
        lock.acquire()
        self.fresh_data.extend(args)
        lock.release()

    @make_method('/muse/elements/raw_fft2', 'f'*129)
    def fft2_callback(self, path, args):
        global lock
        lock.acquire()
        self.fresh_data.extend(args)
        lock.release()

    @make_method('/muse/elements/raw_fft3', 'f'*129)
    def fft3_callback(self, path, args):
        global data, predict, lock
        lock.acquire()
        self.fresh_data.extend(args)
        data.append(self.fresh_data)
        if self.run_count <= 2:
            self.run_count += 1
            if self.run_count == 2:
                classifier.partial_fit(data, [0., 1.], classes=[0., 1.])
                self.fresh_data = []
                data = []

        elif predict and classifier.predict([self.fresh_data])[0] < 1:
            os.system('spd-say "hi"')
            print('Last check: ' + str((datetime.now()-self.last_message).total_seconds()) + 'seconds ago')
            self.last_message = datetime.now()
            if input('Did you just lose focus? y/N') is 'y':
                classifier.fit(data, np.zeros(len(data)))
            else:
                classifier.fit(data, np.ones(len(data)))
            data = []
            predict = False

        self.fresh_data = []
        lock.release()


try:
    server = MuseServer()
except ServerError as err:
    print(str(err))
    sys.exit()

print('Predicting')
server.start()

if __name__ == "__main__":
    while 1:
        print("Waiting...")
        predict = True
        time.sleep(60)
