"""Class to handle the ground truth of a video

HumanDetections are loaded in with a video name that is completely
independent of the path. Users can set the fmdt variables WATEC6_DIR
and WATEC12_DIR to execute database tests
"""

import pandas as pd
import math
import fmdt.core
import fmdt.utils
import fmdt.args
from fmdt.core import TrackedObject
import numpy as np
import os
from termcolor import colored
from deprecated import deprecated

WATEC6_DIR:  str = "./"
WATEC12_DIR: str = "./"

class HumanDetection:

    GROUND_TRUTH = None

    def __init__(
            self,
            video_name: str,
            start_frame: int,
            end_frame: int,
            start_x: float,
            start_y: float,
            end_x: float,
            end_y: float
        ):

        self.video_name = video_name
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y

    def __str__(self) -> str:
        return (
            f"""({self.video_name}, f0: {self.start_frame}, fT: {self.end_frame}, pos0: ({self.start_x}, {self.start_y}), posT: ({self.end_x}, {self.end_y}))"""
        )

    def __lt__(self, other):
        return self.video_name < other.video_name
    
    def is_draco_6(self) -> bool:
        """Return true if part of the Draconids6mm series"""
        # vid_name = self.video_name.split("/")[-1]
        v, _ = fmdt.utils.decompose_video_filename(self.video_name)
        return "Draconids-6mm" in v 
    
    def is_draco_12(self) -> bool:
        """Return true if part of the Draconids6mm series"""
        # vid_name = self.video_name.split("/")[-1]
        v, _ = fmdt.utils.decompose_video_filename(self.video_name)
        return "Draconids-12mm" in v 
    
    def delta_x(self) -> float:
        """Displacement in the x_axis direction"""
        return self.end_x - self.start_x
    
    def delta_y(self) -> float:
        """Displacement in the y direction"""
        return self.end_y - self.start_y
    
    def displacement(self) -> tuple[float, float]:
        return (self.delta_x(), self.delta_y())
    
    def lifetime(self) -> tuple[int, int]:
        return (self.start_frame, self.end_frame)
    
    def nframes_alive(self) -> int:
        return self.end_frame - self.start_frame

    def slope(self) -> float:
        if self.delta_x() == 0:
            return float("inf")
        return self.delta_y() / self.delta_x()
    
    def direction(self) -> float:
        """Return the angle of the displacement vector of this meteor. Units are radians"""
        return math.atan2(self.delta_y(), self.delta_x())
    
    def dx(self) -> float:
        return self.delta_x() / self.nframes_alive()
    
    def interpolate_pos(self, frame_n: int) -> tuple[float, float]:
        f_prime = frame_n - self.start_frame
        xi = self.start_x + (self.dx() * f_prime)
        yi = self.start_y + (self.dx() * self.slope()) * f_prime
        return (xi, yi)

    def is_detected_in_list(self, tracking_list: list[TrackedObject]) -> bool:

        # keep only meteors
        # detected_m = [m for m in tracking_list if m.is_meteor()]

        for tracked in tracking_list: 
            if are_objects_the_same(self, tracked):
                return True

        return False
    
    def test_detection_vary_light(
            self,
            vid: str,
            offset: int = 25,
            light_min_start: int = 150,
            light_min_end: int = 230,
            k_trials: int = 10,
            log: bool = False
        ):

        return vary_light_intervals(
            vid=vid,
            truth=self,
            offset=offset,
            light_min_start=light_min_start,
            light_min_end=light_min_end,
            k_trials=k_trials,
            log=log
        )
    

    def detect(self, args: fmdt.args.Args) -> bool:
        """Paired up with an Args object, frun with fmdt-detect and 
        see if this Truth is registered"""
        res = args.detect()
        return is_meteor_detected(self, res.tracking_list)

    def to_alsoc_format(self) -> str:
        """Convert a HumanDetection into a string specified by the format:

            "{otype} {fbeg} {xbeg} {ybeg} {fend} {xend} {yend}\n"

        """
        return f"meteor {self.start_frame} {self.start_x} {self.start_y} {self.end_frame} {self.end_x} {self.end_y}\n"

    @staticmethod
    def from_pd_row(row: pd.Series, dir_prepend = ""):
        # if dir_prepend[-1] != "/":
            # dir_prepend = dir_prepend + "/"
        return HumanDetection(dir_prepend + row["video_name"],
                            int(row["start_frame"]),
                            int(row["end_frame"]),
                            float(row["start_x"]),
                            float(row["start_y"]),
                            float(row["end_x"]),
                            float(row["end_y"]))

    @staticmethod
    def from_alsoc_format(video_name, alsoc: str):

        lst = alsoc.strip().split()

        return HumanDetection(video_name, start_frame=int(lst[1]), start_x=float(lst[2]), start_y=float(lst[3]),
                              end_frame=int(lst[4]), end_x=float(lst[5]), end_y = float(lst[6]))



    @deprecated(version="0.25.0", reason="We should load in our GroundTruth's with the fmdt.load_gt6() and fmdt.load_gt12() functions")
    @staticmethod
    def init_ground_truth(database_filename: str, video_db_dir: str = "./"):
        """"""
        HumanDetection.GROUND_TRUTH = read_human_detection_csv(database_filename, video_db_dir) 
        return read_human_detection_csv(database_filename, video_db_dir)
    
