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

def help():
    s = """    fmdt.api contains a Python wrapper for the `fmdt-detect` and `fmdt-visu` 
    executables.
    
    fmdt.api contains the public-facing functions (also aliased under fmdt.*):
        fmdt[.api].count
        fmdt[.api].detect
        fmdt[.api].visu
        fmdt[.api].detect_directory

    fmdt.api.count counts the number of celestial objects specified by the parameters
    fmdt.api.detect calls `fmdt-detect` with the given arguments
    fmdt.api.visu calls `fmdt-visu`
    fmdt.api.detect_directory
        
        
        
"""

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
    >>> fmdt.detect(vid_in_path="demo.mp4", trk_out_path="tracks.txt") # Store tracks in tracking file
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

def run_detect_stdout(argv: list[str], timeout: float, log: bool) -> tuple[list[fmdt.core.TrackedObject], int]:

    if log:
        print(f"Executing cmd: {' '.join(argv)}")

    
    # Store this data in a tmp file and then use that to get the tracking list.
    tmp_filename = "fmdt_detect_tmp.txt"
    tmp_file = open(tmp_filename, "w")

    if not timeout is None:

        try:
            res = subprocess.run(argv, timeout=timeout, stdout=tmp_file)
            tmp_file.close()

        except:
            print(f"Subprocess timed out for {colored(' '.join(argv), 'red')}")
            tmp_file.close()
            os.remove(tmp_file)
            return [], 0
    else:
        subprocess.run(argv, stdout=tmp_file)

    if log: 
        with open(tmp_filename) as tmp_file:
            print(tmp_file.read())

    trk_list = fmdt.core.extract_all_information(tmp_filename)
    nframes = fmdt.core.nframes_processed(tmp_filename)

    os.remove(tmp_filename)

    return trk_list, nframes

def run_detect_trk_path(trk_out_path, argv, timeout, log) -> tuple[list[fmdt.core.TrackedObject], int]:

    with open(trk_out_path, 'w') as outfile:
        if log:
            print(f"Executing cmd: {' '.join(argv)}")

        if not timeout is None:
            try: 
                subprocess.run(argv, stdout=outfile, timeout=timeout)
            except:
                print("==================================================================")
                print("")
                print(f"Subprocess timed out for \n\t{colored(' '.join(argv), 'blue')}")
                print("")
                print("==================================================================")
                return [], 0
        else:
            subprocess.run(argv, stdout=outfile)
        
        trk_list = fmdt.core.extract_all_information(trk_out_path)
        nframes = fmdt.core.nframes_processed(trk_out_path)

    return trk_list, nframes
    

def detect(
        #=================== fmdt-detect parameters ================
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
        #================== Additional Parameters ====================
        trk_out_path: str | None = None,
        log: bool = False,
        timeout: float = None
    ) -> fmdt.res.DetectionResult:
    """Wrapper to executable fmdt-detect.

    Parameters
    ----------
    Extensively documented here: https://fmdt.readthedocs.io/en/latest/user/usage/detect.html#

    Wrapper Parameters
    ------------------
    trk_out_path (str): path to redirect stdout of `fmdt-detect`
    log (bool): Print logging messages to stdout (True) or do nothing (False). Default False.
    timeout (float): timeout in seconds of the Python subprocess executing `fmdt-detect`. Default None. 
        Used to speed up ground truth testing.
    """

    # Wrap up all of the arguments into an Args object
    args = fmdt.args.detect_args(vid_in_path, vid_in_start, vid_in_stop, 
        vid_in_skip, vid_in_buff, vid_in_loop, vid_in_threads, light_min, light_max, 
        ccl_fra_path, ccl_fra_id, mrp_s_min, mrp_s_max, knn_k, knn_d, knn_s, trk_ext_d,
        trk_ext_o, trk_angle, trk_star_min, trk_meteor_min, trk_meteor_max, trk_ddev, 
        trk_all, trk_bb_path, trk_mag_path, log_path, trk_out_path, log)

    # Spit out the commandline arguments for fmdt-detect
    argv = args.detect_args.argv()

    #============ Retrieve Tracked list ===========================================#
    if trk_out_path is None:
        trk_list, nframes = run_detect_stdout(argv, timeout, log) 
    else:
        trk_list, nframes = run_detect_trk_path(trk_out_path, argv, timeout, log) 

    #============= Recover data if log_path =======================================#
    if not log_path is None:
        nrois, nassocs, mean_errs, std_devs = fmdt.res.retrieve_log_info(log_path) 
    else:
        nrois = []
        nassocs = []
        mean_errs = []
        std_devs = []

    return fmdt.res.DetectionResult(nframes, nrois, [0] + nassocs, [0.0] + mean_errs, [0.0] + std_devs, args, trk_list)   
            
def visu(
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
    ) -> fmdt.args.Args:
    """Wrapper to executable fmdt-detect.

    Parameters
    ----------
    Extensively documented here: https://fmdt.readthedocs.io/en/latest/user/usage/visu.html
    """
    visu_args = fmdt.args.visu_args(vid_in_path, 
                                    vid_in_start,
                                    vid_in_stop,
                                    vid_in_threads,
                                    trk_path,
                                    trk_bb_path,
                                    trk_id,
                                    trk_nat_num,
                                    trk_only_meteor,
                                    gt_path,
                                    vid_out_path)

    args = fmdt.args.handle_visu_args(**visu_args)

    subprocess.run(args)

    return fmdt.args.Args(visu_args=visu_args)

def detect_directory(dir_name: str, args: fmdt.args.Args, log=False):
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
        # res = fmdt.detect(directory + "/" + v, light_min=150, light_max=245, trk_all=True, log=False, trk_out_path="tracks.txt")
        # a = fmdt.args.video_input(directory + "/" + v)
        # a.detect_args["trk_out_path"] = "tracks.txt"

        # if i > 10:
        #     break
        args.detect_args["vid_in_path"] = dir_name + "/" + v

        fail = args.does_detect_fail(log=log)
        if log: 
            print(f"{v} fails? {fail}")

        if (fail):
            failing_cmds.append(" ".join(args.detect_cmd()))
        
        i = i + 1

    for c in failing_cmds:
        print(c)