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

testing = False
use_scaler = False

parameters = {
            'hidden_layer_sizes': [(50,), (100,), (50,50), (100,50)],
            'activation': ['identity', 'relu', 'logistic', 'tanh'],
            'alpha': [0.01, 0.001, 0.0001],
            # 'tol': [0.1, 0.01, 0.001]
            }


scaler = preprocessing.MaxAbsScaler()
# scaler = preprocessing.StandardScaler(with_mean=True, with_std=True)
# scaler = preprocessing.Normalizer(norm='l1')

# classifier = tree.DecisionTreeClassifier()
# classifier = neighbors.KNeighborsClassifier()
classifier = neural_network.MLPClassifier(hidden_layer_sizes=(100,),
                                          solver='adam',
                                          activation='identity',
                                          alpha=0.0001,
                                          tol=0.01,
                                          early_stopping=True,
                                          warm_start=False,
                                          verbose=True)

# classifier = Pipeline([('feature_selection', SelectPercentile(chi2)),
#                        ('classification', classifier)])

# if testing:
#     classifier = model_selection.GridSearchCV(classifier, parameters, n_jobs=4)

class MuseServer(ServerThread):
    #listen for messages on port 5000
    def __init__(self):
        ServerThread.__init__(self, 5000)
        self.fresh_data = []
        self.last_message = datetime.now()

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
        if use_scaler:
            prediction = classifier.predict(scaler.transform([self.fresh_data]))
        else:
            prediction = classifier.predict([self.fresh_data])

        if prediction[0] < 1 and (datetime.now() - self.last_message).total_seconds() > 3:
            os.system('spd-say "get back to work"')
            self.last_message = datetime.now()

        self.fresh_data = []


filename = 'baseline2' #sys.argv[1]
train_baseline = []
with open(filename + '.csv', 'r') as datafile:
    reader = csv.reader(datafile)
    for row in reader:
        train_baseline.append([item for sublist in row for item in json.loads(sublist)])

filename = 'concentration2' #sys.argv[2]
train_concentration = []
with open(filename + '.csv', 'r') as datafile:
    reader = csv.reader(datafile)
    for row in reader:
        train_concentration.append([item for sublist in row for item in json.loads(sublist)])

filename = 'test2'
test = []
with open(filename + '.csv', 'r') as datafile:
    reader = csv.reader(datafile)
    for row in reader:
        test.append([item for sublist in row for item in json.loads(sublist)])

print('Training')
if use_scaler:
    scaler.partial_fit(train_baseline)
    scaler.partial_fit(train_concentration)
    train_baseline = scaler.transform(train_baseline)
    train_concentration = scaler.transform(train_concentration)

if testing:
    test_size = 4000
    test_baseline = train_baseline[-test_size:]
    train_baseline = train_baseline[:-test_size]
    test_concentration = train_concentration[-test_size:]
    train_concentration = train_concentration[:-test_size]

# classifier.partial_fit(train_baseline, np.zeros(len(train_baseline)), classes=[0,1])
# classifier.partial_fit(train_concentration, np.ones(len(train_concentration)))
X = np.append(train_concentration, train_baseline, axis=0)
y = np.append(np.ones(len(train_concentration)), np.zeros(len(train_baseline)))

classifier.fit(X, y)

if testing:
    test_score = classifier.score(np.append(test_concentration, test_baseline, axis=0),
                                  np.append(np.ones(len(test_concentration)), np.zeros(len(test_baseline))))
    train_score = classifier.score(np.append(train_concentration, train_baseline, axis=0),
                                   np.append(np.ones(len(train_concentration)), np.zeros(len(train_baseline))))

    print("Test set score: ", test_score)
    print("Training set score: ", train_score)

    print("Predicting on fresh data")
    predictions = classifier.predict(test)
    t = np.arange(0, len(predictions))
    fig, ax = plt.subplots()
    ax.plot(t, predictions)
    ax.grid()
    plt.show()


else:
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
