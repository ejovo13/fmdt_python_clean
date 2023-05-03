# High-Level Overview

This section introduces the four fundamental classes of `fmdt-python`:

- `Video`
- `Args`
- `HumanDetection`
- `TrackedObject`

---

## Video
defined in: `fmdt.db` <br>
aliased as: `fmdt.Video`


## Args

The `fmdt.args.Args` (aliased as `fmdt.Args`) class is used to represent a 
specific combination of arguments used to run `fmdt`'s suite of executables.

### Creation

We create a new `Args` object by providing a dictionary of the arguments that we 
want to use for `fmdt-detect`.

```Python
d_args_dict = {
    "ccl_hyst_lo": 55,
    "ccl_hyst_hi": 80,
    "trk_all": True
}

args = fmdt.Args(detect_args=d_args_dict)
```

We can use the `Args` class to call `fmdt.detect`:

```Python
d_args = {
    "vid_in_path": "demo.mp4",
    "trk_path": "trk.txt",
    "ccl_hyst_lo": 55,
    "ccl_hyst_hi": 80
}

args = fmdt.Args(detect_args=fmdt.DetectArgs(**d_args))
args = args.detect()
```

It's important to know that we can also get an `Args` instance as the return 
type from a call to `fmdt.detect`:

```Python
res = fmdt.detect(vid_in_path="demo.mp4")
print(res.args)
```

### Chaining together function calls

We can utilize the fact that a call to `fmdt.detect` returns an `Args` type and 
the fact that an `Args` type has the member functions `detect`, `log_parser` and 
`visu` to chain together detection and visualization:

```Python
d_args = {
    "vid_in_path": "demo.mp4",
    "trk_path": "tracks.txt",          # required for `visu()` to work
    "trk_roi_path": "tracks2rois.txt", # required for `log_parser()` to work
    "log_path": "detect_log",          # required for `log_parser()` to work
}

args = fmdt.Args(detect_args=fmdt.DetectArgs(**d_args))
res = args.detect().log_parser().visu()
```

---

## TrackedObject

A `TrackedOjbect` encodes the results of a call to `fmdt-detect`. A list of 
`TrackedObject` is our representation of the table of tracks outputted by 
`fmdt-detect` (corresponding to the `trk_path` parameter)

### Creation

A list of `TrackedObject` can be retreived two different ways. The first 
involves a fresh call to `fmdt.detect` and uses the `Args` object that we just 
studied. In this method we **have** to specify the `trk_path` so that we can 
later retreive the data.

```Python
d_args = {
    "vid_in_path": "demo.mp4",
    "trk_path": "tracks.txt",
    "ccl_hyst_lo": 55,
    "ccl_hyst_hi": 80
}

res = fmdt.detect(**d_args)

print(res.trk_list) #! Actually a list of TrackedObject
```

Tada! We've actually already automatically been storing the results in our 
returned `Args`.

If the tracking table is already stored in a file ("track.txt" for example) and 
we want to just load it into Python, then we can use the function 
`extract_all_information`:

```Python
fmdt.extract_all_information("track.txt")
```

which could return a list of `TrackedObject`:

```Python
[<Meteor (102, 108)>, <Meteor (110, 126)>, <Meteor (111, 118)>, <Meteor (121, 123)>, 
<Meteor (127, 129)>, <Meteor (129, 131)>, <Meteor (133, 141)>, <Meteor (134, 143)>, 
<Meteor (134, 137)>, <Meteor (136, 138)>, <Meteor (139, 144)>, <Meteor (139, 142)>, 
<Meteor (140, 150)>, <Meteor (146, 149)>, <Meteor (156, 158)>, <Meteor (156, 165)>, 
<Meteor (157, 162)>, <Meteor (160, 163)>, <Meteor (164, 167)>, <Meteor (167, 169)>, 
<Meteor (171, 175)>, <Meteor (174, 180)>, <Meteor (178, 185)>, <Meteor (179, 181)>, 
<Meteor (179, 189)>, <Meteor (180, 184)>, <Meteor (183, 189)>, <Meteor (194, 197)>,
<Meteor (197, 199)>, <Meteor (199, 201)>, <Meteor (200, 205)>, <Meteor (201, 203)>, 
<Meteor (202, 204)>, <Meteor (223, 229)>, <Meteor (224, 228)>, <Meteor (227, 231)>, 
<Meteor (249, 252)>, <Meteor (251, 253)>]
```

