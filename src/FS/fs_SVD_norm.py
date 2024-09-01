
import numpy as np
import pandas as pd
import re
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.decomposition import TruncatedSVD
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
#tworzenie zmienncy dummis
'''
le=LabelEncoder()
for col in dummis_columns:
	le.fit(dataset[col])
	dataset[col] = le.transform(dataset[col])
'''
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

reg = linear_model.LinearRegression()
reg.fit(X_train, Y_train)

Y_pred = reg.predict(X_test)

#print(reg.coef_)
print(mean_squared_error(Y_test, Y_pred))
print(r2_score(Y_test, Y_pred))

print ('SVD:')
for i in range(1,len(X_names)):
	svd = TruncatedSVD(n_components=i)
	X_tr = svd.fit_transform(X_train)
	reg.fit(X_tr, Y_train)
	X_tr = svd.transform(X_test)
	Y_pred = reg.predict(X_tr)
	print('# feature ',i,':')
	print(mean_squared_error(Y_test, Y_pred), r2_score(Y_test, Y_pred))

'''
plt.scatter(X_test['LP'], Y_test, color='black')
plt.scatter(X_test['LP'], Y_pred, color='blue', linewidth=3)

#usuniecie skali na osich
#plt.xticks(())
#plt.yticks(())

plt.show()
'''
