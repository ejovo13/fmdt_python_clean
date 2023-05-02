# Use the Video Class

This section will showcase the operations that we can perform with a video.

Let's start off by loading in our demo video.

```Python
import fmdt
v = fmdt.load_demo()

>>> v
2022_05_31_tauh_34_meteors.mp4
```

Provided that a video has meteors in our database:

```Python
>>> v.has_meteors()
True

>>> v.meteors()
[<fmdt.truth.HumanDetection object at 0x7f17d601d4e0>, <fmdt.truth.HumanDetection object at 0x7f170ecde380>, <fmdt.truth.HumanDetection object at 0x7f170ecde4d0>, <fmdt.truth.HumanDetection object at 0x7f170ecde320>, <fmdt.truth.HumanDetection object at 0x7f170ecde410>, <fmdt.truth.HumanDetection object at 0x7f170ecde260>, <fmdt.truth.HumanDetection object at 0x7f170ecde2c0>, <fmdt.truth.HumanDetection object at 0x7f170ecde350>, <fmdt.truth.HumanDetection object at 0x7f170ecde3b0>, <fmdt.truth.HumanDetection object at 0x7f170ecde200>, <fmdt.truth.HumanDetection object at 0x7f170ecde2f0>, <fmdt.truth.HumanDetection object at 0x7f170ecde140>, <fmdt.truth.HumanDetection object at 0x7f170ecde1a0>, <fmdt.truth.HumanDetection object at 0x7f170ecde230>, <fmdt.truth.HumanDetection object at 0x7f170ecde290>, <fmdt.truth.HumanDetection object at 0x7f170ecde0e0>, <fmdt.truth.HumanDetection object at 0x7f170ecde1d0>, <fmdt.truth.HumanDetection object at 0x7f170ecde020>, <fmdt.truth.HumanDetection object at 0x7f170ecde080>, <fmdt.truth.HumanDetection object at 0x7f170ecde110>, <fmdt.truth.HumanDetection object at 0x7f170ecddea0>, <fmdt.truth.HumanDetection object at 0x7f170ecddf90>, <fmdt.truth.HumanDetection object at 0x7f170ecddd20>, <fmdt.truth.HumanDetection object at 0x7f170ecdddb0>, <fmdt.truth.HumanDetection object at 0x7f170ecddf00>, <fmdt.truth.HumanDetection object at 0x7f170ecddd50>, <fmdt.truth.HumanDetection object at 0x7f170ecddff0>, <fmdt.truth.HumanDetection object at 0x7f170ecdde10>, <fmdt.truth.HumanDetection object at 0x7f170ecde860>, <fmdt.truth.HumanDetection object at 0x7f170ecde050>, <fmdt.truth.HumanDetection object at 0x7f170ecdde70>, <fmdt.truth.HumanDetection object at 0x7f170ecdef80>, <fmdt.truth.HumanDetection object at 0x7f170ecdead0>, <fmdt.truth.HumanDetection object at 0x7f170ecdf190>]
```

We can call `fmdt-detect` and `fmdt-check` easily:

