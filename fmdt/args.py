"""Arguments Class to store shared parameters when calling a chain of .detect(args).visu().split()"""
import fmdt.api
import fmdt.core
import fmdt.utils
import shutil
import subprocess
import pandas as pd
from enum import Enum
import pickle
import hashlib
import copy
import os

# Hardcoded default detect values for FMDT version v1.0.0-109-g03a83f42
# These are used to convert between args in our database and args in python.
# However, they are NOT used as the default arguments to our .detect() API
# since the authors of FMDT should be able to change the default values of their
# own program and the api should allow that.
_DEFAULT_DETECT_ARGS = {
    "vid_in_start": 0,
    "vid_in_stop": 0,
    "vid_in_skip": 0,
    "vid_in_buff": False,
    "vid_in_loop": 1,
    "vid_in_threads": 0,
    "ccl_hyst_lo": 55,
    "ccl_hyst_hi": 80,
    "ccl_fra_path": None,
    "ccl_fra_id": False,
    "cca_mag": False,
    "cca_ell": False,
    "mrp_s_min": 3,
    "mrp_s_max": 1000,
    "knn_k": 3,
    "knn_d": 10,
    "knn_s": 0.125,
    "trk_ext_d": 10,
    "trk_ext_o": 3,
    "trk_angle": 20.0,
    "trk_star_min": 15,
    "trk_meteor_min": 3,
    "trk_meteor_max": 100,
    "trk_ddev": 4.0,
    "trk_all": False,
    "trk_roi_path": None,
    "log_path": None
}

# List of keyword arguments that are unique to visu
_VISU_UNIQUE_ARGS = ['trk_id', 'trk_nat_num', 'trk_only_meteor', 'gt_path', 'vid_out_path']
_LOG_PARSER_UNIQUE_ARGS = []

# Configuration to find fmdt-detect if it doesn't exist on the path
_EXECUTABLE_PATH = None

def set_exec_path(path: str):
    global _EXECUTABLE_PATH
    _EXECUTABLE_PATH = path

def get_exec_path() -> str:
    return _EXECUTABLE_PATH


class AbstractExecutableArgs:
    """Abstract Base Class for args of a specific FMDT executable
    
    Any implementer must conform to the following requirements:

    - has a .api_callable() function that returns the corresponding fmdt.api function.
        For example, VisuArgs.api_callable() returns fmdt.api.visu
    - has a .argument_handler() function that returns the corresponding argument handler.
        For example, VisuArgs.argument_handler() returns fmdt.args.handle_visu_args
    - has a .clutter_list() -> list[str] function
    - [OPTIONAL] has a .video_path() function returning the full path to the most 'relevant' video
    
    """

    
    def api_callable(self):
        """Return the function in fmdt.api that corresponds to this executable"""
        raise AbstractExecutableArgs(f"api_callable() not implemented in child {type(self)}")

    def argument_handler(self):
        """Return the function in fmdt.args that handles this executables arguments"""
        raise AbstractExecutableArgs(f"argument_handler() not implemented in child {type(self)}")

    def video_path(self):
        """Return the full path to the most relevant video for this executable

        For example, VisuArgs should return the name of the OUTPUT video that has been visualized 
        """
        raise AbstractExecutableArgs(f"video_path() not implemented in child {type(self)}")
    
    def clutter_list(self):
        """Return a list of parameters whose files may clutter a users workspace"""
        raise AbstractExecutableArgs(f"clutter_list() not implemented in child {type(self)}")
    
    def to_dict(self, subset: list[str] = None):
        """Convert this AbstractExecutableArgs into a dictionary of FMDT arguments
        
        Parameters
        ----------

        subset (list[str]): a subset of key values to retain.

        Examples
        --------

        >>> d = fmdt.DetectArgs(vid_in_path='demo.mp4', ccl_hyst_lo=150, ccl_hyst_hi=160)
        >>> d.to_dict(subset=['vid_in_path', 'ccl_hyst_lo', 'ccl_hyst_hi'])

        ```
        {'vid_in_path': 'demo.mp4', 'ccl_hyst_lo': 150, 'ccl_hyst_hi': 160}
        ```

        >>> d.to_dict()

        ```
        {'vid_in_path': 'demo.mp4',
         'vid_in_start': None,
         'vid_in_stop': None,
         'vid_in_skip': None,
         'vid_in_buff': None,
         'vid_in_loop': None,
         'vid_in_threads': None,
         'ccl_hyst_lo': 150,
         'ccl_hyst_hi': 160,
         'ccl_fra_path': None,
         'ccl_fra_id': None,
         'cca_mag': None,
         'cca_ell': None,
         'mrp_s_min': None,
         'mrp_s_max': None,
         'knn_k': None,
         'knn_d': None,
         'knn_s': None,
         'trk_ext_d': None,
         'trk_ext_o': None,
         'trk_angle': None,
         'trk_star_min': None,
         'trk_meteor_min': None,
         'trk_meteor_max': None,
         'trk_ddev': None,
         'trk_all': None,
         'trk_roi_path': None,
         'log_path': None,
         'trk_path': None}
        ```
        """
        d = vars(self)

        if subset is None:
            return d
        
        dsub = {}
        for k in subset:
            dsub[k] = d[k]
    
        return dsub

    def to_stripped_dict(self, subset: list[str] = None) -> dict:
        """Return a stripped dictionary that drops all parameters pertaining to paths"""
        d = self.to_dict()

        stripped_dict = {}

        for k in d.keys():
            if 'path' not in k:
                stripped_dict[k] = d[k]

        return stripped_dict 

    def to_reduced_dict(self, subset: list[str] = None) -> dict:
        """Return a new dict where all None values have been filtered out"""
        d = self.to_dict(subset)
        out = {}
        for (k, v) in d.items():
            if not v is None:
                out[k] = v
        
        return out
    
    def clutter(self):

        clut_list = self.clutter_list()
        clut = []
        d = self.to_reduced_dict()

        for k in clut_list:
            if k in d:
                clut.append(d[k])
        
        return clut    
    
    def to_bytes(self) -> bytes:
        """Convert to bytes, removing influence of all path variables"""
        return pickle.dumps(self.to_reduced_dict())
    
    def digest(self) -> str:
        return hashlib.md5(self.to_bytes()).hexdigest()

    def __hash__(self) -> int:
        return int(self.digest(), 16)

    def gen_unique_dir(self) -> str:
        return self.digest()[0:16] 
    
    def gen_unique_file(self, prefix="", suffix=".txt") -> str:
        h = self.digest()
        return prefix + h[0:16] + suffix

    def cache_dir(self) -> str:
        return fmdt.cache_dir() + "/" + self.gen_unique_dir()

    def argv(self) -> list[str]:
        """Return a list of arguments that will be used to execute fmdt-detect"""
        return self.argument_handler()(**self.to_dict())

    def cmd(self) -> str:
        return ' '.join(self.argv())
    
    def exec(self, verbose: bool = False):
        
        fmdt_api = self.api_callable()

        return fmdt_api(**self.to_dict(), verbose=verbose)
    
