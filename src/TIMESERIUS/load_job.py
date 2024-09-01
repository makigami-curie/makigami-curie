
import numpy as np
import pandas as pd

from load_json import load_json_all

def load_job (fname, workers, Y_names, X_names, SKIP_names, DUMMIS_names, sc, setDF, models):
	queue_data = load_json_all(fname)

	queue_data = queue_data.drop(queue_data[SKIP_names],1)

	for i, col in enumerate(queue_data.columns.values):
		if (queue_data[col].dtype != 'object') and (queue_data[col].dtype !='bool') and (col !='WORKER') and (col != Y_names):
			try:
				queue_data[col] = sc[col].transform(pd.DataFrame(queue_data[col]))
			except:
				pass
	nr = list(DUMMIS_names)
	for col in DUMMIS_names:
		try:
			queue_data[col]
		except:
			nr.remove(col)
	
	queue_data = pd.get_dummies(queue_data, columns=nr)

#formatowanie inputu zeby pasowal
	pom=pd.concat([queue_data,setDF]).fillna(0)

	X = pom[X_names]

	workers_time ={}
	for worker in workers:
		Y_pred = models[worker].predict(X)
#		print(models[worker].predict_proba(X))
#		Y_pred = sc[Y_names].inverse_transform(pd.DataFrame(Y_pred))
#		print(Y_pred)
		workers_time[worker] = Y_pred[0]

	return workers_time , min(workers_time, key=workers_time.get)#, sc['TIME'].inverse_transform(pd.DataFrame(queue_data['TIME']))[0,0]


