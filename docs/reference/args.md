The `fmdt.args` module provides an alternative interface to the core executables 
`fmdt-detect` and `fmdt-visu`. This module also provides the `Args` class which 
allows us to represent various configurations of parameters.

#### Args

The `Args` class of this module is aliased by `fmdt.Args` and has the following 
fields:

- detect_args:   dict
- visu_args:     dict
- trk_list:      list[TrackedObject] 

We can create a new `Args` instance by creating a dictionary of parameters and 
then passing it to our constructor

```Python
import fmdt

detect_args = {
    "ccl_hyst_lo": 253,
    "ccl_hyst_hi": 254
}

args = fmdt.Args(detect_args=fmdt.DetectArgs(**detect_args))
```

and then call `fmdt-detect`

```Python
res = args.detect()
```