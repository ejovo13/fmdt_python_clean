"""Module dealing with downloading files and stuff"""
import os
import requests
from appdirs import user_data_dir 

# Let's define some functions that will fetch our data base files

__DATA_DIR = user_data_dir("fmdt_python")

__GITHUB_PREFIX = "https://raw.githubusercontent.com/ejovo13/fmdt_python_clean/build"

__DRACO6_CSV_URL  = __GITHUB_PREFIX + "/human_detections_draco6.csv"
__DRACO12_CSV_URL = __GITHUB_PREFIX + "/human_detections_draco12.csv"
__DRACO_CSV_URL = __GITHUB_PREFIX + "/human_detections.csv"

# "name_of_local_file": "url_of_db"
csv_dict = {
    "human_detections_draco6.csv": __DRACO6_CSV_URL,
    "human_detections_draco12.csv": __DRACO12_CSV_URL,
    "human_detections.csv": __DRACO_CSV_URL
}


def download_file(
        filename: str,
        url: str,
        dir: str = "./",
        log = False,
        overwrite = False
    ) -> bool:
    """Download files whose contents are stored in text"""
    if not dir is None:
        filename = dir + "/" + filename

    if os.path.exists(filename) and not overwrite:
        if (log):
            print(f"{filename} already exists, not downloading anything")
        return False
    else:
        if (log):
            print(f"Downloading csv file from {url}")
        r = requests.get(url)
        with open(filename, "w") as csv: 
            csv.write(r.text)

        return True
    
def download_binary_file(
        filename: str,
        url: str,
        dir: str = "./",
        log = False,
        overwrite = False
    ) -> bool:

    if not dir is None:
        filename = dir + "/" + filename

    if os.path.exists(filename) and not overwrite:
        if (log):
            print(f"{filename} already exists, not downloading anything")
        return False
    else:
        if (log):
            print(f"Downloading csv file from {url}")

        r = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024): 
                if chunk: # filter out keep-alive new chunks
                    f.write(chunk)

        return True
    
def download_draco6_csv(filename: str = "human_detections_draco6.csv", dir = __DATA_DIR) -> bool:
    """Return True if downloading"""
    return download_file(filename, __DRACO6_CSV_URL, dir=dir)


def download_draco12_csv(filename: str = "human_detections_draco12.csv", dir = __DATA_DIR) -> bool:
    return download_file(filename, __DRACO12_CSV_URL, dir=dir)

def download_draco_csv(filename: str = "human_detections.csv", dir = __DATA_DIR) -> bool:
    return download_file(filename, __DRACO_CSV_URL, dir=dir)

def download_csvs(log = False, overwrite = False, dir = __DATA_DIR) -> None:
    for (file, url) in csv_dict.items():
        download_file(file, url, dir, log, overwrite)


def download_videos_db(filename = "videos.db", log = False, overwrite = False, dir = __DATA_DIR):
    """Download videos.db"""
    url  = "https://github.com/ejovo13/fmdt_python_clean/raw/build/videos.db"

    download_binary_file(filename, url, dir, log, overwrite)

def download_dbs(overwrite = True):
    download_videos_db(overwrite=overwrite)

def download_demo_mp4(filename: str = "demo.mp4"):

    url = "https://lip6.fr/adrien.cassagne/data/tauh/in/2022_05_31_tauh_34_meteors.mp4"

    if os.path.exists(filename):
        print(f"{filename} already exists, not downloading")
        return False
    else:
        print(f"Downloading mp4 file from {url}...")
        r = requests.get(url)
        with open(filename, "wb") as file:
            for chunk in r.iter_content(chunk_size=255): 
                if chunk: # filter out keep-alive new chunks
                    file.write(chunk)

            print("Done")
