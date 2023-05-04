"""
API to call fmdt executables. Assumes that fmdt-detect and other executables
are on the system path
"""
import fmdt.res
import random
from os import listdir
import subprocess
import os
import fmdt.core
import fmdt.utils
import fmdt.args
from termcolor import colored
import shutil
import pandas as pd

def help():
    s = """    fmdt.api contains a Python wrapper for the `fmdt-detect` and `fmdt-visu` 
    executables.
    
    fmdt.api contains the public-facing functions (also aliased under fmdt.*):
        fmdt[.api].count
        fmdt[.api].detect
        fmdt[.api].log_parser
        fmdt[.api].visu

    fmdt.api.count counts the number of celestial objects specified by the parameters
    fmdt.api.detect calls `fmdt-detect` with the given arguments
    fmdt.api.log_parser calls `fmdt-log-parser`
    fmdt.api.visu calls `fmdt-visu`
    """
    return s

def count(
        trk_path: str,
        stars: bool = False,
        meteors: bool = True,
        noise: bool = False,
        all: bool = False
    ) -> int:
    """Count the number of objects detected in a tracks_bb file

    Parameters
    ----------
    trk_path (str): Path to file that stores the tracks (stdout of `fmdt-detect`) of detected objects
    stars (bool): When True, include star objects in our count (Default False)
    meteors (bool): When True, include meteor objects in our count (Default True)
    noise (bool): When True, include noise objects in our count (Default False)
    all (bool): When True, include all objects in the count
    
    Examples
    --------
    >>> fmdt.detect(vid_in_path="demo.mp4", trk_path="tracks.txt") # Store tracks in tracking file
    >>> fmdt.count("tracks.txt")  # Count meteors only

    >>> fmdt.count("tracks.txt", all=True) # Count stars, meteors, and noise

    >>> fmdt.count("tracks.txt", stars=True, meteors=False, noise=True) # Count stars and noise 
    """
    if all:
        stars = True
        meteors = True
        noise = True

    tracked = fmdt.core.extract_key_information(trk_path)

    # If we shouldn't keep this object type, filter it out
    def refine(obj_type: bool, type_str: str) -> None: 
        if not obj_type:
            tracked = [t for t in tracked if t["type"] != type_str]
    
    refine(stars, "stars")
    refine(meteors, "meteors")
    refine(noise, "noise")

    # tracked_meteors = fmdt.utils.retain_meteors(tracked)
    return len(tracked)
    

FMDT_TIMEOUT = 1


def detect(
        #=================== fmdt-detect parameters ================
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
        #================== Additional Parameters ====================
        trk_path: str | None = None,
        verbose: bool = False,
        timeout: float = None,
        cache: bool = False,
        save_df: bool = False
    ) -> fmdt.res.DetectionResult:
    """Wrapper to executable fmdt-detect.

    Parameters
    ----------
    Extensively documented here: https://fmdt.readthedocs.io/en/latest/user/usage/detect.html#

    Wrapper Parameters
    ------------------
    trk_path (str): path to redirect stdout of `fmdt-detect`
    verbose (bool): Print logging messages to stdout (True) or do nothing (False). Default False.
    timeout (float): timeout in seconds of the Python subprocess executing `fmdt-detect`. Default None. 
        Used to speed up ground truth testing.
    """


    # Wrap up all of the arguments into an Args object
    args = fmdt.args.detect_args(vid_in_path=vid_in_path,
                                 vid_in_start=vid_in_start,
                                 vid_in_stop=vid_in_stop,
                                 vid_in_skip=vid_in_skip,
                                 vid_in_buff=vid_in_buff,
                                 vid_in_loop=vid_in_loop,
                                 vid_in_threads=vid_in_threads,
                                 ccl_hyst_lo=ccl_hyst_lo,
                                 ccl_hyst_hi=ccl_hyst_hi,
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
                                 log_path=log_path,
                                 trk_path=trk_path,
                                 verbose=verbose)

    if not log_path is None:

        if verbose:
            print(f"Clearing all frame files (matching r'\d*.txt') from {log_path}")

        fmdt.utils.mkdir_p(log_path)

        # Clear all the frame files in log_path
        frames = fmdt.res.get_ordered_frames(log_path) 

        for f in frames:
            os.remove(fmdt.utils.join(log_path, f))
    
    if save_df and log_path is None:
        print("Save_df activated in final detect call")
        args.detect_args.log_path = args.detect_args.cache_dir()

    # Spit out the commandline arguments for fmdt-detect
    argv = args.detect_args.argv()
    cache_file = None

    if cache:
        cache_file = args.detect_args.cache_trk()

    #============ Retrieve Tracked list ===========================================#
    if trk_path is None:
        trk_list, nframes = _run_detect(args.gen_unique_trk(), argv, timeout, verbose, cache, cache_file, tmp_file=True)
    else:
        trk_list, nframes = _run_detect(trk_path, argv, timeout, verbose, cache, cache_file)

    #============= Recover data if log_path =======================================#
    if not args.detect_args.log_path is None:
        nrois, nassocs, mean_errs, std_devs = fmdt.res.retrieve_log_info(args.detect_args.log_path, nframes) 
    else:
        nrois = []
        nassocs = []
        mean_errs = []
        std_devs = []

    # Now construct the result object

    if len(nrois) == 0:
        df = None
    else:
        df =  pd.DataFrame({
                'nroi': nrois,
                'nassoc': [0] + nassocs,
                'mean_err': [0.0] + mean_errs,
                'std_dev': [0.0] + std_devs
            })

    return fmdt.res.DetectionResult(nframes, df, args, trk_list)   

