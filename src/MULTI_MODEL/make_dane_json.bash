
plik=a

./make_dane_json.py  >$plik
sed "s/'/\"/g" -i $plik
