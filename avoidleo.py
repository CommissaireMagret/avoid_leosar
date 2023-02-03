import datetime
import time
import predict
import urllib.request
import json
import urllib.error
from calendar import timegm

"""########################
## VARIABLES GLOBALES ##
########################"""

# Variables pour mettre en forme le temps et déterminer le fuseau h de la machine.
utc_offset = time.localtime().tm_gmtoff
date_time_format = "%d/%m/%Y-%H:%M:%S"

# Variable pour gérer les érreurs réseau
url_error = False

# Var. globale de position géographique
qth = ()

# Décaration de la variable des TLE (chaîne vide)
tles = ""

# Chaîne de caractère pour archiver les passages LEO au dessus de la station au moment de l'emission.
passages_txt = """________                                                     ______   
___  __ \_____ ____________________ _______ _____________    ___  /__________     __  
__  /_/ /  __ `/_  ___/_  ___/  __ `/_  __ `/  _ \_  ___/    __  /_  _ \  __ \\   /_/  
_  ____// /_/ /_(__  )_(__  )/ /_/ /_  /_/ //  __/(__  )     _  / /  __/ /_/ /   __   
/_/     \__,_/ /____/ /____/ \__,_/ _\__, / \___//____/      /_/  \___/\____/   /_/   
                                   /____/                                            
       ~+

                *       +
          '                  |
      ()    .-.,="``"=.    - o -
            '=/_       \     |
         *   |  '=._    |
              \     `=./`,        '
           .   '=.__.=' `='      *
  +                         +
       O      *        '       .\n"""


def read_txt(file_name):
    """Opens a file and returns the content as a String

    :param file_name: The name of the file to read (with the file path if needed).
    :return: The string read in the txt file
    """
    f = open(file_name, 'r')
    return f.read()


def print_txt(file_name):
    """Prints the content of a text file

    :param file_name: The name of the file to print (with the file path if needed)
    """
    print(read_txt(file_name))


def write_txt(file_name, text):
    """Writes a String in a txt file

    :param file_name: Name of the file to write (with the file path if needed)
    :param text: String to write in file
    """
    txt_file = open(file_name, "wt")
    txt_file.write(text)


# Time outputs are in Epoch Unix timestamp (seconds since 01 Jan. 1970) UTC
# One day is 86400 seconds.
def predict_passes(time_start_epoch):
    """Predict passes of LEO SAR satellites with the pypredict library

    :param time_start_epoch: Beginning of the prediction timestamp
    :return: A sorted list of the passes:
             list[tuple[int = pass start time over 5°, int = pass end time under 5°, str = satellite name]]
    """
    print_txt('DISP/cospas70.txt')
    global tles
    global qth
    global url_error
    # Converting the W longitude in E longitude for the pypredict library :
    qth = (qth[0], 360 - qth[1], qth[2])
    # Downloading TLEs of LEOSAR sats from celestrak :
    try:
        urllib.request.urlretrieve("https://celestrak.org/NORAD/elements/gp.php?CATNR=38771", "TLE/tle1.txt")
        urllib.request.urlretrieve("https://celestrak.org/NORAD/elements/gp.php?CATNR=44387", "TLE/tle2.txt")
        urllib.request.urlretrieve("https://celestrak.org/NORAD/elements/gp.php?CATNR=25338", "TLE/tle3.txt")
        urllib.request.urlretrieve("https://celestrak.org/NORAD/elements/gp.php?CATNR=28654", "TLE/tle4.txt")
        urllib.request.urlretrieve("https://celestrak.org/NORAD/elements/gp.php?CATNR=33591", "TLE/tle5.txt")

    except urllib.error.URLError:
        url_error = True

    # Storing TLEs in .txt files :
    tle1 = read_txt('TLE/tle1.txt')
    tle2 = read_txt('TLE/tle2.txt')
    tle3 = read_txt('TLE/tle3.txt')
    tle4 = read_txt('TLE/tle4.txt')
    tle5 = read_txt('TLE/tle5.txt')
    tles = tle1 + tle2 + tle3 + tle4 + tle5

    # Makes a max 10 prediction from the current time. (10 days = 864000 sec.)
    time_end_epoch = int(time.time() + 864000)

    p1 = predict.transits(tle1, qth, time_start_epoch, time_end_epoch)
    p2 = predict.transits(tle2, qth, time_start_epoch, time_end_epoch)
    p3 = predict.transits(tle3, qth, time_start_epoch, time_end_epoch)
    p4 = predict.transits(tle4, qth, time_start_epoch, time_end_epoch)
    p5 = predict.transits(tle5, qth, time_start_epoch, time_end_epoch)

    timing = []
    # Goes through each prediction object of the LEO sats, extract and store the timings of the passes :
    for v, w, x, y, z in zip(p1, p2, p3, p4, p5):
        metop_b = v
        meteor_m2_2 = w
        noaa_15 = x
        noaa_18 = y
        noaa_19 = z

        timing.append(
            (local_to_utc(int(metop_b.above(5).start)), local_to_utc(int(metop_b.above(5).end)), "SARSAT-13 | METOP-B"))
        timing.append((local_to_utc(int(meteor_m2_2.above(5).start)), local_to_utc(int(meteor_m2_2.above(5).end)),
                       "COSPAS-14 | METEOR M2-2"))
        timing.append(
            (local_to_utc(int(noaa_15.above(5).start)), local_to_utc(int(noaa_15.above(5).end)), "SARSAT-07 | NOAA 15"))
        timing.append(
            (local_to_utc(int(noaa_18.above(5).start)), local_to_utc(int(noaa_18.above(5).end)), "SARSAT-10 | NOAA 18"))
        timing.append(
            (local_to_utc(int(noaa_19.above(5).start)), local_to_utc(int(noaa_19.above(5).end)), "SARSAT-12 | NOAA 19"))
    timing.sort()
    count = 0
    # Remove a pass if the start time and end time are the same.
    for i in range(len(timing)):
        if timing[i - count][1] - timing[i - count][0] < 1:
            timing.remove(timing[i - count])
            count += 1
    # for x in range(20): print(datetime.datetime.fromtimestamp(timing[x][0]).strftime("%d/%m/%Y %H:%M:%S => ") +
    # datetime.datetime.fromtimestamp(timing[x][1]).strftime("%d/%m/%Y %H:%M:%S | ") + timing[x][2])  # Ligne de débug
    return timing


