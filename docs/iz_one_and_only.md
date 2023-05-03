# Core Usage

This section presents the core usage of `fmdt-python`. Any examples assume that 
`fmdt` has already been imported:

```python
import fmdt
```

## FMDT executables

We call the main executables `fmdt-*` using `fmdt.*`

=== "fmdt-detect"

    ```python
    fmdt.detect(vid_in_path="2022_05_31_tauh_34_meteors.mp4",
                ccl_hyst_lo=55,
                ccl_hyst_hi=80,
                log_path="log"
                trk_path="trk.txt",
                trk_roi_path="trk2roi.txt") 
    ```

    ??? info "signature"

        ```python
        def detect(
                #=================== fmdt-detect parameters ===================
                vid_in_path: str, 
                vid_in_start: int = None,
                vid_in_stop: int = None,
                vid_in_skip: int = None,
                vid_in_buff: bool = None,
                vid_in_loop: int = None,
                vid_in_threads: int = None,
                ccl_hyst_lo: int = None,
                ccl_hyst_hi: int = None,
                ccl_fra_path: str = None,
                ccl_fra_id: bool = None,
                cca_mag: bool = None,
                cca_ell: bool = None,
                mrp_s_min: int = None,
                mrp_s_max: int = None,
                knn_k: int = None,
                knn_d: int = None,
                knn_s: int = None,
                trk_ext_d: int = None,
                trk_ext_o: int = None,
                trk_angle: float = None,
                trk_star_min: int = None,
                trk_meteor_min: int = None,
                trk_meteor_max: int = None,
                trk_ddev: float = None,
                trk_all: bool = None,
                trk_roi_path: str = None,
                log_path: str = None,
                #================== Additional Parameters =====================
                trk_path: str = "trk.txt",
                log: bool = False,
                timeout: float = None,
                cache: bool = False,
                save_df: bool = False
            ) -> fmdt.res.DetectionResult
        ```

=== "fmdt-log-parser"

    ```python
    fmdt.log_parser(log_path="log",
                    trk_roi_path="trk2roi.txt",
                    trk_bb_path="bb.txt")
    ```

    ??? info "full signature"

        ``` py
        def log_parser(
                log_path: str,
                trk_roi_path: str | None = None,
                log_flt: str | None = None,
                fra_path: str | None = None,
                ftr_name: str | None = None,
                ftr_path: str | None = None,
                trk_path: str | None = None,
                trk_json_path: str | None = None,
                trk_bb_path: str | None = None,
            ) -> fmdt.args.Args:
        ```

=== "fmdt-visu"

    ``` py
    fmdt.visu(vid_in_path="2022_05_31_tauh_34_meteors.mp4",
              trk_path="trk.txt",
              trk_bb_path="bb.txt")
    ```

=== "fmdt-check"

    ``` py 
    fmdt.check(trk_path="trk.txt",
               gt_path="2022_05_31_tauh_34_meteors.txt")
    ```

    ??? info "signature"

        ``` py
        def check(
                trk_path: str,
                gt_path: str,
                stdout: str = None,
                log = False
            ) -> fmdt.res.CheckResult:
        ```

---

