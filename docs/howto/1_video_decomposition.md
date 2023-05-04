# Splitting Videos

This how-to guide showcases various ways to split a video using `fmdt`, using 
[demo.mp4](https://lip6.fr/adrien.cassagne/data/tauh/in/2022_05_31_tauh_34_meteors.mp4)
as our sample video

## Split at arbitrary intervals

We can split a video at any arbitrary interval using the function 
`fmdt.split_video_at_intervals()` which has the following signature:

```python
def split_video_at_intervals(
        video_filename: str,
        start_end: list[tuple[int, int]],
        nframes_before=3,
        nframes_after=3,
        overwrite=False,
        verbose: bool = False,
        condense: bool = True,
        out_dir = None 
    ) -> None:
```

Let's use `split_video_at_intervals` to make two frame-perfect cuts of `demo.mp4` using the 
intervals `(5, 20)` and `(100, 200)`

```python
import fmdt

vid = "demo.mp4"
start_end = [(5, 20), (100, 200)]

fmdt.split_video_at_intervals(vid, start_end, 0, 0, True)
```

This will create a new folder `demo` with the following structure:

```sh
./demo
├── f005-020.mp4
└── f100-200.mp4
```

## Split video at meteors

We can call `fmdt-detect` and then split a video where meteors are detected.

```python
import fmdt

fmdt.detect(vid_in_path="demo.mp4", trk_path="tracks.txt").split()
```

Which uses `ffmpeg` to approximately (to the nearest millisecond) trim a video around non-overlapping 
meteor detections.

There is also a more verbose alternative which accomplishes the same split:

```python
fmdt.detect(vid_in_path="demo.mp4", trk_path="tracks.txt")
fmdt.split_video_at_meteors("demo.mp4", "tracks.txt", overwrite=True)
```

## Split and Visualize

We can produce more informative videos if we apply `fmdt-visu` before our 
splitting operation:

```python
vid = "demo.mp4"
trk = "tracks.txt"
log = "detect_log"
trk2roi = "trk2roi.txt"

dres = fmdt.detect(vid_in_path=vid, 
                   trk_path=trk,
                   log_path=log, 
                   trk_roi_path=trk2roi)

dres.log_parser().visu().split()
```

## Real Examples

In this section we are going to show a real example using 
`fmdt.split_video_at_intervals`. 

```python
intervals = [(102, 149), (156, 189), (194, 204), (223, 231), (249, 256)]

fmdt.split_video_at_intervals(video_filename="demo.mp4", start_end=intervals, nframes_before=-15, nframes_after=50)
```

These are the intervals of interest. In this specific case the frames aren't 
precise so when we call `split_video_at_intervals` we add a `-15` frame buffer 
"before" our intended start plus a `50` frame buffer after our intended stop 
frame.

!!! danger 

    TODO: This is buggy for the last split, indeed 256 + 50 = 306 frames is out 
    of the full video range (full video is 256 frames). We should managed this 
    better.

---

If you have [initialized your config](0_initialization.md) and have all of the 
correct windows videos then we can go ahead and load up the first one:

```python
import fmdt
v = fmdt.load_window()[0]
```

```python
#============ Real interactive session ==================#
>>> v 
window_3_sony_0400-0405UTC.mp4

>>> v.full_path()
'/home/ejovo/Videos/Window/window_3_sony_0400-0405UTC.mp4'
```

We then split the video with one line:

```python
intervals = [(785, 790), (1222, 1250), (1426, 1439), (2288, 2323), (2836, 2850),
             (2810, 2888), (2928, 2933), (3426, 3434), (3857, 3862), (4155, 4179), 
             (4262, 4268), (4447, 4460), (5323, 5330), (6790, 6811), (7199, 7207)]

fmdt.split_video_at_intervals(v.full_path(), intervals, nframes_before=-15, nframes_after=50)
```