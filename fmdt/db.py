"""Module dealing with the database stuff"""

import fmdt.config

import pandas as pd
import sqlite3
from enum import Enum
import os

VIDEOS_FILE = fmdt.config.dir() + "/videos.db"

class VideoType(Enum):
    DRACO6 = 0,
    DRACO12 = 1,
    WINDOW = 2,
    OTHER = 3

    def __str__(self) -> str:
        if self == VideoType.DRACO6:
            return "DRACO6"
        elif self == VideoType.DRACO12:
            return "DRACO12"
        elif self == VideoType.WINDOW:
            return "WINDOW"
        else:
            return "OTHER"
        
    def __repr__(self) -> str:
        return self.__str__()
    
    def dir(self) -> str:

        con = fmdt.config.load_config()
        if self == VideoType.DRACO6:
            return con.d6
        elif self == VideoType.DRACO12:
            return con.d12
        elif self == VideoType.DRACO6:
            return con.win
        else:
            return "./"
        
    
    @staticmethod
    def from_str(str):
        if str == "DRACO6":
            return VideoType.DRACO6 
        elif str == "DRACO12":
            return VideoType.DRACO12
        else:
            return VideoType.WINDOW

# Or maybe recording, night sky watching, stargazing, video of night sky
# type is an enum { draco6, draco12, window}
class Video:

    csv_hdr = "id,name,type\n"
    
    def __init__(self, name: str, type: VideoType = None):
        self.name = name
        self.type = type

    def to_csv(self) -> str:
        return f"{self.name},{self.type}\n"
    
    def __str__(self) -> str:
        return f"{self.name}"
    
    def __repr__(self) -> str:
        return self.__str__()
    
    def is_draco6(self) -> bool:
        return self.type == VideoType.DRACO6
    
    def is_window(self) -> bool:
        return self.type == VideoType.WINDOW
    
    def is_draco12(self) -> bool:
        return self.type == VideoType.DRACO12
    
    def dir(self) -> str:
        return self.type.dir()
        
    # Lookup the id in our default database file.
    def id(self) -> int:

        con = sqlite3.connect(VIDEOS_FILE)

        query = f"""
            select id from video where name = '{self.name}' 
        
        """

        df = pd.read_sql_query(query, con)
        con.close()        

        assert len(df) == 1, f"Something went wrong when looking up {self.name}"
        # Alternatively, we could return -1...
        
        return df.iat[0,0]
    
    def meteors(self) -> list[fmdt.HumanDetection]:
        return retrieve_meteors(self.name)

    @staticmethod
    def from_pd_row(ser: pd.Series):
        out = Video(ser["name"], VideoType.from_str(ser["type"]))
        return out
    


# Take a list of Videos and turn it into a data base.
def videos_to_csv(videos: list[Video], csv_filename: str) -> None:
    # First get the header
    hdr = "id,name,type\n"

    with open(csv_filename, "w") as csv:
        csv.write(hdr)
        
        i = 0
        for v in videos:
            csv.write(f"{i},{v.name},{v.type}\n")
            i += 1

def csv_to_videos(csv_filename: str) -> list[Video]:

    df = pd.read_csv(csv_filename)
    return [Video.from_pd_row(df.iloc[i]) for i in range(len(df))]


def load_in_videos(db_filename: str = "videos.db", dir = fmdt.download.__DATA_DIR) -> list[Video]:
    """Read in the videos stored in 'videos.db' into a list of fmdt.Video"""

    # Download if the database file requested doesnt exist
    if not os.path.exists(dir + "/" + db_filename):
        fmdt.download.download_videos_db(db_filename, log=False, overwrite=False, dir=dir)

    if not dir is None:
        db_filename = dir + "/" + db_filename

    con = sqlite3.connect(db_filename)
    df = pd.read_sql_query("select * from video", con)
    con.close()

    return [fmdt.Video.from_pd_row(df.iloc[i]) for i in range(len(df))]

def load_draco6(db_filename: str = "videos.db", db_dir = fmdt.download.__DATA_DIR) -> list[Video]:
    vids = load_in_videos(db_filename, db_dir)
    return [v for v in vids if v.is_draco6()]

def load_draco12(db_filename: str = "videos.db", db_dir = fmdt.download.__DATA_DIR) -> list[Video]:
    vids = load_in_videos(db_filename, db_dir)
    return [v for v in vids if v.is_draco12()]

def load_window(db_filename: str = "videos.db", db_dir = fmdt.download.__DATA_DIR) -> list[Video]:
    vids = load_in_videos(db_filename, db_dir)
    return [v for v in vids if v.is_window()]

def retrieve_meteors(video_name: str, db_filename: str = "videos.db", dir = fmdt.download.__DATA_DIR) -> list[fmdt.HumanDetection]:

    if not os.path.exists(dir + "/" + db_filename):
        fmdt.download.download_videos_db(db_filename, log=False, overwrite=False, dir=dir)

    if not dir is None:
        db_filename = dir + "/" + db_filename

    query = f"""
        select * from human_detection where video_name = '{video_name}'
    """

    con = sqlite3.connect(db_filename)
    df = pd.read_sql_query(query, con)
    con.close()

    return [fmdt.HumanDetection.from_pd_row(df.iloc[i]) for i in range(len(df))]
    # return df



