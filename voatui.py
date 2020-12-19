#!/usr/bin/env python3

"""

VOATUI.PY - VOACAP Point-to-Point predictions, text-based User Interface.
(c) Jari Perkiömäki OH6BG

CHANGELOG:

19 Dec 2020: Version 3: Major refactoring, enhanced Best Frequency analysis
12 Apr 2018: Version 2: Total refactoring, using voacapl 0.7.3
26 Jun 2016: Small change in handling voaInFile & voaOutFile
25 Jun 2016: Initial release.

Requires voacapl from Jim Watson:
http://www.qsl.net/hz1jw/voacapl/index.html
https://github.com/jawatson/voacapl

"""

import datetime
from itertools import islice
from pathlib import Path
import shlex
import struct
import subprocess
import sys
import urllib.request
import uuid


def zeropad(x):
    return f"{x:02}"


def hour_line():
    return f'|{"|".join(list(map(zeropad, range(1,25))))} |'


def band(x):

    b = [80, 60, 40, 30, 20, 17, 15, 12, 10]
    return str(b[x - 1])


def hour_freq(h, f):

    r = float(REL[h][f])
    s = float(DBW[h][f])

    if r == 0.00 and s >= -164:
        return " * "
    return col(r)


def get_rem(snr, rel, sdbw):
    if snr < 0:
        return '-'
    elif rel < 0.1 and sdbw >= -164:
        return '+'
    elif rel >= 0.1 and sdbw <= -164:
        return '*'

    return ''


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


def create_prediction_graph(file):

    res = "\n"
    with open(file, "r") as voaf:

        head = voaf.readlines()[80:86]
        voaf.seek(0)

        for line in voaf:
            if line.endswith("REL   \n"):
                REL.append(line.split()[1:10])
            if line.endswith("S DBW \n"):
                al = ''
                for i in range(6, 56, 5):
                    al += line[i:i + 5] + " "
                DBW.append(al.split()[1:10])

    x = head[0].split()
    y = head[2].split()
    z = head[3].split()
    w = head[5].split()
    month, year, ssn = x[0], x[1], x[4].rstrip(".")
    tlat, tlon, rlat, rlon, deg, km, mi = y[0] + y[1], y[2] + y[3], y[5] + y[6], y[7] + y[8], \
        round(float(y[9]) + 0.5), \
        round(float(y[12]) + 0.5), \
        round(float(y[12]) * 0.62137 + 0.5)
    pwr = z[-1]
    db = float(w[-2])

    path = "Long-Path" if "<Long>" in head[1] else "Short-Path"

    mode_dict = {'CW': 19.0, 'SSB': 38.0, 'AM': 48.0, 'FT8': 13.0, 'WSPR': 3.0}
    # swap mode dictionary
    mode = {value:key for key, value in mode_dict.items()}

    res += (f"VOACAP Prediction via {path}. {month} {year}: SSN {ssn}. Power={pwr}, {mode[db]}\n"
            f"TX ({tlat}, {tlon}) to RX ({rlat}, {rlon}): {km} km, {mi} mi, {deg} deg\n\n"
            f"  {hour_line()}\n")

    for n in range(9, 0, -1):
        res += f"{band(n)}|"
        for j in range(0, 24):
            res += hour_freq(j, n - 1)
        res += f"|{band(n)}\n"

    res += (f"  {hour_line()}\n\n"
            "A = 90 - 100%   d = 25 - 49%  * = REL 0%, but Signal Power over Noise\n"
            "B = 75 -  89%   e = 10 - 24%\n"
            "C = 50 -  74%   f =  1 -  9%\n")

    return res


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


