# Core Usage

This section presents the core usage of `fmdt-python`.

### Call `fmdt` executables

```
import fmdt

fmdt.detect(vid_in_path="2022_05_31_tauh_34_meteors.mp4", trk_bb_path="bb.txt", trk_out_path="trk.txt", light_min=100, light_max=150, log_path="log")
fmdt.visu(vid_in_path="2022_05_31_tauh_34_meteors.mp4", trk_bb_path="bb.txt", trk_path="trk.txt")
fmdt.check(trk_path="trk.txt", gt_path="2022_05_31_tauh_34_meteors.txt")
```

### Initialize database directories

For a list of videos in our database, go [here](./explanation/video_database.md). For instructions how to initialize your configuration, read [this](./howto/0_initialization.md).

If you haven't already done so, notify `fmdt` where you have the database files stored. If, for example, we have our videos stored on a remote hard drive `Seagate Portable Drive` then we could configure `fmdt` for linux user `ejovo` with:

```
fmdt.init(d6_dir="/run/media/ejovo/Seagate Portable Drive/Meteors/Watec6mm/Meteor",
         d12_dir="/run/media/ejovo/Seagate Portable Drive/Meteors/Watec12mm/Meteor",
         win_dir="/run/media/ejovo/Seagate Portable Drive/Meteors")
```

We can compare what files we have in our local config compared to the files listed in our [database](./explanation/video_database.md) with the function `local_info()`:
```py
>>> fmdt.local_info()
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

### Video interface

We start by loading in our demo:

```py
v = fmdt.load_demo()
```

```py
>>> v
2022_05_31_tauh_34_meteors.mp4

>>> type(v)
<class 'fmdt.db.Video'>

>>> v.full_path()
'/run/media/ejovo/Seagate Portable Drive/Meteors/2022_05_31_tauh_34_meteors.mp4'
```

And we can run a detection with `detect()`:

```
>>> res = v.detect()
(II) Frame n° 255 -- Tracks = ['meteor':  38, 'star':   0, 'noise':   0, 'total':  38]

>>> print(res)
fmdt.res.DetectionResult with args digest: 74fffad3f5036080
objects in trk_list: 38 meteor(s), 0 star(s), 0 noise
```

Access the list of `TrackedObject` with the `trk_list` field:

```
>>> res.trk_list
[<Meteor (102, 108)>, <Meteor (110, 126)>, <Meteor (111, 118)>, <Meteor (121, 123)>, <Meteor (127, 129)>, <Meteor (129, 131)>, <Meteor (133, 141)>, <Meteor (134, 143)>, <Meteor (134, 137)>, <Meteor (136, 138)>, <Meteor (139, 144)>, <Meteor (139, 142)>, <Meteor (140, 150)>, <Meteor (146, 149)>, <Meteor (156, 158)>, <Meteor (156, 165)>, <Meteor (157, 162)>, <Meteor (160, 163)>, <Meteor (164, 167)>, <Meteor (167, 169)>, <Meteor (171, 175)>, <Meteor (174, 180)>, <Meteor (178, 185)>, <Meteor (179, 181)>, <Meteor (179, 189)>, <Meteor (180, 184)>, <Meteor (183, 189)>, <Meteor (194, 197)>, <Meteor (197, 199)>, <Meteor (199, 201)>, <Meteor (200, 205)>, <Meteor (201, 203)>, <Meteor (202, 204)>, <Meteor (223, 229)>, <Meteor (224, 228)>, <Meteor (227, 231)>, <Meteor (249, 252)>, <Meteor (251, 253)>]
```

### Movement Statistics

We can additionally store movement statistics if we manually specify a log directory with the `log_path` argument.

```
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

The movement statistics are stored in the `df` member of our `fmdt.res.DetectionResult`:

```
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

When running multiple diffent videos with the same core set of arguments, it might be a good idea to isolate log_paths. To automatically cache the log information in a unique folder, call `detect` with the `save_df` parameter set to `True` instead of using `log_path`:

```
>>> res = v.detect(save_df=True)
Save_df activated in final detect call
(II) Frame n° 255 -- Tracks = ['meteor':  38, 'star':   0, 'noise':   0, 'total':  38]
Trying to retrieve log info here: /home/ejovo/.cache/fmdt_python/31a2dd4832e985d6
```

Consult the [howto guide](./howto/4_use_the_cache.md) to learn how to monitor and clear the cache.

### Ground Truths

We can retrieve all the ground truths from our database that are associated with a particular video by using the `Video.meteors()` function. Start by loading in our Draco6 videos.

```
d6_all = fmdt.load_draco6() # Loads all 52 Draco6 videos in our database
d6 = [v for v in d6_all if v.has_meteors()] # Filter out the 38 that have gts in our database
```

```
>>> len(d6_all)
52