Consult [`fmdt.api`](./reference/home.md#fmdtapi) for more information about 
`fmdt`'s interface.

## Configuration

???+ info 

    You only need to configure `fmdt-python` once. If you haven't already done 
    so, follow [these instruction](./howto/0_initialization.md).

We configure `fmdt-python` by indicating where our 
[database videos](./explanation/video_database.md) are stored on disk using 
`fmdt.init()`:
```
fmdt.init(d6_dir: str, d12_dir: str, win_dir: str) -> None
```

??? example 

    For unix user `ejovo` with videos stored on a remote hard drive 
    `Seagate Portable Drive` we configure `fmdt` with:

    ``` py
    fmdt.init(
        d6_dir  = "/run/media/ejovo/Seagate Portable Drive/Meteors/Watec6mm/Meteor",
        d12_dir = "/run/media/ejovo/Seagate Portable Drive/Meteors/Watec12mm/Meteor",
        win_dir = "/run/media/ejovo/Seagate Portable Drive/Meteors"
    )
    ```
    which outputs 

    ```
    Saved config to /home/ejovo/.local/share/fmdt_python/config.json
    ```


Print information about our local database configuration with the function 
`local_info()`:

=== "code"
    ``` py
    fmdt.local_info()
    ```

=== "output"

    ``` py
    Printing information about the local environment
    ================================================================================
    Draconids-6mm*.avi videos configured with dir: /run/media/ejovo/Seagate Portable Drive/Meteors/Watec6mm/Meteor/
    ================================================================================
    52 videos exist on disc out of the 52 videos in our database
    38 of which have ground truths out of 38 ground truths in our database

    ================================================================================
    Draconids-12mm*.avi videos configured with dir: /run/media/ejovo/Seagate Portable Drive/Meteors/Watec12mm/Meteor/
    ================================================================================
    41 videos exist on disc out of the 41 videos in our database
    37 of which have ground truths out of 37 ground truths in our database

    ================================================================================
    window*.mp4 videos configured with dir: /run/media/ejovo/Seagate Portable Drive/Meteors/
    ================================================================================
    8 videos exist on disc out of the 8 videos in our database
    0 of which have ground truths out of 0 ground truths in our database
    ```

## Loading Video Objects

After configuration we can load in `Video` objects using `fmdt.load_*`

=== "demo"

    ``` py
    fmdt.load_demo()
    ```

    ``` py
    >>> fmdt.load_demo()
    2022_05_31_tauh_34_meteors.mp4
    ```


=== "draco6"

    ``` py
    fmdt.load_draco6()
    ```

    ``` py
    >>> fmdt.load_draco6()
    [Draconids-6mm1.00-2750-163200.avi, Draconids-6mm1.05-0750-164200.avi, Draconids-6mm1.14-1400-170300.avi, Draconids-6mm1.20-2350-171600.avi, Draconids-6mm1.29-2550-173600.avi, Draconids-6mm1.30-2050-173800.avi, Draconids-6mm1.32-3150-174200.avi, Draconids-6mm1.34-3050-174700.avi, Draconids-6mm2.00.01-1000-201100.avi, Draconids-6mm2.00.01-1500-201200.avi, Draconids-6mm2.00.01-2150-201200.avi, Draconids-6mm2.00.02-0700-201300.avi, Draconids-6mm2.00.03-0450-201500.avi, Draconids-6mm2.00.03-0550-201500.avi, Draconids-6mm2.00.03-0950-201500.avi, Draconids-6mm2.00.04-1500-201800.avi, Draconids-6mm2.00.04-1900-201900.avi, Draconids-6mm2.00.04-2950-201900.avi, Draconids-6mm2.00.05-0120-202000.avi, Draconids-6mm2.00.05-0200-202000.avi, Draconids-6mm2.00.05-0350-202000.avi, Draconids-6mm2.00.07-0900-202400.avi, Draconids-6mm2.00.07-2400-202500.avi, Draconids-6mm2.00.07-3000-202530.avi, Draconids-6mm2.00.09-0600-202900.avi, Draconids-6mm2.00.09-1650-203000.avi, Draconids-6mm2.00.09-3000-203030.avi, Draconids-6mm2.00.10-0300-203100.avi, Draconids-6mm2.00.10-0350-203110.avi, Draconids-6mm2.00.10-1050-203200.avi, Draconids-6mm2.00.11-2100-203400.avi, Draconids-6mm2.00.11-680-203300.avi, Draconids-6mm2.00.11-780-203310.avi, Draconids-6mm2.00.12-1550-203600.avi, Draconids-6mm2.00.12-2550-203700.avi, Draconids-6mm2.00.12-3100-203730.avi, Draconids-6mm2.00.13-0680-203800.avi, Draconids-6mm2.00.13-3100-204000.avi, Draconids-6mm2.00.15-0750-204200.avi, Draconids-6mm2.00.15-2300-204300.avi, Draconids-6mm2.00.15-2850-204330.avi, Draconids-6mm2.00.170050-204700.avi, Draconids-6mm2.00.18-0000-204900.avi, Draconids-6mm2.00.18-2850-205000.avi, Draconids-6mm2.00.19-0680-205100.avi, Draconids-6mm2.00.19-1550-205200.avi, Draconids-6mm2.00.20-2600-205500.avi, Draconids-6mm2.00.20-2900-205510.avi, Draconids-6mm2.00.22-3150-205900.avi, Draconids-6mm2.00.25-2250-210600.avi, Draconids-6mm2.00.26-450-210700.avi, Draconids-6mm2.00.28-1950-211200.avi]
    ```

=== "draco12"

    ``` py
    fmdt.load_draco12()
    ```

    ``` py
    >>> fmdt.load_draco12()
    [Draconids-12mm1.01-1950-163100.avi, Draconids-12mm1.02-1500-163500.avi, Draconids-12mm1.09-800-164900.avi, Draconids-12mm1.11-150-165300.avi, Draconids-12mm1.13-1350-165800.avi, Draconids-12mm1.15-650-170200.avi, Draconids-12mm1.16-250-170400.avi, Draconids-12mm1.19-2400-171200.avi, Draconids-12mm1.20-650-171300.avi, Draconids-12mm1.26-3100-172700.avi, Draconids-12mm1.27-2800-173000.avi, Draconids-12mm1.28-350-173100.avi, Draconids-12mm1.30-1700-173600.avi, Draconids-12mm1.33-2350-174300.avi, Draconids-12mm2.00.01-3000-201200.avi, Draconids-12mm2.00.01-3100-201200.avi, Draconids-12mm2.00.02-1550-201300.avi, Draconids-12mm2.00.02-2950-201400.avi, Draconids-12mm2.00.03-2000-201600.avi, Draconids-12mm2.00.03-550-201500.avi, Draconids-12mm2.00.04-1550-201900.avi, Draconids-12mm2.00.04-2550-201900.avi, Draconids-12mm2.00.04-750-201800.avi, Draconids-12mm2.00.05-150-202000.avi, Draconids-12mm2.00.05-1600-202100.avi, Draconids-12mm2.00.05-2900-202100.avi, Draconids-12mm2.00.05-2950-202100.avi, Draconids-12mm2.00.06-1400-202200.avi, Draconids-12mm2.00.08-3250-202700.avi, Draconids-12mm2.00.09-1250-202900.avi, Draconids-12mm2.00.09-1450-202900.avi, Draconids-12mm2.00.11-650-203300.avi, Draconids-12mm2.00.14-800-204000.avi, Draconids-12mm2.00.15-1850-204300.avi, Draconids-12mm2.00.15-2950-204300.avi, Draconids-12mm2.00.15-3050-204300.avi, Draconids-12mm2.00.21-1250-205500.avi, Draconids-12mm2.00.22-2250-205900.avi, Draconids-12mm2.00.27-1750-210900.avi, Draconids-12mm2.00.28-1800-211100.avi, Draconids-12mm2.00.28-2400-211200.avi]
    ```

=== "window"

    ``` py
    fmdt.load_window()
    ```

    ``` py
    >>> fmdt.load_window()
    [window_3_sony_0400-0405UTC.mp4, window_3_sony_0405-0410UTC.mp4, window_3_sony_0410-0415UTC.mp4, window_3_sony_0415-0420UTC.mp4, window_3_sony_0420-0425UTC.mp4, window_3_sony_0425-0430UTC.mp4, window_3_sony_0500-0505UTC.mp4, 2022_05_31_tauh_34_meteors.mp4]
    ```


## Video interface

The `Video` class allows use to call our FMDT executables using a very succinct 
syntax. Let's get familiar with how we use this class by loading in our demo 
video `2022_05_31_tauh_34_meteors.mp4` using `fmdt.load_demo()`

=== "code"

    ``` py
    v = fmdt.load_demo() 
    ```

=== "example"

    ``` py
    >>> v
    2022_05_31_tauh_34_meteors.mp4

    >>> type(v)
    <class 'fmdt.db.Video'>
    ```


??? warning

    This operation instantiates a `Video` object associated with 
    2022_05_31_tauh_34_meteors.mp4 from our `video.db` file. The presence of `v` 
    does not imply that 2022_05_31_tauh_32_meteors.mp4 exists on disk nor that 
    it will be found by fmdt in the case that it does. For more information, 
    consult our page on [configuring fmdt](./howto/0_initialization.md).

<!-- 
1. `fmdt.load_demo()` loads in the `Video` object associated with 
2022_05_31_tauh_34_meteors.mp4. The existence of this object does not imply that 
the actual video file exists on disk -->

We can get the full path of a `Video` with the `full_path()` function and check 
if the file that we are pointing to exists on disk with `exists()`:


``` py
>>> v.full_path()
'/run/media/ejovo/Seagate Portable Drive/Meteors/2022_05_31_tauh_34_meteors.mp4'

>>> v.exists()
True
```

### Meteors


We can check if `v` has any meteors in our ground truth database using 
`has_meteors()`

``` py
>>> v.has_meteors()
True
```

and use `meteors()` to retrieve them when the previous result is `True`.

``` py 
>>> v.meteors()
[<fmdt.truth.HumanDetection object at 0x7fec74ccbee0>, <fmdt.truth.HumanDetection object at 0x7febad89b520>, <fmdt.truth.HumanDetection object at 0x7febad89b3d0>, <fmdt.truth.HumanDetection object at 0x7febad89b5e0>, <fmdt.truth.HumanDetection object at 0x7febad89b430>, <fmdt.truth.HumanDetection object at 0x7febad89b640>, <fmdt.truth.HumanDetection object at 0x7febad89b490>, <fmdt.truth.HumanDetection object at 0x7febad89b6a0>, <fmdt.truth.HumanDetection object at 0x7febad89b4f0>, <fmdt.truth.HumanDetection object at 0x7febad89b700>, <fmdt.truth.HumanDetection object at 0x7febad89b550>, <fmdt.truth.HumanDetection object at 0x7febad89b760>, <fmdt.truth.HumanDetection object at 0x7febad89b5b0>, <fmdt.truth.HumanDetection object at 0x7febad89b7c0>, <fmdt.truth.HumanDetection object at 0x7febad89b610>, <fmdt.truth.HumanDetection object at 0x7febad89b820>, <fmdt.truth.HumanDetection object at 0x7febad89b670>, <fmdt.truth.HumanDetection object at 0x7febad89b880>, <fmdt.truth.HumanDetection object at 0x7febad89b6d0>, <fmdt.truth.HumanDetection object at 0x7febad89b8e0>, <fmdt.truth.HumanDetection object at 0x7febad89b730>, <fmdt.truth.HumanDetection object at 0x7febad89b940>, <fmdt.truth.HumanDetection object at 0x7febad89b790>, <fmdt.truth.HumanDetection object at 0x7febad89b9a0>, <fmdt.truth.HumanDetection object at 0x7febad89b7f0>, <fmdt.truth.HumanDetection object at 0x7febad89ba00>, <fmdt.truth.HumanDetection object at 0x7febad89b850>, <fmdt.truth.HumanDetection object at 0x7febad89ba60>, <fmdt.truth.HumanDetection object at 0x7febad89b8b0>, <fmdt.truth.HumanDetection object at 0x7febad89bac0>, <fmdt.truth.HumanDetection object at 0x7febad89b910>, <fmdt.truth.HumanDetection object at 0x7febad89bb20>, <fmdt.truth.HumanDetection object at 0x7febad89b970>, <fmdt.truth.HumanDetection object at 0x7febad89bb80>]
```

### FMDT Executables

We can run all three of our core executables starting with a `Video` object.

=== "detect"

    !!! warning

        If `v` is not on disc (`v.exists() == False`) then `v.detect()` will 
        raise an exception

    We can run a detection with `detect()`:

    ``` py
    >>> res = v.detect()
    (II) Frame n° 255 -- Tracks = ['meteor':  38, 'star':   0, 'noise':   0, 'total':  38]
    ```

    === "`res`"

        ``` py
        fmdt.res.DetectionResult with args digest: 31a2dd4832e985d6
        objects in trk_list: 38 meteor(s), 0 star(s), 0 noise
        ```

    === "`res.trk_list`"

        ``` py
        [<Meteor (102, 108)>, <Meteor (110, 126)>, <Meteor (111, 118)>, <Meteor (121, 123)>, <Meteor (127, 129)>, <Meteor (129, 131)>, <Meteor (133, 141)>, <Meteor (134, 143)>, <Meteor (134, 137)>, <Meteor (136, 138)>, <Meteor (139, 144)>, <Meteor (139, 142)>, <Meteor (140, 150)>, <Meteor (146, 149)>, <Meteor (156, 158)>, <Meteor (156, 165)>, <Meteor (157, 162)>, <Meteor (160, 163)>, <Meteor (164, 167)>, <Meteor (167, 169)>, <Meteor (171, 175)>, <Meteor (174, 180)>, <Meteor (178, 185)>, <Meteor (179, 181)>, <Meteor (179, 189)>, <Meteor (180, 184)>, <Meteor (183, 189)>, <Meteor (194, 197)>, <Meteor (197, 199)>, <Meteor (199, 201)>, <Meteor (200, 205)>, <Meteor (201, 203)>, <Meteor (202, 204)>, <Meteor (223, 229)>, <Meteor (224, 228)>, <Meteor (227, 231)>, <Meteor (249, 252)>, <Meteor (251, 253)>]
        ```

    === "`res.nframes`"

        ``` py
        256
        ```

    === "`res.args`"

        ``` py
        <fmdt.args.Args object>
        ====================
        Detect parameters: 
        {'vid_in_path': '/run/media/ejovo/Seagate Portable Drive/Meteors/2022_05_31_tauh_34_meteors.mp4', 'trk_path': 'trk.txt'}
        ```


    #### Movement Statistics

    We can additionally store movement statistics if we manually specify a log 
    directory with the `log_path` argument.

    ``` py
    >>> res = v.detect(log_path="log")
    (II) Frame n° 255 -- Tracks = ['meteor':  38, 'star':   0, 'noise':   0, 'total':  38]
    Trying to retrieve log info here: log

    >>> print(res)
    fmdt.res.DetectionResult with args digest: 74fffad3f5036080
    objects in trk_list: 38 meteor(s), 0 star(s), 0 noise
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

    The estimated movement statistics are stored in the `df` member of our 
    `fmdt.res.DetectionResult`.

    #### Unique `log_path`

    When running multiple diffent videos with the same core set of arguments, it 
    might be a good idea to isolate out `log_path`. To automatically cache the 
    log information in a unique folder, call `detect` with the `save_df` 
    parameter set to `True` instead of using `log_path`:

    !!! danger 
        
        TODO: Explain the `save_df` argument. What does the `df` acronym mean?

    ``` py
    >>> res = v.detect(save_df=True)
    Save_df activated in final detect call
    (II) Frame n° 255 -- Tracks = ['meteor':  38, 'star':   0, 'noise':   0, 'total':  38]
    Trying to retrieve log info here: /home/ejovo/.cache/fmdt_python/31a2dd4832e985d6
    ```

    This will automatically cache our log results in a unique directory. Consult 
    [this](./howto/4_use_the_cache.md) to guide to learn how to monitor and 
    clear the cache.

=== "log_parser"

    !!! failure 
        
        `fmdt.log_parser()` is currently unavailable.

=== "visu"

    !!! failure 
        
        `Video.visu()` is currently unavailable.

=== "check"

    We can retrieve the tracking statistics produced by `fmdt-check` by chaining 
    the function calls `detect()` and `check()` together.

    ``` py
    check_res = v.detect().check()
    ```

    === "`check_res.gt_path`"

        ``` py
        >>> check_res.gt_table
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


    === "`check_res.stats`"

        ``` py
        >>> check_res.stats
            type  gt  ntrk  tpos  fpos  tneg  fneg  trk_rate
        0  meteor  34    38    35     3     0     0      0.95
        1    star   0     0     0     0    38     0       NaN
        2   noise   0     0     0     0    38     0       NaN
        3     all  34    38    35     3    76     0      0.95
        ```

    === "`check_res.*_stats()`"

        ``` py
        >>> check_res.meteor_stats()
        type        meteor
        gt              34
        ntrk            38
        tpos            35
        fpos             3
        tneg             0
        fneg             0
        trk_rate      0.95
        Name: 0, dtype: object


        >>> check_res.star_stats()
        type        star
        gt             0
        ntrk           0
        tpos           0
        fpos           0
        tneg          38
        fneg           0
        trk_rate     NaN
        Name: 1, dtype: object


        >>> check_res.noise_stats()
        type        noise
        gt              0
        ntrk            0
        tpos            0
        fpos            0
        tneg           38
        fneg            0
        trk_rate      NaN
        Name: 2, dtype: object


        >>> check_res.all_stats()
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

For more information about the results of these executables, consult 
[this section](./reference/res.md).

## VideoClip

The class `fmdt.VideoClip` is a subclass of `fmdt.Video` and is used to 
represent a portion of specific video that contains meteors. This class is 
primarily used when working with the [`window`](./explanation/video_database.md) 
videos as they are all 5 minutes long and each contain multiple meteors.

### Creation

We can create a `list[VideoClip]` starting from a `Video` with known ground 
truths. Let's take the first `window` as an example.

``` py
w = fmdt.load_window()[0]
```

Make sure our video has ground truths in our database with `has_meteors()` and 
then instantiate some `VideoClip` objects with `create_clips()`

=== "code"

    ``` py
    clips = w.create_clips()
    ```

=== "output"

    ``` py
    >>> clips
    [window_3_sony_0400-0405UTC.mp4 [773, 802], window_3_sony_0400-0405UTC.mp4 [1213, 1262], window_3_sony_0400-0405UTC.mp4 [1414, 1451], window_3_sony_0400-0405UTC.mp4 [2276, 2335], window_3_sony_0400-0405UTC.mp4 [2823, 2862], window_3_sony_0400-0405UTC.mp4 [2850, 2900], window_3_sony_0400-0405UTC.mp4 [2916, 2945], window_3_sony_0400-0405UTC.mp4 [3414, 3446], window_3_sony_0400-0405UTC.mp4 [3845, 3874], window_3_sony_0400-0405UTC.mp4 [4143, 4191], window_3_sony_0400-0405UTC.mp4 [4250, 4280], window_3_sony_0400-0405UTC.mp4 [4435, 4472], window_3_sony_0400-0405UTC.mp4 [5311, 5342], window_3_sony_0400-0405UTC.mp4 [6778, 6823], window_3_sony_0400-0405UTC.mp4 [7187, 7219]]
    ```

If we want to actually save these clips to disk, we add the parameter 
`save_to_disk=True`

=== "code"

    ``` py
    clips = w.create_clips(save_to_disk=True)
    ```

=== "output"

    ``` py
    Running command 'ffmpeg -ss 00:00:30.920 -i /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC.mp4 -t 00:00:01.160 /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC/f0773-0802_.mp4 -loglevel error'
    Running command 'ffmpeg -ss 00:00:48.520 -i /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC.mp4 -t 00:00:01.960 /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC/f1213-1262_.mp4 -loglevel error'
    Running command 'ffmpeg -ss 00:00:56.560 -i /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC.mp4 -t 00:00:01.480 /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC/f1414-1451_.mp4 -loglevel error'
    Running command 'ffmpeg -ss 00:01:31.040 -i /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC.mp4 -t 00:00:02.360 /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC/f2276-2335_.mp4 -loglevel error'
    Running command 'ffmpeg -ss 00:01:52.920 -i /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC.mp4 -t 00:00:01.560 /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC/f2823-2862_.mp4 -loglevel error'
    Running command 'ffmpeg -ss 00:01:54.000 -i /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC.mp4 -t 00:00:02.000 /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC/f2850-2900_.mp4 -loglevel error'
    Running command 'ffmpeg -ss 00:01:56.640 -i /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC.mp4 -t 00:00:01.160 /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC/f2916-2945_.mp4 -loglevel error'
    Running command 'ffmpeg -ss 00:02:16.560 -i /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC.mp4 -t 00:00:01.280 /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC/f3414-3446_.mp4 -loglevel error'
    Running command 'ffmpeg -ss 00:02:33.800 -i /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC.mp4 -t 00:00:01.160 /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC/f3845-3874_.mp4 -loglevel error'
    Running command 'ffmpeg -ss 00:02:45.720 -i /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC.mp4 -t 00:00:01.920 /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC/f4143-4191_.mp4 -loglevel error'
    Running command 'ffmpeg -ss 00:02:50.000 -i /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC.mp4 -t 00:00:01.200 /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC/f4250-4280_.mp4 -loglevel error'
    Running command 'ffmpeg -ss 00:02:57.400 -i /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC.mp4 -t 00:00:01.480 /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC/f4435-4472_.mp4 -loglevel error'
    Running command 'ffmpeg -ss 00:03:32.440 -i /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC.mp4 -t 00:00:01.240 /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC/f5311-5342_.mp4 -loglevel error'
    Running command 'ffmpeg -ss 00:04:31.120 -i /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC.mp4 -t 00:00:01.800 /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC/f6778-6823_.mp4 -loglevel error'
    Running command 'ffmpeg -ss 00:04:47.480 -i /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC.mp4 -t 00:00:01.280 /run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC/f7187-7219_.mp4 -loglevel error'
    ```

Each individual clip can be interfaced just like as a `Video` above thanks to 
class inheritance. Here we showcase a few examples.

??? example "Get meteors"

    === "code"

        ``` py
        clips[0].meteors()
        ```

    === "output"

        ``` py
        [<fmdt.truth.HumanDetection object at 0x7f2b0c156ad0>]
        ```

??? example "Retrieve the path to the video from which this clip was generated"

    === "code"

        ``` py
        clips[0].parent_path()
        ```

    === "output"

        ``` py
        '/run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC/'
        ```

??? example "Retrieve the full path to this clip"

    === "code"

        ``` py
        clips[0].full_path()
        ```

    === "output"

        ``` py
        '/run/media/ejovo/Seagate Portable Drive/Meteors/window_3_sony_0400-0405UTC/f0773-0802_.mp4'
        ```

??? example "Run a detection"

    === "code"

        ``` py
        clips[0].detect()
        ```

    === "output"

        ``` py
        (II) Frame n°  28 -- Tracks = ['meteor':   0, 'star':   0, 'noise':   0, 'total':   0]
        <fmdt.res.DetectionResult object at 0x7f2b0c1571f0>
        ```

??? example "Retrieve number of frames"

    === "code"

        ``` py
        clips[0].nb_frames()
        ```

    === "output"

        ``` py
        29
        ```


## Ground Truths

We can retrieve all the ground truths from our database that are associated with 
a particular video by using the `Video.meteors()` function. Start by loading in 
our Draco6 videos.

``` py
d6_all = fmdt.load_draco6() # Loads all 52 Draco6 videos in our database
d6 = [v for v in d6_all if v.has_meteors()] # Filter out the 38 that have gts in our database
```

``` py
>>> len(d6_all)
52

>>> len(d6)
38

>>> d6
[Draconids-6mm1.00-2750-163200.avi, Draconids-6mm1.05-0750-164200.avi, Draconids-6mm1.14-1400-170300.avi, Draconids-6mm1.20-2350-171600.avi, Draconids-6mm1.29-2550-173600.avi, Draconids-6mm1.30-2050-173800.avi, Draconids-6mm1.32-3150-174200.avi, Draconids-6mm1.34-3050-174700.avi, Draconids-6mm2.00.01-1000-201100.avi, Draconids-6mm2.00.01-1500-201200.avi, Draconids-6mm2.00.01-2150-201200.avi, Draconids-6mm2.00.02-0700-201300.avi, Draconids-6mm2.00.03-0450-201500.avi, Draconids-6mm2.00.03-0550-201500.avi, Draconids-6mm2.00.03-0950-201500.avi, Draconids-6mm2.00.04-1500-201800.avi, Draconids-6mm2.00.04-1900-201900.avi, Draconids-6mm2.00.04-2950-201900.avi, Draconids-6mm2.00.05-0120-202000.avi, Draconids-6mm2.00.05-0350-202000.avi, Draconids-6mm2.00.07-0900-202400.avi, Draconids-6mm2.00.07-2400-202500.avi, Draconids-6mm2.00.07-3000-202530.avi, Draconids-6mm2.00.09-0600-202900.avi, Draconids-6mm2.00.09-1650-203000.avi, Draconids-6mm2.00.09-3000-203030.avi, Draconids-6mm2.00.10-0300-203100.avi, Draconids-6mm2.00.10-0350-203110.avi, Draconids-6mm2.00.10-1050-203200.avi, Draconids-6mm2.00.11-2100-203400.avi, Draconids-6mm2.00.11-680-203300.avi, Draconids-6mm2.00.11-780-203310.avi, Draconids-6mm2.00.12-1550-203600.avi, Draconids-6mm2.00.12-2550-203700.avi, Draconids-6mm2.00.12-3100-203730.avi, Draconids-6mm2.00.13-0680-203800.avi, Draconids-6mm2.00.13-3100-204000.avi, Draconids-6mm2.00.15-0750-204200.avi]
```

After only keeping videos that have ground truths in our database we retrieve 
the list of meteors associated with the first video:

``` py
>>> d6[2].full_path()
'/run/media/ejovo/Seagate Portable Drive/Meteors/Watec6mm/Meteor/Draconids-6mm1.14-1400-170300.avi'

>>> d6[2].meteors()
[<fmdt.truth.HumanDetection object at 0x7fcd9ae92bf0>]
```

So we can conclude that `Draconids-6mm1.14-1400-170300.avi` has one 
human-verified ground truth meteor in our database.

Let's hold onto that truth.

``` py
hum_det = d6[2].meteors()[0]
```

Retrieve the trk list to see if the human detection is spotted.

``` py
res = d6[2].detect(ccl_hyst_lo=253, ccl_hyst_hi=255)

>>> fmdt.truth.is_meteor_detected(meteor=hum_det, tracking_list=res.trk_list)
True
```

Awesome! With args:

``` py
>>> print(res.args)
<fmdt.args.Args object>
====================
Detect parameters: 
{'vid_in_path': '/run/media/ejovo/Seagate Portable Drive/Meteors/Watec6mm/Meteor/Draconids-6mm1.14-1400-170300.avi', 'ccl_hyst_lo': 253, 'ccl_hyst_hi': 255, 'trk_path': 'trk.txt'}
```

The meteor
``` py
>>> print(hum_det)
(Draconids-6mm1.14-1400-170300.avi, f0: 11, fT: 24, pos0: (11.0, 233.0), posT: (14.0, 273.0))
```

is associated with 

``` py
>>> print(res.trk_list[0])
<Meteor (19, 22), pos0: ((10.2, 260.4)), posT: (12.1, 267.6)>
```