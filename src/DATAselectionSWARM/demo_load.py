
from load_json_MANY_good import load_json_all
from clean_data import clean_data
from train_models import *
from load_job import load_job

import subprocess
import matplotlib.pyplot as plt
import pickle

#uczenie IA
dataset = load_json_all('a')

dataset, workers, X_names, Y_names, SKIP_names, DUMMIS_names ,sc = clean_data(dataset)

#models = train_models_LR(dataset, workers, X_names, Y_names)

filePickle = 'save.pkl'
file_pkl = open(filePickle, 'rb')
models=pickle.load(file_pkl)

#predykcja czasow
#formatowanie inputu zeby pasowal
setDF = dataset.head(1)
setDF = setDF.drop(setDF.index)

ET = {x:0 for x in workers}
ETorg = {x:0 for x in workers}

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

#plt.show()
#	print (i, sorted(workers_time.items()), worker, time)
#	print(sorted(ET.items()))
#	print(sorted(ETorg.items()))
