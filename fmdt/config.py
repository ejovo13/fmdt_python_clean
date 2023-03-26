"""Module dedicated to the management of config files and stuff"""
import jsonpickle
import os
from appdirs import AppDirs
import fmdt.truth
import fmdt.download
import fmdt.res
import pandas as pd
import shutil

dirs = AppDirs("fmdt_python")
config_file = "config.json"
full_path = dirs.user_data_dir + "/" + config_file

if not os.path.exists(dirs.user_data_dir):
    os.mkdir(dirs.user_data_dir)

class Config:

    def __init__(self, draco6_dir, draco12_dir, windows_dir):
        self.d6 = draco6_dir
        self.d12 = draco12_dir
        self.win = windows_dir

    def __str__(self) -> str:
        s0= "============================\n"
        h = "           Config           \n"
        s0= "============================\n"
        s = f"Draco6   {self.d6}\nDraco12  {self.d12}\nWindow   {self.win}"
        return h + s0 + s
    
    def __repr__(self) -> str:
        return self.__str__()

    def to_json(self) -> str:
        return jsonpickle.encode(self)

    def save(self):

        with open(full_path, "w") as file:
            file.write(self.to_json())
        
        print(f"Saved config to {full_path}")

    @staticmethod
    def from_json(json: str):
        return jsonpickle.decode(json)

    @staticmethod
    def load():
        return load_config()
    
    @staticmethod
    def gt6_csv() -> str:
        return dirs.user_data_dir + "/gt6.csv"
    
    @staticmethod
    def gt12_csv() -> str:
        return dirs.user_data_dir + "/gt12.csv"
    
    # @staticmethod
    # def gt612_csv() -> str:
    #     return dirs.user_data_dir + "/gt12.csv"

def check_for_config_file() -> bool:
    """Return True is a fmdt_config.json file exists in the user_data_dir"""
    return os.path.exists(full_path)

def load_config() -> Config:
    if check_for_config_file():
        with open(full_path, "r") as file:
            content = file.read()
            return Config.from_json(content)
    else: # WE HAVENT SET UP OUR CONFIG!!!

        raise Exception(f"""
            ============================================================
                            Config not yet initialized!
            ============================================================

            In order to initialize your config, call 

            >>> fmdt.init(d6_dir="/your/draco6/dir", d12_dir="your/draco12/dir",
                         win_dir="/your/window/dir")

            You only ever have to do this ONE time! 
            
            For example, for a unix user ejovo we could have:

            >>> fmdt.init("/home/ejovo/Videos/Watec6mm", "/home/ejovo/Vidoes/Watec12mm",
                          "/home/ejovo/Videos/Window")

            output:

                Saved config to /home/ejovo/.local/share/fmdt_python/config.json


        """)


def init(d6_dir: str, d12_dir: str, win_dir: str):
    con = Config(d6_dir, d12_dir, win_dir)
    con.save()

def is_video(filename: str) -> bool:
    return filename[-4:] == ".avi" or filename[-4:] == ".mp4"

def is_draco6(filename: str) -> bool:
    return is_video(filename) and "Draconids-6mm" in filename

def is_draco12(filename: str) -> bool:
    return is_video(filename) and "Draconids-12mm" in filename

def is_window(filename: str) -> bool:
    return is_video(filename) and "window" in filename

def listdir() -> list[str]:
    return os.listdir(dirs.user_data_dir)

def dir() -> str:
    return dirs.user_data_dir

def setdir_draco6(d6_dir: str):
    con = load_config()
    con.d6 = d6_dir
    con.save()

def setdir_draco12(d12_dir: str):
    con = load_config()
    con.d12 = d12_dir
    con.save()

def setdir_window(win_dir: str):
    con = load_config()
    con.win = win_dir
    con.save()

def listdir_draco6() -> list[str]:
    """Return a list of videos that are found in the Watec6mm directory"""
    con = load_config()

    d6 = [v for v in os.listdir(con.d6) if is_draco6(v)]
    return d6

