### Pip

`fmdt-python` can be installed using `pip`
```
pip install fmdt-python
```
If you are using Windows or MacOS, you may have to replace `pip` by `pip3`.

`fmdt-python` requires a version of Python as recent as 3.10

Once you've installed `fmdt-python`, open up any python instance and try importing the package via the alias `fmdt`:

```
>>> import fmdt
```

If there are no error messages, then the python module `fmdt` was imported successfully. 
To confirm `fmdt-python`'s installation, try executing:

```
>>> help(fmdt)
```

Congrats! You've successfully installed `fmdt-python` and you are ready to move on to the next steps!

### Github

The source code for `fmdt-python` can be obtained by cloning the github repository via https:
```{bash}
git clone https://github.com/ejovo13/fmdt_python_clean.git
```

or via ssh:

```{bash}
git clone git@github.com:ejovo13/fmdt_python_clean.git
```

The benefit of cloning the github repository is having access to example python scripts of using `fmdt-python` to accomplish basic tasks with `fmdt`.

### Next Steps

Now that you have access to the `fmdt` module through python, make sure that you have
the executables `fmdt-detect` and `fmdt-visu` compiled and in your system's path. For instructions 
on compiling this software, we defer to the [main project's documentation](https://fmdt.readthedocs.io/en/latest/).

Once all that is complete, try working through a few [tutorials](tutorials/0_start.md)!