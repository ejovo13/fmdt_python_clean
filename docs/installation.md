
!!! warning 

    `fmdt-python` requires a version of Python more recent than `3.10`.

We can access the `fmdt` module using either `pip` or by directly cloning the 
source code repository. We recommend using `pip` as it ensures that `fmdt` will 
be located when we use `import`.

=== "pip"

    `fmdt-python` can be installed using `pip`:

    ```bash
    pip install fmdt-python
    ```
    
    If you are using Windows or MacOS, you may have to replace `pip` by `pip3`.

    Once you've installed `fmdt-python`, open up any python instance and try 
    importing the package via the alias `fmdt`:

    ```python
    >>> import fmdt
    ```

    If there are no error messages, then the python module `fmdt` was imported 
    successfully. To confirm `fmdt-python`'s installation, try executing:

    ```python
    >>> help(fmdt)
    ```

    Congrats! You've successfully installed `fmdt-python` and you are ready to 
    move on to the next steps!

=== "GitHub"

    The source code for `fmdt-python` can be obtained by cloning the github 
    repository.

    === "ssh"

        ```bash
        git clone git@github.com:ejovo13/fmdt_python_clean.git
        ```

    === "https"

        ```bash
        git clone https://github.com/ejovo13/fmdt_python_clean.git
        ```
        
    Cloning the github repository provieds you access to sample python scripts 
    that demonstrate the basic usage of `fmdt-python`

## Next Steps

Now that you have access to the `fmdt` module through python, make sure that you 
have the executables `fmdt-detect` and `fmdt-visu` compiled and in your system's 
path. For instructions on compiling this software, we defer to the 
[main project's documentation](https://fmdt.readthedocs.io/en/latest/).

Once all that is complete, try working through a few 
[tutorials](tutorials/0_start.md)!