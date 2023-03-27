# Cache DetectionResults 

We can cache the output of `fmdt-detect` by passing along the `cache=True` kwarg pair
to `fmdt.detect`.

### trk_list

By default, only the list of tracked objects will be cached.

```
import fmdt
res = fmdt.detect(vid_in_path="demo.mp4", cache=True)
```

which produces the following file in `fmdt.cache_dir()`:

```
>>> res.cache_trk()     # Return the full path to the cached file
'/home/ejovo/.cache/fmdt_python/6dac48d907627d1f_trk.txt`

>>> fmdt.cache_dir()
'/home/ejovo/.cache/fmdt_python'
```

### log_path

We can additionally cache the movement estimation statistics (specified with `--log-path`) by passing the 
kwarg pair `save_df=True`

```
res = fmdt.detect(vid_in_path="demo.mp4", cache=True, save_df=True)
```

We can print to the console how large our cache directory is with `fmdt.cache_info()`:

```
>>> fmdt.cache_info()
Cache: /home/ejovo/.cache/fmdt_python has 4KB
```


