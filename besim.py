# This is a sample Python script.

import avoidleo
import argparse
import datetime
import time

utc_offset = time.localtime().tm_gmtoff
time_now = time.time()
timeutc = time_now - utc_offset
date_time_format = "%d/%m/%Y-%H:%M:%S"

latN = 43.559281
longE = 1.487430
longW = 360 - longE
qth = (latN, longE, 146)

parser = argparse.ArgumentParser()
parser.add_argument("num_seq", nargs="?", default="6940", type=str, help='n° séq. bin')
parser.add_argument("duration_seq", nargs="?", default="30", type=int, help='durée séq. en min.')
parser.add_argument("num_cren", nargs="?", default="15", type=int, help='nombre de créneaux')
parser.add_argument("file", nargs="?", default="default.json", type=str, help='nom fichier sortie')
parser.add_argument("time_start", nargs="?", default=datetime.datetime.fromtimestamp(time_now+5*60).strftime(date_time_format), help='date et heure locale de départ (pas UTC) : dd/mm/YYYY hh:mm:ss')
parser.add_argument("type_", nargs="?", default="PERSONAL", type=str, help='Type : PERSONAL or FACTORY (PERSONAL if nothing specified)')
parsed_args = parser.parse_args()

if __name__ == '__main__':
    avoidleo.writebatch(parsed_args.num_seq, parsed_args.duration_seq, parsed_args.num_cren, parsed_args.file, parsed_args.time_start, parsed_args.type_, qth)