class DetectArgs(AbstractExecutableArgs):

    def __init__( 
            self,
            vid_in_path: str, 
            vid_in_start: int | None = None,
            vid_in_stop: int | None = None,
            vid_in_skip: int | None = None,
            vid_in_buff: bool | None = None,
            vid_in_loop: int | None = None,
            vid_in_threads: int | None = None,
            ccl_hyst_lo: int | None = None,
            ccl_hyst_hi: int | None = None,
            ccl_fra_path: str | None = None,
            ccl_fra_id: bool | None = None,
            cca_mag: bool | None = None,
            cca_ell: bool | None = None,
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
            trk_roi_path: str | None = None,
            log_path: str | None = None,
            trk_path: str | None = None,
        ):

        self.vid_in_path = vid_in_path
        self.vid_in_start = vid_in_start
        self.vid_in_stop = vid_in_stop
        self.vid_in_skip = vid_in_skip
        self.vid_in_buff = vid_in_buff
        self.vid_in_loop = vid_in_loop
        self.vid_in_threads = vid_in_threads
        self.ccl_hyst_lo = ccl_hyst_lo
        self.ccl_hyst_hi = ccl_hyst_hi
        self.ccl_fra_path = ccl_fra_path
        self.ccl_fra_id = ccl_fra_id
        self.cca_mag = cca_mag
        self.cca_ell = cca_ell
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
        self.trk_roi_path = trk_roi_path
        self.log_path = log_path
        self.trk_path = trk_path
        
    # ========================= ABC overrides =================================
    def api_callable(self):
        return fmdt.api.detect
    
    def argument_handler(self):
        return handle_detect_args

    def video_path(self):
        return self.vid_in_path

    def clutter_list(self):
        return ["trk_path", "ccl_fra_path", "trk_roi_path"]

    def to_default_stripped_dict(self) -> dict:
        """Produce a stripped dict where all the none values are set to their default""" 

        d = self.to_stripped_dict()

        for k, v in d.items():
            if v is None:
                d[k] = _DEFAULT_DETECT_ARGS[k]

        return d

    def to_sql_insert(
            self,
            id: int,
            table_name: str = "detect_args"
        ) -> str:
        """Create the SQL insertion query that adds this detect args to a table named `table_name`"""

        dict_values = self.to_default_stripped_dict().values()
        n_values = len(dict_values)

        sql = f"INSERT INTO {table_name} VALUES ({id}, "

        for i, v in enumerate(dict_values):

            if i == n_values - 1:
                break
                
            if isinstance(v, bool):
                v = int(v)

            sql += f"{v}, "

        if isinstance(v, bool):
            v = int(v)

        sql += f"{v});"

        return sql
    
    def exec(self, verbose: bool = False, timeout: float = None, cache: bool = False, save_df: bool = False):
        res = fmdt.api.detect(**self.to_dict(), verbose=verbose, timeout=timeout, cache=cache, save_df=save_df)
        return res
    
    def strip(self):
        """Strip Args of path variables that don't affect execution"""

        c = copy.deepcopy(self)
        c.ccl_fra_path = None
        c.log_path = None
        c.trk_roi_path = None
        c.trk_path = None

        return c
            
    def cache_trk(self) -> str:
        """Generate the full path to a unique file to store the results of this detection"""
        return self.cache_dir() + "_trk.txt"

    @staticmethod
    def sql_create_table(table_name: str = "detect_args") -> str:
        """Return the SQL instructions to create a DetectArgs table named `table_name`"""
        sql = (
            f"""
            CREATE TABLE {table_name} (
                id_args INTEGER NON NULL PRIMARY KEY,
                vid_in_start INTEGER,
                vid_in_stop INTEGER,
                vid_in_skip INTEGER,
                vid_in_buff BOOLEAN,
                vid_in_loop INTEGER,
                vid_in_threads INTEGER,
                ccl_hyst_lo INTEGER,
                ccl_hyst_hi INTEGER,
                ccl_fra_id BOOLEAN,
                cca_mag BOOLEAN,
                cca_ell BOOLEAN,
                mrp_s_min INTEGER,
                mrp_s_max INTEGER,
                knn_k INTEGER,
                knn_d INTEGER,
                knn_s NUMERIC,
                trk_ext_d INTEGER,
                trk_ext_o INTEGER,
                trk_angle NUMERIC,
                trk_star_min INTEGER,
                trk_meteor_min INTEGER,
                trk_meteor_max INTEGER,
                trk_ddev NUMERIC,
                trk_all BOOLEAN
            );
            """
        )

        return sql

