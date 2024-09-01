
import numpy as np
import pandas as pd
import json

#Wczytanie danych
#dataset = pd.read_json('vat.json')#, usecols=range(skip_cols,16))

#print(dataset.values)
def kon(d):
	for k in d.keys(): 
		if type(d[k]) != list or len(d[k])>1: d[k] = [d[k]]
	return d

def load_json_all(fname):
#f = open('vat_M.json', 'r')
	f = open(fname,'r')
	f = json.loads(str(f.read()))

	for ff in f:
#		ff ={'PRODUKTY': [{'kwota': 11434.19412755987, 'nazwa': 'a'}], 'KARTA': 'False', 'LP': 1, 'JEZYK': 'polski', 'MIN': 10214.847484414764, 'NR_FAKT': 'FN_1/17', 'DATAin': '2018-12-22', 'WORKER': 'B', 'MIEJSCE': 'Warszawa', 'DATAsell': '2018-12-08', 'NAZWA': 'JJ_dd', 'TIME': 1.1168944538870662, 'KWOTA': 9304.677872433085, 'VAT': 'False', 'DATApay': '7'}
		ff = kon(ff)
		pp = pd.DataFrame.from_dict(ff, orient="index").T
			
#		pp = pd.DataFrame.from_dict(dict(ff),orient="index").T
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
#       	                                        print(n+'_'+ln+'_'+met,getattr(p[ln],met)())
					except:
						pass
#					if n == 'products': print(i, ln, met, new_col)

#		p= pd.DataFrame(p.describe())
#		print(p)
#print (new_col)
#	print(to_remove)
	dataset = dataset.drop(to_remove,1)
	dataset = pd.concat([dataset, pd.DataFrame.from_dict(new_col)], axis=1)
	dataset.fillna(0, inplace=True)
#print (dataset['products_count'],dataset['products_vat_mean'], dataset['products_vat_std'])
	return dataset
'''
	try:
		print (n, "\t", "\t",len(dataset[n].iloc[0][0]))
	except:
		print (n, "\t", "\t NOOOOOO")
'''

