"""Arguments Class to store shared parameters when calling a chain of .detect(args).visu().split()"""
import fmdt.api
import fmdt.core
import shutil
import subprocess


class Args:
    """Args keeps track of a configuration of parameters for all of fmdt's executables

    Upon a call to `fmdt.detect()`, an Args object is returned that remembers the configuration
    used to execute fmdt-detect. We can subsequently use the Args object as an interface to
    directly calling fmdt-visu, without having to respecify some of the more specific arguments.

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
            tracking_list: str | None = None, 
            detect_args: dict | None = None
        ):

        self.tracking_list = tracking_list
        self.detect_args = detect_args

    # We should change this to print out only the arguments that are not none
    # def __str__(self) -> str:
    #     if not self.detect_args:
    #         f"detect_args:"
    
    
    def detect(self):
        """OOP Interface to calling fmdt.api.detect()"""

        # Make sure the detecting arguments are not none
        if self.detect_args is None:
            self.detect_args = default_detect_args()
        
        # Convert the list of detect args to a single command
        args = fmdt.api.detect(**self.detect_args)

        if not args.detect_args["out_track_file"] is None:
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
        """OOP Interface to calling fmdt.api.visu()"""

        print("Not yet implemented")

    # Take the detect argument dictionary and write out a comma separated value string
    def detect_csv_header(self) -> str:
        header = ""
        for k in self.detect_args.keys():
            if k == "log":
                continue
            header = header + f"{k},"

        return header[:-1]

    def detect_to_csv_row(self) -> str:
        csv = ""
        for v in self.detect_args.values():
            if v is None:
                csv = csv + ","
            else:
                csv = csv + f"{str(v)},"
        
        # Drop the last comma
        return csv[:-1]
    
    def get_tracking_list(self) -> list[dict]:
        assert not self.detect_args["out_track_file"] is None, "Out track file not stored"

        return fmdt.core.extract_all_information(self.detect_args["out_track_file"])

    # Write the dictionary of fmdt-detect arguments to a csv file
    # def detect_to_csv(self, csv_filename) -> None:

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
        out_track_file: str | None = None,
        log: bool = False
    ) -> dict:
    """Convert the parameters used in fmdt.detect into a dictionary"""

    return {
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

def detect_args_to_cmd(args: dict) -> list[str]:
    return handle_detect_args(**args)            

    
def main() -> None:
    a = Args()
    # a.detect_args = default_detect_args()
    a.detect_args = detect_args(vid_in_path="demo.mp4")
    print(a.detect_csv_header())
    print(a.detect_to_csv_row())