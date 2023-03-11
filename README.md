
Scripts for video editing rely on [ffmpeg-python's](https://github.com/kkroening/ffmpeg-python) simple Python bindings to ffmpeg. Make sure you install `ffmpeg-python` before trying any of the video editing functionality.

### Introduction

`fmdt` is a Python package used to analyze the performance of the [Fast Meteor Detection Toolbox](https://github.com/alsoc/fmdt)'s executables.

This branch contains the `fmdt`'s documentation and a series of scripts that showcase `fmdt`'s functionality.

### Installation

```
pip install fmdt-python
```

In order to use the functions `fmdt.detect` and `fmdt.visu` (to call `fmdt-detect` and `fmdt-visu`, respectively) you need to have `fmdt-detect` and `fmdt-visu` compiled and locatable via your system's 
`PATH`.

### Example Usage

```
import fmdt

fmdt.detect("demo.mp4", trk_out_path="ex1_detect_tracks.txt")
fmdt.split_video_at_meteors("demo.mp4", "ex1_detect_tracks.txt")
```

### Documentation

Comprehensive documentation is hosted at (readthedocs)[https://fmdt-python-clean.readthedocs.io/en/latest/]