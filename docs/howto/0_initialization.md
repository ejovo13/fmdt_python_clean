# Configure fmdt

This document shows you how to initiliaze your configuration for `fmdt-python`, which only needs
to be done once per human lifetime (or rather, once per computer).

## [Video Database](../explanation/video_database.md)

Our database of videos is hosted on a physical medium (ask us about it) and they are split up into three categories: Draco6 (videos of the form `Draconids-6mm*.avi`), Draco12 (`Draconids-12mm*.avi`), and Window (videos of the form `window*.mp4`). Check out the list of videos in our database [here](../explanation/video_database.md).

## `fmdt.init`

All you need to do is call `fmdt.init` and indicate where we should look for our draco6, draco12, and window videos on your local machine. `fmdt.init` has the signature:

```{python}
init(d6_dir: str, d12_dir: str, win_dir: str) -> None
```

For example, for a unix user named `ejovo` with the following directory tree: 

```
/home/ejovo/Videos/
├── Watec12mm
├── Watec6mm
└── Window
```

we initialize `fmdt` with:

```
fmdt.init("/home/ejovo/Videos/Watec6mm", "/home/ejovo/Videos/Watec12mm", "/home/ejovo/Videos/Window")
```

We could, of course, have all our videos in one directory:

```
/home/ejovo/Videos/
└── Meteors
```

and call

```
vid_dir = "/home/ejovo/Videos/Meteors"
fmdt.init(vid_dir, vid_dir, vid_dir)
```

You should receive a message indicating where your config is being stored.

```
>>> fmdt.init("/home/ejovo/Videos/Watec6mm", "/home/ejovo/Videos/Watec12mm", "/home/ejovo/Videos/Window")
Saved config to /home/ejovo/.local/share/fmdt_python/config.json
```

and we can inspect our config with `fmdt.load_config()`:

```
>>> fmdt.load_config()
           Config           
============================
Draco6   /home/ejovo/Videos/Watec6mm
Draco12  /home/ejovo/Videos/Watec12mm
Window   /home/ejovo/Videos/Window
```

