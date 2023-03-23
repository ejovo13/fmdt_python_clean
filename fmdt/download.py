"""Module dealing with downloading files and stuff"""
import os
import requests

# Let's define some functions that will fetch our data base files

draco6_db_url  = "https://raw.githubusercontent.com/ejovo13/fmdt_python_clean/build/human_detections_draco6.csv"
draco12_db_url = "https://raw.githubusercontent.com/ejovo13/fmdt_python_clean/build/human_detections_draco12.csv"
human_detections = "https://raw.githubusercontent.com/ejovo13/fmdt_python_clean/build/human_detections.csv"

# "name_of_local_file": "url_of_db"
csv_dict = {
    "human_detections_draco6.csv": draco6_db_url,
    "human_detections_draco12.csv": draco12_db_url,
    "human_detections.csv": human_detections
}

def download_file(filename, url, log = False, overwrite = False) -> bool:
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

def download_draco6_csv(filename: str = "human_detections_draco6.csv") -> bool:
    """Return True if downloading"""
    return download_file(filename, draco6_db_url)


def download_draco12_csv(filename: str = "human_detections_draco12.csv") -> bool:
    return download_file(filename, draco12_db_url)

def download_draco_csv(filename: str = "human_detections.csv") -> bool:
    return download_file(filename, human_detections)

def download_csvs(log = False, overwrite = False) -> None:
    for (file, url) in csv_dict.items():
        download_file(file, url, log, overwrite)
        

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
