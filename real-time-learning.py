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


data = []
predict = False
classifier = neural_network.MLPClassifier(hidden_layer_sizes=(100,),
                                          solver='adam',
                                          activation='identity',
                                          alpha=0.0001,
                                          tol=0.01,
                                          early_stopping=True,
                                          warm_start=True,
                                          verbose=True)

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
        data.append(fresh_data)
        if predict and classifier.predict(fresh_data) < 1:
            os.system('spd-say "answer my question"')
            if input('Did you just lose focus? y/N') is 'y':
                classifier.fit(data, np.ones(len(data)))
            else
                classifier.fit(data, np.zeros(len(data)))
            data = []
            predict = False

        self.fresh_data = []

while 1:
    time.sleep(180)
    predict = True
