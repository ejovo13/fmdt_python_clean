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
from sys import exit

VIDEOS_FILE = fmdt.config.dir() + "/videos.db"
DEFAULT_DATA_DIR = fmdt.download.get_db_dir()

class VideoType(Enum):
    DRACO6 = 0,
    DRACO12 = 1,
    WINDOW = 2,
    DEMO = 3,
    OTHER = 4

    def __str__(self) -> str:
        if self == VideoType.DRACO6:
            return "DRACO6"
        elif self == VideoType.DRACO12:
            return "DRACO12"
        elif self == VideoType.WINDOW:
            return "WINDOW"
        elif self == VideoType.DEMO:
            return "DEMO"
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
        elif self == VideoType.DEMO:
            return con.win
        elif self == VideoType.OTHER:
            return con.win
        else:
            return "./"
        
    
    @staticmethod
    def from_str(str):
        if str == "DRACO6":
            return VideoType.DRACO6 
        elif str == "DRACO12":
            return VideoType.DRACO12
        elif str == "WINDOW":
            return VideoType.WINDOW
        elif str == "DEMO":
            return VideoType.DEMO
        else:
            return VideoType.OTHER

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

    def detect_best(
            self,
            log = False 
        ) -> fmdt.res.DetectionResult:
        """Use the arguments from our best_detections database file to call a detection. 
        
        If there is no recorded best detection, then use FMDT's default parameters  
        """

        if self.has_best_detection():

            best_args = self.best_args()
            best_args.detect_args.vid_in_path = self.full_path()
            best_args.log = log

            return best_args.detect()

        else:

            fmdt.utils.stderr(f"WARNING: {self} has no records in best_detections table; using default FMDT arguments")
            return self.detect()

    def validate_best(
            self,
            log = False
        ) -> bool:
        """Call detect_best().check() and see if the trk_rate is the same as what is recorded in our database
        

        Return
        ------

        validated (bool): True when the trk_rate of a fresh run with the best args matches the trk_rate of the
            corresponding entry in our database
        """

        if self.has_best_detection():

            best_args, trk_rate, true_pos = self.best_detection()
            d_args_stripped = best_args.detect_args.to_stripped_dict()

            c_res = self.detect(**d_args_stripped).check()

            return trk_rate == c_res.trk_rate() and true_pos == c_res.true_pos()

        else:

            fmdt.utils.stderr(f"WARNING: {self} has no records in best_detections table; Video.validate_best() returning false")
            return False

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
    def id(
            self,
            db_file = "videos.db",
            db_dir = DEFAULT_DATA_DIR
        ) -> int:

        db_filename = fmdt.utils.join(db_dir, db_file)

        con = sqlite3.connect(db_filename)

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
    
    def meteors(
            self,
            db_filename: str = "videos.db",
            db_dir = DEFAULT_DATA_DIR
    ) -> list[fmdt.HumanDetection]:
        
        return retrieve_meteors(self.name, db_filename, db_dir)
    
    def has_meteors(
            self,
            db_filename: str = "videos.db",
            db_dir = DEFAULT_DATA_DIR
    ) -> bool:
        
        return len(self.meteors(db_filename, db_dir)) > 0
    
    def has_best_detection(
            self,
            db_file: str = "videos.db",
            db_dir = DEFAULT_DATA_DIR
        ) -> bool:
        """Check if this Video has a best detection stored in our database"""

        id = self.id(db_file, db_dir)
        return query_best_detection(id, False, db_file, db_dir)

    def best_detection(
            self,
            db_file: str = "videos.db",
            db_dir = DEFAULT_DATA_DIR
        ) -> tuple[fmdt.Args, float, int]:

        id = self.id(db_file, db_dir)

        if self.has_best_detection(db_file, db_dir):
            args, trk_rate, n_true_pos = retrieve_best_detection(id, db_file=db_file, db_dir=db_dir)
            args.detect_args.vid_in_path = self.full_path()
            return args, trk_rate, n_true_pos

        else:
            fmdt.utils.stderr(f"WARNING: {self} has no best detection in {fmdt.utils.join(db_dir, db_file)}, VideoClip.best_detection(); returning None")
            return None

    def best_args(
            self,
            db_file: str = "videos.db",
            db_dir = DEFAULT_DATA_DIR
        ) -> fmdt.Args:

        args, _, _ = self.best_detection(db_file, db_dir)
        return args

    def best_trk_rate(
            self,
            db_file: str = "videos.db",
            db_dir = DEFAULT_DATA_DIR
        ) -> float:

        _, trk_rate, _ = self.best_detection(db_file, db_dir)

        return trk_rate
        

    def best_true_pos(
            self,
            db_file: str = "videos.db",
            db_dir = DEFAULT_DATA_DIR
        ) -> int:

        _, _, n_true_pos = self.best_detection(db_file, db_dir)

        return n_true_pos

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
    
    def create_clip(self, start_frame: int, end_frame: int):

        valid_bounds = start_frame >= 0 and end_frame <= self.nb_frames()
        assert valid_bounds, f"Cannot create video clip with bounds [{start_frame}, {end_frame}] for {self} ({self.nb_frames()} frames)"

        return VideoClip(self.name, start_frame, end_frame, self.type)

    def create_clips(
            self,
            frame_buffer: int = None,
            condense = True,
            save_to_disk = False,
            db_dir = DEFAULT_DATA_DIR):
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

        if not self.has_meteors(db_dir = db_dir):
            raise GroundTruthError(f"No ground truths in our database for {self}")

        if frame_buffer is None:
            frame_buffer = int(self.frame_rate() / 2) # If no frame_buffer is given, make sure the clip is at least one second long

        # We need to get the intervals associated with the ground truths
        meteors = self.meteors(db_dir = db_dir)
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

    def retrieve_clips(
            self,
            db_file = "videos.db",
            db_dir = DEFAULT_DATA_DIR
        ) -> list:
        """Retrieve predefined clips in the table `video_clips` from our videos.db"""

        db_filename = fmdt.utils.join(db_dir, db_file)

        con = sqlite3.connect(db_filename)
        self_clips = pd.read_sql_query(f"SELECT * FROM video_clips WHERE parent_id = {self.id(db_file, db_dir)}",
                                       con = con)

        return [VideoClip.from_pd_row(r) for _, r in self_clips.iterrows()]


    @staticmethod
    def from_pd_row(ser: pd.Series):
        out = Video(ser["name"], VideoType.from_str(ser["type"]))
        return out
    

    @staticmethod
    def from_db_id(
        id: int,
        db_file = "videos.db",
        db_dir = DEFAULT_DATA_DIR
    ):
        
        con = sqlite3.connect(fmdt.utils.join(db_dir, db_file))

        video_pd = pd.read_sql_query(f"SELECT * FROM video WHERE id = {id}", con = con)
        v = Video.from_pd_row(video_pd.iloc[0])

        con.close()

        return v
    
