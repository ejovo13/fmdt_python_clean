"""Demonstration to detect, visualize, and split a video

"""

import fmdt

in_video  = "demo.mp4"
# in_video  = "window_3.mp4"
tracks    = "demo_tracks.txt"
bbs       = "demo_bbs.txt"
visu      = "demo_visu.mp4"

fmdt.detect(vid_in_path=in_video, out_track_file=tracks, trk_bb_path=bbs, trk_all=True, log=True)
fmdt.visu(in_video=in_video, in_track_file=tracks, in_bb_file=bbs, out_visu_file=visu, show_id=True)
# fmdt.split_video_at_meteors(visu, tracks, 5, 5, overwrite=True, exact_split=True, log=True)

# Now count the number of meteors detected
print(f"Count (meteors): {fmdt.count(tracks)}")
print(f"Count (all): {fmdt.count(tracks, all=True)}")
print(f"Count (meteors + stars): {fmdt.count(tracks, stars=True, meteors=True)}")

import fmdt.args

a = fmdt.args.default_detect_args()
b = fmdt.args.detect_args(vid_in_path=in_video, trk_bb_path=bbs, out_track_file=tracks)
print(a)
print(b)

# fmdt.detect(in_video, tracks, bbs)
# fmdt.visu(in_video, tracks, bbs, visu, show_id=True)
# fmdt.visu("window_3.mp4", "window_3_tracks.txt", "window_3_bbs.txt", "window_3_visu.mp4", show_id=True)
# fmdt.split_video_at_meteors(visu, tracks, 5, 5, overwrite=True, exact_split=True, log=True)
# fmdt.split_video_at_meteors(visu, tracks, 5, 30, overwrite=True, log=True)
# fmdt.split_video_at_meteors("window_3_visu.mp4", "window_3_tracks.txt", 25, 25, overwrite=False)

# fmdt.utils.extract_video_frames("window_3.mp4", 1000, 1200, "test.mp4")

# TODO: Improve the api to save information between calls.
# It would be really nice to take the above block of code and 
# convert it into
#
# (
#     fmdt
#     .detect(in_video, tracks, bbs)
#     .visu()
#     .split()
# )
#
#