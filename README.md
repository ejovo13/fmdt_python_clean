A series of Python scripts to facilitate the processing of [fmdt's](https://github.com/alsoc/fmdt) output

Scripts for video editing rely on [ffmpeg-python's](https://github.com/kkroening/ffmpeg-python) simple Python bindings to ffmpeg. Make sure you install `ffmpeg-python` before trying any of the video editing functionality.

### Installation

```
pip install fmdt-python
```

`fmdt/core.py` should contain the functions that are called directly in scripts.
`fmdt/utils.py` contains utility functions that `fmdt.core` makes use of.

Example to split a video using tracking information already provided by `fmdt-detect`:

```
import fmdt

fmdt.split_video_at_meteors("demo.mp4", "ex1_detect_tracks.txt")
```

#### TODO

- [x] Upload fmdt to pip so that we can download fmdt and call scripts from anywhere
- [x] Add API to call fmdt executables like `fmdt-detect` and `fmdt-visu`
