#!/bin/bash

pip install pypredict

#cat ~/.disps/cospas70.txt

echo ""
echo " Utilisation ligne de commande : "
echo " ./gen_lst.sh <Numéro sequence> <Durée séquence> <Nombre de crénaux> <Nom du fichier lst>"
echo ""

if [ -z "$1" ]
then
	read -p "Numéro de la séquence : " n
	num=$n
	if [ -z "$n" ]
	then
		num="6940"
	fi
else
	num=$1
fi

if [ -z "$2" ]
then
	read -p "Durée des séquences en minutes : " d
	dur=$d
        if [ -z "$d" ]
        then
                dur="30"
	fi
else
        dur=$2
fi

if [ -z "$3" ]
then
	read -p "Nombre de créneaux : " s
        seqs=$s
        if [ -z "$s" ]
        then
                seqs="200"
	fi
else
        seqs=$3
fi

if [ -z "$4" ]
then
	read -p "Nom du fichier de sortie : " file
        file_lst=$file
        if [ -z "$file" ]
        then
                file_lst="default.lst"
	fi
else
        file_lst=$4
fi

#wget https://celestrak.org/NORAD/elements/gp.php?CATNR=38771 -O tle1.txt
#wget https://celestrak.org/NORAD/elements/gp.php?CATNR=44387 -O tle2.txt
#wget https://celestrak.org/NORAD/elements/gp.php?CATNR=25338 -O tle3.txt
#wget https://celestrak.org/NORAD/elements/gp.php?CATNR=28654 -O tle4.txt
#wget https://celestrak.org/NORAD/elements/gp.php?CATNR=33591 -O tle5.txt

#cat tle1.txt tle2.txt tle3.txt tle4.txt tle5.txt > tlesar.txt

python3 lst.py $num $dur $seqs $file_lst

#echo -e "\n$seqs créneaux créés pour la séquence $num de $dur minutes. Liste enregistrée dans "$file_lst"\n"
