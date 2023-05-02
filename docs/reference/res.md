# `fmdt.res`

This module contains the two very important classes `DetectionResult` and 
`CheckResult` which store information that is generated during the execution of 
`fmdt-detect` and `fmdt-check`.

- [`DetectionResult`](#detectionresult)
- [`CheckResult`](#checkresult)

## `DetectionResult`

``` mermaid
classDiagram
  class DetectionResult
  DetectionResult : +int nframes 
  DetectionResult : +Args args
  DetectionResult : +DataFrame df
  DetectionResult : +Video video 
  DetectionResult : +list[TrackedObject] trk_list
  DetectionResult : +detect() 
  DetectionResult : +visu() 
  DetectionResult : +check(String gt_path, String trk_path)
  DetectionResult : +trk_list_summary() 
  DetectionResult : +int n_meteors_detected() 
  DetectionResult : +int n_starts_detected() 
  DetectionResult : +int n_noise_detected() 
```

Any interface to `fmdt.detect` will return a `DetectionResult` object. However, 
the contents of a `DetectionResult` are dependent on the _way_ in which we call 
`fmdt-detect`. 

## Usage

Let's start off loading in our beloved tau demo.

```Python
import fmdt
v = fmdt.load_demo()
```

If the executable `fmdt-detect` is called with a `--log-path` then we save 
movement estimation statistics on disk. By default, we don't store log data. To 
enable log data which will be stored in under the field `DetectionResult.df` we 
pass `save_df=True` to our detection interface.

=== "`res = v.detect()`"

    ??? info "`nframes`"
        
        ```Python
        >>> res.nframes
        256
        ```

    ??? info "`args`"

        ```Python
        >>> res.args
        <fmdt.args.Args object>
        ====================
        Detect parameters: 
        {'vid_in_path': '/run/media/ejovo/Seagate Portable Drive/Meteors/2022_05_31_tauh_34_meteors.mp4', 'trk_path': 'trk.txt'}
        ```

    ???+ info "`df`"

        ```Python
        >>> res.df
        ```

    ???+ info "`trk_list`"

        ```Python
        >>> res.trk_list
        [<Meteor (102, 108)>, <Meteor (110, 126)>, <Meteor (111, 118)>, <Meteor (121, 123)>, <Meteor (127, 129)>, <Meteor (129, 131)>, <Meteor (133, 141)>, <Meteor (134, 143)>, <Meteor (134, 137)>, <Meteor (136, 138)>, <Meteor (139, 144)>, <Meteor (139, 142)>, <Meteor (140, 150)>, <Meteor (146, 149)>, <Meteor (156, 158)>, <Meteor (156, 165)>, <Meteor (157, 162)>, <Meteor (160, 163)>, <Meteor (164, 167)>, <Meteor (167, 169)>, <Meteor (171, 175)>, <Meteor (174, 180)>, <Meteor (178, 185)>, <Meteor (179, 181)>, <Meteor (179, 189)>, <Meteor (180, 184)>, <Meteor (183, 189)>, <Meteor (194, 197)>, <Meteor (197, 199)>, <Meteor (199, 201)>, <Meteor (200, 205)>, <Meteor (201, 203)>, <Meteor (202, 204)>, <Meteor (223, 229)>, <Meteor (224, 228)>, <Meteor (227, 231)>, <Meteor (249, 252)>, <Meteor (251, 253)>]
        ```


    ??? info "`detect()`"

        ```Python
        >>> res.detect()
        (II) Frame n° 255 -- Tracks = ['meteor':  38, 'star':   0, 'noise':   0, 'total':  38]
        <fmdt.res.DetectionResult object at 0x7fb0288f5780>
        ```

    ??? info "`visu()`"

        ```Python
        >>> res.visu()
        #  -------------------
        # |        ----*      |
        # | --* FMDT-VISU --* |
        # |  -------*         |
        #  -------------------
        #
        # Parameters:
        # -----------
        #  * vid-in-path     = /run/media/ejovo/Seagate Portable Drive/Meteors/2022_05_31_tauh_34_meteors.mp4
        #  * vid-in-start    = 0
        #  * vid-in-stop     = 0
        #  * vid-in-threads  = 0
        #  * trk-path        = trk.txt
        #  * trk-bb-path     = bb.txt
        #  * trk-id          = 0
        #  * trk-nat-num     = 0
        #  * trk-only-meteor = 0
        #  * gt-path         = (null)
        #  * vid-out-path    = /run/media/ejovo/Seagate Portable Drive/Meteors/2022_05_31_tauh_34_meteors_visu.mp4
        #
        # Tracks read from file = ['meteor':  38, 'star':   0, 'noise':   0, 'total':  38]
        # The program is running...
        # End of the program, exiting.
        <fmdt.args.Args object at 0x7fb0288f57b0>
        ```


    ??? info "`check()`"

        ```Python
        >>> res.check()
        <fmdt.res.CheckResult object at 0x7fb0288f7af0>


        >>> res.check(log=True)
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
             3 |  meteor ||      8 |   9 ||   111 |   119 ||      1  
             4 |  meteor ||      3 |   3 ||   121 |   123 ||      1  
             5 |  meteor ||      3 |   3 ||   127 |   129 ||      1  
             6 |  meteor ||      3 |   3 ||   129 |   131 ||      1  
             7 |  meteor ||      9 |  10 ||   133 |   142 ||      1  
             8 |  meteor ||     10 |  10 ||   134 |   143 ||      1  
             9 |  meteor ||      4 |   4 ||   134 |   137 ||      1  
            10 |  meteor ||      3 |   4 ||   135 |   138 ||      1  
            11 |  meteor ||      6 |  10 ||   137 |   146 ||      1  
            12 |  meteor ||      4 |   4 ||   139 |   142 ||      1  
            13 |  meteor ||     11 |  11 ||   140 |   150 ||      1  
            14 |  meteor ||      4 |   4 ||   146 |   149 ||      1  
            15 |  meteor ||      3 |   3 ||   156 |   158 ||      1  
            16 |  meteor ||     10 |  10 ||   156 |   165 ||      1  
            17 |  meteor ||      6 |   6 ||   157 |   162 ||      1  
            18 |  meteor ||      4 |   4 ||   160 |   163 ||      1  
            19 |  meteor ||      4 |   4 ||   164 |   167 ||      1  
            20 |  meteor ||      3 |   3 ||   167 |   169 ||      1  
            21 |  meteor ||      5 |   5 ||   171 |   175 ||      1  
            22 |  meteor ||      7 |   7 ||   174 |   180 ||      1  
            23 |  meteor ||      8 |   8 ||   178 |   185 ||      1  
            24 |  meteor ||     11 |  11 ||   179 |   189 ||      1  
            25 |  meteor ||      3 |   3 ||   179 |   181 ||      1  
            26 |  meteor ||      5 |   5 ||   180 |   184 ||      1  
            27 |  meteor ||      7 |   7 ||   183 |   189 ||      1  
            28 |  meteor ||      4 |   4 ||   194 |   197 ||      1  
            29 |  meteor ||      3 |   4 ||   197 |   200 ||      1  
            30 |  meteor ||      6 |   5 ||   199 |   203 ||      2  
            31 |  meteor ||      6 |   6 ||   200 |   205 ||      1  
            32 |  meteor ||      7 |   7 ||   223 |   229 ||      1  
            33 |  meteor ||      5 |   5 ||   224 |   228 ||      1  
            34 |  meteor ||      4 |   4 ||   249 |   252 ||      1  
        Statistics: 
        - Number of GT objs = ['meteor':   34, 'star':    0, 'noise':    0, 'all':   34]
        - Number of tracks  = ['meteor':   38, 'star':    0, 'noise':    0, 'all':   38]
        - True positives    = ['meteor':   35, 'star':    0, 'noise':    0, 'all':   35]
        - False positives   = ['meteor':    3, 'star':    0, 'noise':    0, 'all':    3]
        - True negative     = ['meteor':    0, 'star':   38, 'noise':   38, 'all':   76]
        - False negative    = ['meteor':    0, 'star':    0, 'noise':    0, 'all':    0]
        - tracking rate     = ['meteor': 0.95, 'star': -nan, 'noise': -nan, 'all': 0.95]
        # End of the program, exiting.

        <fmdt.res.CheckResult object at 0x7fb028924100>
        ```



    ??? info "`trk_list_summary()`"

        ```Python
        >>> res.trk_list_summary()
        'objects in trk_list: 38 meteor(s), 0 star(s), 0 noise'
        ```

=== "`res = v.detect(save_df=True)`"

    ??? info "`nframes`"
        
        ```Python
        >>> res.nframes
        256
        ```

    ??? info "`args`"

        ```Python
        >>> res.args
        <fmdt.args.Args object>
        ====================
        Detect parameters: 
        {'vid_in_path': '/run/media/ejovo/Seagate Portable Drive/Meteors/2022_05_31_tauh_34_meteors.mp4', 'trk_path': 'trk.txt'}
        ```

    ???+ info "`df`"

        ```Python
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
    ???+ info "`trk_list`"
        ```
        >>> res.trk_list
        [<Meteor (102, 108)>, <Meteor (110, 126)>, <Meteor (111, 118)>, <Meteor (121, 123)>, <Meteor (127, 129)>, <Meteor (129, 131)>, <Meteor (133, 141)>, <Meteor (134, 143)>, <Meteor (134, 137)>, <Meteor (136, 138)>, <Meteor (139, 144)>, <Meteor (139, 142)>, <Meteor (140, 150)>, <Meteor (146, 149)>, <Meteor (156, 158)>, <Meteor (156, 165)>, <Meteor (157, 162)>, <Meteor (160, 163)>, <Meteor (164, 167)>, <Meteor (167, 169)>, <Meteor (171, 175)>, <Meteor (174, 180)>, <Meteor (178, 185)>, <Meteor (179, 181)>, <Meteor (179, 189)>, <Meteor (180, 184)>, <Meteor (183, 189)>, <Meteor (194, 197)>, <Meteor (197, 199)>, <Meteor (199, 201)>, <Meteor (200, 205)>, <Meteor (201, 203)>, <Meteor (202, 204)>, <Meteor (223, 229)>, <Meteor (224, 228)>, <Meteor (227, 231)>, <Meteor (249, 252)>, <Meteor (251, 253)>]
        ```


    ??? info "`detect()`"

        ```Python
        >>> res.detect()
        (II) Frame n° 255 -- Tracks = ['meteor':  38, 'star':   0, 'noise':   0, 'total':  38]
        <fmdt.res.DetectionResult object at 0x7fb0288f5780>
        ```

    ??? info "`visu()`"

        ```Python
        >>> res.visu()
        #  -------------------
        # |        ----*      |
        # | --* FMDT-VISU --* |
        # |  -------*         |
        #  -------------------
        #
        # Parameters:
        # -----------
        #  * vid-in-path     = /run/media/ejovo/Seagate Portable Drive/Meteors/2022_05_31_tauh_34_meteors.mp4
        #  * vid-in-start    = 0
        #  * vid-in-stop     = 0
        #  * vid-in-threads  = 0
        #  * trk-path        = trk.txt
        #  * trk-bb-path     = bb.txt
        #  * trk-id          = 0
        #  * trk-nat-num     = 0
        #  * trk-only-meteor = 0
        #  * gt-path         = (null)
        #  * vid-out-path    = /run/media/ejovo/Seagate Portable Drive/Meteors/2022_05_31_tauh_34_meteors_visu.mp4
        #
        # Tracks read from file = ['meteor':  38, 'star':   0, 'noise':   0, 'total':  38]
        # The program is running...
        # End of the program, exiting.
        <fmdt.args.Args object at 0x7fb0288f57b0>
        ```


    ??? info "`check()`"

        ```Python
        >>> res.check()
        <fmdt.res.CheckResult object at 0x7fb0288f7af0>


        >>> res.check(log=True)
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
             3 |  meteor ||      8 |   9 ||   111 |   119 ||      1  
             4 |  meteor ||      3 |   3 ||   121 |   123 ||      1  
             5 |  meteor ||      3 |   3 ||   127 |   129 ||      1  
             6 |  meteor ||      3 |   3 ||   129 |   131 ||      1  
             7 |  meteor ||      9 |  10 ||   133 |   142 ||      1  
             8 |  meteor ||     10 |  10 ||   134 |   143 ||      1  
             9 |  meteor ||      4 |   4 ||   134 |   137 ||      1  
            10 |  meteor ||      3 |   4 ||   135 |   138 ||      1  
            11 |  meteor ||      6 |  10 ||   137 |   146 ||      1  
            12 |  meteor ||      4 |   4 ||   139 |   142 ||      1  
            13 |  meteor ||     11 |  11 ||   140 |   150 ||      1  
            14 |  meteor ||      4 |   4 ||   146 |   149 ||      1  
            15 |  meteor ||      3 |   3 ||   156 |   158 ||      1  
            16 |  meteor ||     10 |  10 ||   156 |   165 ||      1  
            17 |  meteor ||      6 |   6 ||   157 |   162 ||      1  
            18 |  meteor ||      4 |   4 ||   160 |   163 ||      1  
            19 |  meteor ||      4 |   4 ||   164 |   167 ||      1  
            20 |  meteor ||      3 |   3 ||   167 |   169 ||      1  
            21 |  meteor ||      5 |   5 ||   171 |   175 ||      1  
            22 |  meteor ||      7 |   7 ||   174 |   180 ||      1  
            23 |  meteor ||      8 |   8 ||   178 |   185 ||      1  
            24 |  meteor ||     11 |  11 ||   179 |   189 ||      1  
            25 |  meteor ||      3 |   3 ||   179 |   181 ||      1  
            26 |  meteor ||      5 |   5 ||   180 |   184 ||      1  
            27 |  meteor ||      7 |   7 ||   183 |   189 ||      1  
            28 |  meteor ||      4 |   4 ||   194 |   197 ||      1  
            29 |  meteor ||      3 |   4 ||   197 |   200 ||      1  
            30 |  meteor ||      6 |   5 ||   199 |   203 ||      2  
            31 |  meteor ||      6 |   6 ||   200 |   205 ||      1  
            32 |  meteor ||      7 |   7 ||   223 |   229 ||      1  
            33 |  meteor ||      5 |   5 ||   224 |   228 ||      1  
            34 |  meteor ||      4 |   4 ||   249 |   252 ||      1  
        Statistics: 
        - Number of GT objs = ['meteor':   34, 'star':    0, 'noise':    0, 'all':   34]
        - Number of tracks  = ['meteor':   38, 'star':    0, 'noise':    0, 'all':   38]
        - True positives    = ['meteor':   35, 'star':    0, 'noise':    0, 'all':   35]
        - False positives   = ['meteor':    3, 'star':    0, 'noise':    0, 'all':    3]
        - True negative     = ['meteor':    0, 'star':   38, 'noise':   38, 'all':   76]
        - False negative    = ['meteor':    0, 'star':    0, 'noise':    0, 'all':    0]
        - tracking rate     = ['meteor': 0.95, 'star': -nan, 'noise': -nan, 'all': 0.95]
        # End of the program, exiting.

        <fmdt.res.CheckResult object at 0x7fb028924100>
        ```



    ??? info "`trk_list_summary()`"

        ```Python
        >>> res.trk_list_summary()
        'objects in trk_list: 38 meteor(s), 0 star(s), 0 noise'
        ```
    
Only the `df` field is altered by this choice.

## `CheckResult`

``` mermaid
classDiagram
  class CheckResult
  CheckResult : +DataFrame gt_table 
  CheckResult : +DataFrame stats
  CheckResult : +Series meteor_stats()
  CheckResult : +Series star_stats()
  CheckResult : +Series noise_stats()
  CheckResult : +Series all_stats()
```
A `CheckResult` stores the information generated by a call to `fmdt-check`. 
Notably, we retrieve the `gt_table` which contains information about the meteors 
in our ground truth file and the `stats` table that summarizes important 
tracking statistics

<!-- === "`fmdt.check`"

    We can create a `CheckResult` object using our simplest interface `fmdt.check` which assumes that 
    we already have a ground truth file and also a track list generated from `fmdt-detect`.

    ```
    res = fmdt.check(trk_path="trk.txt", gt_path="meteors.txt")
    ``` -->

=== "`fmdt.Video.check`"

    Alternatively, we can use a video to call `fmdt-check` (our preferred method)

    ``` Python
    res = fmdt.load_demo().detect().check()
    ```

    ??? note "`gt_table`"

        ```Python
        >>> res.gt_table
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
        ```

    ??? note "`stats`"

        ```Python
        >>> res.stats
            type  gt  ntrk  tpos  fpos  tneg  fneg  trk_rate
        0  meteor  34    38    35     3     0     0      0.95
        1    star   0     0     0     0    38     0       NaN
        2   noise   0     0     0     0    38     0       NaN
        3     all  34    38    35     3    76     0      0.95
        ```

    ??? note "individual functions"

        ```Python
        >>> res.meteor_stats()
        type        meteor
        gt              34
        ntrk            38
        tpos            35
        fpos             3
        tneg             0
        fneg             0
        trk_rate      0.95
        Name: 0, dtype: object


        >>> res.star_stats()
        type        star
        gt             0
        ntrk           0
        tpos           0
        fpos           0
        tneg          38
        fneg           0
        trk_rate     NaN
        Name: 1, dtype: object


        >>> res.noise_stats()
        type        noise
        gt              0
        ntrk            0
        tpos            0
        fpos            0
        tneg           38
        fneg            0
        trk_rate      NaN
        Name: 2, dtype: object

        
        >>> res.all_stats()
        type         all
        gt            34
        ntrk          38
        tpos          35
        fpos           3
        tneg          76
        fneg           0
        trk_rate    0.95
        Name: 3, dtype: object
        ```