class VideoClip(Video):

    def __init__(self, name: str, start_frame: int, end_frame: int, type: VideoType = None):
        super().__init__(name, type)
        self.start_frame = start_frame
        self.end_frame = end_frame

    def __str__(self) -> str:
        s = super().__str__()
        return s + f" [{self.start_frame}, {self.end_frame}]"

    def __eq__(self, rhs) -> bool:
        return (
            self.name == rhs.name and 
            self.start_frame == rhs.start_frame and
            self.end_frame == rhs.end_frame
        )

    def meteors(
            self,
            db_file = "videos.db",
            db_dir = DEFAULT_DATA_DIR
        ):

        p_meteors = super().meteors(db_file, db_dir)

        def pred(hum_det: fmdt.HumanDetection):
            """Check if the meteors start frame is in the clip"""
            return hum_det.start_frame >= self.start_frame and hum_det.start_frame < self.end_frame
        
        def modify_meteor(m: fmdt.HumanDetection):
            """Modify the interval with respect to this video clip"""
            m_c = deepcopy(m)
            m_c.start_frame = m.start_frame - self.start_frame 
            m_c.end_frame   = m.end_frame   - self.start_frame 

            return m_c

        return [modify_meteor(m) for m in p_meteors if pred(m)]

    def has_best_detection(
            self,
            db_file: str = "videos.db",
            db_dir = DEFAULT_DATA_DIR
        ) -> bool:
        """Check if this Video has a best detection stored in our database"""

        id = self.id(db_file, db_dir)
        return query_best_detection(id, True, db_file, db_dir)

    def best_detection(
            self,
            db_file: str = "videos.db",
            db_dir = DEFAULT_DATA_DIR
        ) -> tuple[fmdt.Args, float, int] | None:
        """
        Get the best detection from our database, retrieved as a (args, trk_rate, n_true_pos) tuple. 

        If no best detection exists, return None.
        
        """

        id = self.id(db_file, db_dir)

        if self.has_best_detection(db_file, db_dir):
            return retrieve_best_detection(id, video_clip=True, db_file=db_file, db_dir=db_dir)
        else:
            fmdt.utils.stderr(f"WARNING: {self} has no best detection in {fmdt.utils.join(db_dir, db_file)}, VideoClip.best_detection(); returning None")
            return None
    
    def parent_path(self) -> str:
        """Return the full path to the folder that these clips will appear in"""
        return self.dir() + "/" + self.prefix() + "/"
    
    def full_path(self) -> str:
        return self.parent_path() + f"f{self.start_frame:04}-{self.end_frame:04}_." + self.suffix()

    def save(self, overwrite = False):
        """
        Write this clip to disk 
        """
        fmdt.utils.mkdir_p(self.parent_path())

        fmdt.utils.extract_video_frames(super().full_path(), self.start_frame, self.end_frame, self.full_path(), overwrite=overwrite)

    def parent(
            self,
            db_file = "videos.db",
            db_dir = DEFAULT_DATA_DIR
        ) -> Video:
        """Retrieve a Video object that this clip was created from"""

        videos = retrieve_videos(db_file, db_dir)
        par_list = [v for v in videos if v.name == self.name]

        if len(par_list) != 1:
            raise DatabaseError(f"Video clip {self} did not find parent in database {fmdt.utils.join(db_dir, db_file)}")

        return par_list[0]


    def parent_id(
            self,
            db_file = "videos.db",
            db_dir = DEFAULT_DATA_DIR
        ) -> int:
        """Retrieve the id of the parent video in our database file"""
        return self.parent(db_file, db_dir).id()

    # @override
    def id(
            self,
            db_file = "videos.db",
            db_dir = DEFAULT_DATA_DIR
        ) -> int:
        """Retrieve the clip id of this clip in our database using (parent_id, start_frame, end_frame) as a key
        
        Return
        ------
        clip_id (int): The id of this clip in our database, if it exists. If the database does not contain
            a clip with the corresponding key, raise DatabaseError
        
        """

        con = sqlite3.connect(fmdt.utils.join(db_dir, db_file))

        try:

            df = pd.read_sql_query(f"""
                                    SELECT clip_id 
                                    FROM video_clips
                                    WHERE parent_id = {self.parent_id()}
                                    AND start_frame = {self.start_frame}
                                    AND end_frame = {self.end_frame} 
                                    """, 
                                    con)
        except Exception as db_err:
            
            print(db_err)
            print(colored("Potential solution: update your database file with fmdt.download_dbs()", "green"))
            con.close()
            exit(1)

        con.close()
        
        if len(df) != 1:
            raise DatabaseError(f"{self} has no matches in database {fmdt.utils.join(db_file, db_dir)}")

        return df.iloc[0,0]


    @staticmethod
    def from_pd_row(
        row: pd.Series,
        db_file = "videos.db",
        db_dir = DEFAULT_DATA_DIR
    ):

        parent_video = Video.from_db_id(row["parent_id"], db_file, db_dir)
        return VideoClip(parent_video.name, row["start_frame"], row["end_frame"], parent_video.type)
    
    
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

