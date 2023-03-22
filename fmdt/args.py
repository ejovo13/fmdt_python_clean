"""Arguments Class to store shared parameters when calling a chain of .detect(args).visu().split()"""
import fmdt.api
import fmdt.core
import fmdt.utils
import shutil
import subprocess
import pandas as pd
from enum import Enum

    

def filter_dict(d: dict):
    """Filter out None values in a dict, returning a new dict"""
    out = {}

    for (k, v) in d.items():
        if not v is None:
            out[k] = v

    return out

def row_to_dict(row: pd.Series) -> dict:
    """Convert the non Na values of a pd.DataFrame row to a dict"""
    out = {}
    for k in row.keys():
        if not pd.isna(row[k]):
            out[k] = row[k]
    
    return out

class VideoType(Enum):
    DRACO6 = 0,
    DRACO12 = 1,
    WINDOW = 2

    def __str__(self) -> str:
        if self == VideoType.DRACO6:
            return "DRACO6"
        elif self == VideoType.DRACO12:
            return "DRACO12"
        else:
            return "WINDOW"
        
    def __repr__(self) -> str:
        return self.__str__()
    
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


    
class DetectArgs:

    def __init__( 
        self,
        vid_in_path: Video, 
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
        trk_bb_path: str | None = None,
        trk_mag_path: str | None = None,
        log_path: str | None = None,
        trk_out_path: str | None = None,
    ):

        self.vid_in_path = vid_in_path
        self.vid_in_start = vid_in_start
        self.vid_in_stop = vid_in_stop
        self.vid_in_skip = vid_in_skip
        self.vid_in_buff = vid_in_buff
        self.vid_in_loop = vid_in_loop
        self.vid_in_threads = vid_in_threads
        self.light_min = light_min 
        self.light_max = light_max 
        self.ccl_fra_path = ccl_fra_path
        self.ccl_fra_id = ccl_fra_id
        self.mrp_s_min = mrp_s_min
        self.mrp_s_max = mrp_s_max
        self.knn_k = knn_k
        self.knn_d = knn_d
        self.knn_s = knn_s
        self.trk_ext_d = trk_ext_d
        self.trk_ext_o = trk_ext_o
        self.trk_angle = trk_angle
        self.trk_star_min = trk_star_min
        self.trk_meteor_min = trk_meteor_min
        self.trk_meteor_max = trk_meteor_max
        self.trk_ddev = trk_ddev
        self.trk_all = trk_all
        self.trk_bb_path = trk_bb_path
        self.trk_mag_path = trk_mag_path
        self.trk_out_path = trk_out_path
        self.log_path = log_path

    def to_dict(self) -> dict:
        return {
            "vid_in_path": self.vid_in_path, 
            "vid_in_start": self.vid_in_start,
            "vid_in_stop": self.vid_in_stop,
            "vid_in_skip": self.vid_in_skip,
            "vid_in_buff": self.vid_in_buff,
            "vid_in_loop": self.vid_in_loop,
            "vid_in_threads": self.vid_in_threads,
            "light_min": self.light_min,
            "light_max": self.light_max,
            "ccl_fra_path": self.ccl_fra_path,
            "ccl_fra_id": self.ccl_fra_id,
            "mrp_s_min": self.mrp_s_min,
            "mrp_s_max": self.mrp_s_max,
            "knn_k": self.knn_k,
            "knn_d": self.knn_d,
            "knn_s": self.knn_s,
            "trk_ext_d": self.trk_ext_d,
            "trk_ext_o": self.trk_ext_o,
            "trk_angle": self.trk_angle,
            "trk_star_min": self.trk_star_min,
            "trk_meteor_min": self.trk_meteor_min,
            "trk_meteor_max": self.trk_meteor_max,
            "trk_ddev": self.trk_ddev,
            "trk_all": self.trk_all,
            "trk_bb_path": self.trk_bb_path,
            "trk_mag_path": self.trk_mag_path,
            "log_path": self.log_path,
            "trk_out_path": self.trk_out_path 
        }
    
    def to_red_dict(self) -> dict:
        d = self.to_dict()
        out = {}
        for (k, v) in d.items():
            if not v is None:
                out[k] = v
        
        return out


