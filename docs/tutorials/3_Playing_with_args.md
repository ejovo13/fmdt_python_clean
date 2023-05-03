# 3. Playing with Args

Learning Goal: Understand the role of the `Args` class.

---

Before you get started, it might not be a bad idea to check out the 
[fmdt.args](../reference/args.md) module to read up on the `Args` class and it's 
composition. Nevertheless, we are going to begin with a simple example.

In previous tutorials, we've been passing our arguments directly to 
`fmdt.detect` like so:

```Python
fmdt.detect(vid_in_path="demo.mp4", trk_path="trk.txt")
```

## Creating Args

However, we can explicitly create an `Args` object first, using either 
`fmdt.detect_args` or `fmdt.Args.new`.

```Python
args = fmdt.detect_args(vid_in_path="demo.mp4", trk_path="trk.txt")
args = fmdt.Args.new(vid_in_path="demo.mp4", trk_path="trk.txt")
```

These two calls are semantically equivalent; the difference between 
`Args.new()` and `detect_args()` is that `Args.new` includes extra options for 
`fmdt-log-parser` & `fmdt-visu`, such as `vid_out_path`, that a call to 
`fmdt-detect` does not use.

For example, the following code is valid:

```Python
args = fmdt.Args.new(vid_in_path="demo.mp4", vid_out_path="demo_visu.mp4")
```

whereas 

```Python
args = fmdt.detect_args(vid_in_path="demo.mp4", vid_out_path="demo_visu.mp4") #!!! ERROR !!!# 
```

is not.

!!! danger 

    TODO: The latest does not fail (while it should) because of the `**args` 
    parameter in the `fmdt.detect_args` function.

## Calling `fmdt-detect` from an `Args` instance

We can actually use our new `args` to call `fmdt-detect` with the `detect` 
function. Since the parameters are already stored in `args`, we don't have to 
pass anything:

```Python
args.detect()
```

The benefits of this paradigm shift are subtle but important to reflect on. The 
main advantage is that this allows us to take a single core set of parameters 
and apply them across a list of videos.

Consider the case where we have a list of videeo filenames stored in `vid_list`:

```Python
vid_list = ["Draconids-6mm1-04.avi", ..., "Draconids-6mm2-18.avi"]
```

We can then define a set of parameters:

```Python
args = fmdt.detect_args(ccl_hyst_lo=150, ccl_hyst_hi=160)
```

And call `fmdt-detect` on all of the videos with `args`:

```Python
for v in vid_list:
    args.detect_args.vid_in_path = v # Update the --vid-in-path parameter
    args.detect()                    # Call fmdt-detect
```

## Next Steps

Learn how to access the statistics stored in `fmdt-detect's` log files by 
following along [here](./4_Retrieving_numerical_results.md).