def has_meteors(vids: list[Video]) -> list[Video]:
    return [v for v in vids if v.has_meteors()]

def load_draco6(
        db_filename: str = "videos.db",
        db_dir = DEFAULT_DATA_DIR,
        require_gt = False,
        require_exist = False,
        require_best_det = False
    ) -> list[Video]:
    """Load draco6 `Video` objects that are stored in the `db_dir`/`filename` .db file"""

    vids = retrieve_videos(db_filename, db_dir, require_gt, require_exist, require_best_det)
    return [v for v in vids if v.is_draco6()]
    
def load_draco12(
        db_filename: str = "videos.db",
        db_dir = DEFAULT_DATA_DIR,
        require_gt = False,
        require_exist = False,
        require_best_det = False
    ) -> list[Video]:

    vids = retrieve_videos(db_filename, db_dir, require_gt, require_exist, require_best_det)
    return [v for v in vids if v.is_draco12()]


def load_window(
        db_filename: str = "videos.db",
        db_dir = DEFAULT_DATA_DIR,
        require_gt = False,
        require_exist = False,
        require_best_det = False
    ) -> list[Video]:

    vids = retrieve_videos(db_filename, db_dir, require_gt, require_exist, require_best_det)
    return [v for v in vids if v.is_window()]

def load_window_clips(
        db_file = "videos.db",
        db_dir = DEFAULT_DATA_DIR,
        require_exist = False,
        require_best_det = False
    ) -> list[VideoClip]:
    """Load all of the clips associated with all of our windows objects"""
    return retrieve_video_clips(db_file, db_dir, require_exist, require_best_det)

    