def local_to_utc(local_time):
    """Returns the utc time of an epoch timestamp depending on the time zone of the machine

    :param local_time: int = an epoch timestamp
    :return: int = the same epoch timestamp in utc
    """
    utc_time = local_time - utc_offset
    return utc_time


def create_slots(num_slots, duration_seq, time_start):
    """Creates slots while avoiding LEO sats passes

    :param num_slots: int = number of slots desired
    :param duration_seq: int = duration of the slot in seconds (depends on the duration of the sequence to emit)
    :param time_start: str = date and time of the first slot desired (format : "%dd/%mm/%YYYY-%HH:%MM:%SS")
    :return: list[tuple[start of slot epoch, end of slot epoch]]
    """
    global passages_txt
    time_start_epoch = timegm(time.strptime(time_start, date_time_format))
    duration_s = duration_seq * 60
    passes = predict_passes(time_start_epoch)
    # Take the first slot available depending on the current time. Slots must be on the hour or 1/2 hour
    # i.e. 00:00 or 00:30
    slot = (int(local_to_utc(time_start_epoch) / 1800) + 1) * 1800
    slots = []
    i = 0
    while i < num_slots:
        free_slot = True
        for p in passes:
            if p[0] <= slot <= p[1] or p[0] <= slot + duration_s <= p[1] or slot <= p[0] <= slot + duration_s or slot <= \
                    p[1] <= slot + duration_s:
                free_slot = False
                break
        if free_slot:
            timestamp = datetime.datetime.fromtimestamp(slot)
            timestamp_end = datetime.datetime.fromtimestamp(slot + duration_s)
            slots.append((timestamp, timestamp_end))
            i += 1
        slot += 1800
    j = 0
    while passes[j][0] < slots[len(slots) - 1][1].timestamp():
        passages_txt += datetime.datetime.fromtimestamp(passes[j][0]).strftime("\n%d/%m/%Y %H:%M:%S => ") + \
                        datetime.datetime.fromtimestamp(passes[j][1]).strftime("%H:%M:%S | ") + passes[j][2]
        j += 1
    passages_txt += datetime.datetime.fromtimestamp(passes[j][0]).strftime("\n%d/%m/%Y %H:%M:%S => ") + \
                    datetime.datetime.fromtimestamp(passes[j][1]).strftime("%H:%M:%S | ") + passes[j][2]
    return slots


