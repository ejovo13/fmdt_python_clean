# Use the Cache

We can cache the output of `fmdt-detect` by passing along the `cache=True` parameter pair
to `fmdt.detect`.

```
import fmdt
res = fmdt.detect(vid_in_path="demo.mp4", cache=True)
```

which produces the following files in `fmdt.cache_dir()`:

```
>>> fmdt.cache_dir()
'/home/ejovo/.cache/fmdt_python'


```