def log_parser(
        log_path: str,
        trk_roi_path: str | None = None,
        log_flt: str | None = None,
        fra_path: str | None = None,
        ftr_name: str | None = None,
        ftr_path: str | None = None,
        trk_path: str | None = None,
        trk_json_path: str | None = None,
        trk_bb_path: str | None = None,
        #========================== Additional Options ========================
        stdout: str | None = None,
        verbose: bool = False
    ) -> fmdt.res.LogParserResult:
    """Wrapper to executable fmdt-log-parser.

    Parameters
    ----------
    Extensively documented here: https://fmdt.readthedocs.io/en/latest/user/usage/log.html

    
    stdout (str): A file path to save the contents of the standard out of fmdt-log-parser
    verbose (bool): 


    """
    log_parser_args = fmdt.args.log_parser_args(log_path=log_path,
                                                trk_roi_path=trk_roi_path,
                                                log_flt=log_flt,
                                                fra_path=fra_path,
                                                ftr_name=ftr_name,
                                                ftr_path=ftr_path,
                                                trk_path=trk_path,
                                                trk_json_path=trk_json_path,
                                                trk_bb_path=trk_bb_path)

    argv = fmdt.args.handle_log_parser_args(**log_parser_args.to_dict())

    if stdout is None:

        stdout = log_parser_args.gen_unique_file(prefix="log_parser_")
        _run_process(stdout, argv, verbose, tmp_file=True)

    else:
        _run_process(stdout, argv, verbose)

    args = fmdt.args.Args(log_parser_args=log_parser_args, detect_args=None, visu_args=None)

    return fmdt.res.LogParserResult(args)
            
def visu(
        vid_in_path: str,
        trk_path: str,
        trk_bb_path: str,
        vid_out_path: str,
        vid_in_start: int | None = None,
        vid_in_stop: int | None = None,
        vid_in_threads: int | None = None,
        trk_id: bool | None = None,
        trk_nat_num: bool | None = None,
        trk_only_meteor: bool | None = None,
        gt_path: str | None = None,
        #========================== Additional Options ========================
        verbose: bool = False,
        stdout: str | None = None
    ) -> fmdt.res.VisuResult:
    """Wrapper to executable fmdt-visu.

    Parameters
    ----------
    Extensively documented here: https://fmdt.readthedocs.io/en/latest/user/usage/visu.html
    """
    visu_args = fmdt.args.visu_args(vid_in_path=vid_in_path,
                                    vid_in_start=vid_in_start,
                                    vid_in_stop=vid_in_stop,
                                    vid_in_threads=vid_in_threads,
                                    trk_path=trk_path,
                                    trk_bb_path=trk_bb_path,
                                    trk_id=trk_id,
                                    trk_nat_num=trk_nat_num,
                                    trk_only_meteor=trk_only_meteor,
                                    gt_path=gt_path,
                                    vid_out_path=vid_out_path)

    argv = fmdt.args.handle_visu_args(**visu_args.to_dict())

    if stdout is None:
        stdout = visu_args.gen_unique_file(prefix="visu_")
        _run_process(stdout, argv, verbose, tmp_file=True)
    else:
        _run_process(stdout, argv, verbose)

    args = fmdt.args.Args(visu_args=visu_args, detect_args=None, log_parser_args=None)

    return fmdt.res.VisuResult(args)

