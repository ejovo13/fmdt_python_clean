"""
API to call fmdt executables. Assumes that fmdt-detect and other executables
are on the system path
"""

from os import listdir
import shutil
import subprocess
import fmdt.core
import fmdt.utils
import fmdt.args

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
        trk_bb_path: str,
        stars: bool = False,
        meteors: bool = True,
        noise: bool = False,
        all: bool = False
    ) -> int:
    """Count the number of meteors detected in a tracks_bb file"""
    if all:
        stars = True
        meteors = True
        noise = True

    tracked = fmdt.core.extract_key_information(trk_bb_path)

    # If we shouldn't keep this object type, filter it out
    def refine(obj_type: bool, type_str: str) -> None: 
        if not obj_type:
            tracked = [t for t in tracked if t["type"] != type_str]
    
    refine(stars, "stars")
    refine(meteors, "meteors")
    refine(noise, "noise")

    # tracked_meteors = fmdt.utils.retain_meteors(tracked)
    return len(tracked)
    

def detect(
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
        trk_out_path: str | None = None,
        log_path: str | None = None,
        log: bool = False
    ) -> fmdt.args.Args:
    """Wrapper to executable fmdt-detect.


    
    """

    # Wrap up all of the arguments into a dictionary
    detect_args, visu_args = fmdt.args.detect_args(vid_in_path, vid_in_start, vid_in_stop, 
        vid_in_skip, vid_in_buff, vid_in_loop, vid_in_threads, light_min, light_max, 
        ccl_fra_path, ccl_fra_id, mrp_s_min, mrp_s_max, knn_k, knn_d, knn_s, trk_ext_d,
        trk_ext_o, trk_angle, trk_star_min, trk_meteor_min, trk_meteor_max, trk_ddev, 
        trk_all, trk_bb_path, trk_mag_path, log_path, trk_out_path, log
    )

    # Spit out the commandline
    args = fmdt.args.handle_detect_args(**detect_args)

    if trk_out_path is None:
        if log:
            print(f"Executing cmd: {' '.join(args)}")
        subprocess.run(args)
    else:
        with open(trk_out_path, 'w') as outfile:
            if log:
                print(f"Executing cmd: {' '.join(args)}")
            subprocess.run(args, stdout=outfile)
    
    # And return the Args object that keeps track of the detect call
    if not trk_out_path is None:
        out = fmdt.args.Args(fmdt.core.extract_all_information(trk_out_path), detect_args, visu_args)
    else:
        out = fmdt.args.Args(detect_args=detect_args, visu_args=visu_args)
    
    return out


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

# Launch multiple processes of 