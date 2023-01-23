# avoid_leo Python tool

## Generate .lst files with lst.py :

pyhton3 lst.py [name of bin seq] [duration of the seq. in mins] [number of slots] [name of output file] [start date and hour : dd/mm/YYYY-hh:mm:ss]

### Generate .json file for besim :

pyhton3 besim.py [name of bin seq] [duration of the seq. in mins] [number of slots] [name of output file] [start date and hour : dd/mm/YYYY-hh:mm:ss] [type of beacon : PERSONNAL or FACTORY (PERSONNAL if not specified)]