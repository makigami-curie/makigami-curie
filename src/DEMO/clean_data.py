import numpy as np
import pandas as pd
import re
from sklearn.preprocessing import StandardScaler, LabelEncoder

def clean_data(dataset):
#liczba opuszczanych kolumn od przodu
#	skip_cols = 2
#kolumny do opuszczenia
#	skip_columns = [x for x in range(0,skip_cols)]
#kolumny z datami
	date_columns = []
	for index, ww in enumerate(dataset.iloc[0]):
		if re.search(r'....-..-..', str(ww)) :
			date_columns.append(index)
	skip_columns = date_columns

	skip_columns.append(dataset.columns.get_loc('LP'))
	skip_columns.append(dataset.columns.get_loc('NAZWA'))
	skip_columns.append(dataset.columns.get_loc('NR_FAKT'))
	skip_columns.append(dataset.columns.get_loc('PRODUKTY'))

	SKIP_names = dataset.columns[skip_columns]
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
	Y_names = 'TIME'

	sc = {}
	for i, col in enumerate(namesS):
		sc[col] = StandardScaler()
		if (dataset[col].dtype != 'object') and (dataset[col].dtype !='bool'):
			dataset[col] = sc[col].fit_transform(pd.DataFrame(dataset[col]))
#	print(i,col)
#		dataset[col] = scale(dataset[col])

	dummis_columns = np.setdiff1d(dummis_columns, ['WORKER'])
	workers=np.unique(dataset['WORKER'].values)

#dummis_columns.remove([names[-2])
#tworzenie zmienncy dummis
	dataset = pd.get_dummies(dataset, columns=dummis_columns)	#dopisuje dodatkowe kolumny na koncu

	X_names = np.setdiff1d(dataset.columns.values,(Y_names, 'WORKER'))

	names = dataset.columns.values

	return dataset, workers, X_names, Y_names, SKIP_names, dummis_columns, sc

