"""
API to call fmdt executables. Assumes that fmdt-detect and other executables
are on the system path
"""

import shutil
import subprocess
import fmdt.core
import fmdt.utils
import fmdt.args

def count(trk_bb_path: str, stars: bool = False, meteors: bool = True, noise: bool = False, all: bool = False) -> int:
    """Count the number of meteors detected in a tracks_bb file"""
    if all:
        stars = True
        meteors = True
        noise = True

    tracked = fmdt.core.extract_key_information(trk_bb_path)

    if not stars:
        tracked = [t for t in tracked if t["type"] != "star"]

    if not meteors:
        tracked = [t for t in tracked if t["type"] != "meteor"]

    if not noise:
        tracked = [t for t in tracked if t["type"] != "noise"]

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
        log_path: str | None = None,
        out_track_file: str | None = None,
        log: bool = False
    ) -> fmdt.args.Args:

    # Wrap up all of the arguments into a dictionary
    detect_args = fmdt.args.detect_args(vid_in_path, vid_in_start, vid_in_stop, 
        vid_in_skip, vid_in_buff, vid_in_loop, vid_in_threads, light_min, light_max, 
        ccl_fra_path, ccl_fra_id, mrp_s_min, mrp_s_max, knn_k, knn_d, knn_s, trk_ext_d,
        trk_ext_o, trk_angle, trk_star_min, trk_meteor_min, trk_meteor_max, trk_ddev, 
        trk_all, trk_bb_path, trk_mag_path, log_path, out_track_file, log
    )

    # Spit out the commandline
    args = fmdt.args.handle_detect_args(**detect_args)

    if out_track_file is None:
        if log:
            print(f"Executing cmd: {' '.join(args)}")
        subprocess.run(args)
    else:
        with open(out_track_file, 'w') as outfile:
            if log:
                print(f"Executing cmd: {' '.join(args)}")
            subprocess.run(args, stdout=outfile)
    
    # And return the Args object that keeps track of the detect call

    


def visu(in_video: str, in_track_file: str, in_bb_file: str, out_visu_file: str | None = None, show_id: bool = False) -> None:

    fmdt_visu_exe = shutil.which("fmdt-visu")
    fmdt_visu_found = not fmdt_visu_exe is None
    assert fmdt_visu_found, "fmdt-visu executable not found"   

    args = [fmdt_visu_exe, "--in-video", in_video, "--in-tracks", in_track_file, "--in-bb", in_bb_file] 

    if not out_visu_file is None:
        args.extend(["--out-video", out_visu_file])

    if show_id:
        args.append("--show-id")

    subprocess.run(args)