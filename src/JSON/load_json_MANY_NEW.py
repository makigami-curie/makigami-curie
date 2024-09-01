
import numpy as np
import pandas as pd
import json

#NEW\/
def kon(d):
        for k in d.keys():
                if type(d[k]) != list or len(d[k])>1: d[k] = [d[k]]
        return d

def kon_dic(d):
        out = dict()
        for k in d:
                out.update(k)
        return out
#NEW/\
#Wczytanie danych
#dataset = pd.read_json('vat.json')#, usecols=range(skip_cols,16))

#print(dataset.values)


#f = open('vat_M.json', 'r')
f = open('jsonNEW','r')
#NEW\/
f = json.loads(str(f.read()))['tasks']
#NEW/\

for ff in f:
#NEW\/
	print(ff)
	data = kon( kon_dic(ff['variables']) )
	data.update({'TIME':[ff['duration']],'WORKER':[ff['worker']]})
	pp = pd.DataFrame.from_dict(data,orient="index").T
#NEW/\
#	print (np.array(p['products'].iloc[0]).size)
	try:
		dataset = pd.concat([dataset,pp])
	except:
		dataset = pp

dataset.reset_index(drop=True, inplace=True)

names = dataset.columns.values

new_col = {}
to_remove = set()
for n in names:
	for i in range(len(dataset[n])): 
		if type(dataset[n].loc[i]) is list:
			to_remove.add(n)

for n in to_remove:
	for i in range(len(dataset[n])):
		try:
			p = pd.DataFrame.from_dict(dataset[n].loc[i])
		except:
			p = pd.DataFrame.from_dict([dataset[n].loc[i]])
		loc_names = p.columns.values
		val = p[loc_names[0]].count()
		try:
			new_col[n+'_count'].append(val)
		except:
			new_col[n+'_count'] = [val]
		for ln in loc_names:
			for met in ['mean', 'std']:
				try:
					val = getattr(p[ln],met)()
					try:
						new_col[n+'_'+ln+'_'+met].append(val)
					except:
						new_col[n+'_'+ln+'_'+met] = [val]
#                                               print(n+'_'+ln+'_'+met,getattr(p[ln],met)())
				except:
					pass
#				if n == 'products': print(i, ln, met, new_col)

#		p= pd.DataFrame(p.describe())
#		print(p)
#print (new_col)
print(to_remove)
dataset = dataset.drop(to_remove,1)
dataset = pd.concat([dataset, pd.DataFrame.from_dict(new_col)], axis=1)
dataset.fillna(0, inplace=True)
#print (dataset['products_count'],dataset['products_vat_mean'], dataset['products_vat_std'])
print(dataset)
'''
	try:
		print (n, "\t", "\t",len(dataset[n].iloc[0][0]))
	except:
		print (n, "\t", "\t NOOOOOO")
'''

