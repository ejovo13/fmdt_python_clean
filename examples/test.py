import fmdt

vid    = "demo.mp4"
tracks = "tracks.txt"
bb     = "bb.txt"

fmdt.detect(vid_in_path=vid, trk_out_path=tracks, trk_bb_path=bb).split()