def load_meteors_file(filename: str) -> list[HumanDetection]:
    """Load in a meteors file (ex: https://github.com/alsoc/fmdt/blob/develop/validation/2022_05_31_tauh_34_meteors.txt)
    as a list of `HumanDetection`"""

    with open(filename) as file:
        lines = file.readlines()

        out = [HumanDetection.from_alsoc_format("demo.mp4", l) for l in lines]

    return out

def save_meteors_file(filename: str, meteors: list[HumanDetection]):

    with open(filename, "w") as file:

        for m in meteors:
            file.write(m.to_alsoc_format())


# Verite de terrains for a bunch of individually tracked meteors
class GroundTruth:

    def __init__(self, csv: str, vid_dir: str = './'):
        self.vid_dir = vid_dir

        self.meteors = read_human_detection_csv(csv, vid_dir)

    def __str__(self) -> str:
        return f"GroundTruth with {len(self.meteors)} detections, {self.n_unique_videos()} unique videos, and db dir:\n\t{self.vid_dir}"
    
    def __len__(self) -> int:
        return len(self.meteors)
    
    def __getitem__(self, key):
        return self.meteors[key]

    def n_unique_videos(self) -> int:
        return len(self.vids())

    def try_command(self, args: fmdt.args.Args) -> list[bool]:
        """Take a set of parameters defined by `args` and apply it to every meteor in this database.
        
        Return a list of booleans that are true if the corresponding meteor was
        detected. 
        """
        def try_comm(m: HumanDetection) -> bool:

            args.detect_args.vid_in_path = m.video_name

            print(f"Trying args on video {args.vid()}")
            
            res = args.detect()
            is_detected = is_meteor_detected(m, res.trk_list)
            if not is_detected:
                print(f"{res.args.detect_args.cmd()} {colored('unsuccessful', 'red')}")
            else:
                print(f"{res.args.detect_args.cmd()} {colored('successful', 'green')}")
            
            return is_detected

        # return [try_comm(m) for m in self.meteors if os.path.exists(m.video_name)]
        return [try_comm(m) for m in self.meteors]
    
    def vids(self) -> list[str]:
        """Return the list of unique videos that appear in this database"""
        return set([m.video_name for m in self.meteors])

    def test_span(self, light_min_min, light_min_max, diff):
        # Record the pairs that are successful, and the number of meteors detected 
        
        # n = (light_min_min - light_min_max) // diff
        print(f"test_span({light_min_min}, {light_min_max}, {diff})")

        min_max = []
        dets = []
        successes = []

        n = (light_min_max - light_min_min) / diff + 1

        # d_args = {
        #     "trk_out_path": "trk.txt",
        #     "trk_bb_path": "bb.txt",
        #     "timeout":  1
        # }

        args = fmdt.args.detect_args(timeout=0.5)

        for lmin in np.linspace(light_min_min, light_min_max, int(n)):

            # Get the list
            args.detect_args.light_min = lmin
            args.detect_args.light_max = lmin + diff 

            success_list = self.try_command(args)

            ndets = sum(success_list)

            min_max.append((lmin, lmin + diff)) 
            dets.append(ndets)
            successes.append(success_list)

        return min_max, dets, successes
    
    def draw_heatmap(self, lmin_min, lmax_max, n_intervals):

        successes = []
        diff = (lmax_max - lmin_min) / (n_intervals)

        min_max, _, successes = self.test_span(lmin_min, lmax_max - diff, diff)

        plot_gt(min_max, successes)


import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

def plot_gt(minmax: list[tuple[float, float]], successes: list[list[bool]]):

    lmin_min = minmax[0][0]
    lmin_max = minmax[-1][1]

    _, ax = plt.subplots()
    num_gt = len(successes[0])
    
    print(f"Num intervals: {len(minmax)}")
    print(f"Num ground truths: {num_gt}")

    y_ticks = []

    for i in range(len(minmax)):
        lmin = minmax[i][0]
        lmax = minmax[i][1]
        y_ticks.append(lmin)
        h = lmax - lmin
        w = 1
        print(f"lmin: {lmin}")

        # Now iterate horizontally
        for id in range(num_gt):
            if successes[i][id]:
                # print("Rect")
                ax.add_patch(Rectangle((id, lmin), w, h, facecolor = "green"))
            else:
                ax.add_patch(Rectangle((id, lmin), w, h, facecolor = "black"))

    y_ticks.append(lmin_max)

    plt.xlim([0, num_gt])
    plt.ylim([lmin_min, lmin_max])
    plt.yticks(y_ticks)
    plt.show()