def assess_best_freq(in_file):

    freq, h, i, a = [], [], 0, ''
    mufday, sdbw, snr, snrxx, snrup, rel, siglw, sigup, method_nine = {}, {}, {}, {}, {}, {}, {}, {}, {}
    col_format = '11s5s5s5s5s5s5s5s5s5s5s5s8s'
    muf_format = '64s4s6s6s7s'

    with in_file.open(mode='rb') as lines:

        for hour in list(islice(lines, 41, 65)):
            _, gmt, muf, fot, hpf = struct.unpack(muf_format, hour)
            hh, *mfh = list(map(float, (gmt, muf, fot, hpf)))
            method_nine[int(hh)] = mfh

        for y in lines:
            if y.endswith(b"FREQ\n"):
                z = y.split()
                i = int(float(z[0]))
                if not freq:
                    z = z[2:-1]
                    while z[-1] == b'0.0':
                        del z[-1]
                    freq = list(map(float, z))
            else:
                try:
                    d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11, d12, parameter = struct.unpack(col_format, y)
                except:
                    continue

                if parameter.decode().strip() == 'S DBW':
                    sdbw[i] = list(map(int, (d2, d3, d4, d5, d6, d7, d8, d9, d10)))
                elif parameter.decode().strip() == 'REL':
                    rel[i] = list(map(float, (d2, d3, d4, d5, d6, d7, d8, d9, d10)))
                elif parameter.decode().strip() == 'SNR':
                    snr[i] = list(map(int, (d2, d3, d4, d5, d6, d7, d8, d9, d10)))
                elif parameter.decode().strip() == 'MUFday':
                    mufday[i] = list(map(float, (d2, d3, d4, d5, d6, d7, d8, d9, d10)))
                elif parameter.decode().strip() == 'SIG LW':
                    siglw[i] = list(map(float, (d2, d3, d4, d5, d6, d7, d8, d9, d10)))
                elif parameter.decode().strip() == 'SIG UP':
                    sigup[i] = list(map(float, (d2, d3, d4, d5, d6, d7, d8, d9, d10)))
                elif parameter.decode().strip() == 'SNRxx':
                    snrxx[i] = list(map(int, (d2, d3, d4, d5, d6, d7, d8, d9, d10)))
                elif parameter.decode().strip() == 'SNR UP':
                    snrup[i] = list(map(float, (d2, d3, d4, d5, d6, d7, d8, d9, d10)))
                else:
                    continue

    a += ("The best operating frequencies (FREQ1, FREQ2, FREQ3) by hour\n\n"
          f"{'UTC':<2}"
          f"{'SDBW':>8}"
          f"{'ΔSIG':>10}"
          f"{'REL':>7}"
          f"{'SNR':>6}"
          f"{'ΔSNR':>7}"
          f"{'MUFday':>8}"
          f"{'FOT':>8}"
          f"{'MUF':>8}"
          f"{'HPF':>8}"
          f"{'FREQ1':>8}"
          f"{'FREQ2':>8}"
          f"{'FREQ3':>8}\n\n")

    for t in range(1, 25):
        sig_rem, snr_rem = '', ''
        sig = sorted(list(zip(sdbw[t], freq)), reverse=True)[:3]
        sn = sorted(list(zip(snr[t], freq)), reverse=True)[:3]
        r = sorted(list(zip(rel[t], freq)), reverse=True)[:3]
        muf, fot, hpf = method_nine[t]
        pri, sec, ter = list(zip(*sig))[1]
        muf_t = mufday[t][freq.index(pri)]
        rel_t = rel[t][freq.index(pri)]
        sig_t = sig[0][0]
        sigup_t = sigup[t][freq.index(pri)]
        siglw_t = siglw[t][freq.index(pri)]
        snr_t = snr[t][freq.index(pri)]
        snr90_t = snrxx[t][freq.index(pri)]
        snrup_t = snrup[t][freq.index(pri)]
        rem1 = get_rem(sn[0][0], r[0][0], sig[0][0])
        rem2 = get_rem(sn[1][0], r[1][0], sig[1][0])
        rem3 = get_rem(sn[2][0], r[2][0], sig[2][0])
        sm = f"{sig_t} ({s_meter(sig_t):<3})"

        delta_sig = (sig_t + sigup_t) - (sig_t - siglw_t)
        delta_sig = f"{delta_sig:.1f}"
        if float(delta_sig) >= 47:
            sig_rem = '*'

        delta_snr = (snr_t + snrup_t) - snr90_t
        delta_snr = f"{delta_snr:.1f}"
        if float(delta_snr) >= 47:
            snr_rem = '*'

        a += (f"{t:>02}"
              f"{sm:>12}"
              f"{delta_sig:>7}"
              f"{sig_rem:<1}"
              f"{int(rel_t * 100):>5}%"
              f"{snr_t:>6}"
              f"{delta_snr:>7}"
              f"{snr_rem:<1}"
              f"{int(muf_t * 100):>6}%"
              f"{fot:>8}"
              f"{muf:>8}"
              f"{hpf:>8}"
              f"{pri:>8}"
              f"{rem1:<1}"
              f"{sec:>7}"
              f"{rem2:<1}"
              f"{ter:>7}"
              f"{rem3:<1}\n")

    return a