def load_demo(db_filename: str = "videos.db", db_dir = DEFAULT_DATA_DIR) -> list[Video]:
    """Load video 2022_05_31_tauh_34_meteors.mp4 from our database"""
    vids = retrieve_videos(db_filename, db_dir)
    win = [v for v in vids if v.name == "2022_05_31_tauh_34_meteors.mp4"]

    return win[0]


def load_all(
        db_filename = "videos.db",
        db_dir = DEFAULT_DATA_DIR,
        require_gt = True,
        require_exist = True,
        require_best_det = False
    ) -> list[Video]:
    """Load all Draco6, Draco12, and window_clips
    
    The default behavior is to load all the videos that have at least one ground truth and exist on disk. We can also 
    require that a video has a best detection with the require_best_det parameter

    Parameters
    ----------
    require_gt (bool): When True, all returned videos have a ground truth in our database
        default: True
    require_exist (bool): When True, all returned videos exist on disk
        default: True 
    require_best_det (bool): When True, all returned videos have a recorded best detection in the best_detections table
        of our database.
        default: False

    """

    draco6  = load_draco6 (db_filename, db_dir, require_gt, require_exist, require_best_det)
    draco12 = load_draco12(db_filename, db_dir, require_gt, require_exist, require_best_det)
    windows = load_window_clips(db_filename, db_dir, require_exist, require_best_det)

    return draco6 + draco12 + windows

def retrieve_videos(
        db_file: str = "videos.db",
        db_dir = DEFAULT_DATA_DIR,
        require_gt = False,
        require_exist = False,
        require_best_det = False
    ) -> list[Video]:

    """Read in the videos stored in 'videos.db' into a list of fmdt.Video"""
    db_path = fmdt.utils.join(db_dir, db_file)

    # Download if the database file requested doesnt exist
    if not os.path.exists(db_path):
        fmdt.download.download_videos_db(db_file, log=False, overwrite=False, dir=db_dir)

    con = sqlite3.connect(db_path)
    df = pd.read_sql_query("select * from video", con)
    con.close()

    vids = [fmdt.Video.from_pd_row(df.iloc[i]) for i in range(len(df))]

    if require_gt:
        vids = [v for v in vids if v.has_meteors(db_file, db_dir)]
    
    if require_exist:
        vids = [v for v in vids if v.exists()]

    if require_best_det:
        vids = [v for v in vids if v.has_best_detection(db_file, db_dir)]

    return vids

def retrieve_video_clips(
        db_file: str = "videos.db",
        db_dir = DEFAULT_DATA_DIR,
        require_exist = False,
        require_best_det = False
    ) -> list[Video]:

    db_path = fmdt.utils.join(db_dir, db_file)
    con = sqlite3.connect(db_path)

    df: pd.DataFrame = pd.read_sql_query("select * from video_clips", con = con)
    clips = [VideoClip.from_pd_row(row, db_file, db_dir) for _, row in df.iterrows()]

    con.close()

    if require_exist:
        clips = [c for c in clips if c.exists()]

    if require_best_det:
        clips = [c for c in clips if c.has_best_detection()]

    return clips


