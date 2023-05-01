# 1. Your first meteor

Learning outcome: Learn how to launch `fmdt-detect` using `fmdt`

---

## Prerequisites

In order to follow this tutorial you need to have 

- `fmdt-python` installed (see [installation](../installation.md) if not)
- `fmdt-detect` installed (follow [this link](https://fmdt.readthedocs.io/en/latest/user/installation.html) if not)
- `fmdt-detect` on your system's `PATH` 

## Start

In this tutorial we are going to learn how to detect meteors using the python module `fmdt`. We'll start off by retrieving a sample [video](https://lip6.fr/adrien.cassagne/data/tauh/in/2022_05_31_tauh_34_meteors.mp4), saving it as `demo.mp4`.

Let's open up a new Python script and jot down the following snippet.
``` py title="hello_fmdt.py"
""" A sample program to call `fmdt-detect` using fmdt-python"""
import fmdt

vid    = 'demo.mp4'
trk    = 'trk.txt'
bb     = 'bb.txt'

fmdt.detect(vid_in_path=vid, trk_path=trk, trk_bb_path=bb)
```
The last line executes `fmdt-detect` with the equivalent bash command:
```{bash}
fmdt-detect --vid-in-path demo.mp4 --trk-bb-path bb.txt > trk.txt
```

Open up a terminal and lauch this script (or type in the previous statements in an interactive session)
```{bash}
python3 first_detection.py
```


The function `fmdt.detect` uses the same parameters as the command-line utility `fmdt-detect`,
the only difference being that flags like have their dashes `-` transformed into underscores `_` 
since Python interprets dashes as minus signs. As such, the usual flag `--vid-in-path` is encoded 
as the python argument `vid_in_path`.

For a complete list of parameters, see [API](../reference/api.md).

## Visualizing

We can visualize the tracked meteors with a call to `fmdt.visu`.

```
fmdt.visu(vid_in_path=vid, vid_out_path="demo_v.mp4", trk_path=trk, trk_bb_path=bb)
```

In order to visualize, we need to tell `fmdt` where we stored the tracking list (`trk_path`) as well
as the bounding boxes (`trk_bb_path`)

## Conclusion

Congrats! You've detected your first meteor! 38 of them, if everything went as planned. Go ahead and follow the [next tutorial](./2_Load_Tracked_Objects.md) to find out how to inspect the tracked objects.