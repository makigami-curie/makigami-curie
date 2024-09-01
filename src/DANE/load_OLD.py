
import numpy as np
import pandas as pd
import re

skip_cols = 2
dataset = pd.read_csv('text',header=None, delimiter=" ")#, usecols=range(skip_cols,16))
#dataset = np.loadtxt('text', delimiter=",")
#print (dataset.dtypes)

char_columns = dataset.dtypes.pipe(lambda x: x[x=='object']).index
bool_columns = dataset.dtypes.pipe(lambda x: x[x=='bool']).index

#print( dataset.dtypes == 'bool')
dummis_columns = list(char_columns)+list(bool_columns)
#print (  pd.get_dummies(dataset, columns=dummis_columns) )

skip_columns = [x for x in range(0,skip_cols)]
date_columns = []
for index, ww in enumerate(dataset.iloc[0]):
	if re.search(r'....-..-..', str(ww)) :
		date_columns.append(index)
#print (date_columns)	
cols = skip_columns+date_columns
print(cols)
print (dataset)
dataset = dataset.drop(dataset.columns[cols],1)

print(dataset)

char_columns = dataset.dtypes.pipe(lambda x: x[x=='object']).index
bool_columns = dataset.dtypes.pipe(lambda x: x[x=='bool']).index
dummis_columns = list(char_columns)+list(bool_columns)


#dummis_columns = list (set(dummis_columns) - set(date_columns) -set(skip_columns))
dummis_columns.sort()
#dummis_columns.remove([12])

dataset = pd.get_dummies(dataset, columns=dummis_columns) 
"""
cols = skip_columns+date_columns
print(cols)
print (dataset)
"""
#dataset = dataset.drop(dataset.columns[cols],1)
N_data = len(dataset)

print (dataset)
#print (dummis_columns)
#data = dataset._get_numeric_data()
#print (dataset.iloc[1][0])

'''
fil = open('text', 'r')
data2 =[]
for line in fil:
	print(line)
	for ch in ("\n", "'", "(", ")"):
		line = line.replace(ch,'')
	data2.append(line.split(', '))
fil.close()

print (data2)
'''
