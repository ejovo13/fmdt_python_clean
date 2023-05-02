The module `fmdt.api` provides a set of convenient wrapper functions to the 
executables `fmdt-detect` and `fmdt-visu`.

It is important to know that if `fmdt-detect` or `fmdt-visu` are not found on 
your system's `$PATH` then the functions in this module will immediately fail.

# `detect`

The complete signature for the function `fmdt.api.detect` (aliased as 
`fmdt.detect`) is:

```Python
def detect(
        vid_in_path: str, 
        vid_in_start: int | None = None,
        vid_in_stop: int | None = None,
        vid_in_skip: int | None = None,
        vid_in_buff: bool | None = None,
        vid_in_loop: int | None = None,
        vid_in_threads: int | None = None,
        light_min: int | None = None,
        light_max: int | None = None,
        ccl_fra_path: str | None = None,
        ccl_fra_id: bool | None = None,
        cca_mag: bool | None = None,
        cca_ell: bool | None = None,
        mrp_s_min: int | None = None,
        mrp_s_max: int | None = None,
        knn_k: int | None = None,
        knn_d: int | None = None,
        knn_s: int | None = None,
        trk_ext_d: int | None = None,
        trk_ext_o: int | None = None,
        trk_angle: float | None = None,
        trk_star_min: int | None = None,
        trk_meteor_min: int | None = None,
        trk_meteor_max: int | None = None,
        trk_ddev: float | None = None,
        trk_all: bool | None = None,
        trk_bb_path: str | None = None,
        trk_roi_path: str | None = None,
        trk_path: str | None = None,
        log_path: str | None = None,
        log: bool = False
    ) -> fmdt.args.Args:
```

All of these parameters except for `trk_path` and `log` are extensively 
documented in the main project 
[here](https://fmdt.readthedocs.io/en/latest/user/usage/detect.html). 

`trk_path` is the name of a file where the stdout of `fmdt-detect` will be 
redirected.

For example, the command line call 

```bash
./exe/fmdt-detect --vid-in-path ./2022_05_31_tauh_34_meteors.mp4 --trk-bb-path ./out_detect_bb.txt > ./out_detect_tracks.txt
```

Would get translated as 

```Python
>>> fmdt.detect(vid_in_path="2022_05_31_tauh_34_meteors.mp4", trk_bb_path="out_detect_bb.txt", trk_path = "out_detect_tracks.txt")
```

In practice, I've found that the most important parameters are 

- `vid_in_path`,
- `trk_path`,
- `trk_roi_path`,

as the execution of `fmdt.visu` depends on their inclusion.

# `visu`
