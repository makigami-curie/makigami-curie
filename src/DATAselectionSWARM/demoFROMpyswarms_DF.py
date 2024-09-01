
import sys
sys.path.append('../')

import numpy as np
import seaborn as sns
import pandas as pd

import pyswarms as ps

from sklearn.datasets import make_classification
from sklearn import linear_model

x,y = make_classification(n_samples=100, n_features=15, n_classes=3, n_informative=4, n_redundant=1, n_repeated=2, random_state=1)


df = pd.DataFrame(x)
#df['labels'] = pd.Series(y)

#sns.pairplot(df, hue='labels');

classifier = linear_model.LogisticRegression()

def f_per_particle(pos, alpha):
	total_features = 15
	if np.count_nonzero(pos) == 0:
		X_subset = df
	else:
		index = [ i for i in range(15) if pos[i]]
		X_subset = df.iloc[:,index]
	classifier.fit(X_subset, y)
	p = (classifier.predict(X_subset) == y).mean()

	j = (alpha * ( 1. - p) + (1. - alpha) * (1 - (X_subset.shape[1] / total_features)))

	return j

def f (pos, alpha = 0.88):
	n_particles = pos.shape[0]
	j = [f_per_particle(pos[i], alpha) for i in range (n_particles)]
	
	return np.array(j)

options = {'c1':0.5, 'c2': 0.5, 'w':0.9, 'k':30, 'p':2}

dimensions = 15
#optimizer.reset()
optimizer = ps.discrete.BinaryPSO(n_particles=30, dimensions=dimensions, options=options)

cost, pos = optimizer.optimize(f, print_step=100, iters=1000, verbose=2)

print(pos)
print(df.head())
index = [ i for i in range(15) if pos[i]]
dff = df.iloc[:,index]
print(dff.head())
#print (cost, pos)