# for d in range(len(MIN_MAX)):
#     plot_gt(MIN_MAX[d], SUCCESS[d])


# I want a function that automatically draws that heat map given lmin_min, lmin_max, and n




# Take a row in a csv file from https://docs.google.com/spreadsheets/d/1yYsMy0nnLAsqzTYOoEjof00wVu6oP91vCiLS7orxMpg/edit#gid=365172110
# and convert it to a HumanDetection object
def csv_to_human(csv_row: str) -> HumanDetection:
    entries = csv_row.split(',')
    return HumanDetection(entries[0],
                          int(entries[1]),
                          int(entries[2]),
                          float(entries[3]),
                          float(entries[4]),
                          float(entries[5]),
                          float(entries[6]))

# Take a single row of a pandas data frame of the csv data and return
# a python HumanDetection object
def df_row_to_human(row: pd.Series, dir_prepend: str = "") -> HumanDetection:

    # This function is performing NOOOO sanity checks
    # like do any of these fields even actually exist 
    # in our data frame??

    if dir_prepend[-1] != "/":
        dir_prepend = dir_prepend + "/"

    return HumanDetection(dir_prepend + row["video_name"],
                          int(row["start_frame"]),
                          int(row["end_frame"]),
                          float(row["start_x"]),
                          float(row["start_y"]),
                          float(row["end_x"]),
                          float(row["end_y"]))

def read_human_detection_csv(csv_filename: str, db_dir: str = "") -> list[HumanDetection]:
    df = pd.read_csv(csv_filename)
    return [df_row_to_human(df.iloc[i], db_dir) for i in range(len(df.index))]

def init_ground_truth(csv_filename: str = "human_detections.csv", vid_db_dir: str = "./") -> GroundTruth:
    return GroundTruth(csv=csv_filename, vid_dir=vid_db_dir)


# GROUND_TRUTH : list[HumanDetection] = None

# def init_ground_truth(database_file: str) -> list[HumanDetection]:
#     super(GROUND_TRUTH) = read_human_detection_csv(database_file)
#     return read_human_detection_csv(database_file)

# GROUND_TRUTH = read_human_detection_csv("human_detections.csv")

def is_meteor_detected(meteor: HumanDetection, tracking_list: list[TrackedObject]) -> bool:

    if tracking_list is None:
        return False

    # keep only meteors
    detected_m = [m for m in tracking_list if m.is_meteor()]

    for tracked in detected_m: 
        if are_objects_the_same(meteor, tracked):
            return True

    return False 