def retrieve_meteors(
        video_name: str,
        db_filename: str = "videos.db",
        db_dir = DEFAULT_DATA_DIR
    ) -> list[fmdt.HumanDetection]:

    """Query all of the ground truths in our database"""
    db_path = fmdt.utils.join(db_dir, db_filename)

    if not os.path.exists(db_path):
        fmdt.download.download_videos_db(db_filename, log=False, overwrite=False, dir=db_dir)

    query = f"""
        select * from human_detections where video_name = '{video_name}'
    """

    con = sqlite3.connect(db_path)
    df = pd.read_sql_query(query, con)
    con.close()

    return [fmdt.HumanDetection.from_pd_row(df.iloc[i]) for i in range(len(df))]

def query_best_detection(
        id: int,
        video_clip: bool = False,
        db_file: str = "videos.db",
        db_dir = DEFAULT_DATA_DIR
    ) -> bool:

    """Test if there is a best detection associated with the provided id"""

    db_full_path = fmdt.utils.join(db_dir, db_file)
    con = sqlite3.connect(db_full_path)

    if video_clip:

        df = pd.read_sql_query(f"""
            SELECT * FROM best_detections
            WHERE id_video_clip = {id};
            """, con)
    
    else:

        df = pd.read_sql_query(f"""
            SELECT * FROM best_detections
            WHERE id_video = {id};
            """, con)

    return len(df) == 1


def retrieve_best_detection_df(
        id: int,
        video_clip: bool = False,
        db_file: str = "videos.db",
        db_dir = DEFAULT_DATA_DIR
    ) -> pd.DataFrame:

    db_filename = fmdt.utils.join(db_dir, db_file)

    con = sqlite3.connect(db_filename)

    _ID_ARGS_COL = 2

    if video_clip:
        df = pd.read_sql_query(f"""
            SELECT * FROM best_detections 
            INNER JOIN detect_args
            ON best_detections.id_args = detect_args.id_args
            WHERE id_video_clip = {id};
        """, con)
        
        df = df.drop(df.columns[_ID_ARGS_COL], axis=1)

    else:
        df = pd.read_sql_query(f"""
            SELECT * FROM best_detections 
            INNER JOIN detect_args
            ON best_detections.id_args = detect_args.id_args
            WHERE id_video = {id};
        """, con)
        
        df = df.drop(df.columns[_ID_ARGS_COL], axis=1)

    con.close()
    # Now we want to convert this df into an Args object.
    if len(df) != 1:

        if video_clip:
            raise DatabaseError(f"Error accessing best args for VideoClip by id {id} from {db_filename}")
        else:
            raise DatabaseError(f"Error accessing best args for Video by id {id} from {db_filename}")
    

    return df

def retrieve_best_arg(
        id: int,
        video_clip: bool = False,
        db_file: str = "videos.db",
        db_dir = DEFAULT_DATA_DIR
    ) -> fmdt.Args:
    """
    Retrieve the Args object that is associated with the passed Video or VideoClip id
    
    Parameters
    ----------
    id (int): unique identifier of the Video or VideoClip that we would like to retrieve.
        when video_clip is True, search for a match in the id_video_clip column of our
        best_detection table
    video_clip (bool): Informs this function if we want to retrieve the best args for a VideoClip (True) or 
        for a Video (false)

    Examples
    --------
    >>> args = fmdt.retrieve_best_args(1, video_clip=False) 

    Returns the best Args associated with the *Video* whose id is 1 (Draconids-6mm1.05-0750-164200.avi)

    >>> args = fmdt.retrieve_best_args(4, video_clip=True)

    Returns the vest Args associated with the **VideoClip** whose id is 4  (window_3_sony_0400-0405UTC.mp4 [2823, 2862])

    """
    df = retrieve_best_detection_df(id, video_clip, db_file, db_dir)

    dict = df.to_dict("records")[0]
    return fmdt.detect_args(**dict)

