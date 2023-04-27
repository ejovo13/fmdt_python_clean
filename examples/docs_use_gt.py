"""Tutorial to use the GroundTruth class of fmdt.truth.GroundTruth"""

import fmdt
import fmdt.truth

# We need to define the directory where our GroundTruth videos are found.

vid_dir12 = "/home/ejovo/Videos/Watec12mm"
vid_dir6  = "/home/ejovo/Videos/Watec6mm"

csv12 = "./human_detections_draco12.csv"
csv6  = "./human_detections_draco6.csv"

# We can create a new `GroundTruth` object - a list of `HumanDetection` paired
# with useful functions - two ways

gt12 = fmdt.truth.GroundTruth(csv=csv12, vid_dir=vid_dir12)
gt6  = fmdt.truth.GroundTruth(csv=csv6,  vid_dir=vid_dir6)

print(type(gt12))
print(gt12)

print(type(gt6))
print(gt6)

# We can create an Args and run that command across all the 
# videos in our database with GroundTruth.try_command

d_args = {
    "light_min": 251,
    "light_max": 252,
    "trk_out_path": "tracks.txt",
    "timeout": 1, #! Special parameter of the pyhton SUBPROCESS managing fmdt-detect
}

args = fmdt.Args(detect_args=d_args)

success = gt6.try_command(args)

print(success)
print(sum(success))