def listdir_draco12() -> list[str]:
    """Return a list of videos that are found in the Watec12mm directory"""
    con = load_config()

    d12 = [v for v in os.listdir(con.d12) if is_draco12(v)]
    return d12

def listdir_window() -> list[str]:
    """Return a list of videos that are in the Window directory and start with "window" """
    con = load_config()

    win = [v for v in os.listdir(con.win) if is_window(v)]
    return win 

def listdir_all() -> list[str]:

    d6 = listdir_draco6()
    d12 = listdir_draco12()
    win = listdir_window()

    all = []

    all.extend(d6)
    all.extend(d12)
    all.extend(win)

    return all

def load_gt6() -> fmdt.truth.GroundTruth:

    con = load_config()
    db = "gt6.csv"

    fmdt.download.download_draco6_csv(db)
    return fmdt.GroundTruth(con.gt6_csv(), con.d6)

def load_gt12() -> fmdt.truth.GroundTruth:

    con = load_config()
    db = "gt12.csv"

    fmdt.download.download_draco12_csv(db)
    return fmdt.GroundTruth(con.gt12_csv(), con.d12)


# if check_for_config_file():
    # con = load_config()
    
def draco6_dir():
    con = load_config()
    return con.d6

def draco12_dir():
    con = load_config()
    return con.d12

def window_dir():
    con = load_config()
    return con.win

def cache_dir():
    return dirs.user_cache_dir

def count_files_in_dir(dir: str) -> int:
    total = 0
    for _, _, files in os.walk(dir):
        total += len(files)

    return total

def size_dir(start_path = '.'):
    """Return the size of the contents of a directory in terms of bytes"""
    total_size = 0
    for dirpath, _, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            # skip if it is symbolic link
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)

    return total_size

def size_cache():
    return size_dir(cache_dir())

def bytes_format(x: int) -> str:
    """print 1024 as 1KB"""

    if abs(x) < 1024:
        return str(x) + "B"
    
    if abs(x) < 1024 * 1024:
        return str(x // 1024) + "KB"

    if abs(x) < 1024 * 1024 * 1024:
        return str(x // (1024 * 1024)) + "MB"
    
    if abs(x) < 1024 * 1024 * 1024 * 1024:
        return str(x // (1024 * 1024 * 1024)) + "GB"
    
    if abs(x) < 1024 * 1024 * 1024 * 1024 * 1024:
        return str(x // (1024 * 1024 * 1024 * 1024)) + "TB"

def clear_cache() -> int:
    """Return the total number of files and folders removed"""

    cd = cache_dir()
    paths = os.listdir(cd)
    size_cache_init = size_cache()

    files_removed = 0
    top_level_dir_removed = 0

    for p in paths:

        full_path = cd + "/" + p

        print(f"Treating file {p}...")

        # shutil.rmtree(full_path)

        if os.path.isfile(full_path):
            os.remove(full_path)
            print("file")
            files_removed += 1
            continue
    
        if os.path.isdir(full_path):
            files_removed += count_files_in_dir(p)
            print("dir")
            top_level_dir_removed += 1
            shutil.rmtree(full_path)
            continue

    print(f"{cache_dir()} cleared: {files_removed} total files and {top_level_dir_removed} top-level directories removed from cache ({bytes_format(size_cache_init - size_cache())} cleared)")

def init_cache() -> None:
    if not os.path.exists(cache_dir()):
        os.mkdir(cache_dir())

def listdir_cache() -> list[str]:
    return os.listdir(cache_dir())

def cache_info():
    print(f"Cache: {cache_dir()} has {bytes_format(size_cache())}")

def main():

    # config = Config("/home/ejovo/Videos/Watec6mm", "/home/ejovo/Videos/Watec12mm", "/home/ejovo/Videos/Window")
    # config.save()

    con = Config.load()
    print(con)

    print(listdir_draco6())
    print(listdir_draco12())
    print(listdir_window())

    print(listdir())

    gt6 = load_gt6()
    gt12 = load_gt12()

    print(gt6)
    print(gt12)

if __name__ == "__main__":
    main()