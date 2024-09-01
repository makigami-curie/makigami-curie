
import numpy as np
import pandas as pd
import re
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score

from sklearn.preprocessing import scale, LabelEncoder

import matplotlib.pyplot as plt

import pyswarms.single as ps

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
#tworzenie zmienncy dummis
le = LabelEncoder()
for col in dummis_columns:
	le.fit(dataset[col])
	dataset[col] = le.transform(dataset[col])
dataset = pd.get_dummies(dataset, columns=dummis_columns) 


#liczba rekordow
N_data = len(dataset)

#print(dataset.corr()['TIME'])

train = dataset.sample(frac=.75, random_state=1)
test = dataset.loc[~dataset.index.isin(train.index)]

#nazwy kolumn po wyrzucaniu
names = dataset.columns.values
X_names = np.setdiff1d(names,Y_names)

X_train = train[X_names]
Y_train = train[Y_names]

X_test = test[X_names]
Y_test = test[Y_names]

def f_one(x):
	reg = MLPRegressor(hidden_layer_sizes=(int(x[0]),int(x[1]),int(x[2])) )#,tol=1e-6,max_iter=1000, verbose=True)#, len(X_names)-2))
	reg.fit(X_train, Y_train)

	Y_pred = reg.predict(X_test)
	return -r2_score(Y_test, Y_pred)

def f(x):
        n_part = x.shape[0]
        out = [f_one(x[i]) for i in range(n_part)]
        return np.array(out)

options = {'c1':0.5, 'c2':.3, 'w':0.9}
dim = 3
mins = np.ones(dim)
maxs = 50*np.ones(dim)
bons = (mins, maxs)

opt = ps.GlobalBestPSO(n_particles=10, dimensions=dim, options=options, bounds=bons)
cost, pos = opt.optimize(f, print_step=1, iters=10, verbose=3)

print(pos)
#print(reg.coef_)
#print(mean_squared_error(Y_test, Y_pred))
#print(r2_score(Y_test, Y_pred))

reg = MLPRegressor(hidden_layer_sizes=(int(pos[0]),int(pos[1]),int(pos[2])) )
reg.fit(X_train, Y_train)
Y_pred = reg.predict(X_test)

print(mean_squared_error(Y_test, Y_pred))
print(r2_score(Y_test, Y_pred))

plt.scatter(X_test['LP'], Y_test, color='black')
plt.scatter(X_test['LP'], Y_pred, color='blue', linewidth=3)

#usuniecie skali na osich
#plt.xticks(())
#plt.yticks(())

plt.show()
