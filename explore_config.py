"""Explore the data bases stored in database_6mm and database_12mm"""

import fmdt.truth
import fmdt.args
import fmdt
import pandas as pd
from termcolor import colored


humans = fmdt.init_ground_truth("human_detections.csv", "")

h6 = [h for h in humans if h.is_draco_6()]
h12 = [h for h in humans if h.is_draco_12()]

# for h in humans:
    # print(h)
# print(len(h6))
# print(len(h12))
# print(len(humans))

ground = pd.read_csv("human_detections.csv")

w6 = fmdt.args.csv_to_list_args("database_6mm.csv")
w12 = fmdt.args.csv_to_list_args("database_12mm.csv")

# print(len(w6))
# print(len(w12))

# Get list of videos detected by w6
vid_names6 = [w.detect_args["vid_in_path"] for w in w6]
vid_names12 = [w.detect_args["vid_in_path"] for w in w12]
# print(vid_names6)

print("================")
print(" Configurations ")
print("================")

print(f"{len(set(vid_names6))} out of {len(h6)} unique videos with detections for w6")
print(f"{len(set(vid_names12))} out of {len(h12)} unique videos with detections for w12")
# w6 = pd.read_csv("database_6mm.csv")
# w12 = pd.read_csv("database_12mm.csv")
# print(w6.head())
# print(w12.head())

# Get unique videos sorted
unique_6mm = list(set(vid_names6))
unique_6mm.sort()

unique_12mm = list(set(vid_names12))
unique_12mm.sort()

print(f"w6 videos with detections:") 
print(f"\t{unique_6mm}")
print()
print(f"w12 videos with detections:")
print(f"\t{unique_12mm}")
print()

print("================")
print(" Ground Truths")
print("================")

# for h in h6[1:10]:
for h in h6:
    print(h)


# Now we want to pair up these configs (w6 and w12) with
# the ground truths (h6 and h12)

# What do I have?
# I have a list[Args] and a list[HumanDetection] 
# I want each config to be associated with an id or something
# That might come later..

FILE_DIR_6MM = "/home/ejovo/Videos/Watec6mm/"
FILE_DIR_12MM = "/home/ejovo/Videos/Watec12mm/"

# For each config, let's find out WHICH HumanDetection we detected! 
for config in w6:

    config.detect_args["vid_in_path"] = FILE_DIR_6MM + config.detect_args["vid_in_path"]
    res = config.detect()

    for i in range(len(h6)):
        if h6[i].is_detected_in_list(res.tracking_list): # Detected
            if h6[i].video_name in res.detect_args["vid_in_path"]: # And names are the same
                print(colored(f"config {config}", "red") + " found meteor " + colored(f"{h6[i]}", "blue"))

# for config in w12:

#     config.detect_args["vid_in_path"] = FILE_DIR_12MM + config.detect_args["vid_in_path"]
#     res = config.detect()

#     for i in range(len(h12)):
#         if h12[i].is_detected_in_list(res.tracking_list): # Detected
#             if h12[i].video_name in res.detect_args["vid_in_path"]: # And names are the same
#                 print(colored(f"config {config}", "red") + " found meteor " + colored(f"{h12[i]}", "blue"))