class LogParserArgs(AbstractExecutableArgs):

    def __init__(
            self,
            log_path: str,
            trk_roi_path: str | None = None,
            log_flt: str | None = None,
            fra_path: str | None = None,
            ftr_name: str | None = None,
            ftr_path: str | None = None,
            trk_path: str | None = None,
            trk_json_path: str | None = None,
            trk_bb_path: str | None = None,
        ):

        self.log_path = log_path
        self.trk_roi_path = trk_roi_path
        self.log_flt = log_flt
        self.fra_path = fra_path
        self.ftr_name = ftr_name
        self.ftr_path = ftr_path
        self.trk_path = trk_path
        self.trk_json_path = trk_json_path
        self.trk_bb_path = trk_bb_path

    # ========================= ABC overrides =================================
    def api_callable(self):
        return fmdt.api.log_parser
    
    def argument_handler(self):
        return handle_log_parser_args
    
    def clutter_list(self):
        return ["trk_roi_path", "trk_bb_path", "trk_json_path", "fra_path", "trk_path"]


class VisuArgs(AbstractExecutableArgs):

    def __init__(
            self, 
            vid_in_path: str, 
            trk_path: str,
            trk_bb_path: str | None = None,
            vid_out_path: str | None = None,
            vid_in_start: int | None = None, 
            vid_in_stop: int | None = None, 
            vid_in_threads: int | None = None, 
            trk_id: bool = False,
            trk_nat_num: bool = False,
            trk_only_meteor: bool = False,
            gt_path: str | None = None
        ):

        self.vid_in_path = vid_in_path
        self.vid_in_start = vid_in_start
        self.vid_in_stop = vid_in_stop
        self.vid_in_threads = vid_in_threads
        self.trk_path = trk_path
        self.trk_bb_path = trk_bb_path
        self.trk_id = trk_id
        self.trk_nat_num = trk_nat_num
        self.trk_only_meteor = trk_only_meteor
        self.gt_path = gt_path
        self.vid_out_path = vid_out_path

    # ========================= ABC overrides =================================
    def api_callable(self):
        return fmdt.api.visu
    
    def argument_handler(self):
        return handle_visu_args

    def video_path(self):
        return self.vid_out_path

    def clutter_list(self):
        return ["trk_bb_path", "gt_path", "trk_path"]
    
class CheckArgs(AbstractExecutableArgs):

    def __init__(
            self, 
            trk_path: str,
            gt_path: str | None = None
        ):

        self.trk_path = trk_path
        self.gt_path = gt_path

    # ========================= ABC overrides =================================
    def api_callable(self):
        return fmdt.api.check
    
    def argument_handler(self):
        return handle_check_args

    def clutter_list(self):
        return ["gt_path", "trk_path"]

_DEFAULT_LOG_SUFFIX = '_log'

