#!/bin/bash

wget https://celestrak.org/NORAD/elements/gp.php?CATNR=38771 -O tle1.txt
wget https://celestrak.org/NORAD/elements/gp.php?CATNR=44387 -O tle2.txt
wget https://celestrak.org/NORAD/elements/gp.php?CATNR=25338 -O tle3.txt
wget https://celestrak.org/NORAD/elements/gp.php?CATNR=28654 -O tle4.txt
wget https://celestrak.org/NORAD/elements/gp.php?CATNR=33591 -O tle5.txt

cat tle1.txt tle2.txt tle3.txt tle4.txt tle5.txt > tle_leosar.txt

echo -e "\nTLEs téléchargées pour les 5 LEOSAR uniquement, elles sont regroupées dans le fichier tle_leosar.txt.\n"
