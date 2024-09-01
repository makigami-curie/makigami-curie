
import numpy as np
import pandas as pd
import re
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler, LabelEncoder


import matplotlib.pyplot as plt

#liczba opuszczanych kolumn od przodu
skip_cols = 2
#Wczytanie danych
dataset = pd.read_csv('text',header=0, delimiter=" ")#, usecols=range(skip_cols,16))

#kolumny do opuszczenia
skip_columns = [x for x in range(0,skip_cols)]
#kolumny z datami
date_columns = []
for index, ww in enumerate(dataset.iloc[0]):
	if re.search(r'....-..-..', str(ww)) :
		date_columns.append(index)
skip_columns = skip_columns+date_columns
#wyrzuczanie kolumn
dataset = dataset.drop(dataset.columns[skip_columns],1)

#kolumny dla dummis variables
char_columns = dataset.dtypes.pipe(lambda x: x[x=='object']).index
bool_columns = dataset.dtypes.pipe(lambda x: x[x=='bool']).index
dummis_columns = list(char_columns)+list(bool_columns)

#sortowanie nie jest potrzebne
dummis_columns.sort()

#nazwy zmiennych
namesS = dataset.columns.values
Y_names = namesS[-1]

sc = []
for i, col in enumerate(namesS):
	sc.append(StandardScaler())
	if (dataset[col].dtype != 'object') and (dataset[col].dtype !='bool'):
		dataset[col] = sc[i].fit_transform(pd.DataFrame(dataset[col]))
#	print(i,col)
#		dataset[col] = scale(dataset[col])

dummis_columns = np.setdiff1d(dummis_columns, namesS[-2])
workers=np.unique(dataset[namesS[-2]].values)

#dummis_columns.remove([names[-2])
#tworzenie zmienncy dummis
dataset = pd.get_dummies(dataset, columns=dummis_columns)	#dopisuje dodatkowe kolumny na koncu

X_names = np.setdiff1d(dataset.columns.values,(Y_names, namesS[-2]))

names = dataset.columns.values
subplot = 1

models = {}
for worker in workers:
#	print(dataset[names[-2]].head())
	print (worker,":")
#	print(dataset[dataset[names[-2]]==worker])
	data = dataset[dataset[namesS[-2]]==worker]
	models[worker] = linear_model.LinearRegression()

	N_data = len(dataset)
	train = data.sample(frac=.75, random_state=1)
	test = data.loc[~data.index.isin(train.index)]

	X_train = train[X_names]
	Y_train = train[Y_names]

	X_test = test[X_names]
	Y_test = test[Y_names]

	models[worker].fit(X_train, Y_train)
	
	Y_pred = models[worker].predict(X_test)
	
#	print(models[worker].coef_)
#	print(mean_squared_error(Y_test, Y_pred))
#	print(r2_score(Y_test, Y_pred))

	X = X_test['LP']
	X =  sc[0].inverse_transform(pd.DataFrame(X))
#	X_test['LP'] = sc[0].inverse_transform(pd.DataFrame(X_test['LP']))
	Y_test =  sc[11].inverse_transform(pd.DataFrame(Y_test))
	Y_pred =  sc[11].inverse_transform(pd.DataFrame(Y_pred))

	plt.subplot(2,2,subplot)	
	plt.title(worker)
	plt.scatter(X, Y_test, color='black')
	plt.scatter(X, Y_pred, color='blue', linewidth=3)
	subplot +=1
#	X_test['LP'] = sc[0].transform(pd.DataFrame(X_test['LP']))
#	Y_test =  sc[11].transform(pd.DataFrame(Y_test))

#plt.show()

#wczytywanie zadania do kolejkowania
queue_data = pd.read_csv('test', header=0, delimiter=" ")
queue_data = queue_data.drop(queue_data.columns[skip_columns],1)
for i, col in enumerate(namesS):
        if (queue_data[col].dtype != 'object') and (queue_data[col].dtype !='bool'):
                queue_data[col] = sc[i].transform(pd.DataFrame(queue_data[col]))
queue_data = pd.get_dummies(queue_data, columns=dummis_columns)

#formatowanie inputu zeby pasowal
pom = dataset.head(1)

pom.drop(pom.index, inplace=True)
pom=pd.concat([queue_data,pom]).fillna(0)


X = pom[X_names]

subplot = 1
workers_time ={}
for worker in workers:
	Y_pred = models[worker].predict(X)
	_X = X['LP']
	_X =  sc[0].inverse_transform(pd.DataFrame(_X))
#	X['LP'] = sc[0].inverse_transform(pd.DataFrame(X['LP']))
	Y_pred =  sc[11].inverse_transform(pd.DataFrame(Y_pred))
	plt.subplot(2,2,subplot)
	plt.scatter(_X, Y_pred, color='red', linewidth=10,marker='x' )
	workers_time[worker] = Y_pred[0,0]
	subplot+=1
plt.show()	

print("times:\n",workers_time)
workers_time = sorted(workers_time, key=workers_time.get)

#print(workers_time)
workers_queue = pd.read_csv('queue', header=0, delimiter=' ')
worker_comp = pd.read_csv('comp', header=0, delimiter=' ')

print("queue:\n",workers_queue)
print("comp:\n",worker_comp)

queue_mean = float(workers_queue.mean(axis=1))

for worker in workers_time:
	if worker_comp.get_value(0, worker):
		if workers_queue.get_value(0, worker) < queue_mean:
			print("\n\nOUTPUT:  ",worker)
			break