```Python
>>> v.detect().check()
# [...]
GroundTruth table
-----------------
    id   types  detects  gts  starts  stops  tracks
0    1  meteor        7    7     102    108       1
1    2  meteor       17   16     110    125       1
2    3  meteor        8    9     111    119       1
3    4  meteor        3    3     121    123       1
4    5  meteor        3    3     127    129       1
5    6  meteor        3    3     129    131       1
6    7  meteor        9   10     133    142       1
7    8  meteor       10   10     134    143       1
8    9  meteor        4    4     134    137       1
9   10  meteor        3    4     135    138       1
10  11  meteor        6   10     137    146       1
11  12  meteor        4    4     139    142       1
12  13  meteor       11   11     140    150       1
13  14  meteor        4    4     146    149       1
14  15  meteor        3    3     156    158       1
15  16  meteor       10   10     156    165       1
16  17  meteor        6    6     157    162       1
17  18  meteor        4    4     160    163       1
18  19  meteor        4    4     164    167       1
19  20  meteor        3    3     167    169       1
20  21  meteor        5    5     171    175       1
21  22  meteor        7    7     174    180       1
22  23  meteor        8    8     178    185       1
23  24  meteor       11   11     179    189       1
24  25  meteor        3    3     179    181       1
25  26  meteor        5    5     180    184       1
26  27  meteor        7    7     183    189       1
27  28  meteor        4    4     194    197       1
28  29  meteor        3    4     197    200       1
29  30  meteor        6    5     199    203       2
30  31  meteor        6    6     200    205       1
31  32  meteor        7    7     223    229       1
32  33  meteor        5    5     224    228       1
33  34  meteor        4    4     249    252       1
Tracking stats
--------------
     type  gt  ntrk  tpos  fpos  tneg  fneg  trk_rate
0  meteor  34    39    35     4     0     0      0.95
1    star   0     0     0     0    39     0       NaN
2   noise   0     0     0     0    39     0       NaN
3     all  34    39    35     4    78     0      0.95
```

We could also store the detection results in an intermediate variable to 
retrieve motion estimation statistics:

```Python
>>> res = v.detect(save_df=True)
(II) Frame n° 255 -- Tracks = ['meteor':  38, 'star':   0, 'noise':   0, 'total':  38]

>>> res.df
     nroi  nassoc  mean_err  std_dev
0      45       0    0.0000   0.0000
1      63      17    0.1663   0.1411
2      67      19    0.2939   0.3953
3      82      24    0.2738   0.2614
4      35      18    0.1601   0.2101
..    ...     ...       ...      ...
251    52      18    0.3344   0.3212
252    59      22    0.9310   1.2554
253    65      17    0.1500   0.1209
254    50      17    0.1251   0.1058
255    66      19    0.3721   0.2947

[256 rows x 4 columns]
```

then call `check` from our `DetectionResult`:

```Python
>>> res.check()
GroundTruth table
-----------------
    id   types  detects  gts  starts  stops  tracks
0    1  meteor        7    7     102    108       1
1    2  meteor       17   16     110    125       1
2    3  meteor        8    9     111    119       1
3    4  meteor        3    3     121    123       1
4    5  meteor        3    3     127    129       1
5    6  meteor        3    3     129    131       1
6    7  meteor        9   10     133    142       1
7    8  meteor       10   10     134    143       1
8    9  meteor        4    4     134    137       1
9   10  meteor        3    4     135    138       1
10  11  meteor        6   10     137    146       1
11  12  meteor        4    4     139    142       1
12  13  meteor       11   11     140    150       1
13  14  meteor        4    4     146    149       1
14  15  meteor        3    3     156    158       1
15  16  meteor       10   10     156    165       1
16  17  meteor        6    6     157    162       1
17  18  meteor        4    4     160    163       1
18  19  meteor        4    4     164    167       1
19  20  meteor        3    3     167    169       1
20  21  meteor        5    5     171    175       1
21  22  meteor        7    7     174    180       1
22  23  meteor        8    8     178    185       1
23  24  meteor       11   11     179    189       1
24  25  meteor        3    3     179    181       1
25  26  meteor        5    5     180    184       1
26  27  meteor        7    7     183    189       1
27  28  meteor        4    4     194    197       1
28  29  meteor        3    4     197    200       1
29  30  meteor        6    5     199    203       2
30  31  meteor        6    6     200    205       1
31  32  meteor        7    7     223    229       1
32  33  meteor        5    5     224    228       1
33  34  meteor        4    4     249    252       1
Tracking stats
--------------
     type  gt  ntrk  tpos  fpos  tneg  fneg  trk_rate
0  meteor  34    39    35     4     0     0      0.95
1    star   0     0     0     0    39     0       NaN
2   noise   0     0     0     0    39     0       NaN
3     all  34    39    35     4    78     0      0.95
```

Soon we will have the tracking statistics stored in a python object 
`CheckResult`.
