
import numpy as np
import pandas as pd
import re
from sklearn.cluster import KMeans
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
#tworzenie zmienncy dummis
le=LabelEncoder()
for col in dummis_columns:
	le.fit(dataset[col])
	dataset[col] = le.transform(dataset[col])
#dataset = pd.get_dummies(dataset, columns=dummis_columns) 


#liczba rekordow
N_data = len(dataset)

#print(dataset.corr()['TIME'])

train = dataset.sample(frac=.75, random_state=1)
test = dataset.loc[~dataset.index.isin(train.index)]

#nazwy kolumn po wyrzucaniu
names = dataset.columns.values
X_names = np.setdiff1d(names,Y_names)

X_train = dataset[X_names]

ms = KMeans(n_clusters=4)
for i in range(1,10): ms.fit(X_train)

labels = ms.labels_
n_labels = len(np.unique(labels))
print(n_labels)

#print(X_train.head())
color = ['b','g','r','c','m','y','k']

plt.figure(1)
plt.clf()
for k in range(0, n_labels): 
	my_members = labels == k
	cl_center = ms.cluster_centers_[k] 
	plt.scatter(X_train.loc[my_members]['LP'],X_train.loc[my_members]['SR'], color=color[k])
	plt.scatter(cl_center[4],cl_center[8], color='black', marker='x',s=150) 
#usuniecie skali na osich
#plt.xticks(())
#plt.yticks(())

plt.show()
