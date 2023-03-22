# Your first meteor

In this tutorials we'll learn how to detect meteors using the python module `fmdt`.

In order to follow this tutorial you need to 

- have `fmdt-python` installed (see [installation](../installation.md) if not)
- have `fmdt-detect` installed (follow [this link](https://fmdt.readthedocs.io/en/latest/user/installation.html) if not)
- have `fmdt-detect` on your system's `PATH` 

We'll start off by retrieving a sample [video](https://lip6.fr/adrien.cassagne/data/tauh/in/2022_05_31_tauh_34_meteors.mp4), saving it as `demo.mp4`.

Let's open up a new Python script and jot down
```
"""detect.py - A sample program to call `fmdt-detect` using fmdt-python"""
import fmdt

vid    = 'demo.mp4'
tracks = 'demo_tracks.txt'
bb     = 'demo_bb.txt'

fmdt.detect(vid_in_path=vid, trk_in_path=tracks, trk_bb_path=bb)
```
We execute `fmdt-detect` using the function `fmdt.detect`

Open up a terminal and lauch this script (or type in the previous statements in an interactive session)
```{bash}
python3 demo.py
```


The function `fmdt.detect` uses the same parameters as the command-line utility `fmdt-detect`,
the only difference being that flags like have their dashes `-` transformed into underscores `_` 
because Python interprets dashes as minus signs. As such, the usual flag `--vid-in-path` is encoded 
as the python argument `vid_in_path`.

For a complete list of parameters, see [API](../fmdt/modules/api.md).