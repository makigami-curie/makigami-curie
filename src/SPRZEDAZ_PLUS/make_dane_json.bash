
plik=b

#./make_dane_json.py  >$plik
python3 klient.py > $plik
sed "s/'/\"/g" -i $plik
