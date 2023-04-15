"""Module dealing with the database stuff"""

from fmdt.exceptions import *
import fmdt.config
import fmdt.args
import fmdt.truth
import fmdt.download
import fmdt.utils
import fmdt.res
import fmdt.api

from copy import (
    deepcopy
)

import pandas as pd
import numpy as np
import sqlite3
from enum import Enum
from termcolor import colored
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
    
    def visu_name(self) -> str:

        beg, ext = fmdt.utils.decompose_video_filename(self.name)

        return beg + "_visu." + ext
    
    def prefix(self) -> str:

        pre, _ = fmdt.utils.decompose_video_filename(self.name)
        return pre

    def suffix(self) -> str:
        _, suffix = fmdt.utils.decompose_video_filename(self.name)
        return suffix
    
    def default_trk_path(self, dir: str = "."):
        return dir + "/" + self.prefix() + "_trk.txt" 

    # def visu
    def detect(self,
        #=================== fmdt-detect parameters ================
        vid_in_start: int | None = None,
        vid_in_stop: int | None = None,
        vid_in_skip: int | None = None,
        vid_in_buff: bool | None = None,
        vid_in_loop: int | None = None,
        vid_in_threads: int | None = None,
        light_min: int | None = None,
        light_max: int | None = None,
        ccl_fra_path: str | None = None,
        ccl_fra_id: bool | None = None,
        mrp_s_min: int | None = None,
        mrp_s_max: int | None = None,
        knn_k: int | None = None,
        knn_d: int | None = None,
        knn_s: int | None = None,
        trk_ext_d: int | None = None,
        trk_ext_o: int | None = None,
        trk_angle: float | None = None,
        trk_star_min: int | None = None,
        trk_meteor_min: int | None = None,
        trk_meteor_max: int | None = None,
        trk_ddev: float | None = None,
        trk_all: bool | None = None,
        trk_bb_path: str | None = "bb.txt",
        trk_mag_path: str | None = None,
        log_path: str | None = None,
        #================== Additional Parameters ====================
        trk_out_path: str | None = "trk.txt",
        log: bool = False,
        timeout: float = None,
        #================== Parameters for logging ===================
        cache: bool = False,
        save_df: bool = False
    ) -> fmdt.res.DetectionResult:
        """Call fmdt-detect with the provided parameters"""

        args = fmdt.args.detect_args(self.full_path(), vid_in_start, vid_in_stop, 
        vid_in_skip, vid_in_buff, vid_in_loop, vid_in_threads, light_min, light_max, 
        ccl_fra_path, ccl_fra_id, mrp_s_min, mrp_s_max, knn_k, knn_d, knn_s, trk_ext_d,
        trk_ext_o, trk_angle, trk_star_min, trk_meteor_min, trk_meteor_max, trk_ddev, 
        trk_all, trk_bb_path, trk_mag_path, log_path, trk_out_path, log, timeout=timeout)

        res = args.detect(cache=cache, save_df=save_df)
        res.video = self

        return res