class Args:
    """Args keeps track of a configuration of parameters for all of fmdt's
    executables

    Upon a call to `fmdt.detect()`, an Args object is returned that remembers
    the configuration used to execute fmdt-detect. We can subsequently use the
    Args object as an interface to directly calling `fmdt-log-parser` and
    `fmdt-visu`, without having to respecify some of the more specific
    arguments.

    Consider the difference between the two calls:
    ```
    fmdt.detect(vid_in_path  = "vid.mp4",
                trk_path     = "tracks.txt",
                trk_roi_path = "trk2roi.txt",
                log_path     = "detect_log")
    fmdt.log_parser(log_path     = "detect_log",
                    trk_roi_path = "trk2roi.txt",
                    trk_bb_path  = "bb.txt")
    fmdt.visu(vid_in_path  = "vid.mp4",
              trk_path     = "tracks.txt",
              trk_bb_path  = "bb.txt",
              vid_out_path = "vid_visu.mp4")
    ```

    and
    ```
    fmdt.detect(vid_in_path  = "vid.mp4",
                trk_path     = "tracks.txt",
                trk_roi_path = "trk2roi.txt",
                log_path     = "detect_log")
        .log_parser().visu()
    ```  
    where storing the configuration for `fmdt-detect` in an Args object allows
    us to fill in the parameters needed by a call to `fmdt-log-parser` and
    `fmdt-visu`.

    This class is therefore a collection of dictionaries of parameters and
    interfaces to the fmdt.api functions.

    ==================

    Args has the fields

    detect_args: DetectArgs
    log_parser_args: LogParserArgs
    visu_args: VisuArgs
    verbose: bool
    timeout: float
    """

    def __init__(
        self,
        detect_args: DetectArgs | None = None,
        log_parser_args: LogParserArgs | None = None,
        visu_args: VisuArgs | None = None,
        verbose: bool = False,
        timeout: float | None = None
    ):
        self.detect_args = detect_args
        self.log_parser_args = log_parser_args
        self.visu_args = visu_args
        self.verbose = verbose
        self.timeout = timeout

    @staticmethod
    def new(
        #=================== DetectArgs =======================================
        vid_in_path: str = "default.mp4", 
        vid_in_start: int | None = None,
        vid_in_stop: int | None = None,
        vid_in_skip: int | None = None,
        vid_in_buff: bool | None = None,
        vid_in_loop: int | None = None,
        vid_in_threads: int | None = None,
        ccl_hyst_lo: int | None = None,
        ccl_hyst_hi: int | None = None,
        ccl_fra_path: str | None = None,
        ccl_fra_id: bool | None = None,
        cca_mag: bool | None = None,
        cca_ell: bool | None = None,
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
        trk_roi_path: str | None = None,
        log_path: str | None = None,
        trk_path: str | None = None,
        #=================== LogParserArgs ====================================
        # log_path: str = None,
        # trk_roi_path: str = None,
        log_flt: str | None = None,
        fra_path: str| None = None,
        ftr_name: str | None = None,
        ftr_path: str | None = None,
        # trk_path: str | None = None,
        trk_json_path: str | None = None,
        trk_bb_path: str | None = None,
        #=================== VisuArgs =========================================
        trk_id: bool | None = None,
        trk_nat_num: bool| None = None,
        trk_only_meteor: bool | None = None,
        gt_path: str | None = None,
        vid_out_path: str | None = None,
        #================== Python Args========================================
        verbose: bool | None = False, 
        timeout: float | None = None,
    ):

        detect_args = DetectArgs(vid_in_path=vid_in_path,
                                 vid_in_start=vid_in_start,
                                 vid_in_stop=vid_in_stop,
                                 vid_in_skip=vid_in_skip,
                                 vid_in_buff=vid_in_buff,
                                 vid_in_loop=vid_in_loop,
                                 vid_in_threads=vid_in_threads,
                                 ccl_hyst_lo =ccl_hyst_lo,
                                 ccl_hyst_hi =ccl_hyst_hi,
                                 ccl_fra_path=ccl_fra_path,
                                 ccl_fra_id=ccl_fra_id,
                                 cca_mag=cca_mag,
                                 cca_ell=cca_ell,
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
                                 trk_roi_path=trk_roi_path,
                                 trk_path=trk_path,
                                 log_path=log_path)
        
        log_parser_args = LogParserArgs(log_path=log_path,
                                        trk_roi_path=trk_roi_path,
                                        log_flt=log_flt,
                                        fra_path=fra_path,
                                        ftr_name=ftr_name,
                                        ftr_path=ftr_path,
                                        trk_path=trk_path,
                                        trk_json_path=trk_json_path,
                                        trk_bb_path=trk_bb_path)

        if vid_out_path is None:
            name, ext = fmdt.utils.decompose_video_filename(vid_in_path)
            vid_out_path = f"{name}_visu.{ext}"

        visu_args = VisuArgs(vid_in_path=vid_in_path,
                             vid_in_start=vid_in_start,
                             vid_in_stop=vid_in_stop,
                             vid_in_threads=vid_in_threads,
                             trk_path=trk_path,
                             trk_bb_path=trk_bb_path,
                             trk_id=trk_id,
                             trk_nat_num=trk_nat_num,
                             trk_only_meteor=trk_only_meteor,
                             gt_path=gt_path,
                             vid_out_path=os.path.basename(vid_out_path))
        
        return Args(detect_args, log_parser_args, visu_args, verbose, timeout)

    def __str__(self) -> str:

        a0 = "<fmdt.args.Args object>"
        a1 = "\n===================="
        a2 = "\nDetect parameters: \n"
        a = str(self.detect_args.to_reduced_dict())

        return a0 + a1 + a2 + a

    # ======================== Executables ====================================
    def detect(self, cache: bool = False, save_df: bool = False):
        """OOP Interface for calling fmdt.api.detect()
        
        Parameters
        ----------
        cache (bool): When true, store the output of fmdt-detect in a unique 
            file corresponding to the set of parameters 
        """

        # Make sure the detecting arguments are not none
        if self.detect_args is None:
            self.detect_args = DetectArgs(**empty_detect_args())

        return self.detect_args.exec(self.verbose, self.timeout, cache, save_df)
    
    def log_parser(self, autocorrect=True):
        """OOP Interface to calling fmdt.api.log_parser
        
        
        Parameters
        ----------
        autocorrect (bool): If no log path exists, rerun a detection with a default log path 
        
        """

        # Do we have log_parser arguments?
        assert self.has_log_parser_args(), f"Cannot run Args.log_parser() as this arg's log_parser_args field is None"

        if self.log_parser_args.log_path is None:

            if not autocorrect:
                raise AssertionError("Cannot run Args.log_parser() as no log_path has been set. Try rerunning fmdt.detect(log_path=YOUR_LOG_PATH)")

            self.modify_log_path()

            fmdt.utils.stderr(f"No log_path specified; rerunning Args.detect(log_path='{self.detect_args.log_path}') [.log_parser(autocorrect=False) to disable]")

            return self.detect().log_parser()

        res = self.log_parser_args.exec(verbose=self.verbose)

        # When calling log_parser_args.exec, only the log_parser_args are stored.
        # Overwrite the other two args with this args's parameters
        res.args.detect_args = self.detect_args
        res.args.visu_args = self.visu_args

        return res

    def visu(self, autocorrect=True):
        """OOP Interface to calling fmdt.api.visu()

        Parameters
        ----------
        autocorrect (bool): If no log path exists, rerun a detection with a default log path 
        """ 


        # Do we have visu arguments?
        assert self.has_visu_args(), "No visu args for this object"


        # visu depends on three files: trk_path, trk_bb_path, and trk_roi_path
        # let's go through and verify that visu can be called from this args
        trk_path_exists = os.path.exists(self.trk_path())
        trk_roi_path_exists = os.path.exists(self.trk_roi_path())
        trk_bb_path_exists = os.path.exists(self.trk_bb_path())

        if trk_path_exists and trk_roi_path_exists and not trk_bb_path_exists:
            # Then we need to only rerun log_parser

            if not autocorrect:
                raise AssertionError("trk_bb_path does not exist, run Args.log_parser() to generate it")

            fmdt.utils.stderr(f"trk_bb_path does not exist; rerunning Args.log_parser() to generate it. [.visu(autocorrect=False) to disable]")

            return self.log_parser().visu()

        if not trk_bb_path_exists or not trk_roi_path_exists:
            # Then we need to rerun the entire detection

            if not autocorrect:
                raise AssertionError("trk_path does not exist, rerun Args.detect(log_path=YOUR_LOG_PATH).log_parser() to generate it")

            fmdt.utils.stderr(f"trk_path does not exist; rerunning Args.detect().log_parser() to generate it. [.visu(autocorrect=False) to disable]")

            if not self.has_detect_args():
                raise AssertionError(f"Cannot rerun detection because self.detect_args is empty [{self}]")

            return self.detect().log_parser().visu()

        vres = self.visu_args.exec(verbose=self.verbose) 

        return vres

    # TODO: Add .check interface

    
    # ========================== Inquiry functions ============================
    def trk_path(self) -> str | None:
        """Alias to Args.tracks"""
        return self.tracks()

    def trk_bb_path(self) -> str | None:
        """Alias to Args.bbs"""
        return self.bbs()

    def trk_roi_path(self) -> str | None:
        if self.has_detect_args():
            if not self.detect_args.trk_roi_path is None:
                return self.detect_args.trk_roi_path
        elif self.has_log_parser_args():
            if not self.log_parser_args.trk_roi_path is None:
                return self.log_parser_args.trk_roi_path
        else:
            return None

    def log_path(self) -> str | None:
        if self.has_detect_args():
            if not self.detect_args.log_path is None:
                return self.detect_args.log_path
        if self.has_log_parser_args():
            if not self.log_parser_args.log_path is None:
                return self.log_parser_args.log_path
        else:
            return None
        
    def vid_in_path(self) -> str | None:
        """Return the name of the input video file"""
        if self.has_detect_args():
            if not self.detect_args.vid_in_path is None:
                return self.detect_args.vid_in_path
        elif self.has_visu_args():
            if not self.visu_args.vid_in_path is None:
                return self.visu_args.vid_in_path
        else:
            return None
    
    def vid_out_path(self) -> str | None:
        return self.visu_vid()
        
        
    def tracks(self) -> str | None:
        """Return the name of the tracks file, if it exists"""

        if self.has_detect_args():
            if not self.detect_args.trk_path is None:
                return self.detect_args.trk_path
        elif self.has_log_parser_args():
            if not self.log_parser_args.trk_path is None:
                return self.log_parser_args.trk_path
        elif self.has_visu_args():
            if not self.visu_args.trk_path is None:
                return self.visu_args.trk_path
        else:
            return None

    def bbs(self) -> str | None:
        """Return the name of the bounding boxes (BBs) file, if it exists"""
        if self.has_log_parser_args():
            if not self.log_parser_args.trk_bb_path is None:
                return self.log_parser_args.trk_bb_path
        elif self.has_visu_args():
            if not self.visu_args.trk_bb_path is None:
                return self.visu_args.trk_bb_path
        else:
            return None

    def detect_cmd(self) -> str | None:
        if self.has_detect_args():
            return self.detect_args.cmd()
        else:
            return None
    
    def visu_cmd(self) -> str | None:
        if self.has_visu_args():
            return self.visu_args.cmd()
        else:
            return None

    def log_parser_cmd(self) -> str | None:
        if self.has_log_parser_args():
            return self.log_parser_args.cmd()
        else:
            return None

    def does_detect_fail(self, verbose=False) -> bool:
        """Returns true if the stderr pipe of a call to fmdt-detect is not empty"""

        if self.detect_args["vid_in_path"] is None:
            return True

        detect_cmd = self.detect_args.cmd()
        if (verbose):
            print(detect_cmd)
        res = subprocess.run(detect_cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        if res.returncode != 0:
            return True
        
        return False
    
    # ================================= Helper functions ======================
    def has_detect_args(self) -> bool:
        return not self.detect_args is None
    
    def has_visu_args(self) -> bool:
        return not self.visu_args is None
    
    def has_log_parser_args(self) -> bool:
        return not self.log_parser_args is None

    def visu_vid(self) -> str | None:
        """Return the path of the video output by fmdt-visu"""
        if self.has_visu_args():
            return self.visu_args.video_path()
        else:
            return None

    def detect_vid(self) -> str | None:
        """Return the path of the video input to fmdt-detect"""
        if self.has_detect_args(): 
            return self.detect_args.video_path()
        else:
            return None

    def vid(self) -> str | None:
        """Return the name of the video, if it exists"""
        if not self.detect_args.vid_in_path is None:
            return self.detect_args.vid_in_path
        elif not self.visu_args.vid_in_path is None:
            return self.visu_args.vid_in_path
        else:
            return None

    # Take the detect argument dictionary and write out a comma separated value string
    def detect_csv_header(self) -> str:
        """Return the header line used in a csv file storing multiple argument configurations"""
        header = ""
        for k in self.detect_args.keys():
            if k == "verbose":
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
        """Retreive the list of TrackedObject that is stored in the trk_path file"""
        assert not self.detect_args.trk_path is None, "Out track file not stored"

        return fmdt.core.extract_all_information(self.detect_args.trk_path)
    
    def command(self) -> str:
        """Return the command used to execute fmdt-detect with this configuration"""
        return ' '.join(handle_detect_args(**self.detect_args.to_dict()))
    
    def digest(self) -> str:
        return hashlib.md5(pickle.dumps(self)).hexdigest()

    def __hash__(self) -> int:
        # return int.from_bytes(pickle.dumps(self), "big")
        return int(hashlib.md5(pickle.dumps(self)).hexdigest(), 16)
    
    def gen_unique_trk(self) -> str:
        """Generate a unique trk file corresponding to this set of parameters"""
        h = self.digest()
        return "trk_" + h[0:16] + ".txt" 
    
    def gen_unique_file(self, prefix="", suffix=".txt") -> str:
        h = self.digest()
        return prefix + h[0:16] + suffix

    def clutter(self) -> list[str]:
        """Return a list of files that have been created throughout this args lifetime"""

        clut = []

        if self.has_detect_args():
            clut.extend(self.detect_args.clutter())

        if self.has_log_parser_args():
            clut.extend(self.log_parser_args.clutter())
        
        if self.has_visu_args():
            clut.extend(self.visu_args.clutter())

        return clut
    
    def modify_log_path(self):
        """Create a new log_path corresponding to the relevant video and modify self.detect_args"""
        name, _ = fmdt.utils.decompose_video_filename(self.vid_in_path())
        self.detect_args.log_path = os.path.basename(name) + _DEFAULT_LOG_SUFFIX


class FMDTResult:

    def __init__(self, arg_err: list[float] = None, ecarts_type: list[float] = None, nrois: list[int] = None, args: Args = None):
        self.arg_err = arg_err
        self.ecarts_type = ecarts_type
        self.nrois = nrois
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
    a.detect_args = empty_detect_args()
    a.detect_args.vid_in_path = filename
    return a

__DEFAULT_TRK_ROI_PATH_SUFFIX = "_trk2roi.txt"
__DEFAULT_TRK_PATH_SUFFIX = "_trk.txt"

# Create an Args object from the fmdt-detect parameters
def detect_args(
        vid_in_path: str = "default.mp4", 
        vid_in_start: int | None = None,
        vid_in_stop: int | None = None,
        vid_in_skip: int | None = None,
        vid_in_buff: bool | None = None,
        vid_in_loop: int | None = None,
        vid_in_threads: int | None = None,
        ccl_hyst_lo: int | None = None,
        ccl_hyst_hi: int | None = None,
        ccl_fra_path: str | None = None,
        ccl_fra_id: bool | None = None,
        cca_mag: bool | None = None,
        cca_ell: bool | None = None,
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
        trk_roi_path: str | None = None,
        log_path: str | None = None,
        trk_path: str | None = None,
        verbose: bool = False,
        timeout: float = None,
        **args # any leftovers, useful when converting sql query to args object
    ) -> Args:
    """Convert the parameters used in fmdt.detect into an Args object"""

    assert not vid_in_path is None, "vid_in_path cannot be None"

    vid_basename = os.path.basename(vid_in_path)
    name, _ = fmdt.utils.decompose_video_filename(vid_basename)

    if trk_roi_path is None:
        trk_roi_path = name + __DEFAULT_TRK_ROI_PATH_SUFFIX

    if trk_path is None:
        trk_path = name + __DEFAULT_TRK_PATH_SUFFIX

    # Make sure that the leftovers in **args doesnt contain any visu parameters
    for k in args.keys():
        if k in _VISU_UNIQUE_ARGS:
            raise TypeError(f"{k} is not a fmdt-detect parameter. Consider calling fmdt.Args.new instead")

    d_args = DetectArgs(vid_in_path, vid_in_start, vid_in_stop, vid_in_skip, vid_in_buff,
                        vid_in_loop, vid_in_threads, ccl_hyst_lo, ccl_hyst_hi, ccl_fra_path,
                        ccl_fra_id, cca_mag, cca_ell, mrp_s_min, mrp_s_max, knn_k, knn_d, knn_s,
                        trk_ext_d, trk_ext_o, trk_angle, trk_star_min, trk_meteor_min, trk_meteor_max,
                        trk_ddev, trk_all, trk_roi_path, log_path, trk_path)

    name, ext = fmdt.utils.decompose_video_filename(vid_in_path)

    bb_name = f"{name}_bbs.txt"
    l_args = LogParserArgs(log_path=log_path,
                           trk_roi_path=trk_roi_path,
                           trk_bb_path=os.path.basename(bb_name))

    visu_name = f"{name}_visu.{ext}"

    v_args = VisuArgs(vid_in_path=vid_in_path,
                      vid_in_start=vid_in_start,
                      vid_in_stop=vid_in_stop,
                      vid_in_threads=vid_in_threads,
                      trk_path=trk_path,
                      trk_bb_path=os.path.basename(bb_name),
                      vid_out_path=os.path.basename(visu_name))
    
    return Args(d_args, l_args, v_args, verbose, timeout)

def log_parser_args(
        log_path: str = None,
        trk_roi_path: str = None,
        log_flt: str = None,
        fra_path: str = None,
        ftr_name: str = None,
        ftr_path: str = None,
        trk_path: str = None,
        trk_json_path: str = None,
        trk_bb_path: str = None,
    ) -> LogParserArgs:

    # While this is extremely ugly, it allows us to have a nicer user-facing api
    return LogParserArgs( **{
        "log_path": log_path,
        "trk_roi_path": trk_roi_path,
        "log_flt": log_flt,
        "fra_path": fra_path,
        "ftr_name": ftr_name,
        "ftr_path": ftr_path,
        "trk_path": trk_path,
        "trk_json_path": trk_json_path,
        "trk_bb_path": trk_bb_path,
    }
    )

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
    ) -> VisuArgs:

    # While this is extremely ugly, it allows us to have a nicer user-facing api
    return VisuArgs( **{
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
    )

def empty_detect_args() -> dict:       

    """Create a new Dictionary of detect args with all None entries."""

    default_detect = {
        "vid_in_path": None, 
        "vid_in_start": None,
        "vid_in_stop": None,
        "vid_in_skip": None,
        "vid_in_buff": None,
        "vid_in_loop": None,
        "vid_in_threads": None,
        "ccl_hyst_lo": None,
        "ccl_hyst_hi": None,
        "ccl_fra_path": None,
        "ccl_fra_id": None,
        "cca_mag": None,
        "cca_ell": None,
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
        "trk_roi_path": None,
        "log_path": None,
        "trk_path": None
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
        ccl_hyst_lo: int | None = None,
        ccl_hyst_hi: int | None = None,
        ccl_fra_path: str | None = None,
        ccl_fra_id: bool | None = None,
        cca_mag: bool | None = None,
        cca_ell: bool | None = None,
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
        trk_roi_path: str | None = None,
        log_path: str | None = None,
        **args
    ) -> list[str]:
    """Convert the arguments needed for fmdt-detect into a fmdt-detect command-line call
    """
    if get_exec_path() is None:
        fmdt_detect_exe = shutil.which("fmdt-detect")
    else:
        fmdt_detect_exe = shutil.which("fmdt-detect", path=get_exec_path())

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
    arg_str(ccl_hyst_lo, "ccl-hyst-lo")
    arg_str(ccl_hyst_hi, "ccl-hyst-hi")
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
    arg_str(trk_roi_path, "trk-roi-path")
    arg_str(log_path, "log-path")
    arg_str(trk_angle, "trk-angle")
    arg_str(trk_star_min, "trk-star-min")
    arg_str(vid_in_start, "vid-in-start")
    arg_str(vid_in_stop, "vid-in-stop")
    arg_str(trk_bb_path, "trk-bb-path")
    arg_str(vid_in_loop, "vid-in-loop")

    # ======== Arguments of the form --toggle
    arg_bool(vid_in_buff, "vid_in_buff")
    arg_bool(ccl_fra_id, "ccl-fra-id")
    arg_bool(cca_mag, "cca-mag")
    arg_bool(cca_ell, "cca-ell")
    arg_bool(trk_all, "trk-all")

    return args

def handle_log_parser_args(
        log_path: str = None,
        trk_roi_path: str = None,
        log_flt: str = None,
        fra_path: str = None,
        ftr_name: str = None,
        ftr_path: str = None,
        trk_path: str = None,
        trk_json_path: str = None,
        trk_bb_path: str = None,
    ) -> list[str]:

    if get_exec_path() is None:
        fmdt_log_parser_exe = shutil.which("fmdt-log-parser")
    else:
        fmdt_log_parser_exe = shutil.which("fmdt-log-parser", path=get_exec_path())

    fmdt_log_parser_found = not fmdt_log_parser_exe is None
    assert fmdt_log_parser_found, "fmdt-log-parser executable not found"

    assert not log_path is None, "No input log path specified"

    args = [fmdt_log_parser_exe, "--log-path", log_path]

    # helper closure to clean up repetitive code
    def add_arg(arg, flag):
        if not arg is None:
            args.extend([flag, str(arg)])

    add_arg(trk_roi_path, "--trk-roi-path")
    add_arg(log_flt, "--log-flt")
    add_arg(fra_path, "--fra-path")
    add_arg(ftr_name, "--ftr-name")
    add_arg(ftr_path, "--ftr-path")
    add_arg(trk_path, "--trk-path")
    add_arg(trk_json_path, "--trk-json-path")
    add_arg(trk_bb_path, "--trk-bb-path")

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

    if get_exec_path() is None:
        fmdt_visu_exe = shutil.which("fmdt-visu")
    else:
        fmdt_visu_exe = shutil.which("fmdt-visu", path=get_exec_path())

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
        args.extend(["--vid-out-path", os.path.basename(new_name)])

    # helper closure to clean up repetitive code
    def add_arg(arg, flag):
        if not arg is None:
            args.extend([flag, str(arg)])

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

def handle_check_args(
        trk_path: str,
        gt_path: str
    ) -> list[str]:

    if get_exec_path() is None:
         fmdt_check_exe = shutil.which("fmdt-check")
    else:
         fmdt_check_exe = shutil.which("fmdt-check", path=get_exec_path())

    fmdt_check_found = not fmdt_check_exe is None
    assert fmdt_check_found, "fmdt-check executable not found"

    assert not trk_path is None, "No input track path"
    assert not gt_path is None, "No input track path"

    args = [fmdt_check_exe, "--trk-path", trk_path, "--gt-path", gt_path] 

    return args
    

def main() -> None:
    a = Args()
    a.detect_args = detect_args(vid_in_path="demo.mp4")
    print(a.detect_csv_header())
    print(a.detect_to_csv_row())