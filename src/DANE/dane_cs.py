
#print (NR_FAKT, NAZWA, LP, JEZYK, SR, MIN, MAX, KWOTA, VAT, KARTA, MIEJSCE, str(DATEin), str(DATEsell), str(DATEpay), WORKER, TIME)

import random
from datetime import datetime
from datetime import timedelta

def CLAS (male, JEZYK, LP, SR, KWOTA, VAT, KARTA) :
	return  int(VAT==1 or KARTA==1 or (LP>5 and KARTA==0 and SR>5000))*(VAT*2+KARTA)

def WypiszFakture() :
	NR_FAKT = 'FN_'+str(random.randint(1,15))+'/17'
#print(NR_FAKT)

	male = (random.randint(0,10) < 2)

	Nazwa1 = {1:'AA', 2:'BB', 3:'CC', 4:'DD', 5:'EE', 6:'FF', 7:'GG', 8:'HH', 9:'II', 10:'JJ'}
	Nazwa2 = {1:'aa', 2:'bb', 3:'cc', 4:'dd', 5:'ee', 6:'ff', 7:'gg', 8:'hh', 9:'ii', 10:'jj'}
	NAZWA = Nazwa1[random.randint(1,10)] + '_' +  Nazwa2[random.randint(1,10)]
#print (NAZWA)

	LP = random.randint(1,10)
	if male: LP += 20
#print(LP)

	Jezyk = {1:'polski',2:'angielski'}
	JEZYK = Jezyk[random.randint(1,2)]
#print(JEZYK)

	if JEZYK == 'angielski':
		SR = random.uniform(100,10000)+2000
	else:
		SR = random.uniform(10, 10000)
	if male: SR = random.uniform(1,25)
#print(SR)

	var = random.uniform(1*LP,SR/2.) 
	MAX = SR + var
	MIN = SR - var
	KWOTA = LP * SR
#print (MIN, SR, MAX, KWOTA) 

	VAT = random.randint(1,10)<3 or male
#print(VAT)

	KARTA = random.randint(0,100)<5
#print(KARTA)

	MiejscaPL = {1:'Warszawa',2:'Warszawa',3:'Sopot',4:'Warszawa',5:'Lublin'}
	MiejscaANG = {1:'Londyn'}

	if JEZYK == 'angielski' : MIEJSCE = MiejscaANG[random.randint(1,len(MiejscaANG))]
	else: MIEJSCE = MiejscaPL[random.randint(1,len(MiejscaPL))]
	#print(MIEJSCE)

	year = random.choice(range(2017,2019)) 
	month = random.choice(range(1,13))
	plusday = 0
	if month != 2:
		if month in [1,3,5,7,8,10,12]:
			plusday = 3
		else:
			plusday = 2
	day = random.choice(range(1,29+plusday))
	
	DATEin = datetime(year, month, day).date()
	DATEsell = DATEin - timedelta(days=random.randint(0,14))
	DATEpay = random.choice([7,14,30])
#print(DATEin, DATEsell, DATEpay)

#do testow
#	WORKER = 'D'
	clas= CLAS (male, JEZYK, LP, SR, KWOTA, VAT, KARTA)
#print(WORKER, TIME)

#DATE = (NR_FAKT, NAZWA, LP, JEZYK, SR, MIN, MAX, KWOTA, VAT, KARTA, MIEJSCE, str(DATEin), str(DATEsell), str(DATEpay), WORKER, TIME)
#print DATE
	print NR_FAKT, NAZWA, LP, JEZYK, SR, MIN, MAX, KWOTA, VAT, KARTA, MIEJSCE, str(DATEin), str(DATEsell), str(DATEpay), clas
#3.4:
#print (NR_FAKT, NAZWA, LP, JEZYK, SR, MIN, MAX, KWOTA, VAT, KARTA, MIEJSCE, str(DATEin), str(DATEsell), str(DATEpay), WORKER, TIME)