# import os

    # def check(
    #         self,
    #         **kwargs
    #         # args: fmdt.args.Args = None # Optional
    #     ) -> fmdt.res.CheckingResult:
    #     """Call fmdt-check after a call to fmdt-detect with detection parameters `args`"""

    #     assert self.has_meteors(), f"Cannot call Video.check() because {self.name} has no ground truths in our database"

    #     args = fmdt.detect_args(**kwargs)
        
    #     # I want to see if we have a cached trk list
    #     cached_trk_path = args.detect_args.cache_trk()
    #     cached_met_path = args.detect_args.cache_dir() + "_meteors.txt"


    #     if not os.path.exists(cached_trk_path):
    #         # Then we can directly call fmdt.check
    #         args.detect()
    #         # gen tmp file using meteors
        

    #     pass


    
    def check_args(self, args: fmdt.Args) -> list[bool]: 
        """Check which meteors are detected by this choice of args using our internal python implementation to check if
        a meteor and tracked object are the same

        Returns
        -------

        success_list (list[bool]): a list indicating which meteors were detected by this set of parameters
        """

        args.detect_args.vid_in_path = self.full_path()
        res = args.detect()

        return [m.is_detected_in_list(res.trk_list) for m in self.meteors()] 
    



    def evaluate(self,        
        #=================== fmdt-detect parameters ================
        vid_in_start: int | None = None,
        vid_in_stop: int | None = None,
        vid_in_skip: int | None = None,
        vid_in_buff: bool | None = None,
        vid_in_loop: int | None = None,
        vid_in_threads: int | None = None,
        light_min: int | None = None,
        light_max: int | None = None,
        ccl_fra_path: str | None = None,
        ccl_fra_id: bool | None = None,
        mrp_s_min: int | None = None,
        mrp_s_max: int | None = None,
        knn_k: int | None = None,
        knn_d: int | None = None,
        knn_s: int | None = None,
        trk_ext_d: int | None = None,
        trk_ext_o: int | None = None,
        trk_angle: float | None = None,
        trk_star_min: int | None = None,
        trk_meteor_min: int | None = None,
        trk_meteor_max: int | None = None,
        trk_ddev: float | None = None,
        trk_all: bool | None = None,
        trk_bb_path: str | None = "bb.txt",
        trk_mag_path: str | None = None,
        log_path: str | None = None,
        #================== Additional Parameters ====================
        trk_out_path: str | None = "trk.txt",
        log: bool = False,
        timeout: float = None,
        #================== Check ====================================
        stdout: str = None,
        log_check = False
        ):

        args = fmdt.args.detect_args(self.full_path(), vid_in_start, vid_in_stop, 
        vid_in_skip, vid_in_buff, vid_in_loop, vid_in_threads, light_min, light_max, 
        ccl_fra_path, ccl_fra_id, mrp_s_min, mrp_s_max, knn_k, knn_d, knn_s, trk_ext_d,
        trk_ext_o, trk_angle, trk_star_min, trk_meteor_min, trk_meteor_max, trk_ddev, 
        trk_all, trk_bb_path, trk_mag_path, log_path, trk_out_path, log, timeout=timeout)

        res = args.detect()

        self.evaluate_args(args, res.trk_list, stdout, log=log_check)


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
    
    def has_id(self, rhs_id: int) -> bool:
        """Return true if self has the same id as rhs_id"""
        return self.id() == rhs_id
    
    def full_path(self) -> str:
        return self.dir() + "/" + self.name
    
    def meteors(self) -> list[fmdt.HumanDetection]:
        return retrieve_meteors(self.name)
    
    def has_meteors(self) -> bool:
        return len(self.meteors()) > 0

    def exists(self) -> bool:
        """Check whether the video path in self.full_path() exists on disk"""
        return os.path.exists(self.full_path())
    
    def compute_trk_rate(self, **detect_args):

        c_res = self.detect(**detect_args).check()
        return c_res.trk_rate()
    
    def frame_rate(self) -> float:
        return fmdt.utils.get_avg_frame_rate(self.full_path())
    
    def nb_frames(self) -> int:
        return fmdt.utils.get_video_nb_frames(self.full_path())
    
    def duration(self) -> float:
        return fmdt.utils.get_video_duration(self.full_path())
    
    def get_intervals(self, dur_s: float) -> list[tuple[int, int]]:
        """Compute a list of (start_frame, end_frame) intervals whose length is dur_s"""
        fps = self.frame_rate()
        total_dur = self.duration()
        is_cfr = fmdt.utils.video_has_cfr(self.full_path())

        if not is_cfr:
            print(colored(f"\tWARNING: {self} doesnt have constant frame rate (CFR), computed intervals may not return desired length of {dur_s} s", "red"))

        # let's first get a list of intervals in seconds
        start_points = np.arange(0, total_dur + dur_s, dur_s)

        ints = []
        for i in range(len(start_points) - 1):
            f_start = int(start_points[i] * fps)
            f_end   = int(start_points[i + 1] * fps)
            ints.append((f_start, f_end))

        return ints

    def partition(self, dur_s: float) -> None:
        """Partition a video into smaller segments of size dur_s"""
        ints = self.get_intervals(dur_s)
        fmdt.split_video_at_intervals(self.full_path(), ints, 0, 0, condense=False)

    def evaluate_args(
            self,
            args: fmdt.Args,
            meteors: list[fmdt.truth.HumanDetection],
            rerun: bool = False,
            tmp_gt_file = "tmp_meteors.txt",
            stdout: str = None,
            log = False
        ):
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

        return fmdt.check(args.detect_args.trk_out_path, tmp_gt_file, stdout, log)
    
    def create_clip(self, frame_start: int, frame_end: int):

        valid_bounds = frame_start >= 0 and frame_end <= self.nb_frames()
        assert valid_bounds, f"Cannot create video clip with bounds [{frame_start}, {frame_end}] for {self} ({self.nb_frames()} frames)"

        return VideoClip(self.name, frame_start, frame_end, self.type)

    def create_clips(self, frame_buffer: int = None, condense = True, save_to_disk = False):
        """
        If a video has meteors in our data base, create video clips that capture each meteor
        
        Parameters
        ----------
        frame_buffer: int
            The number of frames to include before and after the appearance of a meteor
        condense: bool
            Whether or not to condense sequences that overlap. For example if two meteors have the frame 
            intervals [0, 10] and [5, 15] and condense == True, then only create one video clip with frames
            [0, 15]
        """

        if not self.has_meteors():
            raise GroundTruthError(f"No ground truths in our database for {self}")

        if frame_buffer is None:
            frame_buffer = int(self.frame_rate() / 2) # If no frame_buffer is given, make sure the clip is at least one second long

        # We need to get the intervals associated with the ground truths
        meteors = self.meteors()
        intervals = [m.interval() for m in meteors]

        if condense:
            intervals = fmdt.utils.condense_start_end(intervals, frame_buffer)

        def get_clip(interval: int):
            """Helper function to compute VideoClip with proper bounds"""
            lower = max(interval[0] - frame_buffer, 0) # don't dip below zero
            upper = min(interval[1] + frame_buffer, self.nb_frames()) # don't go above nb_frames

            return self.create_clip(lower, upper)

        clips = [get_clip(i) for i in intervals]

        if save_to_disk:
            for c in clips:
                c.save()
        
        return clips

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

