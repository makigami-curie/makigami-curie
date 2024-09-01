
from load_json_MANY_good import load_json_all
from clean_data import clean_data
from train_models import *
from load_job import load_job
from fs_swarm import fs_swarm

import subprocess
import matplotlib.pyplot as plt
import pickle

from sklearn.metrics import mean_squared_error, r2_score

#uczenie IA
dataset = load_json_all('a')

dataset, workers, X_names, Y_names, SKIP_names, DUMMIS_names ,sc = clean_data(dataset)
X_names = fs_swarm(dataset, workers, X_names, Y_names)

models = train_models_LR(dataset, workers, X_names, Y_names)

#predykcja czasow
#formatowanie inputu zeby pasowal
setDF = dataset.head(1)
setDF = setDF.drop(setDF.index)

ET = {x:0 for x in workers}
ETorg = {x:0 for x in workers}

data = dataset[dataset['WORKER'] == 'A']
Y_pred = models['A'].predict(data[X_names])
Y_test = data[Y_names]
print(r2_score(data[Y_names], Y_pred))

if 'PRODUKTY_count' in X_names:
	name = 'PRODUKTY_count'
else:
	name = X_names[1]
plt.scatter(data[name], Y_test, color='blue', marker='o',s=100 )
plt.scatter(data[name], Y_pred, color='red', marker='x')

plt.show()
'''
ax = plt.subplot()

for i in range (100):
	subprocess.Popen("./make_aa")

	workers_time, worker, time = load_job ('aa', workers, X_names, SKIP_names, DUMMIS_names, sc, setDF, models)
	times = {x:ET[x] + workers_time[x] for x in workers}

	w = min(times, key=times.get)
	ET[w] = times[w]

	ETorg[worker] += time


	ai = ax.bar( np.arange(len(workers)), list(ET.values())   , color='g', width=.3)
	rd = ax.bar( np.arange(len(workers))+.3, list(ETorg.values()), color='r', width=.3)	

	ax.set_xticks(np.arange(len(workers))+.15)
	ax.set_xticklabels (list(ET.keys()) )
	ax.legend((ai,rd),('AI','RAND'), loc="upper right")
	plt.pause(0.05)

plt.show()
#	print (i, sorted(workers_time.items()), worker, time)
#	print(sorted(ET.items()))
#	print(sorted(ETorg.items()))


filePickle = 'save.pkl'
file_pkl = open(filePickle, 'wb')
pickle.dump(models, file_pkl)
'''
