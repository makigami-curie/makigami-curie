
import numpy as np
import pandas as pd

from load_json_MANY_good import load_json_all

def load_job (fname, workers, X_names, SKIP_names, DUMMIS_names, sc, setDF, models):
	queue_data = load_json_all(fname)

	queue_data = queue_data.drop(queue_data[SKIP_names],1)

	for i, col in enumerate(queue_data.columns.values):
		if (queue_data[col].dtype != 'object') and (queue_data[col].dtype !='bool'):
			queue_data[col] = sc[col].transform(pd.DataFrame(queue_data[col]))

	queue_data = pd.get_dummies(queue_data, columns=DUMMIS_names)

#formatowanie inputu zeby pasowal
	pom=pd.concat([queue_data,setDF]).fillna(0)

	X = pom[X_names]

	workers_time ={}
	for worker in workers:
		Y_pred = models[worker].predict(X)
		Y_pred = sc['TIME'].inverse_transform(pd.DataFrame(Y_pred))
		workers_time[worker] = Y_pred[0,0]

	return workers_time , queue_data['WORKER'][0], sc['TIME'].inverse_transform(pd.DataFrame(queue_data['TIME']))[0,0]


