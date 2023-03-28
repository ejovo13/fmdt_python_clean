# Use the Video Class

This section will showcase the operations that we can perform with a video

Let's start off by loading in our demo video

```
import fmdt
v = fmdt.load_demo()


>>> v
2022_05_31_tauh_34_meteors.mp4
```

Provided that a video has meteors in our database:

```
>>> v.has_meteors()
True

>>> v.meteors()
[<fmdt.truth.HumanDetection object at 0x7f17d601d4e0>, <fmdt.truth.HumanDetection object at 0x7f170ecde380>, <fmdt.truth.HumanDetection object at 0x7f170ecde4d0>, <fmdt.truth.HumanDetection object at 0x7f170ecde320>, <fmdt.truth.HumanDetection object at 0x7f170ecde410>, <fmdt.truth.HumanDetection object at 0x7f170ecde260>, <fmdt.truth.HumanDetection object at 0x7f170ecde2c0>, <fmdt.truth.HumanDetection object at 0x7f170ecde350>, <fmdt.truth.HumanDetection object at 0x7f170ecde3b0>, <fmdt.truth.HumanDetection object at 0x7f170ecde200>, <fmdt.truth.HumanDetection object at 0x7f170ecde2f0>, <fmdt.truth.HumanDetection object at 0x7f170ecde140>, <fmdt.truth.HumanDetection object at 0x7f170ecde1a0>, <fmdt.truth.HumanDetection object at 0x7f170ecde230>, <fmdt.truth.HumanDetection object at 0x7f170ecde290>, <fmdt.truth.HumanDetection object at 0x7f170ecde0e0>, <fmdt.truth.HumanDetection object at 0x7f170ecde1d0>, <fmdt.truth.HumanDetection object at 0x7f170ecde020>, <fmdt.truth.HumanDetection object at 0x7f170ecde080>, <fmdt.truth.HumanDetection object at 0x7f170ecde110>, <fmdt.truth.HumanDetection object at 0x7f170ecddea0>, <fmdt.truth.HumanDetection object at 0x7f170ecddf90>, <fmdt.truth.HumanDetection object at 0x7f170ecddd20>, <fmdt.truth.HumanDetection object at 0x7f170ecdddb0>, <fmdt.truth.HumanDetection object at 0x7f170ecddf00>, <fmdt.truth.HumanDetection object at 0x7f170ecddd50>, <fmdt.truth.HumanDetection object at 0x7f170ecddff0>, <fmdt.truth.HumanDetection object at 0x7f170ecdde10>, <fmdt.truth.HumanDetection object at 0x7f170ecde860>, <fmdt.truth.HumanDetection object at 0x7f170ecde050>, <fmdt.truth.HumanDetection object at 0x7f170ecdde70>, <fmdt.truth.HumanDetection object at 0x7f170ecdef80>, <fmdt.truth.HumanDetection object at 0x7f170ecdead0>, <fmdt.truth.HumanDetection object at 0x7f170ecdf190>]
```
We can call `fmdt-detect` and `fmdt-check` easily:

```
>>> v.detect().check()
(II) Frame n° 255 -- Tracks = ['meteor':  38, 'star':   0, 'noise':   0, 'total':  38]
#  --------------------
# |         ----*      |
# | --* FMDT-CHECK --* |
# |   -------*         |
#  --------------------
#
# Parameters:
# -----------
#  * trk-path = trk.txt
#  * gt-path  = tmp_meteors.txt
#
# The program is running...
# ---------------||--------------||---------------||--------
#    GT Object   ||     Hits     ||   GT Frames   || Tracks 
# ---------------||--------------||---------------||--------
# -----|---------||--------|-----||-------|-------||--------
#   Id |    Type || Detect |  GT || Start |  Stop ||      # 
# -----|---------||--------|-----||-------|-------||--------
     1 |  meteor ||      7 |   7 ||   102 |   108 ||      1  
     2 |  meteor ||     17 |  16 ||   110 |   125 ||      1  
                                .
                                .
                                .
Statistics: 
  - Number of GT objs = ['meteor':   34, 'star':    0, 'noise':    0, 'all':   34]
  - Number of tracks  = ['meteor':   38, 'star':    0, 'noise':    0, 'all':   38]
  - True positives    = ['meteor':   35, 'star':    0, 'noise':    0, 'all':   35]
  - False positives   = ['meteor':    3, 'star':    0, 'noise':    0, 'all':    3]
  - True negative     = ['meteor':    0, 'star':   38, 'noise':   38, 'all':   76]
  - False negative    = ['meteor':    0, 'star':    0, 'noise':    0, 'all':    0]
  - tracking rate     = ['meteor': 0.95, 'star': -nan, 'noise': -nan, 'all': 0.95]
# End of the program, exiting.
```

We could also store the detection results in an intermediate variable to retrieve motion estimation
statistics:

```
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

then call `check` from our `DetectionResult`

```
>>> res.check()
Statistics: 
  - Number of GT objs = ['meteor':   34, 'star':    0, 'noise':    0, 'all':   34]
  - Number of tracks  = ['meteor':   38, 'star':    0, 'noise':    0, 'all':   38]
  - True positives    = ['meteor':   35, 'star':    0, 'noise':    0, 'all':   35]
  - False positives   = ['meteor':    3, 'star':    0, 'noise':    0, 'all':    3]
  - True negative     = ['meteor':    0, 'star':   38, 'noise':   38, 'all':   76]
  - False negative    = ['meteor':    0, 'star':    0, 'noise':    0, 'all':    0]
  - tracking rate     = ['meteor': 0.95, 'star': -nan, 'noise': -nan, 'all': 0.95]
# End of the program, exiting.
```

Soon we will have the tracking statistics stored in a python object `CheckResult`

