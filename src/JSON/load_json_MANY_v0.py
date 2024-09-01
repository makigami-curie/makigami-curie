
import numpy as np
import pandas as pd
import json

#Wczytanie danych
#dataset = pd.read_json('vat.json')#, usecols=range(skip_cols,16))

#print(dataset.values)


f = open('vat_M.json', 'r')
f = json.loads(str(f.read()))
#for ff in f: print(ff,"\n")

for ff in f:
	pp = pd.DataFrame.from_dict(ff,orient="index").T
#	print (np.array(p['products'].iloc[0]).size)
	try:
		p = pd.concat([p,pp])
	except:
		p = pp

p.reset_index(drop=True, inplace=True)
print (p['tax'].values)
