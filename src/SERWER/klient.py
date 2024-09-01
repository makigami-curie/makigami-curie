
import numpy.random as random
import numpy as np

PLEC = ('M','K')
PPLEC = (.7, .3)
WIEK = [18, 70]
STAN_CYW = ['WOL', 'WZW']
PSTAN_CYW = [.3, .7]
OSOBY_NA_UTRZ = range(0,6)
POSOBY_NA_UTRZ = [.3, .3, .2, .1, .07, .03]
WYKSZTALCENIE = ['podst', 'zawod','sred','wyzsze']
PWYKSZTALCENIE = [.2, .3, .4, .1]
DOCHOD = [1000,4000]
ZAMELDOWANIE = ['wies', 'male', 'srednie', 'duze','Warszawa']
PZAMELDOWANIE = [.3, .3, .1, .2, .1]
SAMOCHOD = ['Nie', 'stary', 'nowy']
PSAMOCHOD = [.2, .5, .3]
ZATRUDNIENIE = ['Tak', 'Nie']
PZATRUDNIENIE = [.8, .2]
POGODA = range(1, 10)
DZIEN = ['pn','wt','sr','czw','pi','so','ni']
PDZIEN = [.05, .2, .1, .1, .2, .3, .05]

def kupno(plec, wiek, stan, osoby_na_utrz, wyksztalcenie, dochod, zameldowanie, samochod, zatrudnienie, pogoda, dzien):
	if plec == 'M':
		Ep = 1
	else: Ep = -1
	Ew = - wiek / 20.
	if stan == 'WOL':
		Es = 2
	else: Es = 0
	if osoby_na_utrz == 0: Eo = 2
	if osoby_na_utrz == 1: Eo = 1
	if osoby_na_utrz == 2: Eo = 3
	if osoby_na_utrz == 3: Eo = 0
	if osoby_na_utrz > 3 : Eo = -2
	Ewk = 0
	if wyksztalcenie in ('podst', 'zawod'): Ewk  = 1
	if wyksztalcenie == 'wyzsze': Ewk = 2
	if dochod > 3000: 
		Ed = 1
	else: Ed = 0
	Ez = 0
	if zameldowanie in ('wies', 'male'):
		Ez = -1
	if zameldowanie == 'duze': Ez = 1
	if zameldowanie == 'Warswawa': Ez = -1
	
	E = Ep + Ew + Es + Eo + Ewk +Ed + Ez 
	P = np.exp(E -1)
	if pogoda < 3: P = P - .2
	if pogoda > 6: P = P + .1
	if pogoda ==9: P = P + .1
	if dzien == 'pn': P = P - .1
	if dzien == 'pi': P = P + .1
	
	if random.random() < P: 
		return 1
	else:
		return 0

		

def make_klient ():
	plec = random.choice(PLEC, p=PPLEC)
	wiek = random.randint(10, 70)
	stan = random.choice(STAN_CYW, p=PSTAN_CYW)
	osoby_na_utrz = random.choice(OSOBY_NA_UTRZ, p=POSOBY_NA_UTRZ)
	wyksztalcenie = random.choice(WYKSZTALCENIE, p=PWYKSZTALCENIE)
	dochod = random.normal(2500, 500)
	zameldowanie = random.choice(ZAMELDOWANIE, p=PZAMELDOWANIE)
	samochod = random.choice(SAMOCHOD, p=PSAMOCHOD)
	zatrudnienie = random.choice(ZATRUDNIENIE, p=PZATRUDNIENIE)
	pogoda = random.randint(1,10)
	dzien = random.choice(DZIEN, p=PDZIEN)

	print({'variables':[{'plec':plec}, {'wiek':wiek}, {'stan':stan}, {'osoby_na_utrz':osoby_na_utrz}, {'wyksztalcenie':wyksztalcenie}, \
		{'dochody':dochod}, {'zameldowanie':zameldowanie}, {'samochod':samochod}, {'zatrudnienie':zatrudnienie},  \
		{'KUPNO':kupno(plec, wiek, stan, osoby_na_utrz, wyksztalcenie, dochod, zameldowanie, samochod, zatrudnienie, pogoda, dzien) } ]})


N=1
print("{\"tasks\":[")
for i in range(N):
	make_klient()
	if i<N-1: print(',')
print("], \"id\":1}")
