# Spliting Videos

This how-to guide showcases various ways to split a video using `fmdt`, using 
[demo.mp4](https://lip6.fr/adrien.cassagne/data/tauh/in/2022_05_31_tauh_34_meteors.mp4)
as our sample video

### Split at arbitrary intervals

We can split a video at any arbitrary interval using the function `fmdt.split_video_at_intervals()`
which has the following signature:
```
def split_video_at_intervals(
        video_filename: str,
        start_end: list[tuple[int, int]],
        nframes_before=3,
        nframes_after=3,
        overwrite=False,
        exact_split: bool = False,
        log: bool = False,
        condense: bool = True
    ) -> None:
```

If we wanted to make two frame-perfect cuts of our video demo.mp4, say with the 
two pairs (5, 20) and (100, 200), we would call:

```
import fmdt

vid = "demo.mp4"
start_end = [(5, 20), (100, 200)]

fmdt.split_video_at_intervals(vid, start_end, 0, 0, True, exact_split=True)
```

When `exact_split` is set to `True` we load in the entire video as a numpy array and 
are able to make frame-perfect cuts. We can quickly run out of RAM when dealing with large videos
so in general we should avoid `exact_split=True` unless the video is only a few seconds long.

### Split video at meteors

We can call `fmdt-detect` and then split a video where meteors are detected.

```
import fmdt

vid    = "demo.mp4"
tracks = "tracks.txt"
bb     = "bb.txt"

fmdt.detect(vid_in_path=vid, trk_out_path=tracks, trk_bb_path=bb).split()
```

Which uses ffmpeg to _approximately_ trim a video around non-overlapping meteor 
detections.

There is also a more verbose alternative which accomplishes the same split:

```
fmdt.detect(vid_in_path=vid, trk_out_path=tracks, trk_bb_path=bb)
fmdt.split_video_at_meteors(vid, tracks, overwrite=True)
```

### Split and visualize

We can produce more informative videos if we apply `fmdt-visu` before our splitting 
operation

```
fmdt.detect(vid_in_path=vid, trk_out_path=tracks, trk_bb_path=bb).visu().split()
```

which will apply the split to the video that contains bounding boxes on objects 
detected by `fmdt-detect`.

### Real Example

In this section we are going to show a real example using `fmdt.split_video_at_intervals`. 

```
intervals = [(785, 790), (1222, 1250), (1426, 1439), (2288, 2323), (2836, 2850),
             (2810, 2888), (2928, 2933), (3426, 3434), (3857, 3862), (4155, 4179), 
             (4262, 4268), (4447, 4460), (5323, 5330), (6790, 6811), (7199, 7207)]
```

These are the intervals of interest. In this specific case the frames aren't precise so
when we call `split_video_at_intervals` we add a -15 frame buffer "before" our intended start plus a 
50 frame buffer after our intended stop frame.

If you have [initialized your config](0_initialization.md) and have all of the correct windows videos then we can go ahead and load up the first one:

```
import fmdt
v = fmdt.load_window()[0]
```

```
#============ Real interactive session ==================#
>>> v 
window_3_sony_0400-0405UTC.mp4

>>> v.full_path()
'/home/ejovo/Videos/Window/window_3_sony_0400-0405UTC.mp4'
```

We then split the video with one line:

```
fmdt.split_video_at_intervals(v.full_path(), intervals, nframes_before=-15, nframes_after=50)
```