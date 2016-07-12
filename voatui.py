#!/usr/bin/env python3
# -*- coding: latin-1 -*-

'''

VOATUI.PY - VOACAP text-based User Interface.
(c) Jari Perkiömäki OH6BG 

26 Jun 2016: Small change in handling voaInFile & voaOutFile 
25 Jun 2016: Initial release.

Requires voacapl from Jim Watson: http://www.qsl.net/hz1jw/voacapl/index.html

'''

def drawLine( len, char ):
    print(''.ljust(len, char))

def hourLine():
    
    a = ''
    for i in range (1,25):
        a += "|" + str(i).zfill(2) 
    if i == 24:
        a += " |"
    else:
        a += "|"
    return a

def band( x ):
    
    if x == 1:
        return "80"
    elif x == 2:
        return "60"
    elif x == 3:
        return "40"
    elif x == 4:
        return "30"
    elif x == 5:
        return "20"
    elif x == 6:
        return "17"
    elif x == 7:
        return "15"
    elif x == 8:
        return "12"
    elif x == 9:
        return "10"

def hourFreq( h, f ):

    r = float(rel[h][f])
    s = float(dbw[h][f])
    
    if ( r == 0.00 and s >= -167 ):
        return " * "
    else:
        return col(r)

def col( y ):

    if y == 0.00:
        return "   "
    elif ( y > 0.00  and y < 0.10 ):
        return " f "
    elif ( y >= 0.10 and y < 0.25 ):
        return " e "
    elif ( y >= 0.25 and y < 0.50 ):
        return " d "
    elif ( y >= 0.50 and y < 0.75 ):
        return " C "
    elif ( y >= 0.75 and y < 0.90 ):
        return " B "
    elif ( y >= 0.90 and y < 1.01 ):
        return " A "
    else:
        return " ? "

def process( file ):

    res = ""
    with open(file, "r") as voaf:
        
        head = voaf.readlines()[26:31]
        voaf.seek(0)
        for line in voaf:
            if "-  REL" in line:
                rel.append(line.split()[1:10])
            if "S DBW" in line:
                al = ''
                for i in range(6,56,5):
                    al += line[i:i+5] + " "
                dbw.append(al.split()[1:10])

    x = head[0].split()
    y = head[2].split()
    z = head[3].split()
    w = head[4].split()
    month, year, ssn = x[0], x[1], x[4].rstrip(".")
    tlat, tlon, rlat, rlon, deg, km, mi = \
          y[0]+y[1], y[2]+y[3], y[5]+y[6], y[7]+y[8], round(float(y[9])+0.5), round(float(y[12])+0.5), round(float(y[12])*0.62137+0.5)
    pwr = z[-1]
    db = float(w[-2])

    if "<Long>" in head[1]:
        path = "Long-Path"
    else:
        path = "Short-Path"

    if db == 24.0:
        mode = "CW"
    elif db == 38.0:
        mode = "SSB"
    elif db == 48.0:
        mode = "AM"
    else:
        mode = ""

    res += "VOACAP Prediction via " + path + ". " + month + " " + str(year) + ": SSN " + str(ssn) + ". Power = " + pwr + ", " + mode + "\n";
    res += "TX (" + tlat + ", " + tlon + ") to RX (" + rlat + ", " + rlon + "): " + str(km) + " km, " + str(mi) + " mi, " + str(deg) + " deg\n\n";
    res += "  " + hourLine() + "\n";

    for i in range(9, 0, -1):
        res += band(i) + "|"
        for j in range(0, 24):
            res += hourFreq(j,i-1)
        res += "|" + band(i) + "\n"

    res += "  " + hourLine() + "\n\n";
    res += "A = 90 - 100%   d = 25 - 49%  * = REL 0%, but Signal Power over Noise\n";
    res += "B = 75 -  89%   e = 10 - 24%\n";
    res += "C = 50 -  74%   f =  1 -  9%\n";
    
    return res

import os, sys, urllib.request

rel = []
dbw = []
path = ''

voaInFile = os.path.join(os.path.expanduser('~'), 'itshfbc', 'run', 'voatui.dat')
voaOutFile = os.path.join(os.path.expanduser('~'), 'itshfbc', 'run', 'voatui.out')

os.system("clear")

print("Welcome to the VOACAP text-based User Interface!")
print("by Jari Perkiömäki OH6BG (www.voacap.com)")
drawLine(80,".")

ssnFile = os.path.join(os.path.expanduser('~'), 'itshfbc', 'ssn.txt')
ssnFileExists = os.path.isfile(ssnFile)
ssnUrl = "ftp://ftp.ngdc.noaa.gov/STP/space-weather/solar-data/solar-indices/sunspot-numbers/predicted/table_international-sunspot-numbers_monthly-predicted.txt"

if not ssnFileExists:
    try:
        print('Fetching the SSN data from the Internet...')
        urllib.request.urlretrieve(ssnUrl, ssnFile)
    except:
        print('Failed to fetch the SSN data. Are you connected to the Internet? Aborting...')
        sys.exit(1)

print("\nPredefined values:")
print("TX Antenna: Isotropic, 0 dBi gain")
print("RX Antenna: Isotropic, 0 dBi gain\n")

yr = 0

while ( yr == 0 ) :

    yr = input("Enter year (2016..2020): ")
    if ( int(yr) < 2016 or int(yr) > 2020 ):
        yr = 0
    else:
        break

mo = 0

