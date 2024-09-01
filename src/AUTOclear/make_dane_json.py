
import os
from dane_json import WypiszFakture


N=400
print("[\n")
for i in range(N):
	WypiszFakture()
	if i <N-1 : print (",\n")
print("]")