class VisuArgs:



    pass




class Args:
    """Args keeps track of a configuration of parameters for all of fmdt's executables

    Upon a call to `fmdt.detect()`, an Args object is returned that remembers
    the configuration used to execute fmdt-detect. We can subsequently use the
    Args object as an interface to directly calling fmdt-visu, without having to respecify some of the more specific arguments.

    Consider the difference between the two calls:
    ```
    fmdt.detect(vid_in_path = "vid.mp4")
    fmdt.visu(vid_in_path = "vid.mp4", vid_out_path = "vid_visu.mp4")
    ```

    and
    ```
    fmdt.detect(vid_in_path = "vid.mp4").visu()
    ```  
    where storing the configuration for `fmdt-detect` in an Args object allows us to fill
    in the parameters needed by a call to `fmdt-visu`.

    This class is therefore a collection of dictionaries of parameters and interfaces to
    the fmdt.api functions.
    
    """

    def __init__(
        self,
        vid_in_path: str, 
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
        trk_bb_path: str | None = None,
        trk_mag_path: str | None = None,
        log_path: str | None = None,
        trk_out_path: str | None = None,
    ):

        det_args = DetectArgs(vid_in_path=vid_in_path,
                              vid_in_start=vid_in_start,
                              vid_in_stop=vid_in_stop,
                              vid_in_skip=vid_in_skip,
                              vid_in_buff=vid_in_buff,
                              vid_in_loop=vid_in_loop,
                              vid_in_threads=vid_in_threads,
                              light_min =light_min ,
                              light_max =light_max ,
                              ccl_fra_path=ccl_fra_path,
                              ccl_fra_id=ccl_fra_id,
                              mrp_s_min=mrp_s_min,
                              mrp_s_max=mrp_s_max,
                              knn_k=knn_k,
                              knn_d=knn_d,
                              knn_s=knn_s,
                              trk_ext_d=trk_ext_d,
                              trk_ext_o=trk_ext_o,
                              trk_angle=trk_angle,
                              trk_star_min=trk_star_min,
                              trk_meteor_min=trk_meteor_min,
                              trk_meteor_max=trk_meteor_max,
                              trk_ddev=trk_ddev,
                              trk_all=trk_all,
                              trk_bb_path=trk_bb_path,
                              trk_mag_path=trk_mag_path,
                              trk_out_path=trk_out_path,
                              log_path=log_path)
        
        

    # def __init__(
    #         self, 
    #         tracking_list: str | None = None, 
    #         detect_args: dict | None = None,
    #         visu_args: dict | None = None
    #     ):

    #     self.tracking_list = tracking_list
    #     self.detect_args = detect_args
    #     self.visu_args = visu_args

    # We should change this to print out only the arguments that are not none
    # def __str__(self) -> str:
    #     if not self.detect_args:
    #         f"detect_args:"

    def __repr__(self) -> str:

        if not self.detect_args is None:
            d = filter_dict(self.detect_args)

        # s = ""
        # for (k, v) in self.detect_args.items():
            # if not v is None:
                # s += f'"{k}": {v}, ' 
        
        # return "{" + s[:-2] + "}"
        return d.__repr__()
    
    # def to_csv
    
    def detect(self):
        """OOP Interface to calling fmdt.api.detect()"""

        # Make sure the detecting arguments are not none
        if self.detect_args is None:
            self.detect_args = default_detect_args()
        
        # Convert the list of detect args to a single command
        args = fmdt.api.detect(**self.detect_args)

        if not args.detect_args["trk_out_path"] is None:
            args.tracking_list = args.get_tracking_list()

        return args
    
    def does_detect_fail(self, log=False) -> bool:
        """Returns true if the stderr pipe of a call to fmdt-detect is not empty"""

        if self.detect_args["vid_in_path"] is None:
            return True

        detect_cmd = detect_args_to_cmd(self.detect_args)
        if (log):
            print(detect_cmd)
        res = subprocess.run(detect_cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        # print(res.stderr.decode())

        if res.returncode != 0:
            return True
        
        return False
    
    def detect_cmd(self) -> str:
        return handle_detect_args(**self.detect_args)

    def visu(self, **kwargs):
        """OOP Interface to calling fmdt.api.visu()"""

        # Do we have visu arguments?
        assert not self.visu_args is None, "No visu args for this object"

        for k, v in kwargs.items():
            self.visu_args[k] = v

        fmdt.api.visu(**self.visu_args)

        return self
    
    def vid(self) -> str | None:
        """Return the name of the video, if it exists"""
        if not self.detect_args["vid_in_path"] is None:
            return self.detect_args["vid_in_path"]
        elif not self.visu_args["vid_in_path"] is None:
            return self.visu_args["vid_in_path"]
        else:
            return None
        
    def tracks(self) -> str | None:
        """Return the name of the tracks file, if it exists"""
        if not self.detect_args["trk_out_path"] is None:
            return self.detect_args["trk_out_path"]
        elif not self.visu_args["trk_path"] is None:
            return self.visu_args["trk_path"]
        else:
            return None

    def bbs(self) -> str | None:
        """Return the name of the bounding boxes (BBs) file, if it exists"""
        if not self.detect_args["trk_bb_path"] is None:
            return self.detect_args["trk_bb_path"]
        elif not self.visu_args["trk_bb_path"] is None:
            return self.visu_args["trk_bb_path"]
        else:
            return None

    def split(self, nframes_buffer=3, overwrite=False, exact_split=False, log=False):
        # Check to see if we have the tracks saved.
        fmdt.core.split_video_at_meteors(video_filename=self.vid(), 
                                         detect_tracks_in=self.tracks(),
                                         nframes_before=nframes_buffer,
                                         nframes_after=nframes_buffer,
                                         overwrite=overwrite,
                                         exact_split=exact_split,
                                         log=log)

    # Take the detect argument dictionary and write out a comma separated value string
    def detect_csv_header(self) -> str:
        """Return the header line used in a csv file storing multiple argument configurations"""
        header = ""
        for k in self.detect_args.keys():
            if k == "log":
                continue
            header = header + f"{k},"

        return header[:-1] + "\n"

    def detect_to_csv_row(self) -> str:
        """Return the csv representation of a detect_args dict"""
        csv = ""
        for v in self.detect_args.values():
            if v is None:
                csv = csv + ","
            else:
                csv = csv + f"{str(v)},"
        
        # Drop the last comma
        return csv[:-1] + "\n"
    
    def get_tracking_list(self) -> list[fmdt.core.TrackedObject]:
        """Retreive the list of TrackedObject that is stored in the trk_out_path file"""
        assert not self.detect_args["trk_out_path"] is None, "Out track file not stored"

        return fmdt.core.extract_all_information(self.detect_args["trk_out_path"])
    
    def command(self) -> str:
        """Return the command used to execute fmdt-detect with this configuration"""
        return ' '.join(handle_detect_args(**self.detect_args))

    # Write the dictionary of fmdt-detect arguments to a csv file
    # def detect_to_csv(self, csv_filename) -> None:

class FMDTResult:

    def __init__(self, arg_err: list[float] = None, ecarts_type: list[float] = None, rois: list[int] = None, args: Args = None):
        self.arg_err = arg_err
        self.ecarts_type = ecarts_type
        self.rois = rois
        self.args = args

# Need some functions to retrieve the results from a log thing






def list_args_to_csv(lst: list[Args], csv_file: str):

    with open(csv_file, "w") as f:

        f.write(lst[0].detect_csv_header())
        for a in lst:
            f.write(a.detect_to_csv_row())

def csv_to_list_args(csv_file: str) -> list[Args]:

    df = pd.read_csv(csv_file)
    n_rows = len(df)
    
    return [Args.from_row(df.loc[i]) for i in range(n_rows)]

def video_input(filename: str) -> Args:
    a = Args()
    a.detect_args = default_detect_args()
    a.detect_args["vid_in_path"] = filename
    return a

class ArgList:
    """This class allows us to read in the arguments to calls to fmdt-detect from a csv file"""
    pass



def detect_args(
        vid_in_path: str, 
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
        trk_bb_path: str | None = None,
        trk_mag_path: str | None = None,
        log_path: str | None = None,
        trk_out_path: str | None = None,
        log: bool = False
    ) -> tuple[dict, dict]:
    """Convert the parameters used in fmdt.detect into a dictionary"""

    d_args = {
        "vid_in_path": vid_in_path, 
        "vid_in_start": vid_in_start,
        "vid_in_stop": vid_in_stop,
        "vid_in_skip": vid_in_skip,
        "vid_in_buff": vid_in_buff,
        "vid_in_loop": vid_in_loop,
        "vid_in_threads": vid_in_threads,
        "light_min": light_min,
        "light_max": light_max,
        "ccl_fra_path": ccl_fra_path,
        "ccl_fra_id": ccl_fra_id,
        "mrp_s_min": mrp_s_min,
        "mrp_s_max": mrp_s_max,
        "knn_k": knn_k,
        "knn_d": knn_d,
        "knn_s": knn_s,
        "trk_ext_d": trk_ext_d,
        "trk_ext_o": trk_ext_o,
        "trk_angle": trk_angle,
        "trk_star_min": trk_star_min,
        "trk_meteor_min": trk_meteor_min,
        "trk_meteor_max": trk_meteor_max,
        "trk_ddev": trk_ddev,
        "trk_all": trk_all,
        "trk_bb_path": trk_bb_path,
        "trk_mag_path": trk_mag_path,
        "log_path": log_path,
        "trk_out_path": trk_out_path 
    }

    assert not vid_in_path is None, "vid_in_path cannot be None"

    name, ext = fmdt.utils.decompose_video_filename(vid_in_path)
    visu_name = f"{name}_visu.{ext}"

    v_args = {
        "vid_in_path": vid_in_path,
        "vid_in_start": vid_in_start,
        "vid_in_stop": vid_in_stop,
        "vid_in_threads": vid_in_threads,
        "trk_path": trk_out_path,
        "trk_bb_path": trk_bb_path,
        "vid_out_path": visu_name
    }

    return d_args, v_args

def visu_args(
        vid_in_path: str = None,
        vid_in_start: int = None,
        vid_in_stop: int = None,
        vid_in_threads: int = None,
        trk_path: str = None,
        trk_bb_path: str = None,
        trk_id: bool = None,
        trk_nat_num: bool = None,
        trk_only_meteor: bool = None,
        gt_path: str = None,
        vid_out_path: str = None
    ) -> dict:

    return {

        "vid_in_path": vid_in_path,
        "vid_in_start": vid_in_start,
        "vid_in_stop": vid_in_stop,
        "vid_in_threads": vid_in_threads,
        "trk_path": trk_path,
        "trk_bb_path": trk_bb_path,
        "trk_id": trk_id,
        "trk_nat_num": trk_nat_num,
        "trk_only_meteor": trk_only_meteor,
        "gt_path": gt_path,
        "vid_out_path": vid_out_path

    }

def default_detect_args() -> dict:       
    # Hi 
    default_detect = {
        "vid_in_path": None, 
        "vid_in_start": None,
        "vid_in_stop": None,
        "vid_in_skip": None,
        "vid_in_buff": None,
        "vid_in_loop": None,
        "vid_in_threads": None,
        "light_min": None,
        "light_max": None,
        "ccl_fra_path": None,
        "ccl_fra_id": None,
        "mrp_s_min": None,
        "mrp_s_max": None,
        "knn_k": None,
        "knn_d": None,
        "knn_s": None,
        "trk_ext_d": None,
        "trk_ext_o": None,
        "trk_angle": None,
        "trk_star_min": None,
        "trk_meteor_min": None,
        "trk_meteor_max": None,
        "trk_ddev": None,
        "trk_all": None,
        "trk_bb_path": None,
        "trk_mag_path": None,
        "log_path": None,
        "trk_out_path": None
    }

    return default_detect

def handle_detect_args(
        vid_in_path: str, 
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
        trk_bb_path: str | None = None,
        trk_mag_path: str | None = None,
        log_path: str | None = None,
        trk_out_path: str | None = None,
        log: bool = False
    ) -> list[str]:
    """Convert the arguments needed for fmdt-detect into a fmdt-detect command-line call
    
     
    
    
    """



    fmdt_detect_exe = shutil.which("fmdt-detect")
    fmdt_detect_found = not fmdt_detect_exe is None
    assert fmdt_detect_found, "fmdt-detect executable not found"
    args = [fmdt_detect_exe, "--vid-in-path", vid_in_path]

    def arg_str(arg: str | None, flag: str) -> None:
        """Modify args in place if arg is not None"""
        if not arg is None:
            args.extend(["--" + flag, str(arg)])

    def arg_bool(arg: bool | None, flag: str) -> None:
        """Modify args in place if arg is True"""
        if arg:
            args.append("--" + flag)

    # ====== Arguments of the form --flag <arg_value>
    arg_str(vid_in_skip, "vid-in-skip")
    arg_str(vid_in_threads, "vid-in-threads")
    arg_str(light_min, "ccl-hyst-lo")
    arg_str(light_max, "ccl-hyst-hi")
    arg_str(ccl_fra_path, "ccl_fra_path")
    arg_str(mrp_s_min, "mrp-s-min")
    arg_str(mrp_s_max, "mrp-s-max")
    arg_str(knn_k, "knn-k")
    arg_str(knn_d, "knn-d")
    arg_str(knn_s, "knn-s")
    arg_str(trk_ext_d, "trk-ext-d")
    arg_str(trk_ext_o, "trk-ext-o")
    arg_str(trk_star_min, "trk-star-min")
    arg_str(trk_meteor_min, "trk-meteor-min")
    arg_str(trk_meteor_max, "trk-meteor-max")
    arg_str(trk_ddev, "trk-ddev")
    arg_str(trk_mag_path, "trk-mag-path")
    arg_str(log_path, "log-path")
    arg_str(trk_angle, "trk-angle")
    arg_str(trk_star_min, "trk-star-min")
    arg_str(vid_in_start, "vid-in-start")
    arg_str(vid_in_stop, "vid-in-stop")
    arg_str(trk_bb_path, "trk-bb-path")
    arg_str(vid_in_loop, "vid-in-loop")
    arg_str(log_path, "log-path")

    # ======== Arguments of the form --toggle
    arg_bool(vid_in_buff, "vid_in_buff")
    arg_bool(ccl_fra_id, "ccl-fra-id")
    arg_bool(trk_all, "trk-all")

    return args

def handle_visu_args(
        vid_in_path: str = None,
        vid_in_start: int = None,
        vid_in_stop: int = None,
        vid_in_threads: int = None,
        trk_path: str = None,
        trk_bb_path: str = None,
        trk_id: bool = None,
        trk_nat_num: bool = None,
        trk_only_meteor: bool = None,
        gt_path: str = None,
        vid_out_path: str = None
    ) -> list[str]:


    fmdt_visu_exe = shutil.which("fmdt-visu")
    fmdt_visu_found = not fmdt_visu_exe is None
    assert fmdt_visu_found, "fmdt-visu executable not found"


    assert not vid_in_path is None, "No input video specified"
    assert not trk_path is None, "No input track path"
    assert not trk_bb_path is None, "No input bounding boxes file"

    args = [fmdt_visu_exe, "--vid-in-path", vid_in_path, "--trk-bb-path", trk_bb_path, "--trk-path", trk_path] 

    if not vid_out_path is None:
        args.extend(["--vid-out-path", vid_out_path])
    else:
        name, ext = fmdt.utils.decompose_video_filename(vid_in_path)
        new_name = f"{name}_visu.{ext}"
        args.extend(["--vid-out-path", new_name])

    # helper closure to clean up repetitive code
    def add_arg(arg, flag):
        if not arg is None:
            args.extend([flag, str(args)])

    add_arg(vid_in_start, "--vid-in-start")
    add_arg(vid_in_stop, "--vid-in-stop")
    add_arg(vid_in_threads, "--vid-in-threads")
    add_arg(gt_path, "--gt-path")

    if trk_id:
        args.append("--trk-id")

    if trk_nat_num:
        args.append("--trk-nat-num")

    if trk_only_meteor:
        args.append("--trk-only-meteor")

    return args



def detect_args_to_cmd(args: dict) -> list[str]:
    return handle_detect_args(**args)            

    
def main() -> None:
    a = Args()
    # a.detect_args = default_detect_args()
    a.detect_args = detect_args(vid_in_path="demo.mp4")
    print(a.detect_csv_header())
    print(a.detect_to_csv_row())