while ( mo == 0 ) :

    mo = input("Enter month number (1..12): ")
    if ( int(mo) < 1 or int(mo) > 12 ):
        mo = 0
    else:
        break

print("\nTRANSMITTER (TX)")
drawLine(16,"-")

tlat = 0.00

while ( tlat == 0.00 ) :

    tlat = input("Enter latitude (-90..90): ")
    if ( float(tlat) < -90 or float(tlat) > 90 ):
        tlat = 0.00
    else:
        tlat = "%.2f" % float(tlat)
        if float(tlat) < 0.00:
            tlat = str(tlat).lstrip('-') + "S"
        else:
            tlat = str(tlat) + "N"
        break

tlon = 0.00

while ( tlon == 0.00 ) :

    tlon = input("Enter longitude (-180..180): ")
    if ( float(tlon) < -180 or float(tlon) > 180 ):
        tlon = 0.00
    else:
        tlon = "%.2f" % float(tlon)
        if float(tlon) < 0.00:
            tlon = str(tlon).lstrip('-') + "W"
        else:
            tlon = str(tlon) + "E"
        break

print("\nRECEIVER (RX)")
drawLine(16,"-")

rlat = 0.00

while ( rlat == 0.00 ) :

    rlat = input("Enter latitude (-90..90): ")
    if ( float(rlat) < -90 or float(rlat) > 90 ):
        rlat = 0.00
    else:
        rlat = "%.2f" % float(rlat)
        if float(rlat) < 0.00:
            rlat = str(rlat).lstrip('-') + "S"
        else:
            rlat = str(rlat) + "N"
        break

rlon = 0.00

while ( rlon == 0.00 ) :

    rlon = input("Enter longitude (-180..180): ")
    if ( float(rlon) < -180 or float(rlon) > 180 ):
        rlon = 0.00
    else:
        rlon = "%.2f" % float(rlon)
        if float(rlon) < 0.00:
            rlon = str(rlon).lstrip('-') + "W"
        else:
            rlon = str(rlon) + "E"
        break

power = 0

while ( power == 0 ) :

    power = input("\nEnter power in Watts (1..1500): ")
    if ( float(power) < 1 or float(power) > 1500 ):
        power = 0
    else:
        power = float(power) * 0.0008
        power = "%.4f" % power
        break

m = 0
mode = 0.00

while ( m == 0 ) :

    m = input("Enter mode (1 = CW; 2 = SSB; 3 = AM): ")
    if ( int(m) < 1 or int(m) > 3 ):
        m = 0
    elif int(m) == 1:
        mode = 24.0
    elif int(m) == 2:
        mode = 38.0
    elif int(m) == 3:
        mode = 48.0
    else:
        break

# grep the SSN from ssnFile

with open(ssnFile, "r") as ssnf:
        
    for line in ssnf:
        if yr in line:
            ssn = line.split()[int(mo)]
            ssn = round(float(ssn) + 0.5)
            ssn = "%.1f" % ssn

mo = "%.2f" % float(mo)

# create the input file & run prediction

inp1  = "LINEMAX     999       number of lines-per-page\n"
inp1 += "COEFFS    CCIR\n"
inp1 += "TIME          1   24    1    1\n"
inp1 += "MONTH      " + str(yr) + " " + str(mo).rjust(5) + "\n"
inp1 += "SUNSPOT    " + str(ssn).rjust(5) + "\n"
inp1 += "LABEL     " + "TX".ljust(20) + "RX".ljust(20) + "\n"
sp    = "CIRCUIT   " + tlat.rjust(6) + "   " + tlon.rjust(7) + "    " + rlat.rjust(6) + "   " + rlon.rjust(7) + "  " + "S     0\n"
inp2  = "SYSTEM       1. 155. 3.00  90. " + str(mode) + " 3.00 0.10\n"
inp2 += "FPROB      1.00 1.00 1.00 0.00\n"
inp2 += "ANTENNA       1    1    2   30     0.000[samples/sample.00    ]  0.0  " + str(power).rjust(8) + "\n"
inp2 += "ANTENNA       2    2    2   30     0.000[samples/sample.00    ]  0.0    0.0000\n"
inp2 += "FREQUENCY  3.60 5.30 7.1010.1014.1018.1021.1024.9028.20 0.00 0.00\n"
inp2 += "METHOD       30    0\n"
inp2 += "BOTLINES      8   12   21\n"
inp2 += "TOPLINES      1    2    3    4    6\n"
inp2 += "EXECUTE\n"
inp2 += "QUIT\n"

inp = inp1 + sp + inp2

print("\nThank you! Your VOACAP input file is as follows:\n\n" + inp)
input("Press ENTER to run the prediction...")
os.system("clear")

with open(voaInFile, "w") as out_file:
    print(inp, file=out_file)

print("\nCalculating Short-Path & Long-Path...")
os.system("voacapl -s ~/itshfbc voatui.dat voatui.out")
result = process(voaOutFile) + "\n"

rel = []
dbw = []

lp  = "CIRCUIT   " + tlat.rjust(6) + "   " + tlon.rjust(7) + "    " + rlat.rjust(6) + "   " + rlon.rjust(7) + "  " + "L     1\n"
inp = inp1 + lp + inp2

with open(voaInFile, "w") as out_file:
    print(inp, file=out_file)

os.system("voacapl -s ~/itshfbc voatui.dat voatui.out")
result += process(voaOutFile)

print(result)
sys.exit(1)

## ENJOY! ##
