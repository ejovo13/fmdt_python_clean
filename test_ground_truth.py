"""Companion script for https://fmdt-python-clean.readthedocs.io/en/latest/howto/2_test_db/"""
import fmdt
import os

vid_dir = "DATABASE_DIR_NOT_SET"        # Path to draco6 videos on my machine
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
success_list = gt6.try_command(args)

print(success_list)
print(f"GroundTruths detected: {sum(success_list)}")