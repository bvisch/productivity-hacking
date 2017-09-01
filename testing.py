import json
import csv
from sklearn import neural_network, preprocessing, model_selection, neighbors
import numpy as np


parameters = {
            'hidden_layer_sizes': [(50,), (100,), (50,50), (100,50)],
            'activation': ['identity', 'relu', 'logistic', 'tanh'],
            'alpha': [0.01, 0.001, 0.0001],
            # 'tol': [0.1, 0.01, 0.001]
            }


# classifier = neural_network.MLPClassifier(hidden_layer_sizes=(100,),
#                                           solver='adam',
#                                           activation='identity',
#                                           alpha=0.0001,
#                                           tol=0.01,
#                                           early_stopping=True,
#                                           warm_start=False,
#                                           verbose=True)

classifier = neighbors.KNeighborsClassifier()
scaler = preprocessing.MaxAbsScaler()
# scaler = preprocessing.StandardScaler(with_mean=True, with_std=True)
# scaler = preprocessing.Normalizer(norm='l1')
# if testing:
#     classifier = model_selection.GridSearchCV(classifier, parameters, n_jobs=4)


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
classifier.fit(np.append(train_concentration, train_baseline, axis=0),
               np.append(np.ones(len(train_concentration)), np.zeros(len(train_baseline))))

if testing:
    test_score = classifier.score(np.append(test_concentration, test_baseline, axis=0),
                                  np.append(np.ones(len(test_concentration)), np.zeros(len(test_baseline))))
    train_score = classifier.score(np.append(train_concentration, train_baseline, axis=0),
                                   np.append(np.ones(len(train_concentration)), np.zeros(len(train_baseline))))

    print("Test set score: ", test_score)
    print("Training set score: ", train_score)