def check(
        trk_path: str,
        gt_path: str,
        stdout: str = None,
        verbose = False
    ) -> fmdt.res.CheckResult:
    """Call fmdt-check
    
    Parameters
    ----------
    std_out (str): File to store stdout of fmdt-check"""

    argv = fmdt.args.handle_check_args(trk_path, gt_path)

    _run_process(stdout, argv, verbose, False)

    stats = fmdt.res.load_check_stats(stdout)
    gt_table = fmdt.res.load_check_gt_table(stdout)
    
    return fmdt.res.CheckResult(gt_table=gt_table, stats=stats)

def detect_directory(dir_name: str, args: fmdt.args.Args, verbose=False):
    """Call `fmdt-detect` on all videos in the directory `dir_name` using the settings stored in `args`
    
    Parameters
    ----------
    dir_name (str): Path to the directory of videos that you'd like to detect
    args: (fmdt.args.Args): Configuration of parameters used to call fmdt.detect    
    
    
    """

    entries = listdir(dir_name)
    is_video_fn = lambda v: v[-3:] == "mp4" or v[-3:] == "avi"
    videos = [e for e in entries if is_video_fn(e)]

    assert len(videos) > 0, "Directory is empty, call to fmdt.detect_directory failed"

    # Now let's call fmdt detect one time for each video
    failing_cmds = []
    i = 0
    for v in videos:

        args.detect_args["vid_in_path"] = dir_name + "/" + v

        fail = args.does_detect_fail(verbose=verbose)
        if verbose: 
            print(f"{v} fails? {fail}")

        if (fail):
            failing_cmds.append(" ".join(args.detect_cmd()))
        
        i = i + 1

    for c in failing_cmds:
        print(c)


# ===================== _run_$EXECUTABLE ======================================
def _run_detect(
        trk_path: str,
        argv: list[str],
        timeout: float,
        verbose: bool,
        cache: bool,
        cache_file: str,
        tmp_file: bool = False
    ) -> tuple[list[fmdt.core.TrackedObject], int]:
    """Handle the final logic of calling `fmdt-detect`
    

    Parameters
    ----------
    tmp_file (bool): Indicates whether `trk_path` is a temporary file that should be deleted after execution.
        Default False
    
    """

    with open(trk_path, 'w') as outfile:

        if verbose:
            print(f"Executing cmd: {' '.join(argv)}")

            if tmp_file:
                print(f"{trk_path} marked as a temporary file")

        if not timeout is None:
            try: 
                proc = subprocess.Popen(argv, stdout=subprocess.PIPE)
                outs, _ = proc.communicate(timeout=timeout)
                lines = outs.decode("utf-8").split("\n")
                for line in lines:
                    if verbose:
                        print(line)
                    outfile.write(line + "\n")
                proc.wait(timeout=timeout)
            except:
                print("==================================================================")
                print("")
                print(f"Subprocess timed out for \n\t{colored(' '.join(argv), 'blue')}")
                print("")
                print("==================================================================")
                return [], 0
        else:
            proc = subprocess.Popen(argv, stdout=subprocess.PIPE)
            outs, _ = proc.communicate()
            lines = outs.decode("utf-8").split("\n")
            for line in lines:
                if verbose:
                    print(line)
                outfile.write(line + "\n")
            proc.wait()
        
    trk_list = fmdt.core.extract_all_information(trk_path)
    nframes = fmdt.core.nframes_processed(trk_path)
            
    if cache:
        shutil.copyfile(src=trk_path, dst=cache_file)

    if tmp_file:
        os.remove(trk_path)

    return trk_list, nframes

def _run_process(
        stdout_file,
        argv: list[str],
        verbose: bool,
        tmp_file: bool = False
    ) -> tuple[list[fmdt.core.TrackedObject], int]:
    """Handle the final logic of calling `fmdt-log-parser`
    
    Parameters
    ----------
    stdout_file (str): File path to capture standard out of log_parser
    tmp_file (bool): Indicates whether `trk_path` is a temporary file that should be deleted after execution.
        Default False
    
    """
    with open(stdout_file, 'w') as outfile:

        if verbose:
            print(f"Executing cmd: {' '.join(argv)}")

        proc = subprocess.Popen(argv, stdout=subprocess.PIPE)
        outs, _ = proc.communicate()
        lines = outs.decode("utf-8").split("\n")
        for line in lines:
            if verbose:
                print(line)
            outfile.write(line + "\n")
        proc.wait()

    if tmp_file:
        os.remove(stdout_file)