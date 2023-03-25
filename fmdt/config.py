"""Module dedicated to the management of config files and stuff"""
import jsonpickle
import os
from appdirs import AppDirs
import fmdt.truth
import fmdt.download
import pandas as pd

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
        h = "           Config           \n"
        s0= "============================\n"
        s = f"Draco6   {self.d6}\nDraco12  {self.d12}\nWindow   {self.win}"
        return h + s0 + s

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

def check_for_config_file() -> bool:
    """Return True is a fmdt_config.json file exists in the user_data_dir"""
    return os.path.exists(full_path)

def load_config() -> Config:
    if check_for_config_file():
        with open(full_path, "r") as file:
            content = file.read()
            return Config.from_json(content)


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

def get_draco6() -> list[str]:
    """Return a list of videos that are found in the Watec6mm directory"""
    con = load_config()

    d6 = [v for v in os.listdir(con.d6) if is_draco6(v)]
    return d6

def get_draco12() -> list[str]:
    """Return a list of videos that are found in the Watec12mm directory"""
    con = load_config()

    d12 = [v for v in os.listdir(con.d12) if is_draco12(v)]
    return d12

def get_window() -> list[str]:
    """Return a list of videos that are in the Window directory and start with "window" """
    con = load_config()

    win = [v for v in os.listdir(con.win) if is_window(v)]
    return win 

def get_local_vids() -> list[str]:

    d6 = get_draco6()
    d12 = get_draco12()
    win = get_window()

    all = []

    all.extend(d6)
    all.extend(d12)
    all.extend(win)

    return all

def load_gt6() -> fmdt.truth.GroundTruth:

    con = load_config()
    db = "gt6.csv"

    fmdt.download.download_draco6_csv(db)
    return fmdt.GroundTruth(db, con.d6)

def load_gt12() -> fmdt.truth.GroundTruth:

    con = load_config()
    db = "gt12.csv"

    fmdt.download.download_draco12_csv(db)
    return fmdt.GroundTruth(db, con.d12)


def main():

    # config = Config("/home/ejovo/Videos/Watec6mm", "/home/ejovo/Videos/Watec12mm", "/home/ejovo/Videos/Window")
    # config.save()

    con = Config.load()
    print(con)

    print(get_draco6())
    print(get_draco12())
    print(get_window())

    print(get_local_vids())

    gt6 = load_gt6()
    gt12 = load_gt12()

    print(gt6)
    print(gt12)

if __name__ == "__main__":
    main()