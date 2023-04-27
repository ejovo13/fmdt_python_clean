import fmdt
from termcolor import colored
# import fractions

d6 = fmdt.load_draco6(require_gt=True)
d12 = fmdt.load_draco12(require_gt=True, require_exist= True)
w = fmdt.load_window()

print(len(d6))
print(len(d12))

# Video With Detection (VWD) 

def get_vwd_ids(vids: list[fmdt.Video], light_min, light_max) -> list[int]:

    video_ids = []
    
    for v in vids:
        res = v.detect(light_min=light_min, light_max=light_max, save_df=True, timeout=1.0)
        c_res = res.check()
        trk_rate = c_res.meteor_stats()["trk_rate"]

        if c_res.meteors_detected():
            print(colored(f"{v} has tracking rate {trk_rate}", "green"))
            video_ids.append(v.id())

        else:
            print(colored(f"{v} has tracking rate {trk_rate}", "red"))

    return video_ids


# ids_245 = get_vwd_ids(d12, 245, 250) 
ids_245 = [57, 58, 62, 65, 73, 75, 77, 83, 84, 85]

# ids_215 = get_vwd_ids(d12, 215, 220)
ids_215 = [54, 56, 57, 58, 60, 62, 63, 64, 65, 92]

# ids_225 = get_vwd_ids(d12, 225, 230)
ids_225 = [57, 58, 60, 61, 62, 65, 79, 83, 89, 92]

d12_ids = set(ids_245 + ids_215 + ids_225)

print(d12_ids)
print(len(d12_ids))

# Let's first select the 8 videos that are detected

# print(get_vwd_ids(d6, 253, 255))
# print(get_vwd_ids(d12, ))

import fmdt.db

v = fmdt.db.get_video_by_id(2)

print(v)

def discrete_video_measure(vid: fmdt.Video, interval: tuple[int, int], step_size = 5, log = False) -> tuple[int, int]: 
    """Returns the number of successes (n_successes, total_intervals)"""

    assert vid.exists(), f"Video {vid} does not exist on disk. Check your local config with fmdt.local_info() and fmdt.load_config()"
    assert interval[0] >= 0, f"light_min ({interval[0]}) must be >= 0"
    assert interval[1] <= 255, f"light_max ({interval[1]}) must be <= 0"

    gap = interval[1] - interval[0]
    
    assert step_size <= gap

    total_intervals = 0
    n_successes  = 0

    for lmin in range(interval[0], interval[1] - step_size + 1, step_size):
        print(colored(f"[{lmin}, {lmin + step_size}]", "red"))
        c_res = vid.detect(light_min=lmin, light_max=lmin + step_size, save_df=True, log=log).check()
        total_intervals += 1

        if c_res.meteors_detected():
            n_successes += 1

    return n_successes, total_intervals


# REAL WORLD RESULTS

d6_video_ids = [2, 5, 6, 20, 22, 25, 29, 35, 36]

d6_detected = fmdt.db.get_video_by_ids(d6_video_ids)
d12_detected = fmdt.db.get_video_by_ids(d12_ids)



print(d6_detected)
print(len(d6_detected))

interval = (240, 255)
step_size = 1

# ======================= id: 2 ============================
v = fmdt.db.get_video_by_id(2)

# ======================== id: 5 ============================
# v = fmdt.db.get_video_by_id(5)


# ================================================================
# def num_intervals(step_size):
#    pass 

# step_sizes = [1, 2, 3, 4, 5, 15]

# res = [discrete_video_measure(v, interval, s) for s in step_sizes]

# n_success = [r[0] for r in res]
# n_intervals = [r[1] for r in res]

# ratios = []
# for i in range(len(res)):
#     ratios.append(n_success[i] / n_intervals[i])

# print(step_sizes)
# print(n_success)
# print(n_intervals)
# print(ratios)
# =========================================================================

# Now I guess we want to compare MOVEMENT statistics with TRACKING RATE

# v = fmdt.db.get_video_by_id(2)
# v = fmdt.db.get_video_by_id(5)
# print(v)

# args = {
#     "light_min": 240,
#     "light_max": 255,
#     "save_df": True
# }

# res = v.detect(**args)

# print(res.df.head())
# print(res.roa())
# print(res.mean_roa())
# print(v.compute_trk_rate(**args))

import numpy as np
import pandas as pd

