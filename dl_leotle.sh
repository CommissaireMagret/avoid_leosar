#!/bin/bash

wget https://celestrak.org/NORAD/elements/gp.php?CATNR=38771 -O TLE/tle1.txt
wget https://celestrak.org/NORAD/elements/gp.php?CATNR=44387 -O TLE/tle2.txt
wget https://celestrak.org/NORAD/elements/gp.php?CATNR=25338 -O TLE/tle3.txt
wget https://celestrak.org/NORAD/elements/gp.php?CATNR=28654 -O TLE/tle4.txt
wget https://celestrak.org/NORAD/elements/gp.php?CATNR=33591 -O TLE/tle5.txt

cd TLE
cat tle1.txt tle2.txt tle3.txt tle4.txt tle5.txt > tle_leosar.txt

echo -e "\nTLEs téléchargées pour les 5 LEOSAR uniquement, elles sont regroupées dans le fichier tle_leosar.txt.\n"