>>> len(d6)
38

>>> d6
[Draconids-6mm1.00-2750-163200.avi, Draconids-6mm1.05-0750-164200.avi, Draconids-6mm1.14-1400-170300.avi, Draconids-6mm1.20-2350-171600.avi, Draconids-6mm1.29-2550-173600.avi, Draconids-6mm1.30-2050-173800.avi, Draconids-6mm1.32-3150-174200.avi, Draconids-6mm1.34-3050-174700.avi, Draconids-6mm2.00.01-1000-201100.avi, Draconids-6mm2.00.01-1500-201200.avi, Draconids-6mm2.00.01-2150-201200.avi, Draconids-6mm2.00.02-0700-201300.avi, Draconids-6mm2.00.03-0450-201500.avi, Draconids-6mm2.00.03-0550-201500.avi, Draconids-6mm2.00.03-0950-201500.avi, Draconids-6mm2.00.04-1500-201800.avi, Draconids-6mm2.00.04-1900-201900.avi, Draconids-6mm2.00.04-2950-201900.avi, Draconids-6mm2.00.05-0120-202000.avi, Draconids-6mm2.00.05-0350-202000.avi, Draconids-6mm2.00.07-0900-202400.avi, Draconids-6mm2.00.07-2400-202500.avi, Draconids-6mm2.00.07-3000-202530.avi, Draconids-6mm2.00.09-0600-202900.avi, Draconids-6mm2.00.09-1650-203000.avi, Draconids-6mm2.00.09-3000-203030.avi, Draconids-6mm2.00.10-0300-203100.avi, Draconids-6mm2.00.10-0350-203110.avi, Draconids-6mm2.00.10-1050-203200.avi, Draconids-6mm2.00.11-2100-203400.avi, Draconids-6mm2.00.11-680-203300.avi, Draconids-6mm2.00.11-780-203310.avi, Draconids-6mm2.00.12-1550-203600.avi, Draconids-6mm2.00.12-2550-203700.avi, Draconids-6mm2.00.12-3100-203730.avi, Draconids-6mm2.00.13-0680-203800.avi, Draconids-6mm2.00.13-3100-204000.avi, Draconids-6mm2.00.15-0750-204200.avi]
```

After only keeping videos that have ground truths in our database we retrieve the list of meteors associated with the first video:

```
>>> d6[2].full_path()
'/run/media/ejovo/Seagate Portable Drive/Meteors/Watec6mm/Meteor/Draconids-6mm1.14-1400-170300.avi'

>>> d6[2].meteors()
[<fmdt.truth.HumanDetection object at 0x7fcd9ae92bf0>]
```

So we can conclude that Draconids-6mm1.14-1400-170300.avi has one human-verified ground truth meteor 
in our database.

Let's hold onto that truth.

```
hum_det = d6[2].meteors()[0]
```

Retrieve the trk list to see if the human detection is spotted.

```
res = d6[2].detect(light_min=253, light_max=255)

>>> fmdt.truth.is_meteor_detected(meteor=hum_det, tracking_list=res.trk_list)
True
```

Awesome! With args:

```
>>> print(res.args)
<fmdt.args.Args object>
====================
Detect parameters: 
{'vid_in_path': '/run/media/ejovo/Seagate Portable Drive/Meteors/Watec6mm/Meteor/Draconids-6mm1.14-1400-170300.avi', 'light_min': 253, 'light_max': 255, 'trk_bb_path': 'bb.txt', 'trk_out_path': 'trk.txt'}
```

The meteor
```
>>> print(hum_det)
(Draconids-6mm1.14-1400-170300.avi, f0: 11, fT: 24, pos0: (11.0, 233.0), posT: (14.0, 273.0))
```

is associated with 

```
>>> print(res.trk_list[0])
<Meteor (19, 22), pos0: ((10.2, 260.4)), posT: (12.1, 267.6)>
```