import fmdt
import fmdt.utils
import numpy as np
import os
import sys
import fmdt.truth

# dir = "/run/media/ejovo/Seagate Portable Drive/Meteors/Watec12mm/Meteor/"

# name = "Draconids-12mm2.00.09-1450-202900.avi"
# vid = "Draconids-6mm1.00-2750-163200.avi"; human = fmdt.truth.HumanDetection(vid, 45, 59, 240, 226, 125, 264)
# vid = "Draconids-6mm1.05-0750-164200.avi"; human = fmdt.truth.HumanDetection(vid, 16, 26, 12, 339, 4, 360)
vid = "Draconids-6mm1.14-1400-170300.avi"; human = fmdt.truth.HumanDetection(vid, 11, 24, 11, 233, 14, 273)
vid = "Draconids-6mm1.20-2350-171600.avi" ; human = fmdt.truth.HumanDetection(vid, 22, 38, 232, 368, 237, 396)

# vid = dir + name

if vid is None and len(sys.argv) < 2:
    assert False, "No video selected. Pass the path of a video as an argument or change the variable `vid` in this script"

for lmin in np.linspace(150, 235, 15, dtype=int):

    offset    = 25 
    light_min = int(lmin)
    light_max = light_min + offset

    # track_file = f"tracks_{i:03}.txt"
    # track_bb_path = f"track_bb_{i:03}.txt"
    track_file = "tracks.txt"
    track_bb_path = "track_bb.txt"

    vname, ext = fmdt.utils.decompose_video_filename(vid)
    vname = f"{vname}_off{offset}"

    res = fmdt.detect(vid, 
                    out_track_file=track_file,
                    log=True,
                    light_min=light_min,
                    light_max=light_max,
                    trk_all=True,
                    # trk_star_min=20,
                    # trk_meteor_min=mmin,
                    # knn_s=knns,
                    # knn_k=knnk,
                    trk_bb_path=track_bb_path)

    if len(res.tracking_list) != 0:

        if not os.path.isdir(vname):
            os.mkdir(vname)

        if human.is_detected(res.tracking_list):
            addon = "_detected"
            if human.is_detected([t for t in res.tracking_list if t.is_meteor()]):
                addon = f"{addon}_as_meteor"
        else:
            addon = ""

        

        fmdt.visu(vid, track_file, track_bb_path, f"{vname}/lmin{light_min}_lmax{light_max}{addon}.{ext}")

    meteors = [m for m in res.tracking_list if m.is_meteor()]
    for m in meteors:
        print(m)
    # print(meteors)

