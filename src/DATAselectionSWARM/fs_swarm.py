
import numpy as np
import seaborn as sns
import pandas as pd

import pyswarms as ps

from train_models import train_models_LR
from sklearn.datasets import make_classification
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

def fs_swarm (dataset, workers, X_names, Y_names):

	def f_per_particle(m, alpha):
		if np.count_nonzero(m) == 0:
			xx_names = X_names
		else:
			xx_names = [ X_names[i] for i in range(len(X_names)) if m[i]]
		models = {}
		models = train_models_LR(dataset, workers, xx_names, Y_names)

		p = 0
		for worker in workers:
			data = dataset[dataset['WORKER']==worker]
			Y_pred = models[worker].predict(data[xx_names])
			p = p+ r2_score(data[Y_names], Y_pred)	

		return -p/4. 

	def f (x, alpha = 0.88):
		n_particles = x.shape[0]
		j = [f_per_particle(x[i], alpha) for i in range (n_particles)]
	
		return np.array(j)

	options = {'c1':.5, 'c2': .5, 'w':.9, 'k':30, 'p':2}

	dimensions = len(X_names)
#optimizer.reset()
	optimizer = ps.discrete.BinaryPSO(n_particles=30, dimensions=dimensions, options=options)

	cost, pos = optimizer.optimize(f, print_step=1, iters=10, verbose=2)

	xx_names = [ X_names[i] for i in range(len(X_names)) if pos[i]]

	print(pos, np.count_nonzero(pos))
	print(xx_names)
	return xx_names
#print (cost, pos)


