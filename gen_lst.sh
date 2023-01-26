#!/bin/bash

pip install pypredict

echo ""
echo " Utilisation ligne de commande : "
echo " ./gen_lst.sh <Numéro sequence> <Durée séquence> <Nombre de crénaux> <Nom du fichier lst> <Date et heure de départ : dd/mm/YYYY-HH:MM:SS>"
echo ""

if [ -z "$1" ]
then
	read -p "Numéro de la séquence binaire : " n
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
	read -p "Durée de la séquence en minutes : " d
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
	read -p "Nombre de créneaux/répétitions : " s
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

if [ -z "$5" ]
then
	read -p "Date et heure locale de départ (pas UTC) (dd/mm/YYYY-HH:MM:SS) :" d_t
        d_t_lst=$d_t
        if [ -z "$d_t" ]
        then
                d_t_lst=`date +"%d/%m/%Y-%T"`
	fi
else
        d_t_lst=$5
fi

python3 lst.py $num $dur $seqs $file_lst $d_t_lst