def create_input_file(yr, mo, ssn, txlat, txlon, rxlat, rxlon, txmode, power, path=0):

    mo = f"{float(mo):.2f}"
    ssn = f"{ssn:.1f}"

    txlat = f"{txlat:.2f}"
    if float(txlat) < 0:
        txlat = txlat.lstrip('-') + "S"
    else:
        txlat += "N"

    txlon = f"{txlon:.2f}"
    if float(txlon) < 0:
        txlon = txlon.lstrip('-') + "W"
    else:
        txlon += "E"

    rxlat = f"{rxlat:.2f}"
    if float(rxlat) < 0:
        rxlat = rxlat.lstrip('-') + "S"
    else:
        rxlat += "N"

    rxlon = f"{rxlon:.2f}"
    if float(rxlon) < 0:
        rxlon = rxlon.lstrip('-') + "W"
    else:
        rxlon += "E"

    mode = [19.0, 38.0, 48.0, 13.0, 3.0][txmode - 1]
    power = f"{power * 0.0008:.4f}"
    p = "S     0" if not path else "L     1"

    input_file = ("LINEMAX     999       number of lines-per-page\n"
                  "COEFFS    CCIR\n"
                  "TIME          1   24    1    1\n"
                  f"MONTH      {yr}{mo:>5}\n"
                  f"SUNSPOT    {ssn:>5}\n"
                  f"LABEL     {'TX':<20}{'RX':<20}\n"
                  f"CIRCUIT   {txlat:>6}   {txlon:>7}    {rxlat:>6}   {rxlon:>7}  {p}\n"
                  f"SYSTEM       1. 153. 3.00  90. {mode} 3.00 0.10\n"
                  "FPROB      1.00 1.00 1.00 0.00\n"
                  f"ANTENNA       1    1    2   30     0.000[samples/sample.00    ]  0.0  {power:>8}\n"
                  "ANTENNA       2    2    2   30     0.000[samples/sample.00    ]  0.0    0.0000\n"
                  "FREQUENCY  3.60 5.36 7.1010.1014.1018.1021.1024.9028.20 0.00 0.00\n"
                  "METHOD        9    0\n"
                  "EXECUTE\n"
                  "METHOD       30    0\n"
                  "EXECUTE\n"
                  "QUIT\n")

    return input_file


def to_loc(maiden):

    assert isinstance(maiden, str), 'Maidenhead is a string'
    maiden = maiden.strip().upper()

    N = len(maiden)
    assert 8 >= N >= 2 and N % 2 == 0, 'Maidenhead locator requires 2-8 characters, even number of characters'

    O = ord('A')
    lon = -180
    lat = -90

    lon += (ord(maiden[0]) - O) * 20
    lat += (ord(maiden[1]) - O) * 10

    if N >= 4:
        lon += int(maiden[2]) * 2
        lat += int(maiden[3]) * 1
    elif N >= 6:
        lon += (ord(maiden[4]) - O) * 5./60
        lat += (ord(maiden[5]) - O) * 2.5/60
    elif N >= 8:
        lon += int(maiden[6]) * 5./600
        lat += int(maiden[7]) * 2.5/600

    return lat, lon


def to_maiden(position, precision=4):

    assert len(position) == 2, 'lat lon required'
    lat = float(position[0])
    lon = float(position[1])

    A = ord('A')
    a = divmod(lon + 180, 20)
    b = divmod(lat + 90, 10)
    astring = chr(A + int(a[0])) + chr(A + int(b[0]))
    lon = a[1] / 2.
    lat = b[1]
    i = 1

    while i < precision:

        i += 1
        a = divmod(lon, 1)
        b = divmod(lat, 1)

        if not (i % 2):
            astring += str(int(a[0])) + str(int(b[0]))
            lon = 24 * a[1]
            lat = 24 * b[1]
        else:
            astring += chr(A + int(a[0])) + chr(A + int(b[0]))
            lon = 10 * a[1]
            lat = 10 * b[1]

    if len(astring) >= 6:
        astring = astring[:4] + astring[4:6].lower() + astring[6:]

    return astring


def get_ssn(yr, mo):

    mo = f"{mo:02}"
    mydate = ' '.join([str(yr), mo])

    ssn = -1
    with open(ssnFile, "r") as ssnf:
        for row in ssnf:
            if mydate in row:
                ssn = float(row.split()[4]) * 0.7

    if not isinstance(ssn, float):
        print(f"Sunspot number NOT found for {mo}/{yr}. Check SSNs from: {ssnFile}")
        sys.exit()

    return ssn


