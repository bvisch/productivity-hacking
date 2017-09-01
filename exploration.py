import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn import decomposition, manifold
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

# baseline = np.array(baseline_data).T
# concentration = np.array(concentration_data).T

# baseline = np.flip(baseline, axis=0)
# concentration = np.flip(concentration, axis=0)
#
# comparison = np.append(baseline[:, 5000:6000], concentration[:, 5000:6000], axis=0)

# plt.set_cmap('magma') #https://matplotlib.org/examples/color/colormaps_reference.html

baseline = np.array(baseline_data)
concentration = np.array(concentration_data)
X = np.append(baseline, concentration, axis=0)
y = np.append(np.zeros(len(baseline)), np.ones(len(concentration)))



# pca = decomposition.PCA(n_components=3, whiten=True, svd_solver='auto')
# pca.fit(X)
# X = pca.transform(X)
X = manifold.TSNE(n_components=3, init='pca').fit_transform(X)

fig = plt.figure(1, figsize=(4, 3))
plt.clf()
ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
plt.cla()

for name, label in [('baseline', 0), ('concentration', 1)]:
    ax.text3D(X[y == label, 0].mean(),
              X[y == label, 1].mean() + 1.5,
              X[y == label, 2].mean(), name,
              horizontalalignment='center',
              bbox=dict(alpha=.5, edgecolor='w', facecolor='w'))

ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=y, cmap=plt.cm.spectral)

ax.w_xaxis.set_ticklabels([])
ax.w_yaxis.set_ticklabels([])
ax.w_zaxis.set_ticklabels([])

plt.show()



# X = decomposition.PCA(n_components=2, whiten=False, svd_solver='auto').fit_transform(X)
# X = manifold.TSNE(n_components=2, init='pca').fit_transform(X)
# X = manifold.Isomap(n_neighbors=30, n_components=2).fit_transform(X)

# plt.figure()
# colors = ['navy', 'darkorange']
# for color, i, target_name in zip(colors, [0, 1], ['baseline', 'concentration']):
#     plt.scatter(X[y == i, 0], X[y == i, 1], color=color, alpha=.8, lw=2, label=target_name)
#
# plt.show()