def has_meteors(vids: list[Video]) -> list[Video]:
    return [v for v in vids if v.has_meteors()]

def load_draco6(
        filename: str = "videos.db",
        db_dir = fmdt.download.__DATA_DIR,
        require_gt = False,
        require_exist = False
    ) -> list[Video]:
    """Load draco6 `Video` objects that are stored in the `db_dir`/`filename` .db file"""

    vids = load_in_videos(filename, db_dir)
    d6 = [v for v in vids if v.is_draco6()]

    if require_gt:
        d6 = [v for v in d6 if v.has_meteors()]

    if require_exist:
        d6 = [v for v in d6 if v.exists()]
    
    return d6

def load_draco12(
        db_filename: str = "videos.db",
        db_dir = fmdt.download.__DATA_DIR,
        require_gt = False,
        require_exist = False
    ) -> list[Video]:

    vids = load_in_videos(db_filename, db_dir)
    d12 = [v for v in vids if v.is_draco12()]

    if require_gt:
        d12 = [v for v in d12 if v.has_meteors()]

    if require_exist:
        d12 = [v for v in d12 if v.exists()]
    
    return d12

def load_window(
        db_filename: str = "videos.db",
        db_dir = fmdt.download.__DATA_DIR,
        require_gt = False,
        require_exist = False
    ) -> list[Video]:

    vids = load_in_videos(db_filename, db_dir)
    win = [v for v in vids if v.is_window()]

    if require_gt:
        win = [v for v in win if v.has_meteors()]

    if require_exist:
        win = [v for v in win if v.exists()]
    
    return win
    
def load_demo(db_filename: str = "videos.db", db_dir = fmdt.download.__DATA_DIR) -> list[Video]:
    """Load video 2022_05_31_tauh_34_meteors.mp4 from our database"""
    vids = load_in_videos(db_filename, db_dir)
    win = [v for v in vids if v.name == "2022_05_31_tauh_34_meteors.mp4"]

    return win[0]


def retrieve_meteors(video_name: str, db_filename: str = "videos.db", dir = fmdt.download.__DATA_DIR) -> list[fmdt.HumanDetection]:

    """Query all of the ground truths in our database"""

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


def get_video_by_id(id: int) -> Video | None:
    videos = load_in_videos()
    v = [v for v in videos if v.has_id(id)]
    if len(v) != 0:
        return v[0]
    else:
        return None 

def get_video_by_ids(ids: list[int]) -> Video | None:
    return [get_video_by_id(id) for id in ids if not get_video_by_id(id) is None] 


#!============================== Modifying our data base ============================
def add_human_detection_to_gt(meteor: fmdt.HumanDetection):
    pass

class VideoClip(Video):

    def __init__(self, name: str, frame_start: int, frame_end: int, type: VideoType = None):
        super().__init__(name, type)
        self.frame_start = frame_start
        self.frame_end = frame_end

    def __str__(self) -> str:
        s = super().__str__()
        return s + f" [{self.frame_start}, {self.frame_end}]"

    def meteors(self):
        p_meteors = super().meteors()

        def pred(hum_det: fmdt.HumanDetection):
            """Check if the meteors start frame is in the clip"""
            return hum_det.start_frame >= self.frame_start and hum_det.start_frame <= self.frame_end
        
        def modify_meteor(m: fmdt.HumanDetection):
            """Modify the interval with respect to this video clip"""
            m_c = deepcopy(m)
            m_c.start_frame = m.start_frame - self.frame_start 
            m_c.end_frame   = m.end_frame   - self.frame_start 

            return m_c

        return [modify_meteor(m) for m in p_meteors if pred(m)]
    
    def parent_path(self) -> str:
        """Return the full path to the folder that these clips will appear in"""
        return self.dir() + "/" + self.prefix() + "/"
    
    def full_path(self) -> str:
        return self.parent_path() + f"f{self.frame_start:04}-{self.frame_end:04}_." + self.suffix()

    def save(self, overwrite = False):
        """
        Write this clip to disk 
        """
        fmdt.utils.mkdir_p(self.parent_path())

        fmdt.utils.extract_video_frames(super().full_path(), self.frame_start, self.frame_end, self.full_path(), overwrite=overwrite)
