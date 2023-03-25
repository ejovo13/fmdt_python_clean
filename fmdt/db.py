"""Module dealing with the database stuff"""

import fmdt.config
import fmdt.args
import fmdt.truth
import fmdt.download

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
        elif self == VideoType.WINDOW:
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
    
    def full_path(self) -> str:
        return self.dir() + "/" + self.name
    
    def meteors(self) -> list[fmdt.HumanDetection]:
        return retrieve_meteors(self.name)
    
    def has_meteors(self) -> bool:
        return len(self.meteors()) > 0

    def exists(self) -> bool:
        """Check whether the video path in self.full_path() exists on disk"""
        return os.path.exists(self.full_path())

    def evaluate_args(self, args: fmdt.Args, meteors: list[fmdt.truth.HumanDetection], rerun: bool = False, tmp_gt_file = "tmp_meteors.txt"):
        """Call fmdt-detect and fmdt-check to evaluate how well a given set of arguments detects our ground truth
        
        Parameters
        ----------
        
        args (fmdt.Args): The set of fmdt-detect parameters that we want to evaluate
        meteors (list[fmdt.HumanDetection]): The list of meteors in our ground truth
        rerun (bool): Used to determine if we should rerun fmdt-detect when the trk_out_path file
            already exists
        """
        assert not args.detect_args.trk_out_path is None, "Missing `trk_out_path` from `args: fmdt.Args` required for evaluation"
        # assert not args.detect_args.vid_in_path  is None, "Missing `vid_in_path` required to evaluate an fmdt.Args"
        args.detect_args.vid_in_path = self.full_path()

        if rerun:
            args.detect()

        # Check if the trk_out_path file already exists
        if not os.path.exists(args.detect_args.trk_out_path):
            args.detect()

        # We guarentee that the file exist at this point

        # Let's write the data from meteors to a temp file
        fmdt.truth.save_meteors_file(tmp_gt_file, meteors)

        # Then call fmdt_check

        fmdt.check(args.detect_args.trk_out_path, tmp_gt_file)


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

def load_draco6(filename: str = "videos.db", db_dir = fmdt.download.__DATA_DIR) -> list[Video]:
    """Load draco6 `Video` objects that are stored in the `db_dir`/`filename` .db file"""
    vids = load_in_videos(filename, db_dir)
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

def get_video_diagnostics(vids: list[Video]) -> tuple[int, int]:
    """Print information about the local environment"""
    # d6 = fmdt.load_draco6()/
    on_disc = [v for v in vids if v.exists()]
    has_meteors = [v for v in on_disc if v.has_meteors()]

    n_exist = len(on_disc)
    n_with_meteors = len(has_meteors)

    return n_exist, n_with_meteors

def print_diagnostics(vids: list[Video]):

    n_exist, n_with_meteors = get_video_diagnostics(vids)


    print(f"{n_exist} videos exist on disc out of the {len(vids)} videos in our database")
    print(f"{n_with_meteors} of which have ground truths out of {len([v for v in vids if v.has_meteors()])} ground truths in our database")

def print_diagnostics_d6():
    print("================================================================================")
    print(f"Draconids-6mm*.avi videos configured with dir: {fmdt.config.draco6_dir()}")
    print("================================================================================")
    print_diagnostics(fmdt.load_draco6())
    
def print_diagnostics_d12():
    print("================================================================================")
    print(f"Draconids-12mm*.avi videos configured with dir: {fmdt.config.draco12_dir()}")
    print("================================================================================")
    print_diagnostics(fmdt.load_draco12())

def print_diagnostics_win():
    print("================================================================================")
    print(f"window*.mp4 videos configured with dir: {fmdt.config.window_dir()}")
    print("================================================================================")
    print_diagnostics(fmdt.load_window())

def print_diagnostics_all():
    """Print diagnostic information for the three class of videos in our database, Draco6, Draco12, and window

    We compare the number of videos that are present on disk with the number of videos in our database. 
    
    """
    print("Printing information about the local environment")
    print_diagnostics_d6()
    print()
    print_diagnostics_d12()
    print()
    print_diagnostics_win()
    print()

def info():
    print_diagnostics_all()