def are_objects_the_same(meteor: HumanDetection, tracked_obj: TrackedObject, log: bool = False) -> bool:
    """Check if a HumanDetected meteor is the same as a tracked obj
    
    A tracked object is a dictionary with keys:
        start_frame,
        end_frame,
        start_x,
        end_x,
        start_y,
        end_y 
    """

    # Are the lifetimes the same???
    # ====================== Lifetime ===========================
    lifetime_meteor = (meteor.start_frame, meteor.end_frame)
    lifetime_object = (tracked_obj.start_frame, tracked_obj.end_frame)

    # meteor:                        [***********************]           
    # object:        [------]
    if lifetime_object[1] < lifetime_meteor[0]:
        return False
    
    # meteor:                       [***********************]           
    # object:                                                       [------]
    if lifetime_object[0] > lifetime_meteor[1]:
        return False
    
    # =============== Compare Direction ==========================
    angle_meteor_rad = meteor.direction() 
    angle_object_rad = tracked_obj.direction() 

    MAX_ANGLE_DIFF = 0.5 #!!! ARBITRARY

    if log:
        print(f"Meteor has angle: {angle_meteor_rad}")
        print(f"Object has angle: {angle_object_rad}")

    if abs(angle_meteor_rad - angle_object_rad) > MAX_ANGLE_DIFF:
        if log:
            print("Angles are too far apart")
        return False
    

    # ================ Compare Flight paths ==========================
    # At this point, there are only four cases left
    #   TRUTH      [***********************]           
    # case 1: 
    #         [------]
    #
    # case 2:
    #                                 [----------]
    #
    # case 3:
    #                [---------------]
    #
    # cse 4:
    #       [---------------------------------------]


    # We'll start with case 1 and 2
    if tracked_obj.start_frame < meteor.start_frame: # CASE 1!!!
        # Let's ALSO create a flight path for our object, starting at frame meteor.start_frame
        frames_object = [i for i in range(lifetime_meteor[0], lifetime_object[1] + 1)] 

    elif tracked_obj.end_frame > meteor.end_frame: # Case 2!!!!

        frames_object = [i for i in range(lifetime_object[0], lifetime_meteor[1] + 1)]

    elif tracked_obj.end_frame > meteor.end_frame and tracked_obj.start_frame < meteor.start_frame: # Case 4!!!!

        frames_object = [i for i in range(lifetime_meteor[0], lifetime_meteor[1] + 1)]

    else: # Case 3
        frames_object = [i for i in range(lifetime_object[0], lifetime_object[1] + 1)]

    # Now we want to compare the two flight paths!
    # TODO choisir judiciement un epsilon
    MAX_DIST = 10 # ????????????????????????????????????????????????? 

    # If the any two points in the flight path are too far away, then they are not the 
    # same meteor.
    for f in frames_object:

        pos_meteor = meteor.interpolate_pos(f) 
        pos_object = tracked_obj.interpolate_pos(f - 1)

        # print(f"f: {f}, pos_m: {meteor.interpolate_pos(f)}, pos_o: {tracked_obj.interpolate_pos(f)}")

        # print(pos_meteor)
        # print(po)

        sqr = lambda x : x * x

        dist = math.sqrt(sqr(pos_object[0] - pos_meteor[0]) + sqr(pos_object[1] - pos_meteor[1]))

        if dist > MAX_DIST:
            # print(f"Position at frame {f} is too far apart (dist: {dist})")
            return False
        
    return True
        

def vary_light_intervals(
        vid: str,
        truth: HumanDetection,
        offset: int,
        light_min_start: int,
        light_min_end: int,
        k_trials: int,
        log: bool = False
    ) -> list[fmdt.args.Args]:
    """Vary light min and light max to try and detect the truth
    
    Return a list of args that succesfully detected this truth
    """

    args = []

    for lmin in np.linspace(light_min_start, light_min_end, k_trials, dtype=int):


        light_min = int(lmin)
        light_max = light_min + offset

        track_file = "tracks.txt"
        track_bb_path = "track_bb.txt"

        vname, ext = fmdt.utils.decompose_video_filename(vid)
        vname = f"{vname}_off{offset}"

        res = fmdt.detect(vid, 
                        trk_out_path=track_file,
                        log=True,
                        light_min=light_min,
                        light_max=light_max,
                        trk_all=True,
                        trk_bb_path=track_bb_path)

        if len(res.tracking_list) != 0:

            if not os.path.isdir(vname):
                os.mkdir(vname)

            if truth.is_detected_in_list(res.tracking_list):
                addon = "_detected"
                if truth.is_detected_in_list([t for t in res.tracking_list if t.is_meteor()]):
                    addon = f"{addon}_as_meteor"
                    args.append(res)
            else:
                addon = ""

            fmdt.visu(vid, track_file, track_bb_path, f"{vname}/lmin{light_min}_lmax{light_max}{addon}.{ext}", show_id=True)

        if log: 
            meteors = [m for m in res.tracking_list if m.is_meteor()]
            for m in meteors:
                print(m)

    return args

def main() -> None:
    # dets = read_human_detection_csv("human_detection.csv")
    # for d in dets:
    #     print(d)

    m = HumanDetection("demo.mp4", 180, 184, 797.2, 459.7, 810.7, 482.0)

    tracking_list = fmdt.core.extract_all_information("demo.txt")
    meteors = [obj for obj in tracking_list if obj.is_meteor()]

    # print(m)
    # print(tracking_list)

    # for obj in tracking_list:
        # print(are_objects_the_same(m, obj))

    obj_to_hum = lambda obj, name: HumanDetection(name, obj.start_frame, obj.end_frame, obj.start_x, obj.start_y, obj.end_x, obj.end_y)

    hums = [obj_to_hum(obj, "demo.mp4") for obj in meteors]

    # for i in range(len(hums)):
    # for i in range(5):
        # print(meteors[i])
        # print(hums[i])

    # for h in hums:
        # print(h)

    # Now let's test to see if each "human" detection was found in the tracking list!

    print(m)
    print(f"Is m detected: {is_meteor_detected(m, tracking_list)}")

    for h in hums:
        print(f"Is h: {h} detected? {is_meteor_detected(h, tracking_list)}")


    # for h in hums:
        # print(h)

    # for obj in meteors:
        # print(are_objects_the_same(hums[15], obj))

    print(len(hums))

    # print(GROUND_TRUTH)
    