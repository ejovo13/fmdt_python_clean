import fmdt
import fmdt.utils
import numpy as np
import os
import sys
vid = None

if vid is None and len(sys.argv) < 2:
    assert False, "No video selected. Pass the path of a video as an argument or change the variable `vid` in this script"

for lmin in np.linspace(190, 225, 10, dtype=int):

    offset    = 50 
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
                    trk_star_min=20,
                    # trk_meteor_min=mmin,
                    # knn_s=knns,
                    # knn_k=knnk,
                    trk_bb_path=track_bb_path)

    if len(res.tracking_list) != 0:

        if not os.path.isdir(vname):
            os.mkdir(vname)
        fmdt.visu(vid, track_file, track_bb_path, f"{vname}/lmin{light_min}_lmax{light_max}.{ext}")
    meteors = [m for m in res.tracking_list if m.is_meteor()]
    for m in meteors:
        print(m)
    # print(meteors)