def run_prediction(yr, k, ssn, tlat, tlon, rlat, rlon, m, power, path):

    input_deck = create_input_file(yr, k, ssn, tlat, tlon, rlat, rlon, m, power, path)

    with open(voaInPathFile, "w") as out_file:
        print(input_deck, file=out_file)

    args = shlex.split(voacaplCmd)
    try:
        cp = subprocess.run(args, stderr=subprocess.PIPE, stdout=subprocess.PIPE, timeout=5)
    except Exception as msg:
        print(f"Error in subprocess: {msg}")
        sys.exit()

    return f"{create_prediction_graph(voaOutPathFile)}\n{assess_best_freq(voaOutPathFile)}"


if __name__ == '__main__':

    preID = str(uuid.uuid4().fields[-1])[:8]
    preDir = Path.cwd() / 'predictions' / preID
    itshfbcDir = Path("/root/itshfbc")
    voacaplBin = f"/usr/local/bin/voacapl --run-dir={preDir} --absorption-mode=a -s"
    voaInFile = f"{preID}.dat"
    voaOutFile = f"{preID}.out"
    voaInPathFile = preDir / voaInFile
    voaOutPathFile = preDir /voaOutFile

    voacaplCmd = f"{voacaplBin} {itshfbcDir} {voaInFile} {voaOutFile}"

    # set your default coordinates here
    def_lat = 63.146
    def_lon = 21.542

    print(f"{'.' * 80}\n"
          "VOACAP Point-to-Point Predictions, Version 3\n"
          "by Jari Perkiömäki OH6BG (www.voacap.com)\n"
          f"{'.' * 80}")

    # Create prediction directory
    if not preDir.exists():

        try:
            preDir.mkdir(parents=True, exist_ok=True)
        except Exception as msg:
            print(msg)
            sys.exit()
    
    # Get recent sunspot numbers
    ssnFile = preDir / 'ssn.txt'
    ssnUrl = "http://sidc.oma.be/silso/FORECASTS/prediML.txt"

    if not ssnFile.exists():

        try:
            print('Fetching the SSN data from the Internet...')
            urllib.request.urlretrieve(ssnUrl, ssnFile)
        except Exception as msg:
            print(f'Error getting SSNs: {msg}')
            sys.exit()

    with open(ssnFile) as f:
        lines = f.read().splitlines()
        fst_year, fst_month, *_ = lines[0].split()
        lst_year, lst_month, *_ = lines[-1].split()
    
    print("\nPREDEFINED VALUES:\n"
          "TX Antenna: Isotropic, 0 dBi gain\n"
          "RX Antenna: Isotropic, 0 dBi gain\n"
          "Min. TOA  : 3 degrees\n"
          f"SSN dates : {fst_month}/{fst_year}..{lst_month}/{lst_year}\n"
    )

    yr = 0
    while not 2020 <= yr <= 2021:

        try:
            yr = int(input("Enter year (2020..2021) [%d]: " % datetime.datetime.now().year))
        except ValueError:
            yr = datetime.datetime.now().year
            break

    mo = []
    while len(mo) < 1:

        mo = input("Enter month number (1..12): ").split()
        mo = [int(x) for x in mo if x.isdigit()]
        mo = list(set(mo))
        mo = sorted([x for x in mo if 1 <= x <= 12])
        mo = list(range(1, 13)) if not mo else mo

    print("\nTRANSMITTER (TX)\n"
    f"{'.' * 16}")

    tlat = -99
    while not -90 <= tlat <= 90:

        try:
            tlat = float(input("Enter latitude (-90..90) [63.146]: "))
        except ValueError:
            tlat = def_lat
            break

    tlon = -199
    while not -180 <= tlon <= 180:

        try:
            tlon = float(input("Enter longitude (-180..180) [21.542]: "))
        except ValueError:
            tlon = def_lon
            break

    print("\nRECEIVER (RX)\n"
    f"{'.' * 16}")

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
    while not 1 <= power <= 5000:

        try:
            power = float(input("\nEnter power in Watts (1..5000) [1500]: "))
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

    for k in mo:

        ssn = get_ssn(yr, k)
        REL, DBW = [], []
        print(run_prediction(yr, k, ssn, tlat, tlon, rlat, rlon, m, power, 0))
        REL, DBW = [], []
        print(run_prediction(yr, k, ssn, tlat, tlon, rlat, rlon, m, power, 1))

    for p in preDir.glob("*.dat"):
        p.unlink()

    print(f"Prediction directory: {preDir}")
