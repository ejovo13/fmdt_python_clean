# Loading Videos

This guide will show you how to load and play with videos loaded via the `fmdt.load_draco6()`, `fmdt.load_draco12()`, and `fmdt.load_window()` functions.

## Draco6

We load the Draconids-6mm videos as a `list[Video]` with `load_draco6()`.

```
d6 = fmdt.load_draco6()
```

```
>>> d6
[Draconids-6mm1.00-2750-163200.avi, Draconids-6mm1.05-0750-164200.avi, Draconids-6mm1.14-1400-170300.avi, Draconids-6mm1.20-2350-171600.avi, Draconids-6mm1.29-2550-173600.avi, Draconids-6mm1.30-2050-173800.avi, Draconids-6mm1.32-3150-174200.avi, Draconids-6mm1.34-3050-174700.avi, Draconids-6mm2.00.01-1000-201100.avi, Draconids-6mm2.00.01-1500-201200.avi, Draconids-6mm2.00.01-2150-201200.avi, Draconids-6mm2.00.02-0700-201300.avi, Draconids-6mm2.00.03-0450-201500.avi, Draconids-6mm2.00.03-0550-201500.avi, Draconids-6mm2.00.03-0950-201500.avi, Draconids-6mm2.00.04-1500-201800.avi, Draconids-6mm2.00.04-1900-201900.avi, Draconids-6mm2.00.04-2950-201900.avi, Draconids-6mm2.00.05-0120-202000.avi, Draconids-6mm2.00.05-0200-202000.avi, Draconids-6mm2.00.05-0350-202000.avi, Draconids-6mm2.00.07-0900-202400.avi, Draconids-6mm2.00.07-2400-202500.avi, Draconids-6mm2.00.07-3000-202530.avi, Draconids-6mm2.00.09-0600-202900.avi, Draconids-6mm2.00.09-1650-203000.avi, Draconids-6mm2.00.09-3000-203030.avi, Draconids-6mm2.00.10-0300-203100.avi, Draconids-6mm2.00.10-0350-203110.avi, Draconids-6mm2.00.10-1050-203200.avi, Draconids-6mm2.00.11-2100-203400.avi, Draconids-6mm2.00.11-680-203300.avi, Draconids-6mm2.00.11-780-203310.avi, Draconids-6mm2.00.12-1550-203600.avi, Draconids-6mm2.00.12-2550-203700.avi, Draconids-6mm2.00.12-3100-203730.avi, Draconids-6mm2.00.13-0680-203800.avi, Draconids-6mm2.00.13-3100-204000.avi, Draconids-6mm2.00.15-0750-204200.avi, Draconids-6mm2.00.15-2300-204300.avi, Draconids-6mm2.00.15-2850-204330.avi, Draconids-6mm2.00.170050-204700.avi, Draconids-6mm2.00.18-0000-204900.avi, Draconids-6mm2.00.18-2850-205000.avi, Draconids-6mm2.00.19-0680-205100.avi, Draconids-6mm2.00.19-1550-205200.avi, Draconids-6mm2.00.20-2600-205500.avi, Draconids-6mm2.00.20-2900-205510.avi, Draconids-6mm2.00.22-3150-205900.avi, Draconids-6mm2.00.25-2250-210600.avi, Draconids-6mm2.00.26-450-210700.avi, Draconids-6mm2.00.28-1950-211200.avi]

>>> len(d6)
52

>>> type(d6[0])
<class 'fmdt.db.Video'>
```

##### fmdt.db.Video

We can query if a video has any ground truths in our database with `has_meteors()`. Let's use the first Draco6 video as an example:
```
v = d6[0]
>>> v
Draconids-6mm1.00-2750-163200.avi

>>> v.full_path()
'/home/ejovo/Videos/Watec6mm/Draconids-6mm1.00-2750-163200.avi'

>>> v.has_meteors()
True

>>> v.meteors()   # returns a list of HumanDetection
[<fmdt.truth.HumanDetection object at 0x7f58c5fcdc30>]
```

In the background we have downloaded a `videos.db` file that has a detailed list of our ground truth detections and the videos in our draco6, draco12, and window categories.

## Printing Diagnostics

We can print some information about which videos `fmdt` can find on your system with `fmdt.db_info()`
```
fmdt.db_info()
```

```
>>> fmdt.db_info()
Printing information about the local environment
================================================================================
Draconids-6mm*.avi videos configured with dir: /home/ejovo/Videos/Watec6mm
================================================================================
52 videos exist on disc out of the 52 videos in our database
38 of which have ground truths out of 38 ground truths in our database

================================================================================
Draconids-12mm*.avi videos configured with dir: /home/ejovo/Videos/Watec12mm
================================================================================
41 videos exist on disc out of the 41 videos in our database
37 of which have ground truths out of 37 ground truths in our database

================================================================================
window*.mp4 videos configured with dir: /home/ejovo/Videos/Window
================================================================================
7 videos exist on disc out of the 7 videos in our database
0 of which have ground truths out of 0 ground truths in our database
```

## Detect from a Video

We can detect from a video using `detect()` just as we are used to.

```
vid = d6[1]
res = vid.detect(light_min=253, light_max=255)
```