import numpy.random as random
import numpy as np


IMIE = ('Julia', 'Zofia', 'Maja', 'Hanna', 'Lena', 'Alicja', 'Maria', 'Amelia', 'Oliwia', 'Aleksandra', 'Antoni', 'Jakub', 'Jan', 'Szymon', 'Aleksander', 'Franciszek', 'Filip', 'Wojciech', 'Mikołaj', 'Kacper', 'Adam')
NAZWISKO=('Nowak','Kowalski','Wisniewski','Wojcik','Kowalczyk','Kamiński','Lewandowski','Zieliński','Szymański','Wozniak','Dabrowski','Kozłowski','Jankowski','Mazur','Wojciechowski','Kwiatkowski','Krawczyk','Kaczmarek','Piotrowski','Grabowski','Zajac','Pawłowski','Michalski','Krol','Wieczorek','Jabłoński','Wrobel','Nowakowski','Majewski','Olszewski','Stepień','Malinowski','Jaworski','Adamczyk','Dudek','Nowicki','Pawlak','Gorski','Witkowski','Walczak','Sikora','Baran','Rutkowski','Michalak','Szewczyk','Ostrowski','Tomaszewski','Pietrzak','Zalewski','Wroblewski','Marciniak','Jasiński','Zawadzki','Bak','Jakubowski','Sadowski','Duda','Włodarczyk','Wilk','Chmielewski')
ODPOWIEDZ=('A','B','C','X')
ODPOWIEDZP0=(0.2 ,0.4 ,0.3 ,0.1)
ODPOWIEDZP1=(0.1 ,0.2 ,0.6 ,0.1)
ODPOWIEDZP2=(0.4 ,0.2 ,0.3 ,0.1)
ODPOWIEDZP3=(0.3 ,0.2 ,0.3 ,0.2)
ODPOWIEDZP4=(0.1 ,0.6 ,0.2 ,0.1)

PYTANIAdosw = (	'Doswiadczenie zawodowe',\
		'Znakomosc branzy oraz organizacji',\
		'Pytania o mocne strony',\
		'Pytania wokol slabych stron',\
		'Motywacja')
PYTANIAang = (	'Slownictwo',\
		'Plynnosc mowy',\
		'Zrozumienie')
OKRESWYPOWIEDZENIA = ('<1','1','3','>3')

WAGIdos = {'A':1, 'B':3, 'C':5, 'X':-4}
WAGIang = {'A':1, 'B':3, 'C':5, 'X':-4}

def make_cv():
	odpowiedzidos = {'A':0, 'B':0, 'C':0, 'X':0}
	odpowiedziang = {'A':0, 'B':0, 'C':0, 'X':0}

	print('   { "variables":[')
	for i, pytanie in enumerate (PYTANIAdosw):
		odp = random.choice(ODPOWIEDZ, p=ODPOWIEDZP0)
		odpowiedzidos[odp] +=1
		print ('\t{"',pytanie,'":"',odp,'"}')
		print("\t,")
	for i, pytanie in enumerate(PYTANIAang):
		odp = random.choice(ODPOWIEDZ, p=ODPOWIEDZP1)
		odpowiedziang[odp] +=1
		print ('\t{"', pytanie, '":"',odp,'"}')
		if i < len(PYTANIAang)-1 : print("\t,")
	odp = 0
	for i in odpowiedzidos.keys():
		odp += odpowiedzidos[i]*WAGIdos[i]
	print(',\t{"Ocena doswiadczenia":',odp/20.,'}')
	odp = 0
	for i in odpowiedziang.keys():
		odp += odpowiedziang[i]*WAGIang[i]
	print(',\t{"Ocena jezyka":', odp/15.,'}') 
	print ('\t   ] \n    }')
	return odpowiedzidos, odpowiedziang

N=1
print("{\"tasks\":[")
for i in range(N):
        odpowiedzidos, odpowiedziang = make_cv()
        if i<N-1: print(',')
print("    ], \n \"id\":\"1\"\n, \"target\":\"Ocena doswiadczenia\"\n,\"predworker\":\"False\"}")

