import fmdt

vid = "demo.mp4"
track = "track.txt"
bb = "bb.txt"
visu = "demo_visu.mp4"

args = fmdt.detect(vid_in_path=vid, trk_out_path=track, trk_bb_path=bb, trk_all=True)
args.visu()

# fmdt.split_video_at_meteors(visu, track, 5, 5, overwrite=True, exact_split=True)