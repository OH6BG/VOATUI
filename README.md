# VOATUI
Text-based User Interface for voacapl (Python), version 3

This is a completely refactored version of voatui.py.

This Python script requires voacapl 0.7.4 or later from Jim Watson: https://github.com/jawatson/voacapl

## Quick Guide

1. In the Python script, set the parameters "itshfbcDir" and "voacaplBin" as per your system.
2. You can set the Python script executable: chmod u+x voatui.py
3. Set your default TX coordinates in the script.
4. Run the script: ./voatui.py
5. For each run, the script tries to connect to the Internet and save the sunspot numbers in the prediction directory.

### A sample run:

```
................................................................................
VOACAP Point-to-Point Predictions, Version 3
by Jari Perkiömäki OH6BG (www.voacap.com)
................................................................................
Fetching the SSN data from the Internet...

PREDEFINED VALUES:
TX Antenna: Isotropic, 0 dBi gain
RX Antenna: Isotropic, 0 dBi gain
Min. TOA  : 3 degrees
SSN dates : 06/2020..11/2021

Enter year (2020..2021) [2020]:
Enter month number (1..12): 6

TRANSMITTER (TX)
................
Enter latitude (-90..90) [63.146]:
Enter longitude (-180..180) [21.542]:

RECEIVER (RX)
................
Enter latitude (-90..90): 1
Enter longitude (-180..180): 1

Enter power in Watts (1..5000) [1500]:
Enter mode (1 = CW; 2 = SSB; 3 = AM; 4 = FT8; 5 = WSPR) [1]:

VOACAP Prediction via Short-Path. Jun 2020: SSN 4. Power=1.200kW, CW
TX (63.15N, 21.54E) to RX (1.00N, 1.00E): 7115 km, 4421 mi, 203 deg

  |01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24 |
10|                                                                        |10
12|                                                 f     f  f             |12
15|                   f  f  f  f  f                 d  e  C  C  f          |15
17|                f  d  C  C  C  d  d  e  e  e  e  B  C  B  B  d  f  f    |17
20| f  e        e  C  C  C  d  C  d  d  d  C  C  C  A  A  A  A  B  B  C  f |20
30| C  C  d  e  d  C  f                          f  C  A  A  A  A  B  B  B |30
40| A  B  C  C  d  *                                *  C  A  A  A  A  A  A |40
60| A  B  C  C  f                                      f  d  A  A  A  A  A |60
80| B  C  d  f                                            f  e  B  B  B  B |80
  |01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24 |

A = 90 - 100%   d = 25 - 49%  * = REL 0%, but Signal Power over Noise
B = 75 -  89%   e = 10 - 24%
C = 50 -  74%   f =  1 -  9%

The best operating frequencies (FREQ1, FREQ2, FREQ3) by hour

UTC    SDBW      ΔSIG    REL   SNR   ΔSNR  MUFday     FOT     MUF     HPF   FREQ1   FREQ2   FREQ3

01  -117 (S7 )   21.7    92%    38   24.6     96%     8.0    10.3    12.4     7.1     5.4     3.6
02  -119 (S7 )   25.7    86%    36   28.2     92%     7.3     9.4    12.6     7.1     5.4     3.6
03  -124 (S6 )   21.8    74%    28   26.9     98%     6.3     8.1    10.8     5.4     7.1     3.6
04  -133 (S4 )   22.6    52%    20   27.7     97%     6.1     7.8    10.4     5.4     7.1     3.6
05  -138 (S4 )   21.1    49%    19   26.3     96%     7.9    10.1    13.6     7.1    10.1     5.4
06  -136 (S4 )   20.1    73%    27   25.2     96%    11.3    14.6    16.7    10.1    14.1     7.1-
07  -146 (S2 )   32.7    60%    24   35.6     86%    13.7    16.7    19.2    14.1    10.1    18.1+
08  -151 (S1 )   43.0    57%    23   45.8     34%    14.1    17.2    19.8    18.1    14.1    10.1-
09  -151 (S1 )   40.8    57%    23   42.7     35%    14.2    17.3    19.9    18.1    14.1    10.1-
10  -151 (S1 )   26.7    51%    20   30.9     89%    14.0    16.9    19.6    14.1    18.1    10.1-
11  -153 (S1 )   30.4    42%    17   33.5     86%    13.6    16.4    19.0    14.1    18.1    10.1-
12  -153 (S1 )   34.9    40%    17   38.1     79%    13.3    15.8    18.4    14.1    18.1*   10.1-
13  -152 (S1 )   36.0    44%    17   38.1     73%    13.1    15.3    17.8    14.1    18.1*   10.1-
14  -149 (S2 )   37.4    52%    20   39.4     71%    12.8    15.1    17.2    14.1    18.1-   10.1-
15  -143 (S3 )   36.3    63%    26   39.3     71%    12.8    15.1    17.2    14.1    10.1-   18.1-
16  -137 (S4 )   31.4    74%    31   33.6     78%    13.2    15.5    17.7    14.1    10.1    18.1
17  -121 (S6 )   16.1    99%    45   20.2     99%    16.3    19.2    21.8    14.1    18.1    10.1
18  -125 (S6 )   19.3    97%    40   22.2     94%    14.8    17.6    20.2    14.1    10.1     7.1
19  -121 (S6 )   16.7    99%    45   20.5     98%    15.9    18.9    21.7    14.1    10.1     7.1
20  -118 (S7 )   13.9   100%    42   18.8    100%    16.0    19.1    21.9    10.1     7.1    14.1
21  -117 (S7 )   17.0    97%    39   21.5     99%    10.5    14.4    17.7     7.1    10.1     5.4
22  -116 (S7 )   15.9    96%    35   19.0    100%    10.7    13.8    16.6     5.4     7.1     3.6
23  -116 (S7 )   16.2    95%    35   19.2    100%    10.0    12.9    15.5     5.4     7.1     3.6
24  -116 (S7 )   20.1    95%    39   23.3     97%     8.3    10.8    12.9     7.1     5.4     3.6


VOACAP Prediction via Long-Path. Jun 2020: SSN 4. Power=1.200kW, CW
TX (63.15N, 21.54E) to RX (1.00N, 1.00E): 32910 km, 20449 mi, 23 deg

  |01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24 |
10|                                                                        |10
12|                                                                        |12
15|                                        f  f  f  f  f                   |15
17|                      e  f  f  f     f  f  f  e  e  e  f                |17
20|                   e  f  f  f           f  f  f  e  e  e  f             |20
30| f                                                        f  f  f  f  f |30
40|                                                                        |40
60|                                                                        |60
80|                                                                        |80
  |01|02|03|04|05|06|07|08|09|10|11|12|13|14|15|16|17|18|19|20|21|22|23|24 |

A = 90 - 100%   d = 25 - 49%  * = REL 0%, but Signal Power over Noise
B = 75 -  89%   e = 10 - 24%
C = 50 -  74%   f =  1 -  9%

The best operating frequencies (FREQ1, FREQ2, FREQ3) by hour

UTC    SDBW      ΔSIG    REL   SNR   ΔSNR  MUFday     FOT     MUF     HPF   FREQ1   FREQ2   FREQ3

01  -181 (-- )   50.0*    3%   -18   51.3*    28%     6.9     8.8    11.8    10.1-   14.1-    7.1-
02  -206 (-- )   50.0*    0%   -43   51.3*    37%     6.2     9.2    12.6    10.1-   14.1-   18.1-
03  -205 (-- )   50.0*    0%   -42   51.4*    28%     5.8     8.7    11.9    10.1-   14.1-    7.1-
04  -223 (-- )   50.0*    0%   -60   51.5*     9%     4.9     7.3    10.0    10.1-    7.1-   14.1-
05  -234 (-- )   50.0*    0%   -72   51.6*     5%     4.6     6.9     9.4    10.1-    7.1-   14.1-
06  -215 (-- )   50.0*    0%   -52   52.7*    28%     8.1     9.3    11.1    10.1-   14.1-    7.1-
07  -172 (-- )   50.0*   15%    -2   52.5*    48%    12.2    14.0    16.6    14.1-   18.1-   10.1-
08  -179 (-- )   41.0     2%    -9   43.7     88%    13.9    16.0    18.8    14.1-   18.1-   21.1-
09  -189 (-- )   50.0*    5%   -15   51.6*    18%    14.0    16.1    18.8    18.1-   14.1-   21.1-
10  -199 (-- )   48.5*    1%   -29   50.0*    89%    14.0    16.1    18.8    14.1-   18.1-   21.1-
11  -206 (-- )   50.0*    1%   -32   52.6*    20%    13.6    15.9    19.3    18.1-   14.1-   21.1-
12  -209 (-- )   50.0*    0%   -35   52.6*    20%    13.5    15.9    19.3    18.1-   14.1-   21.1-
13  -206 (-- )   50.0*    1%   -32   52.6*    22%    13.7    16.1    19.5    18.1-   14.1-   21.1-
14  -199 (-- )   50.0*    1%   -25   52.6*    23%    13.7    16.2    19.6    18.1-   14.1-   21.1-
15  -184 (-- )   50.0*    4%   -15   52.4*    76%    12.4    16.3    19.8    14.1-   18.1-   21.1-
16  -180 (-- )   50.0*   10%    -7   52.5*    27%    12.4    16.4    20.0    18.1-   14.1-   21.1-
17  -172 (-- )   50.0*   18%     1   52.4*    24%    12.3    16.1    19.7    18.1*   14.1-   21.1-
18  -164 (S0 )   50.0*   18%     1   51.5*    71%    12.0    15.7    19.2    14.1*   18.1*   10.1-
19  -166 (-- )   50.0*   17%     0   51.4*    36%    10.2    13.0    17.1    14.1*   10.1-   18.1-
20  -174 (-- )   50.0*    5%   -14   51.5*    45%     7.7     9.8    12.9    10.1-   14.1-    7.1-
21  -188 (-- )   50.0*    1%   -27   51.4*    20%     6.6     8.4    11.0    10.1-    7.1-   14.1-
22  -189 (-- )   50.0*    1%   -28   51.3*    21%     6.5     8.3    11.1    10.1-   14.1-    7.1-
23  -188 (-- )   50.0*    1%   -26   51.3*    24%     6.6     8.5    11.4    10.1-   14.1-    7.1-
24  -187 (-- )   50.0*    1%   -24   51.3*    25%     6.7     8.5    11.4    10.1-   14.1-    7.1-

Prediction directory: /root/voatui/predictions/63580740
```
