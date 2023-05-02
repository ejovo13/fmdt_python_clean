# 4. Retrieving Detection Statistics

Learning Goal: Access the statistics stored in `fmdt-detect's` log files.

---

In order to enable the creation of log files, we must specify a directory using 
the `log_path` parameter.

```Python
res = fmdt.detect(vid_in_path="demo.mp4", log_path="log")
```

During detection, `fmdt-detect` will store important statistics for each frame. 
The 5th frame, for example, will have its statistics stored in the file 
`./log/00004.txt`.

We've actually already done the heavy lifting and stored a few relevant 
statistics in our `res`. To extract them to a `pandas.DataFrame`, we call the 
`to_dataframe()` function.

```Python
>>> print(res)
fmdt.res.DetectionResult with args digest: 137719b27ea97a86
objects in trk_list: 38 meteor(s), 0 star(s), 0 noise
     nroi  nassoc  mean_err  std_dev
0      45       0    0.0000   0.0000
1      63      17    0.1669   0.1450
2      67      19    0.2917   0.3966
3      82      24    0.2733   0.2614
4      35      18    0.1626   0.2126
..    ...     ...       ...      ...
251    52      18    0.3126   0.2950
252    59      22    0.9310   1.2554
253    65      17    0.1500   0.1209
254    50      17    0.1123   0.1086
255    66      19    0.3718   0.2947

[256 rows x 4 columns]
```

Where, for each frame:

- `nroi` is the number of regions of interest,
- `nassoc` is the number of associated regions between frame `t - 1` and 
  frame `t`,
- `mean_err` and `std_dev` are motion estimation statistics explained 
  [here](https://fmdt.readthedocs.io/en/latest/user/usage/detect.html#detect-log-path), 
  also between frame `t - 1` and frame `t`.

---

**IMPORTANT:** If the argument `log_path` is not provided then trying to call 
`print(res)` will not show the motion statistics.
