
import numpy as np
import pandas as pd
import re
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import scale, LabelEncoder


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
names = dataset.columns.values
Y_names = names[-1]

for col in names:
	if (dataset[col].dtype != 'object') and (dataset[col].dtype !='bool'):
		dataset[col] = scale(dataset[col])


dummis_columns = np.setdiff1d(dummis_columns, names[-2])
workers=np.unique(dataset[names[-2]].values)

#dummis_columns.remove([names[-2])
#tworzenie zmienncy dummis
dataset = pd.get_dummies(dataset, columns=dummis_columns)	#dopisuje dodatkowe kolumny na koncu

X_names = np.setdiff1d(dataset.columns.values,(Y_names, names[-2]))

subplot = 1

models = {}
for worker in workers:
#	print(dataset[names[-2]].head())
	print (worker,":")
#	print(dataset[dataset[names[-2]]==worker])
	data = dataset[dataset[names[-2]]==worker]
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
	print(mean_squared_error(Y_test, Y_pred))
	print(r2_score(Y_test, Y_pred))

	plt.subplot(2,2,subplot)	
	plt.title(worker)
	plt.scatter(X_test['LP'], Y_test, color='black')
	plt.scatter(X_test['LP'], Y_pred, color='blue', linewidth=3)
	subplot +=1
plt.show()
