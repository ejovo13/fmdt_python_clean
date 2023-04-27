"""Companion script for https://fmdt-python-clean.readthedocs.io/en/latest/howto/2_test_db/"""
import fmdt
import os
import random

vid_dir = "/home/ejovo/Videos/Watec6mm"        # Path to draco6 videos on my machine
draco6_db = "human_detections_draco6.csv"

if not os.path.exists(vid_dir):
    print("Please specify the database directory")

assert os.path.exists(vid_dir), f"vid_dir: '{vid_dir}' not a path"
assert os.path.exists(draco6_db), f"draco6_db: '{draco6_db}' does not exist"

gt6 = fmdt.GroundTruth(csv=draco6_db, vid_dir=vid_dir)

d_args = {
    "light_min": 250,
    "light_max": 253,
    "trk_out_path": "trk.txt",
    "trk_bb_path": "bb.txt",
    "timeout": 1          # timeout in seconds for the fmdt-detect subprocess
}

args = fmdt.Args(detect_args=d_args)

args.detect_args["light_min"] = 240
args.detect_args["light_max"] = 250

# success_list = gt6.try_command(args)

# print(success_list)
# print(f"GroundTruths detected: {sum(success_list)}")

# dets = [gt6.meteors[i] for i in range(len(gt6.meteors)) if success_list[i]]
# ids  = [i for i in range(len(gt6.meteors)) if success_list[i]]


# Sample randomly in the range 

LIGHT_MIN_MIN = 230
LIGHT_MIN_MAX = 240
DIFF_MAX = 30

k_trials = 7 

# with open("gt_ids_det.csv", "a") as file:

#     for k in range(k_trials):

#         light_min  = random.randint(LIGHT_MIN_MIN, LIGHT_MIN_MAX)
#         light_diff = random.randint(1, min(255 - light_min, DIFF_MAX))

#         light_max = light_min + light_diff

#         args.detect_args["light_min"] = light_min 
#         args.detect_args["light_max"] = light_max 

#         success_list = gt6.try_command(args)

#         dets = [gt6.meteors[i] for i in range(len(gt6.meteors)) if success_list[i]]
#         ids  = [i for i in range(len(gt6.meteors)) if success_list[i]]

#         for i in ids:
#             file.write(str(i) + ",")


# Let's try to hold the interval constant, and systematically check all of the light_min values

DIFF = 5
LIGHT_MIN_MIN = 245
LIGHT_MIN_MAX = 255 - DIFF 

import numpy as np

# for k in range(k_trials):
def test_span_gt6(light_min_min, light_min_max, diff):
    # Record the pairs that are successful, and the number of meteors detected 

    min_max = []
    dets = []


    for lmin in np.linspace(light_min_min, light_min_max, 3):

        # Get the list
        args.detect_args["light_min"] = lmin
        args.detect_args["light_max"] = lmin + diff 

        success_list = gt6.try_command(args)

        ndets = sum(success_list)

        min_max.append((lmin, lmin + diff)) 
        dets.append(ndets)

    return min_max, dets

MIN_MAX = []
DETS = []

# for diff in [1, 3, 5]:
#     min_max, dets = test_span_gt6(LIGHT_MIN_MIN, LIGHT_MIN_MAX, diff)
#     MIN_MAX.append(min_max)
#     DETS.append(dets)

print(MIN_MAX)
print(DETS)

# for d in dets:
#     print(f"Detected: {d}")

# for i in ids:
#     print(i)

# We can work with a subset of the ground truth data sets if we only use

# visible = [0, 2, 3, 6, 34, 35]
visible = [0, 2, 3, 5, 6, 24, 28, 34, 35]
red_mets = [gt6.meteors[i] for i in visible]

gt_small = fmdt.GroundTruth("human_detections_draco6.csv")
gt_small.meteors = red_mets

print(len(gt_small.meteors))

def test_span_gt_small(light_min_min, light_min_max, diff):
    # Record the pairs that are successful, and the number of meteors detected 

    min_max = []
    dets = []
    successes = []


    for lmin in np.linspace(light_min_min, light_min_max, 2):

        # Get the list
        args.detect_args["light_min"] = lmin
        args.detect_args["light_max"] = lmin + diff 

        success_list = gt_small.try_command(args)

        ndets = sum(success_list)

        min_max.append((lmin, lmin + diff)) 
        dets.append(ndets)
        successes.append(success_list)

    return min_max, dets, successes

MIN_MAX = []
DETS = []
SUCCESS = []

# for diff in [1, 3, 5]:
# for diff in [5]:
#     min_max, dets, success = test_span_gt_small(LIGHT_MIN_MIN, LIGHT_MIN_MAX, diff)
#     MIN_MAX.append(min_max)
#     DETS.append(dets)
#     SUCCESS.append(success)

# print(MIN_MAX)
# print(DETS)
# print(SUCCESS)

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

def draw_heatmap(gt: fmdt.GroundTruth, lmin_min, lmax_max, n_intervals):

    min_max = []
    dets = []
    successes = []
    diff = (lmax_max - lmin_min) / (n_intervals)

    for lmin in np.linspace(lmin_min, lmax_max - diff, n_intervals):

        # Get the list
        args.detect_args["light_min"] = lmin
        args.detect_args["light_max"] = lmin + diff 

        success_list = gt.try_command(args)

        ndets = sum(success_list)

        min_max.append((lmin, lmin + diff)) 
        dets.append(ndets)
        successes.append(success_list)

    plot_gt(min_max, successes)


# draw_heatmap(gt_small, 150, 255, 2)


# draw_heatmap(gt_small, 240, 255, 15)

# draw_heatmap(gt6, 240, 255, 10)

draco12 = "human_detections_draco12.csv"
vid_dir12 = "/home/ejovo/Videos/Watec12mm"

gt12 = fmdt.GroundTruth(draco12, vid_dir12)

draw_heatmap(gt12, 150, 255, 155)