
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
			p = pd.DataFrame.from_dict(dataset[n].loc[i])
			loc_names = p.columns.values
#		print(loc_names)
			val = p[loc_names[0]].count()
			try:
				new_col[n+'_count'].append(val)
			except:
				new_col[n+'_count'] = [val]
			for ln in loc_names:
				for met in ['mean', 'std']:
#				print(n+'_'+met+'_mean',getattr(p[ln],met)())
					try:
						val = getattr(p[ln],met)()
						try:
							new_col[n+'_'+ln+'_'+met].append(val)
						except:
							new_col[n+'_'+ln+'_'+met] = [val]
#						print(n+'_'+ln+'_'+met,getattr(p[ln],met)())
				
					except:
						pass	
			to_remove.add(n)
#		p= pd.DataFrame(p.describe())
#		print(p)
#print (new_col)
print(to_remove)
dataset = dataset.drop(to_remove,1)
#WYWALA SIE KIEDY W JEDNYM OBIEKCIE COS NIE JESET LISTA A JEST W POZOSTALYCH
dataset = pd.concat([dataset, pd.DataFrame.from_dict(new_col)], axis=1)
print (dataset)
'''
	try:
		print (n, "\t", "\t",len(dataset[n].iloc[0][0]))
	except:
		print (n, "\t", "\t NOOOOOO")
'''

