# GroundTruth Testing
Companion script: [test_ground_truth.py](https://github.com/ejovo13/fmdt_python_clean/blob/main/test_ground_truth.py)

---

### Attention

Version `0.0.25` of `fmdt-python` updated the way we access the database.

In this guide you'll learn how to use `fmdt` to test the performance of `fmdt-detect`. The relevant
functions for ground truth testing are stored in the `fmdt.truth` module.

# > 0.0.25

## Initial config

You must perform the steps in this section once and only once.

- Call the function `fmdt.init` to inform `fmdt-python` where you have stored the Draconids-6mm, Draconids-12mm, and window videos from our database.


**prototype**

```
import fmdt
fmdt.init(d6_dir  = "/your/dir/Videos/Watec6mm",
          d12_dir = "/your/dir/Videos/Watec12mm",
          win_dir = "/your/dir/Videos")
```

**real example**
```
>>> import fmdt
>>> fmdt.init(d6_dir  = "/home/ejovo/Videos/Watec6mm",
...           d12_dir = "/home/ejovo/Videos/Watec12mm",
...           win_dir = "/home/ejovo/Videos")
Saved config to /home/ejovo/.local/share/fmdt_python/config.json
```

That's it.

## Loading GroundTruths 

We have several utility functions to load up the `GroundTruth` objects corresponding to Draco6 (`gt6`), Draco12 (`gt12`), and window (`gtw`).

```
gt6  = fmdt.load_gt6()
gt12 = fmdt.load_gt12()
# gtw  = fmdt.load_gtw() Not implemented yet!
```

---

```
>>> gt6
<fmdt.truth.GroundTruth object at 0x7f590d0939d0>

>>> print(gt6)
GroundTruth with 38 detections, 38 unique videos, and db dir:
        /home/ejovo/Videos/Watec6mm

>>> print(gt12)
GroundTruth with 39 detections, 39 unique videos, and db dir:
        /home/ejovo/Videos/Watec12mm
```

## Testing a configuration of parameters

Specify a set of arguments and then see which `HumanDetection`s are detected.

```
args = fmdt.detect_args(light_min=253, light_max=255, trk_all=True)
success_list = gt6.try_command(args)
```
---

```
>>> success_list
[False, False, True, True, False, True, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False, False, False, False, False, False, False, True, True, False, False]

>>> sum(success_list)
7
```

## Heatmap

Create a heatmap (sort of) of the meteors that are detected for different `[light_min, light_max]` intervals with the `draw_heatmap()` function:

```
gt6.draw_heatmap(lmin_min=240, lmax_max=255, n_intervals=5)
```

# < 0.0.25 (Should still work)

## Loading the Database

Currently there are two ground truth databases accessible. Files of the form 
`Draconids-6mm*` (denoted draco6) and `Draconids-12mm*` (denoted draco12) have their
ground truths stored in the [draco6](https://github.com/ejovo13/fmdt_python_clean/blob/build/human_detections_draco6.csv) and [draco12](https://github.com/ejovo13/fmdt_python_clean/blob/build/human_detections_draco12.csv) csv files. 

You should be able to download these all the database files that you'll need with `fmdt.download_csvs()`

```
fmdt.download_csvs()
```

These two database files contain the ground truth values that will be loaded into python as
`GroundTruth` objects, which are essentially a list of `HumanDetection` paired with helpful
functions. Let's start by creating a `GroundTruth` object corresponding to the draco6 videos.

### draco6

To create a new `GroundTruth`, we have to pass in the name of the database file + a path 
to where those videos are stored on your machine.

```
vid_dir   = "/your/dir/here/"        # Path to draco6 videos
draco6_db = "human_detections_draco6.csv"

gt6 = fmdt.GroundTruth(csv=draco6_db, vid_dir=vid_dir)
```

The operation we are performing is the following:

![gt_diagram](../media/gt_diagram.png)

Once we have loaded in a `GroundTruth` object, we can access its list of `TrackedObjects`
via the `.meteors` field:

```
print(type(gt6.meteors))    # list
print(type(gt6.meteors[0])) # fmdt.truth.HumanDetection
```

To see a complete list of members and functions, consult `help(fmdt.GroundTruth)` or `help(fmdt.HumanDetection)`

### Testing a single command

In this section we test our database by holding the **configuration** of fmdt-detect 
constant and applying this fixed assortment of parameters across all videos to see 
which meteors were able to be detected. 

For example, consider the set of arguments

- `--light_min 150`
- `--light_max 200`
- `--trk-meteor-min 5`

We can encode this in an `fmdt.Args` object in two steps: defining a dictionary of 
detect arguments followd by a call to the `Args` constructor.

```
d_args = {
    "light_min": 150,
    "light_max": 200,
    "trk_meteor_min": 5
}

args = fmdt.Args(detect_args=d_args)
```

We can then go ahead and use the function `GroundTruth.try_command()` in order to 
test which meteors are detected by this set of arguments:

```
success_list = gt6.try_command(args)
```

The function `try_command()` returns a `list[bool]` where a `True` indicates successful
detection of the corresponding meteor. Later editions will feature a more sophisticated
result that provides more information than a binary `True/False`.

In practice some of the `fmdt-detect` commands using this configuration of parameters will fail,
causing the process to hang. To speed up testing of our database, we can optionally
include a `timeout` parameter for our `detect_args`:

```
d_args = {
    "light_min": 250,
    "light_max": 253,
    "timeout": 1          # timeout in seconds for the fmdt-detect subprocess
}

gt6.try_command(fmdt.Args(detect_args=d_args))
```

This set of parameters will detect up to 6 of the ground truth meteors in the draco6 database.