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

In order to actually use `fmdt` you need to have installed the [Fast Meteor Detection Toolbox](https://github.com/alsoc/fmdt)
and have the executables `fmdt-detect`, `fmdt-visu`, and `fmdt-check` on your system `PATH`.

```
import fmdt

fmdt.detect("demo.mp4", trk_out_path="ex1_detect_tracks.txt")
fmdt.split_video_at_meteors("demo.mp4", "ex1_detect_tracks.txt")
```

### Documentation

Comprehensive documentation is hosted at [readthedocs](https://fmdt-python-clean.readthedocs.io/en/latest/)