def generate_data(vid: fmdt.Video, light_min_min, light_max_max):

    int_size = light_max_max - light_min_min
    
    x = np.arange(1, int_size + 1)
    f = lambda i: np.floor(int_size / i)
    total_data_points = int(np.array(list(map(f, x))).sum())

    trk_rate = np.zeros(total_data_points)
    mean_roa = np.zeros(total_data_points)
    mean_nroi = np.zeros(total_data_points)
    mean_nassoc = np.zeros(total_data_points)
    mean_mean_err = np.zeros(total_data_points)
    mean_std_dev = np.zeros(total_data_points)

    trk_rate = []
    mean_roa = []
    mean_nroi = []
    mean_nassoc = []
    mean_mean_err = []
    mean_std_dev = []
    # Now i have the number of intervals for each, but that doesnt really do anything.
    # What am i actually iterating through? 
    # Two loops

    for step_size in x:

        for lmin in range(light_min_min, light_max_max - step_size + 1, step_size):
            print(colored(f"[{lmin}, {lmin + step_size}]", "red"))
            res = vid.detect(light_min=lmin, light_max=lmin + step_size,
                               save_df=True, log=False)
            
            c_res = res.check()

            if not res.df is None:
                trk_rate.append(c_res.trk_rate())
                mean_roa.append(res.mean_roa())
                mean_nroi.append(res.mean_nroi())
                mean_nassoc.append(res.mean_nassoc())
                mean_mean_err.append(res.mean_mean_err())
                mean_std_dev.append(res.mean_std_dev())


    return pd.DataFrame({
        "trk_rate": trk_rate,
        "mean_roa": mean_roa,
        "mean_nroi": mean_nroi,
        "mean_nassoc": mean_nassoc,
        "mean_mean_err": mean_mean_err,
        "mean_std_dev": mean_std_dev
    })

def generate_data_for_videos(vids: list[fmdt.Video], light_min_min, light_max_max):

    int_size = light_max_max - light_min_min

    x = [1]
    i = 0
    while x[i] <= int_size:
        x.append(x[i] * 2)
        i += 1


    # x = np.logspace(0, np.log2(int_size), base=2)
    # f = lambda i: np.floor(int_size / i)
    # total_data_points = int(np.array(list(map(f, x))).sum()) * len(vids)

    print(x)

    # # raise AssertionError("You messed up")

    # trk_rate = np.zeros(total_data_points)
    # mean_roa = np.zeros(total_data_points)
    # mean_nroi = np.zeros(total_data_points)
    # mean_nassoc = np.zeros(total_data_points)
    # mean_mean_err = np.zeros(total_data_points)
    # mean_std_dev = np.zeros(total_data_points)
    # Now i have the number of intervals for each, but that doesnt really do anything.
    # What am i actually iterating through? 
    # Two loops

    trk_rate = []
    mean_roa = []
    mean_nroi = []
    mean_nassoc = []
    mean_mean_err = []
    mean_std_dev = []

    for vid in vids:

        for step_size in x:

            for lmin in range(light_min_min, light_max_max - step_size + 1, step_size):
                print(colored(f"[{lmin}, {lmin + step_size}]", "red"))
                res = vid.detect(light_min=lmin, light_max=lmin + step_size,
                                save_df=True, log=False, timeout=1.0)
                
                c_res = res.check()
                    
                if not res.df is None:
                    trk_rate.append(c_res.trk_rate())
                    mean_roa.append(res.mean_roa())
                    mean_nroi.append(res.mean_nroi())
                    mean_nassoc.append(res.mean_nassoc())
                    mean_mean_err.append(res.mean_mean_err())
                    mean_std_dev.append(res.mean_std_dev())

    return pd.DataFrame({
        "trk_rate": trk_rate,
        "mean_roa": mean_roa,
        "mean_nroi": mean_nroi,
        "mean_nassoc": mean_nassoc,
        "mean_mean_err": mean_mean_err,
        "mean_std_dev": mean_std_dev
    })

# df = generate_data(v, 230, 255)
# df.to_csv(f"data_{v.prefix()}.csv")

# Let's get the beast 9 videos
# vids = fmdt.db.get_video_by_ids(d6_video_ids)

# print(vids)

df = generate_data_for_videos(d12_detected, 155, 255)
df.to_csv(f"draco12_data.csv")