"""Demonstraction to use Args object"""

import fmdt

# An Args object is composed of a (possibly None) dictionary for the detection parameters, a 
# (possibly None) dictionary of visu parameters, and a possible None list of
# `TrackedObject`
# We create a new Args object by passing one or all of these:

d_args = {
    "vid_in_path": "demo.mp4",
    "light_min": 50,
    "light_max": 85,
    "trk_bb_path": "bb.txt",
    "trk_out_path": "out.txt"
}

a = fmdt.Args(detect_args=d_args)
print(a)

# We can then call `fmdt-detect` using a as an interface:

a.detect()

# The function `Args.detect` returns a _new_ `Args` object that contains 
# (if "trk_out_path" set) a list of `TrackedObject` detected by fmdt-detect.
# We can call the same function as above, this time storing the results

a = a.detect()

print(a.tracking_list)

# Object is either a meteor, star, or noise.