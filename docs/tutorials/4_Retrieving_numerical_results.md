# 4. Retrieving Detection Statistics

Learning Goal: Access the statistics stored in `fmdt-detect's` log files.

---

In order to enable the creation of log files, we must specify a directory using the `log_path` parameter.

```
res = fmdt.detect(vid_in_path="demo.mp4", log_path="log")
```

During detection, `fmdt-detect` will store important statistics for each frame. The 5th frame, for example, will have its statistics stored in the file `./log/00004.txt`.

We've actually already done the heavy lifting and stored a few relevant statistics in our `res`. To extract them to a `pandas.DataFrame`, we call the `to_dataframe()` function.

```
>>> res.to_dataframe()
     nrois  nassocs  mean_errs  std_devs
0       45        0     0.0000    0.0000
1       63       17     0.1663    0.1411
2       67       19     0.2939    0.3953
3       82       24     0.2738    0.2614
4       35       18     0.1601    0.2101
..     ...      ...        ...       ...
251     52       18     0.3344    0.3212
252     59       22     0.9310    1.2554
253     65       17     0.1500    0.1209
254     50       17     0.1251    0.1058
255     66       19     0.3721    0.2947

[256 rows x 4 columns]
```

Where, for each frame:

- `nrois` is the number of regions of interest 
- `nassocs` is the number of associated regions between frame `t - 1` and frame `t`
- `mean_errs` and `std_devs` are motion estimation statistics explained [here](https://fmdt.readthedocs.io/en/latest/user/usage/detect.html#detect-log-path), also between frame `t - 1` and frame `t`

---
**IMPORTANT:** If the argument `log_path` is not provided then trying to call `to_dataframe()` will result in an error as there is no data stored on disk to retrieve.