---

# GroundTruth

A `GroundTruth` represents a database of `HumanDetection` instances. For 
example, we can study the databases of the Draconids-6mm (draco6) and 
Draconids-12mm (draco12) separately. Two csv files containing a table of 
`HumanDetection`  objects can be retrieved for 
[draco6](https://github.com/ejovo13/fmdt_python_clean/blob/main/data/human_detections_draco6.csv) 
and 
[draco12](https://github.com/ejovo13/fmdt_python_clean/blob/main/data/human_detections_draco12.csv).

### Creation

In order to create a `GroundTruth` object, you need to have a csv containing a 
table of `HumanDetection`. If you would like to actually analyze any aspects of 
the database you additionally need to have the _videos_ stored on your computer.

The following snipped of code will load in a `GroundTruth` object that will be 
used to study the demo video. It works because the csv file is in the current 
working directory and the demo video file are stored physically on my disk under 
the `/home/ejovo/Videos/Window` directory.

```Python
vid_dir  = "/home/ejovo/Videos/Window"
csv_file = "human_detections_demo.csv"

gt_demo = fmdt.GroundTruth(csv=csv_file, vid_dir=vid_dir)
```

We can go ahead and apply a single `Args` object across our entire `GroundTruth` 
database using the function `GroundTruth.try_command()`:

```Python
truth_detected = gtdemo.try_command(args=fmdt.Args.new(**d_args)) # use any fmdt.Args from before
```

which will store a list of booleans indicating whether or not the corresponding 
`HumanDetection` was found after a call to `fmdt-detect` with the parameters 
indicated by `Args`.

### Heatmap

We can use a `GroundTruth` object combined with a linspace of `ccl_hyst_lo` and 
`ccl_hyst_hi` to create a heat map of which meteors were detected usign the 
specified lumonisity parameters. To do so we simply call the function 
`GroundTruth.heat_map`, which has a similar argument placement as numpy's 
`linspace`.

```Python
vid_dir  = "/home/ejovo/Videos/Watec12mm"
csv_file = "human_detections_draco12.csv"

gt12 = fmdt.GroundTruth(csv=csv_file, vid_dir=vid_dir)

# this operation can take a while... you have been warned ;-)
gt12.draw_heatmap(150, 250, 20)
```

---

# HumanDetection

A `HumanDetection` represents the blood, sweat, and tears of a human being that 
was spent to painstakenly detect a meteor. It records the video in which the 
meteor appears, start position, end position, and lifetime in terms of frames.

To see a complete list of the operations that can be performed, call 
`help(fmdt.HumanDetection)`

`HumanDetection` objects are compared with `TrackedObject`s to measure the 
performace of `fmdt-detect`.

### Creation

A `HumanDetection` should not be instantiated manually. The creation of 
`HumanDetection`s is handled by the `GroundTruth` class, which represents an 
individual database of `HumanDetection`.

Assuming that we have loaded in a `HumandDetection` (see 
[GroundTruth](#GroundTruth)) as `hum`, and a list of `TrackedObject` as 
`objects`, we can go ahead and test for the presence of `hum` in `objects` with 
the `is_meteor_detected()` function of the `fmdt.truth` module:

```Python
detect_res = fmdt.detect(vid_in_path="demo.mp4", trk_path="tracks.txt")

# hum is a fmdt.HumanDetection
hum = gt_demo.meteors[2]
# objects is a list[fmdt.TrackedObject]
objects = detect_res.trk_list

hum_detected = fmdt.truth.is_meteor_detected(hum, objects)
```

which returns `True` if the `HumanDetection` `hum` matches up with any of the 
`TrackedObject`s in `objects`.
