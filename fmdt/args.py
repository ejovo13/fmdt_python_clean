"""Arguments Class to store shared parameters when calling a chain of .detect(args).visu().split()"""
import fmdt.api
import shutil

class Args:

    def __init__(self, tracking_list, detect_args: dict | None = None):
        self.tracking_list = tracking_list
        self.detect_args = detect_args
    
    @classmethod
    def detect(self):

        # Make sure the detecting arguments are not none
        if self.detect_args is None:
            self.detect_args = self.default_detect_args()
        
        # Convert the list of detect args to a single command

        return fmdt.api.detect(**self.detect_args)

    def visu(
            self,
            vid_in_path: str | None = None,
            vid_in_start: int | None = None,
            vid_in_stop:  int | None = None,
            vid_in_threads: int | None = None,
            trk_path: str | None = None,
            trk_bb_path: str | None = None,
            trk_id: bool | None = None,
            trk_nat_num: bool | None = None,
            trk_only_meteor: bool | None = None,
            gt_path: str | None = None,
            vid_out_path: str | None = None
        ):

        print("Not yet implemented")
    


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
    out_track_file: str | None = None,
    log: bool = False
) -> dict:

    detect_args = {
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
        "out_track_file": out_track_file 
    }

    return detect_args


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
        "out_track_file": None
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
    out_track_file: str | None = None,
    log: bool = False

) -> list[str]:

    fmdt_detect_exe = shutil.which("fmdt-detect")
    fmdt_detect_found = not fmdt_detect_exe is None
    assert fmdt_detect_found, "fmdt-detect executable not found"
    args = [fmdt_detect_exe, "--vid-in-path", vid_in_path]

    if not vid_in_skip is None:
        args.extend(["--vid-in-skip", vid_in_skip])

    if vid_in_buff:
        args.append("--vid-in-buff")

    if not vid_in_threads is None:
        args.extend(["--vid-in-threads", vid_in_threads])

    if not light_min is None:
        args.extend(["--ccl-hyst-lo", light_min])

    if not light_max is None:
        args.extend(["--ccl-hyst-hi", light_max])

    if not ccl_fra_path is None:
        args.extend(["--ccl_fra_path", ccl_fra_path])

    if not ccl_fra_id is None:
        args.extend(["--ccl-fra-id"])

    if not mrp_s_min is None:
        args.extend(["--mrp-s-min", mrp_s_min])

    if not mrp_s_max is None:
        args.extend(["--mrp-s-max", mrp_s_max])

    if not knn_k is None:
        args.extend(["--knn-k", knn_k])

    if not knn_d is None:
        args.extend(["--knn-d", knn_d])

    if not knn_s is None:
        args.extend(["--knn-s", knn_s])

    if not trk_ext_d is None:
        args.extend(["--trk-ext-d", trk_ext_d])

    if not trk_ext_o is None:
        args.extend(["--trk-ext-o", trk_ext_o])

    if not trk_star_min is None:
        args.extend(["--trk-star-min", trk_star_min])

    if not trk_meteor_min is None:
        args.extend(["--trk-meteor-min", trk_meteor_min])

    if not trk_meteor_max is None:
        args.extend(["--trk-meteor-max", trk_meteor_max])

    if not trk_ddev is None:
        args.extend(["--trk-ddev", trk_ddev])

    if trk_all:
        args.append("--trk-all")

    if not trk_mag_path is None:
        args.extend(["--trk-mag-path", trk_mag_path])

    if not log_path is None:
        args.extend(["--log-path", log_path])

    if not trk_angle is None:
        args.extend(["--trk-angle", trk_angle])

    if not trk_star_min is None:
        args.extend(["--trk-star-min", trk_star_min])

    if not vid_in_start is None:
        args.extend(["--vid-in-start", vid_in_start])

    if not vid_in_stop is None:
        args.extend(["--vid-in-stop", vid_in_stop])

    if not trk_bb_path is None:
        args.extend(["--trk-bb-path", trk_bb_path])

    if not vid_in_loop is None:
        args.extend(["--vid-in-loop", vid_in_loop])

    if not log_path is None:
        args.extend(["--log-path", log_path])

    return args

def detect_args_to_cmd(args: dict) -> list[str]:
    return handle_detect_args(**args)            

    
