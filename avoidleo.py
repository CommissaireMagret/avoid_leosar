import datetime
import time
import predict
import urllib.request
import json
import urllib.error
from calendar import timegm

utc_offset = time.localtime().tm_gmtoff

date_time_format = "%d/%m/%Y-%H:%M:%S"

url_error = False

qth = ()


def read_txt(file_name):
    f = open(file_name, 'r')
    return f.read()


def print_txt(file_name):
    print(read_txt(file_name))


def write_txt(file_name, text):
    txt_file = open(file_name, "wt")
    txt_file.write(text)


# Time outputs are in Epoch Unix timestamp (seconds since 01 Jan. 1970) UTC
# One day is 86400 seconds.
def predict_passes(time_start_epoch):
    global qth
    qth = (qth[0], 360 - qth[1], qth[2])
    global url_error
    try:
        urllib.request.urlretrieve("https://celestrak.org/NORAD/elements/gp.php?CATNR=38771", "TLE/tle1.txt")
        urllib.request.urlretrieve("https://celestrak.org/NORAD/elements/gp.php?CATNR=44387", "TLE/tle2.txt")
        urllib.request.urlretrieve("https://celestrak.org/NORAD/elements/gp.php?CATNR=25338", "TLE/tle3.txt")
        urllib.request.urlretrieve("https://celestrak.org/NORAD/elements/gp.php?CATNR=28654", "TLE/tle4.txt")
        urllib.request.urlretrieve("https://celestrak.org/NORAD/elements/gp.php?CATNR=33591", "TLE/tle5.txt")

    except urllib.error.URLError:
        url_error = True

    tle1 = read_txt('TLE/tle1.txt')
    tle2 = read_txt('TLE/tle2.txt')
    tle3 = read_txt('TLE/tle3.txt')
    tle4 = read_txt('TLE/tle4.txt')
    tle5 = read_txt('TLE/tle5.txt')

    time_end_epoch = int(time.time() + 864000)

    p1 = predict.transits(tle1, qth, time_start_epoch, time_end_epoch)
    p2 = predict.transits(tle2, qth, time_start_epoch, time_end_epoch)
    p3 = predict.transits(tle3, qth, time_start_epoch, time_end_epoch)
    p4 = predict.transits(tle4, qth, time_start_epoch, time_end_epoch)
    p5 = predict.transits(tle5, qth, time_start_epoch, time_end_epoch)

    timing = []
    for v, w, x, y, z in zip(p1, p2, p3, p4, p5):
        metop_b = v
        meteor_m2_2 = w
        noaa_15 = x
        noaa_18 = y
        noaa_19 = z

        timing.append((int(metop_b.start) - utc_offset, int(metop_b.end) - utc_offset))
        timing.append((int(meteor_m2_2.start) - utc_offset, int(meteor_m2_2.end) - utc_offset))
        timing.append((int(noaa_15.start) - utc_offset, int(noaa_15.end) - utc_offset))
        timing.append((int(noaa_18.start) - utc_offset, int(noaa_18.end) - utc_offset))
        timing.append((int(noaa_19.start) - utc_offset, int(noaa_19.end) - utc_offset))
    # print(datetime.datetime.fromtimestamp(timing[0][0]).strftime("%d/%m/%Y %H:%M:%S")) # Ligne de débug
    # print(datetime.datetime.fromtimestamp(timing[0][1]).strftime("%d/%m/%Y %H:%M:%S")) # Ligne de débug
    return timing


def local_to_utc(local_time):
    utc_time = local_time - utc_offset
    return utc_time


def create_slots(num_slots, duration_seq, time_start):
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
        for j in range(len(passes)):
            if passes[j][0] <= slot <= passes[j][1] or passes[j][0] <= slot + duration_s <= passes[j][1]:
                free_slot = False
                break

            if slot <= passes[j][0] <= slot + duration_s or slot <= passes[j][1] <= slot + duration_s:
                free_slot = False
                break

        if free_slot:
            timestamp = datetime.datetime.fromtimestamp(slot)
            timestamp_end = datetime.datetime.fromtimestamp(slot + duration_s)
            slots.append((timestamp, timestamp_end))
            i += 1
        slot += 1800
    return slots


def writelst(num_seq, duration_seq, num_cren, file, time_start, file_path, qth_):
    global qth
    qth = qth_
    print_txt('DISP/cospas70.txt')
    slots = create_slots(num_cren, duration_seq, time_start)
    lst = ""
    for i in range(len(slots)):
        date = slots[i][0].strftime("%Y%m%d")
        hour = slots[i][0].strftime("%H%M%S000")
        str_date_h = str(i+1) + "," + date + '-' + hour + "," + file_path + str(num_seq) + ".bin,1"
        lst += str_date_h + "\n"
    print(lst)
    print(str(len(slots)) + ' slots créés ---> LST/' + file)
    print()
    write_txt('LST/' + file, lst)
    print('Décallage UTC de votre machine : ' + str(time.localtime().tm_gmtoff) + ' secondes (pris en compte pour la'
                                                                                  ' création des slots).')


def writebatch(num_seq, duration_seq, num_cren, file, time_start, type_, qth_):
    global qth
    qth = qth_
    print_txt('DISP/cospas70.txt')
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
    print("\n" + str(len(slots)) + ' slots créés ---> BESIM/' + file)
    print()
    write_txt('BESIM/' + file, json_slots)
    print('Décallage UTC de votre machine : ' + str(time.localtime().tm_gmtoff) + ' secondes (pris en compte pour la'
                                                                                  ' création des slots).\n')
    if url_error:
        print("Votre machine ne semble pas connectée à internet. Les TLE peuvent être obsolètes.\nIl est recommandé "
              "d'éxecuter le programe avec une connexion internet.\nSi vous avez mis à jour les TLE manuellement vous "
              "pouvez ignorer ce message...\n")
