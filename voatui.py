#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""

VOATUI.PY - VOACAP text-based User Interface, v2
(c) 2018 Jari Perkiömäki OH6BG

CHANGELOG:

22 Apr 2018: Total refactoring, using voacapl 0.7.4
26 Jun 2016: Small change in handling voaInFile & voaOutFile 
25 Jun 2016: Initial release.

Requires voacapl 0.7.4 from Jim Watson: https://github.com/jawatson/voacapl

"""

import datetime
import os
import sys
import urllib.request
import uuid
from pathlib import Path


def hour_line():

    a = ''
    for i in range(1, 25):
        a += "|%02d" % i
        if i == 24:
            a += " |"
    return a


def band(x: int):

    b = [80, 60, 40, 30, 20, 17, 15, 12, 10]
    return str(b[x - 1])


def hour_freq(h, f):

    r = REL[h][f]
    s = SDBW[h][f]

    if r == 0.00 and s >= -167:
        return " * "
    return col(r)


def col(y):

    if y == 0.00:
        return "   "
    elif 0.00 < y < 0.10:
        return " f "
    elif 0.10 <= y < 0.25:
        return " e "
    elif 0.25 <= y < 0.50:
        return " d "
    elif 0.50 <= y < 0.75:
        return " C "
    elif 0.75 <= y < 0.90:
        return " B "
    elif 0.90 <= y < 1.01:
        return " A "
    else:
        return " ? "


def create_prediction_graph():

    month, year, sunspot = X[0], X[1], X[4].rstrip(".")
    txlat, txlon, rxlat, rxlon, deg, km, mi = \
        Y[0] + Y[1], Y[2] + Y[3], Y[5] + Y[6], Y[7] + Y[8],\
        round(float(Y[9]) + 0.5),\
        round(float(Y[12]) + 0.5),\
        round(float(Y[12]) * 0.62137 + 0.5)
    pwr = Z[-1]
    db = float(W[-2])

    mode_dict = {'CW': 19.0, 'SSB': 38.0, 'AM': 48.0, 'FT8': 13.0, 'WSPR': 3.0}
    mode = list(mode_dict.keys())[list(mode_dict.values()).index(db)]

    res = "\nVOACAP Prediction via " + PATH + ". " + month + " " + str(year) +\
          ": SSN " + str(sunspot) + ". Power = " + pwr + ", " + mode + "\n"
    res += "TX (" + txlat + ", " + txlon + ") to RX (" + rxlat + ", " + rxlon + "): " +\
           str(km) + " km, " + str(mi) + " mi, " + str(deg) + " deg\n\n"
    res += "  %s\n" % hour_line()

    for n in range(9, 0, -1):

        res += "%s|" % band(n)
        for j in range(1, 25):
            res += hour_freq(j, n-1)
        res += "|%s\n" % band(n)

    res += "  %s\n\n" % hour_line()
    res += "A = 90 - 100%   d = 25 - 49%  * = REL 0%, but Signal Power over Noise\n"
    res += "B = 75 -  89%   e = 10 - 24%\n"
    res += "C = 50 -  74%   f =  1 -  9%\n"

    return res


def list_compare(a, b):

    for i in range(3):
        if not a[i][1] == b[i][1]:
            return i, a[i][1], b[i][1]


def print_frequencies(a):

    _, f = zip(*a)
    return list(f)


def s_meter(sig):

    if -164 <= sig <= -154:
        return "S0"
    elif -154 < sig <= -151:
        return "S1"
    elif -151 < sig <= -145:
        return "S2"
    elif -145 < sig <= -139:
        return "S3"
    elif -139 < sig <= -133:
        return "S4"
    elif -133 < sig <= -127:
        return "S5"
    elif -127 < sig <= -121:
        return "S6"
    elif -121 < sig <= -115:
        return "S7"
    elif -115 < sig <= -109:
        return "S8"
    elif -109 < sig <= -103:
        return "S9"
    elif sig > -103:
        return "S9+"

    return "--"


def assess_best_freq():

    rel3 = {}
    sdbw3 = {}
    snr3 = {}

    a = "The best operating frequencies (FREQ, FREQ2, FREQ3) by hour\n\n"
    a += "UTC".ljust(2) + \
         "SDBW".rjust(8) + \
         "REL".rjust(10) + \
         "SNR".rjust(8) + \
         "MUFday".rjust(9) + \
         "FOT".rjust(8) + \
         "MUF".rjust(8) + \
         "HPF".rjust(8) + \
         "FREQ".rjust(8) + \
         "FREQ2".rjust(8) + \
         "FREQ3".rjust(8) + \
         "\n\n"

    for t in range(1, 25):

        rel3[t] = sorted(zip(REL[t], FREQ), reverse=True)[:3]
        sdbw3[t] = sorted(zip(SDBW[t], FREQ), reverse=True)[:3]
        snr3[t] = sorted(zip(SNR[t], FREQ), reverse=True)[:3]

        if list_compare(rel3[t], sdbw3[t]):

            item, rel_fq, sdbw_fq = list_compare(rel3[t], sdbw3[t])
            if item == 2:
                fqs = print_frequencies(rel3[t])
                fqs[item] = sdbw_fq
            else:
                fqs = print_frequencies(sdbw3[t])

        else:
            fqs = print_frequencies(rel3[t])

        fot = METHOD_NINE[t][1]
        hpf = METHOD_NINE[t][2]

        pri, sec, ter = fqs
        muf = MUFDAY[t][FREQ.index(pri)]
        sig = SDBW[t][FREQ.index(pri)]
        rel1 = REL[t][FREQ.index(pri)]
        snr1 = SNR[t][FREQ.index(pri)]

        if snr3[t][0][0] < 0:
            rem = '-'
        elif rel3[t][0][0] < 0.1 and sdbw3[t][0][0] >= -164:
            rem = '+'
        elif rel3[t][0][0] < 0.1 and sdbw3[t][0][0] <= -164:
            rem = '*'
        else:
            rem = ''

        signal = str(sig) + " (" + s_meter(sig).ljust(3) + ")"

        a += "{0}{1}{2}%{3}{4}%{5}{6}{7}{8}{9}{10}{11}\n".format(str(t).rjust(2, '0'),
                                                                 signal.rjust(12),
                                                                 str(int(rel1 * 100)).rjust(6),
                                                                 str(snr1).rjust(8),
                                                                 str(int(muf * 100)).rjust(8),
                                                                 str(fot).rjust(8),
                                                                 str(MUFFREQ[t]).rjust(8),
                                                                 str(hpf).rjust(8),
                                                                 str(pri).rjust(8),
                                                                 rem.ljust(1),
                                                                 str(sec).rjust(7),
                                                                 str(ter).rjust(8)
                                                                 )

    return a


def create_input_file(yr, mo, ssn, txlat, txlon, rxlat, rxlon, txmode, power, path=0):

    mo = "%.2f" % float(mo)
    ssn = "%.1f" % ssn

    txlat = "%.2f" % txlat
    if float(txlat) < 0:
        txlat = txlat.lstrip('-') + "S"
    else:
        txlat += "N"

    txlon = "%.2f" % txlon
    if float(txlon) < 0:
        txlon = txlon.lstrip('-') + "W"
    else:
        txlon += "E"

    rxlat = "%.2f" % rxlat
    if float(rxlat) < 0:
        rxlat = rxlat.lstrip('-') + "S"
    else:
        rxlat += "N"

    rxlon = "%.2f" % rxlon
    if float(rxlon) < 0:
        rxlon = rxlon.lstrip('-') + "W"
    else:
        rxlon += "E"

    mode = [19.0, 38.0, 48.0, 13.0, 3.0][txmode - 1]
    power = "%.8f" % (power * 0.0008)

    if not path:
        p = "S     0\n"
    else:
        p = "L     1\n"

    input_file = "LINEMAX     999       number of lines-per-page\n"
    input_file += "COEFFS    CCIR\n"
    input_file += "TIME          1   24    1    1\n"
    input_file += "MONTH      " + str(yr) + " " + str(mo).rjust(5) + "\n"
    input_file += "SUNSPOT    " + str(ssn).rjust(5) + "\n"
    input_file += "LABEL     " + "TX".ljust(20) + "RX".ljust(20) + "\n"
    input_file += "CIRCUIT   " + txlat.rjust(6) + "   " + txlon.rjust(7) + "    " + rxlat.rjust(6) + "   " +\
                  rxlon.rjust(7) + "  " + p
    input_file += "SYSTEM       1. 155. 3.00  90. " + str(mode) + " 3.00 0.10\n"
    input_file += "FPROB      1.00 1.00 1.00 0.00\n"
    input_file += "ANTENNA       1    1    2   30     0.000[samples/sample.00    ]  0.0  " + str(power).rjust(8) + "\n"
    input_file += "ANTENNA       2    2    2   30     0.000[samples/sample.00    ]  0.0    0.0000\n"
    input_file += "FREQUENCY  3.60 5.30 7.1010.1014.1018.1021.1024.9028.20 0.00 0.00\n"
    input_file += "METHOD        9    0\n"
    input_file += "EXECUTE\n"
    input_file += "METHOD       30    0\n"
    input_file += "BOTLINES      5    8   10   12   21\n"
    input_file += "TOPLINES      1    2    3    4    6\n"
    input_file += "EXECUTE\n"
    input_file += "QUIT\n"

    return input_file


def get_ssn(yr, mo):

    mo = "%02d" % mo
    mydate = ' '.join([str(yr), mo])

    ssn = -1
    with open(ssnFile, "r") as ssnf:

        for row in ssnf:
            if mydate in row:
                ssn = float(row.split()[4]) * 0.7

    if not isinstance(ssn, float):

        print("Sunspot number not known for %s/%s. Exiting." % (mo, str(yr)))
        sys.exit(1)

    return ssn


def run_prediction(yr, k, ssn, tlat, tlon, rlat, rlon, m, power, path):

    global FREQ, METHOD_NINE, MUFFREQ, MUFDAY, SDBW, SNR, REL, X, Y, Z, W, PATH

    FREQ = []
    METHOD_NINE = []
    X = []
    Y = []
    Z = []
    W = []
    MUFFREQ = {}
    MUFDAY = {}
    SDBW = {}
    SNR = {}
    REL = {}

    input_deck = create_input_file(yr, k, ssn, tlat, tlon, rlat, rlon, m, power, path)

    with open(voaInPathFile, "w") as out_file:
        print(input_deck, file=out_file)

    os.system(voacaplCmd)

    FREQ, MUFFREQ, MUFDAY, SDBW, SNR, REL, X, Y, Z, W, PATH = parse_voacap_output(voaOutPathFile)
    METHOD_NINE = parse_method_nine(voaOutPathFile)

    return "{0}\n{1}".format(create_prediction_graph(), assess_best_freq())


def parse_method_nine(in_file):

    h = [0]
    method9 = {}

    with open(in_file, 'r') as f:

        h.extend(f.readlines()[43:67])
        f.seek(0)

    for rb in range(1, len(h)):

        bb = h[rb].split()
        method9[rb] = [float(x) for x in bb[-3:]]

    return method9


def parse_voacap_output(file):

    freq = []
    rel = {}
    snr = {}
    sdbw = {}
    mufday = {}
    muffreq = {}
    i = 0

    with open(file, 'r') as f:

        head = f.readlines()[82:87]
        f.seek(0)

        x = head[0].split()
        y = head[2].split()
        z = head[3].split()
        w = head[4].split()

        if "<Long>" in head[1]:
            path = "Long-Path"
        else:
            path = "Short-Path"

        for line in f:

            if line.endswith("FREQ\n"):
                freq_line = line.split()
                i = int(float(freq_line[0]))
                muffreq[i] = float(freq_line[1])
                if not len(freq):
                    freq = [float(x) for x in freq_line[2:11]]
            elif line.endswith("REL   \n"):
                rel_line = line.split()
                rel[i] = [float(x) for x in rel_line[1:10]]
            elif line.endswith("MUFday\n"):
                muf_line = line.split()
                mufday[i] = [float(x) for x in muf_line[1:10]]
            elif line.endswith("S DBW \n"):
                al = ''
                for j in range(6, 56, 5):
                    al += line[j:j + 5] + " "
                sdbw[i] = [int(x) for x in al.split()[1:10]]
            elif line.endswith("SNR   \n"):
                al = ''
                for j in range(6, 56, 5):
                    al += line[j:j + 5] + " "
                snr[i] = [int(x) for x in al.split()[1:10]]

    return freq, muffreq, mufday, sdbw, snr, rel, x, y, z, w, path


if __name__ == '__main__':

    preID = str(uuid.uuid4().fields[-1])[:8]
    preDir = os.path.join(os.getcwd(), 'predictions', preID)
    itshfbcDir = "/home/user/itshfbc"
    voacaplBin = "/usr/local/bin/voacapl --run-dir=%s --absorption-mode=a -s " % preDir
    voaInFile = preID + ".dat"
    voaOutFile = preID + ".out"
    voaInPathFile = os.path.join(preDir, voaInFile)
    voaOutPathFile = os.path.join(preDir, voaOutFile)
    voacaplCmd = voacaplBin + itshfbcDir + " " + voaInFile + " " + voaOutFile

    print("VOACAP P2P Text, version 2")
    print("by Jari Perkiömäki OH6BG (www.voacap.com)")
    print('.' * 80)

    ssnFile = os.path.join(itshfbcDir, 'ssn.txt')
    ssnFileExists = os.path.isfile(ssnFile)
    ssnUrl = "http://sidc.oma.be/silso/FORECASTS/prediML.txt"

    if not ssnFileExists:

        try:
            print('Trying to fetch the SSN data from the Internet...')
            urllib.request.urlretrieve(ssnUrl, ssnFile)
        except Exception as msg:
            print('Error getting SSNs: %s' % str(msg))
            sys.exit(1)

    print("\nPredefined values:")
    print("TX Antenna: Isotropic, 0 dBi gain")
    print("RX Antenna: Isotropic, 0 dBi gain\n")

    yr = 0
    while not 2017 <= yr <= 2019:

        try:
            yr = int(input("Enter year (2017..2019) [%d]: " % datetime.datetime.now().year))
        except ValueError:
            yr = datetime.datetime.now().year
            break

    mo = []
    while len(mo) < 1:

        # you can enter many different months at the same time, e.g. 1 4 9 12
	# 0 means all months from Jan to Dec
        mo = input("Enter month number (0..12) [0 = all]: ").split()
        mo = [int(x) for x in mo if x.isdigit()]
        mo = list(set(mo))
        mo = sorted([x for x in mo if 0 <= x <= 12])

    if 0 in mo:
        mo = list(range(1, 13))

    print("\nTRANSMITTER (TX)")
    print('-' * 16)

    tlat = -99
    while not -90 <= tlat <= 90:

        try:
            tlat = float(input("Enter latitude (-90..90) [1.0]: "))
        except ValueError:
            # set your own default latitude here
            tlat = 1.0
            break

    tlon = -199
    while not -180 <= tlon <= 180:

        try:
            tlon = float(input("Enter longitude (-180..180) [-1.0]: "))
        except ValueError:
            # set your own default longitude here
            tlon = -1.0
            break

    print("\nRECEIVER (RX)")
    print('-' * 16)

    rlat = -99
    while not -90 <= rlat <= 90:

        try:
            rlat = float(input("Enter latitude (-90..90): "))
        except ValueError:
            continue

    rlon = -199
    while not -180 <= rlon <= 180:

        try:
            rlon = float(input("Enter longitude (-180..180): "))
        except ValueError:
            continue

    power = 0
    while not 0.01 <= power <= 5000:

        try:
            power = float(input("\nEnter power in Watts (0.01..5000) [1500]: "))
        except ValueError:
            power = 1500
            break

    m = 0
    while not 1 <= m <= 5:

        try:
            m = int(input("Enter mode (1 = CW; 2 = SSB; 3 = AM; 4 = FT8; 5 = WSPR) [1]: "))
        except ValueError:
            m = 1
            break

    if not os.path.exists(preDir):

        try:
            os.makedirs(preDir)
        except Exception as msg:
            print(str(msg))
            sys.exit(1)

    for _, k in enumerate(mo):

        ssn = get_ssn(yr, k)
        print(run_prediction(yr, k, ssn, tlat, tlon, rlat, rlon, m, power, 0))
        print(run_prediction(yr, k, ssn, tlat, tlon, rlat, rlon, m, power, 1))

    for p in Path(preDir).glob("*.dat"):
        p.unlink()

    print("The result directory:", preDir)
