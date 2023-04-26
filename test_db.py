"""Load in a data base stored in DATA_BASE_FILE


"""
import fmdt
import fmdt.truth
import fmdt.args
# import pandas as pd
from os import listdir


DATA_BASE_FILE = "human_detections.csv"
# DATA_BASE_FILE = "human_detection.csv"

humans = fmdt.HumanDetection.init_ground_truth(DATA_BASE_FILE)

# file = "Draconids-6mm1.14-1400-170300.avi"

# meteors_in_file = [m for m in humans if m.video_name == file]

# print(humans)

# for h in humans:
#     print(h)

# print(meteors_in_file)
# for m in meteors_in_file:
#     print(m)

# Now specify a directory that we want to test against our database
watec6  = "/home/ejovo/Videos/Watec6mm"
watec12 = "/home/ejovo/Videos/Watec12mm"
# dir = watec12
dir = watec6

is_video = lambda x : x[-3:] == "avi" or x[-3:] == "mp4"
entries = listdir(dir)
entries = [v for v in entries if is_video(v)]

def get_meteors(vid: str) -> bool:
    return [m for m in humans if m.video_name == vid]

def has_meteors(vid: str) -> bool:
    return len(get_meteors(vid)) > 0

ground_truths = [get_meteors(video) for video in entries if has_meteors(video)]

print(f"Detected {len(ground_truths)} videos with ground truth meteors")

successful_args = []

MAX_ITER = 100 
i = 0

for truth_list in ground_truths: 
    # most times theres only one element in this list

    if i >= MAX_ITER:
        break
    
    i += 1
    args = []

    for truth in truth_list:
        full_vid_name = dir + "/" + truth.video_name
        print(f"Processing video: {full_vid_name}")

        args.append(truth.test_detection_vary_light(full_vid_name,
                                                    k_trials = 10))
    
    successful_args.append(args)

print(successful_args)

flattened_args = []

for video in successful_args:
    for meteor in video:
        for args in meteor:
            # print(f"args: {args} detected meteor!")
            flattened_args.append(args)
        
for a in flattened_args:
    print(a)

fmdt.args.list_args_to_csv(flattened_args, "database_6mm.csv")
# fmdt.args.list_args_to_csv(flattened_args, "database_12mm.csv")