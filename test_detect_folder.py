import os
import fmdt
import fmdt.args
import sys

# Directory whose videos you would like to view
directory = None

def print_help() -> None:
    print("Type the name of the directory you wish to process:")
    usr = input()
    # print(f"Ex: {sys.argv[0]} ~/Videos/Meteors")

if directory is None and len(sys.argv) == 1:
    print_help()
    assert False
else:
    directory = sys.argv[1]


entries = os.listdir(directory)

is_video = lambda v: v[-3:] == "mp4" or v[-3:] == "avi"

videos = [e for e in entries if is_video(e)]

# Now let's call fmdt detect one time for each video
failing_cmds = []
i = 0
for v in videos:
    # res = fmdt.detect(directory + "/" + v, light_min=150, light_max=245, trk_all=True, log=False, out_track_file="tracks.txt")
    # a = fmdt.args.video_input(directory + "/" + v)
    # a.detect_args["out_track_file"] = "tracks.txt"

    # if i > 10:
    #     break

    args = {
        "out_track_file": "tracks.txt",
        "vid_in_path": directory + "/" + v,
        "light_min": 190,
        "light_max": 235, # None of the videos fail with _just_ a light max
        "trk_all": True,
        "log": True
    }

    a = fmdt.args.Args(detect_args=args)

    fail = a.does_detect_fail(log=True)
    print(f"{v} fails? {fail}")

    if (fail):
        failing_cmds.append(" ".join(a.detect_cmd()))
    
    i = i + 1

for c in failing_cmds:
    print(c)