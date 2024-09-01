
import numpy as np
import pandas as pd
import json

#Wczytanie danych
#dataset = pd.read_json('vat.json')#, usecols=range(skip_cols,16))

#print(dataset.values)


f = open('vat.json', 'r')
f = json.loads(str(f.read()))
#print(f)
p = pd.DataFrame.from_dict(f,orient="index").T
print (np.array(p['products'].iloc[0]).size)