def writelst(num_seq, duration_seq, num_cren, file, time_start, file_path, qth_):
    """Writes the slots in a lst  file using above functions

    :param num_seq: str = name of the binary sequence without the ".bin" extension
    :param duration_seq: int = duration of the sequence to emit (rounded up)
    :param num_cren: int = number of slots desired
    :param file: str = name (with path if needed) of the .lst file to write
    :param time_start: str = date and time of the first slot desired (format : "%dd/%mm/%YYYY-%HH:%MM:%SS")
    :param file_path: str = path to the directory where .bin seq are stored on the FGB/SGB-simulator
    :param qth_: tuple[int = longitude, int = latitude EAST, int = altitude in meters]
    """
    global qth
    qth = qth_
    slots = create_slots(num_cren, duration_seq, time_start)
    lst = ""
    for i in range(len(slots)):
        date = slots[i][0].strftime("%Y%m%d")
        hour = slots[i][0].strftime("%H%M%S000")
        str_date_h = str(i + 1) + "," + date + '-' + hour + "," + file_path + str(num_seq) + ".bin,1"
        lst += str_date_h + "\n"
    print(lst)
    print(str(len(slots)) + ' slots créés ---> LST/' + file + '.lst')
    print()
    write_txt('LST/' + file + '.lst', lst)
    write_txt('TLE/tle_' + file + '_lst.tle', tles)
    write_txt('PASSES/PASSAGES_LEO_' + file + '.txt', passages_txt)
    print('Décallage UTC de votre machine : ' + str(time.localtime().tm_gmtoff) + ' secondes (pris en compte pour la'
                                                                                  ' création des slots).')
    if url_error:
        print("Votre machine ne semble pas connectée à internet. Les TLE peuvent être obsolètes.\nIl est recommandé "
              "d'éxecuter le programe avec une connexion internet.\nSi vous avez mis à jour les TLE manuellement vous "
              "pouvez ignorer ce message...\n")


def writebatch(num_seq, duration_seq, num_cren, file, time_start, type_, qth_):
    """Writes the slots in a json  file using above functions

    :param num_seq: str = name of the binary sequence without the ".bin" extension
    :param duration_seq: int = duration of the sequence to emit (rounded up)
    :param num_cren: int = number of slots desired
    :param file: str = name (with path if needed) of the .lst file to write
    :param time_start: str = date and time of the first slot desired (format : "%dd/%mm/%YYYY-%HH:%MM:%SS")
    :param file_path: str = path to the directory where .bin seq are stored on the FGB/SGB-simulator
    :param type_: = type for the simulator (PERSONAL or FACTORY, PERSONAL by default)
    :param qth_: tuple[int = longitude, int = latitude EAST, int = altitude in meters]
    """
    global qth
    qth = qth_
    json_list = []
    slots = create_slots(num_cren, duration_seq, time_start)
    for i in range(len(slots)):
        date = slots[i][0].strftime("%d/%m/%Y")
        hour = slots[i][0].strftime("%H:%M:%S")
        str_date_h = date + ' ' + hour
        date_end = slots[i][1].strftime("%d/%m/%Y")
        hour_end = slots[i][1].strftime("%H:%M:%S")
        str_date_h_end = date_end + ' ' + hour_end
        json_list.append({"id": {"name": num_seq, "type": type_}, "dateStart": str_date_h, "dateEnd": str_date_h_end,
                          "duration": str(duration_seq * 60)})
    json_batch = {"dateFormat": "dd/MM/yyyy HH:mm:ss", "scenarioList": json_list}
    json_slots = json.dumps(json_batch, indent=4)

    print(json_slots)
    print("\n" + str(len(slots)) + ' slots créés ---> BESIM/' + file + '.json')
    print()
    write_txt('BESIM/' + file + '.json', json_slots)
    write_txt('TLE/tle_' + file + '_besim.tle', tles)
    print('Décallage UTC de votre machine : ' + str(time.localtime().tm_gmtoff) + ' secondes (pris en compte pour la'
                                                                                  ' création des slots).\n')
    if url_error:
        print("Votre machine ne semble pas connectée à internet. Les TLE peuvent être obsolètes.\nIl est recommandé "
              "d'éxecuter le programe avec une connexion internet.\nSi vous avez mis à jour les TLE manuellement vous "
              "pouvez ignorer ce message...\n")