def retrieve_best_detection(
        id: int,
        video_clip: bool = False,
        db_file: str = "videos.db",
        db_dir = DEFAULT_DATA_DIR
    ) -> tuple[fmdt.Args, float, int]:
    """
    Retrieve the best detection result (args, trk_rate, true_pos) associated with a Video or VideoClip id
    
    Parameters
    ----------
    id (int): unique identifier of the Video or VideoClip that we would like to retrieve.
        when video_clip is True, search for a match in the id_video_clip column of our
        best_detection table
    video_clip (bool): Informs this function if we want to retrieve the best args for a VideoClip (True) or 
        for a Video (false)

    Return
    ------

    best_detection (tuple): A tuple of the form (args, trk_rate, true_pos)

    """
    df = retrieve_best_detection_df(id, video_clip, db_file, db_dir)

    dict = df.to_dict("records")[0]
    args = fmdt.detect_args(**dict)
    trk_rate = df["trk_rate"].iloc[0]
    n_true_pos = df["true_pos"].iloc[0]

    return args, trk_rate, n_true_pos
    
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

def get_video(selector: str | int) -> Video | None:
    if isinstance(selector, str):
        return get_video_by_name(selector)
    elif isinstance(selector, int):
        return get_video_by_id(selector)
    else:
        raise TypeError(f"get_video can only access videos with an `int` or `str`. Passed object type: {type(selector)}")

def get_video_by_id(id: int) -> Video | None:
    videos = retrieve_videos()
    v = [v for v in videos if v.has_id(id)]
    if len(v) != 0:
        return v[0]
    else:
        return None 



def get_video_by_name(name: str) -> Video | None:
    videos = retrieve_videos()
    v = [v for v in videos if v.name == name]
    if len(v) != 0:
        return v[0]
    else:
        return None

def get_video_by_ids(ids: list[int]) -> Video | None:
    return [get_video_by_id(id) for id in ids if not get_video_by_id(id) is None] 


#!============================== Modifying our data base ============================
def add_human_detection_to_gt(meteor: fmdt.HumanDetection):
    pass


import json
# ==================== Functions dealing with Json output =================== #

def best_draco6(
        parameter_subset: list[str] = ["light_min", "light_max", "kdd_n"],
        db_file = "videos.db",
        db_dir = DEFAULT_DATA_DIR
) -> str:

    # get the draco 6 videos along with their arguments
    # db_filename = fmdt.utils.join(db_dir, db_file)

    # con = sqlite3.connect(db_filename)
    
    # df = pd.read_sql_query(f"""
    #     SELECT * FROM best_detections as bd
    #     INNER JOIN video as v
    #     ON bd.id_video = v.id
    #     INNER JOIN detect_args as da
    #     ON bd.id_args = da.id_args
    #     WHERE v.type = 'DRACO6'
    #     """,
    #     con)

    # print(df)

    # con.close()

    d6 = load_draco6(require_gt = True, require_exist = True, require_best_det = True)

    best_dets = [(d.name, d.best_detection()) for d in d6]







    



# ======================= Load Relational Database tables as pd.DataFrames ==================== #

def retrieve_table(
    table_name: str,
    db_file = "videos.db",
    db_dir  = DEFAULT_DATA_DIR
) -> pd.DataFrame:

    db_full_path = fmdt.utils.join(db_dir, db_file)

    con = sqlite3.connect(db_full_path)

    sql = f"""select * from {table_name}"""
    df = pd.read_sql_query(sql, con)

    con.close()

    return df

def retrieve_table_video(
    db_file = "videos.db",
    db_dir  = DEFAULT_DATA_DIR
) -> pd.DataFrame:
    return retrieve_table("video", db_file, db_dir)

def retrieve_table_video_clips(
    db_file = "videos.db",
    db_dir  = DEFAULT_DATA_DIR
) -> pd.DataFrame:
    return retrieve_table("video_clips", db_file, db_dir)

def retrieve_table_best_detections(
    db_file = "videos.db",
    db_dir  = DEFAULT_DATA_DIR
) -> pd.DataFrame:
    return retrieve_table("best_detections", db_file, db_dir)

def retrieve_table_human_detections(
    db_file = "videos.db",
    db_dir  = DEFAULT_DATA_DIR
) -> pd.DataFrame:
    return retrieve_table("human_detections", db_file, db_dir)

def retrieve_table_detect_args(
    db_file = "videos.db",
    db_dir  = DEFAULT_DATA_DIR
) -> pd.DataFrame:
    return retrieve_table("detect_args", db_file, db_dir)