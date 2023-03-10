"""Load up a configuration of fmdt-detect commands to run, and expect to find a specific meteor"""

import fmdt.truth
import fmdt

import random

DATA_BASE_FILE = "human_detections.csv"
# DATA_BASE_FILE = "human_detection.csv"

humans = fmdt.HumanDetection.init_ground_truth(DATA_BASE_FILE)

# watec6 = None
# watec12 = None
watec6  = "/home/ejovo/Videos/Watec6mm"
watec12 = "/home/ejovo/Videos/Watec12mm"

# I actually think that I might want to 

# Need to load in the configs 
# Load them in as Args
gt12 = fmdt.init_ground_truth(vid_db_dir=watec12)
gt12.meteors = [m for m in gt12.meteors if m.is_draco_12()]


gt6 = fmdt.init_ground_truth(vid_db_dir=watec6)
gt6.meteors = [m for m in gt6.meteors if m.is_draco_6()]

print(gt6)
print(gt12)

print(gt6.meteors)

print(gt6.vids())


d_args = {
    "light_min": 221,
    "light_max": 246,
    "trk_bb_path": "bb.txt",
    "trk_out_path": "trk.txt",
    "timeout": 1
}

a = fmdt.Args(detect_args=d_args)

# Apply a single command across the entire database
# detections = gt6.try_command(a)
# print(detections)


# EXPERIMENTAL RESULTS
detections = [False, False, True, False, False, False, True, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, False, True, False, False, False]


print(f"Sum detections: {sum(detections)}")
print(gt6)

def roll_parameters():
    light_min = random.randint(0, 254)
    diff = random.randint(1, 255 - light_min)

    d_args["light_min"] = light_min
    d_args["light_max"] = light_min + diff

    det = gt6.try_command(fmdt.Args(detect_args=d_args))
    print(f"[{light_min}, {light_min + diff}] detected {sum(det)} gts")

# roll_parameters()


N_TRIALS = 05 
# N_TRIALS = 150  

# I want a list of light min and light max pairs
lm_pairs = []
gts_det  = []
lst_detections = [[]]

MAX_LIGHT_DIFF = 40
LIGHT_MIN_MIN = 150
LIGHT_MIN_MAX = 254

# ============================ ~ 20 minute run ========================
for k in range(N_TRIALS):
    light_min = random.randint(LIGHT_MIN_MIN, LIGHT_MIN_MAX)
    diff = random.randint(1, min(255 - light_min, MAX_LIGHT_DIFF))

    d_args["light_min"] = light_min
    d_args["light_max"] = light_min + diff

    # det = gt6.try_command(fmdt.Args(detect_args=d_args))
    det = gt12.try_command(fmdt.Args(detect_args=d_args))
    print(f"[{light_min}, {light_min + diff}] detected {sum(det)} gts")

    lm_pairs.append((light_min, light_min + diff))
    gts_det.append(sum(det))
    lst_detections.append(det)

# print(lm_pairs)
# print(gts_det)
# ======================================================================

# #! =============== Experimental Results ===========================
# lm_pairs = [(253, 254), (164, 176), (215, 237), (200, 214), (218, 230), (250, 253), (186, 188), (250, 255), (199, 238), (151, 190), (220, 230), (202, 214), (191, 211), (205, 227), (224, 252), (250, 253), (227, 237), (196, 235), (176, 189), (194, 219)]
# gts_det = [8, 0, 2, 0, 3, 6, 2, 6, 2, 0, 3, 1, 1, 0, 3, 6, 3, 1, 0, 0]

# # Let's try and plot this as a 3d surface?

# import matplotlib.pyplot as plt
# import matplotlib.patches as patches
# import numpy as np

lmin_lst = [l[0] for l in lm_pairs]
lmax_lst = [l[1] for l in lm_pairs]

print(lmin_lst)
print(lmax_lst)
print(gts_det)


