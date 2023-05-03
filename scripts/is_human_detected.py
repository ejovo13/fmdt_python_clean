import fmdt
import fmdt.truth

vid = "Draconids-6mm1.00-2750-163200.avi"

ccl_hyst_lo = 186
ccl_hyst_hi = 211

human = fmdt.truth.HumanDetection(vid, 45, 59, 240, 226, 125, 264)

track = "tracks.txt"
bb    = "bb.txt"

# res = fmdt.detect(vid, ccl_hyst_lo=ccl_hyst_lo, ccl_hyst_hi=ccl_hyst_hi, trk_all=True, trk_out_path=track, trk_bb_path=bb)

# fmdt.visu(vid, track, bb, "visu.mp4", True)

# Get the tracking list
print(fmdt.extract_all_information(track))

tracking_list = fmdt.extract_all_information(track)

for t in tracking_list:
    print(t)

is_det = fmdt.truth.is_meteor_detected(human, tracking_list)
print(f"Ground truth: {human} detected in {tracking_list}? : {is_det}")