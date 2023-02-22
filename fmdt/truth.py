"""Class to handle the ground truth of a video"""

import pandas as pd
import math
import fmdt.core
from fmdt.core import TrackedObject

class HumanDetection:

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
            f"""({self.video_name}, f0: {self.start_frame}, fT: {self.end_frame}, pos0: ({self.start_x}, {self.end_x}), posT: ({self.start_y}, {self.end_y}))"""
        )
    
    # def __repr__(self) -> str:
        # return self.__str__()


    # I want to convert a csv of truth values into a HumanDetection object

    # Ultimately, I will need a function that takes in a csv of truth values and converts it into 
    # a list of HumanDetection objects

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
def df_row_to_human(row: pd.Series) -> HumanDetection:

    # This function is performing NOOOO sanity checks
    # like do any of these fields even actually exist 
    # in our data frame??

    return HumanDetection(row["video_name"],
                          int(row["start_frame"]),
                          int(row["end_frame"]),
                          float(row["start_x"]),
                          float(row["start_y"]),
                          float(row["end_x"]),
                          float(row["end_y"]))

def read_human_detection_csv(csv_filename: str) -> list[HumanDetection]:
    df = pd.read_csv(csv_filename)
    return [df_row_to_human(df.iloc[i]) for i in range(len(df.index))]

def is_meteor_detected(meteor: HumanDetection, tracking_list: list[TrackedObject]) -> bool:

    # keep only meteors
    detected_m = [m for m in tracking_list if m.is_meteor()]

    for tracked in detected_m: 
        if are_objects_the_same(meteor, tracked):
            return True

    return False 

def are_objects_the_same(meteor: HumanDetection, tracked_obj: TrackedObject) -> bool:
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
    # TODO
    # ====================== Lifetime ===========================
    lifetime_meteor = (meteor.start_frame, meteor.end_frame)
    lifetime_object = (tracked_obj.start_frame, tracked_obj.end_frame)

    nframes_meteor = lifetime_meteor[1] - lifetime_meteor[0]
    nframes_object = lifetime_object[1] - lifetime_object[0]

    # meteor:                        [***********************]           
    # object:        [------]
    if lifetime_object[1] < lifetime_meteor[0]:
        return False
    
    # meteor:                       [***********************]           
    # object:                                                       [------]
    if lifetime_object[0] > lifetime_meteor[1]:
        return False
    
    # TODO compare the ratio of slopes rather than the difference
    # ====================== Slope ===========================
    slope_meteor = (meteor.end_y - meteor.start_y) / (meteor.end_x - meteor.start_x)
    slope_object = (tracked_obj.end_y - tracked_obj.start_y) / (tracked_obj.end_x - tracked_obj.start_x)

    epsilon = 0.5 # ARBITRARY AS FUCK

    if abs(slope_meteor - slope_object) > epsilon:
        return False
    

    # ====================== Flight Path ===========================
    # create the flight path
    dx_meteor = (meteor.end_x - meteor.start_x) / nframes_meteor # change in x per frame
    dx_object = (tracked_obj.end_x - tracked_obj.start_x) / nframes_object # change in x per frame

    frames_meteor    = [i for i in range(lifetime_meteor[0], lifetime_meteor[1] + 1)]

    def calculate_meteor_position(frame):
        f_prime = frame - meteor.start_frame
        xi = meteor.start_x + (dx_meteor * f_prime)
        yi = meteor.start_y + (dx_meteor * slope_meteor)
        return (xi, yi)

    # Create the flight path of the meteor, which is a list of (x, y) coordinate
    # pairs 
    positions_meteor: list[tuple[float, float]] = (
        [calculate_meteor_position(frame_i) for frame_i in frames_meteor]
    )

    # Now we've calculated our flight path.
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

    def calculate_object_position(frame):
        f_prime = frame - meteor.start_frame
        xi = tracked_obj.start_x + (dx_object * f_prime)
        yi = tracked_obj.start_y + (dx_object * slope_object)
        return (xi, yi)

    # Create the flight path of the object
    positions_object = [calculate_object_position(frame) for frame in frames_object]
    
    # Now we want to compare the two flight paths!
    # TODO choisir judiciement un epsilon
    MAX_DIST = 5 # ????????????????????????????????????????????????? 
    
    # If the any two points in the flight path are too far away, then they are not the 
    # same meteor.
    for i in range(len(frames_object)):

        f = frames_object[i]
        
        pos_meteor = positions_meteor[i]
        pos_object = positions_object[i]

        sqr = lambda x : x * x

        dist = math.sqrt(sqr(pos_object[0] - pos_meteor[0]) + sqr(pos_object[1] - pos_meteor[1]))

        if dist > MAX_DIST:
            return False
        
    return True
        

# I want to compare the human results with the automatic results.

# First thing I need is a pipeline to get the automatic results

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
    