# VOATUI
Text-based User Interface for voacapl (Python), version 2

This is a completely refactored version of voatui.py.

This Python script requires voacapl 0.7.4 from Jim Watson: https://github.com/jawatson/voacapl

## Quick Guide

1. In the Python script, set the parameters "itshfbcDir" and "voacaplBin" as per your system.
2. You can set the Python script executable: chmod u+x voatui.py
3. Run the script: ./voatui.py . When run for the first time, the script tries to connect to the Internet and fetch the sunspot numbers.

### A sample run:

```
VOACAP P2P Text, version 2
by Jari Perkiömäki OH6BG (www.voacap.com)
................................................................................

Predefined values:
TX Antenna: Isotropic, 0 dBi gain
RX Antenna: Isotropic, 0 dBi gain

Enter year (2017..2019) [2018]: 2018
Enter month number (0..12) [0 = all]: 4

TRANSMITTER (TX)
----------------
Enter latitude (-90..90) [1.0]: 10.5
Enter longitude (-180..180) [-1.0]: -20.8

RECEIVER (RX)
----------------
Enter latitude (-90..90): 50
Enter longitude (-180..180): -100

Enter power in Watts (0.01..5000) [1500]: 100
Enter mode (1 = CW; 2 = SSB; 3 = AM; 4 = FT8; 5 = WSPR) [1]: 1

VOACAP Prediction via Short-Path. Apr 2018: SSN 7. Power = 0.080kW, CW
TX (10.50N, 20.80W) to RX (50.00N, 100.00W): 8344 km, 5185 mi, 320 deg

  |01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24 |
10|                                                                        |10
12|                                                                        |12
15|                                     f  f                 f  f     f    |15
17| f                                f  e  e  e     f  e  e  d  d  d  d  e |17
20| d  d  f                       d  d  e  e  e  e  d  d  d  C  C  C  C  d |20
30| C  C  d  d  e  e  f  f  f  e  e  *                    f  e  d  C  C  C |30
40| B  B  C  C  C  C  C  d  e  f  *                                f  C  C |40
60| C  B  B  C  C  C  C  d  f  *                                   *  d  C |60
80| C  C  C  C  C  C  d  f  *                                         *  d |80
  |01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24 |

A = 90 - 100%   d = 25 - 49%  * = REL 0%, but Signal Power over Noise
B = 75 -  89%   e = 10 - 24%
C = 50 -  74%   f =  1 -  9%

The best operating frequencies (FREQ, FREQ2, FREQ3) by hour

UTC    SDBW       REL     SNR   MUFday     FOT     MUF     HPF    FREQ   FREQ2   FREQ3

01  -128 (S5 )    76%      30      99%     9.0    11.7    15.3     7.1     5.3    10.1
02  -125 (S6 )    78%      29     100%     8.8    11.6    14.6     5.3     7.1     3.6
03  -124 (S6 )    76%      29      99%     7.1     9.4    11.9     5.3     3.6     7.1
04  -122 (S6 )    71%      25     100%     6.3     8.4    10.6     3.6     5.3     7.1
05  -123 (S6 )    68%      27      96%     6.1     8.1    10.2     5.3     3.6     7.1
06  -126 (S6 )    63%      24      95%     5.9     7.8     9.8     5.3     3.6     7.1
07  -127 (S5 )    63%      23      97%     6.0     7.4     8.9     5.3     3.6     7.1
08  -133 (S4 )    40%      17      96%     5.9     7.3     8.7     5.3     7.1     3.6
09  -142 (S3 )    24%      13      75%     6.4     7.9     9.5     7.1     5.3     3.6
10  -149 (S2 )     5%       8      95%     7.7     9.6    11.5     7.1    10.1     5.3
11  -152 (S1 )    18%      12      86%     9.8    12.1    14.5    10.1    14.1     7.1
12  -157 (S0 )    40%      15      49%    11.4    14.1    16.9    14.1    10.1    18.1
13  -162 (S0 )    19%       9      80%    13.1    16.1    19.3    14.1    18.1    10.1
14  -166 (-- )    17%       5      75%    12.7    15.7    18.8    14.1    18.1    10.1
15  -164 (S0 )    14%       7      63%    12.7    15.1    17.8    14.1    18.1    10.1
16  -159 (S0 )    23%      11      76%    13.2    15.2    17.7    14.1    10.1    18.1
17  -157 (S0 )    27%      13      82%    13.5    15.5    17.7    14.1    10.1    18.1
18  -154 (S0 )    37%      15      82%    13.6    15.5    17.9    14.1    10.1    18.1
19  -151 (S1 )    43%      17      73%    13.4    15.5    18.0    14.1    10.1    18.1
20  -147 (S2 )    54%      21      77%    12.9    15.9    18.4    14.1    10.1    18.1
21  -142 (S3 )    62%      25      80%    13.0    16.1    18.7    14.1    10.1    18.1
22  -140 (S3 )    65%      27      78%    12.9    15.9    18.4    14.1    10.1     7.1
23  -137 (S4 )    64%      26      87%     9.6    13.9    18.5    10.1     7.1    14.1
24  -133 (S4 )    68%      28      96%     8.4    12.1    16.1     7.1     5.3    10.1


VOACAP Prediction via Long-Path. Apr 2018: SSN 7. Power = 0.080kW, CW
TX (10.50N, 20.80W) to RX (50.00N, 100.00W): 31681 km, 19686 mi, 140 deg

  |01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24 |
10|                                                                        |10
12|       f                                                                |12
15|       f                                                                |15
17| f  f  f  f                                      f           f  f  f  f |17
20| f  f  f  f     f  f                          f  f  f  f  f  f  f  f    |20
30|             f  f  f  f                                                 |30
40|                                                                        |40
60|                                                                        |60
80|                                                                        |80
  |01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24 |

A = 90 - 100%   d = 25 - 49%  * = REL 0%, but Signal Power over Noise
B = 75 -  89%   e = 10 - 24%
C = 50 -  74%   f =  1 -  9%

The best operating frequencies (FREQ, FREQ2, FREQ3) by hour

UTC    SDBW       REL     SNR   MUFday     FOT     MUF     HPF    FREQ   FREQ2   FREQ3

01  -187 (-- )     2%     -22      79%    12.9    16.0    18.5    14.1-   10.1    18.1
02  -186 (-- )     1%     -19      84%    13.4    16.5    19.2    14.1-   18.1    10.1
03  -181 (-- )     5%     -13      68%    10.6    16.0    22.5    14.1-   18.1    21.1
04  -189 (-- )     3%     -19      36%     8.4    12.7    17.7    14.1-   10.1    18.1
05  -192 (-- )     1%     -31      42%     6.3     9.5    13.3    10.1-   14.1     7.1
06  -183 (-- )     2%     -21      56%     6.9    10.5    14.7    10.1-   14.1     7.1
07  -183 (-- )     2%     -21      74%     8.7    11.6    14.6    10.1-   14.1    18.1
08  -187 (-- )     2%     -24      67%     8.3    11.0    13.9    10.1-   14.1     7.1
09  -203 (-- )     0%     -39      56%     7.8    10.4    13.1    10.1-   14.1     7.1
10  -230 (-- )     0%     -66      40%     7.2     9.6    12.1    10.1-   14.1     7.1
11  -266 (-- )     0%    -103      21%     7.2     9.0    10.7    10.1-   14.1    24.9
12  -290 (-- )     0%    -126      22%     7.3     9.1    10.8    10.1-   14.1    24.9
13  -285 (-- )     0%    -121      46%     8.0    10.0    11.8    10.1-   14.1    24.9
14  -242 (-- )     0%     -71       8%     9.4    11.7    13.9    14.1-   10.1    18.1
15  -212 (-- )     0%     -41      42%    11.1    13.7    16.4    14.1-   18.1    10.1
16  -191 (-- )     2%     -21      56%    12.3    14.4    17.3    14.1-   18.1    21.1
17  -195 (-- )     1%     -25      74%    13.0    15.6    18.7    14.1-   18.1    21.1
18  -190 (-- )     2%     -20      81%    13.5    15.5    17.9    14.1-   18.1    10.1
19  -190 (-- )     2%     -22      88%    13.9    16.0    18.0    14.1-   18.1    10.1
20  -192 (-- )     1%     -24      92%    14.4    16.5    18.6    14.1-   18.1    10.1
21  -193 (-- )     1%     -26      76%    14.1    16.2    19.1    14.1-   18.1    21.1
22  -188 (-- )     1%     -21      77%    13.1    16.3    19.3    14.1-   18.1    21.1
23  -183 (-- )     1%     -17      84%    13.4    16.5    19.1    14.1-   18.1    21.1
24  -189 (-- )     4%     -17      21%    13.3    16.5    19.1    18.1-   14.1    21.1

The result directory: /root/voatui/predictions/20163119
```
