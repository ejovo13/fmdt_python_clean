# Use different parameters of fmdt to try and find the human detected meteor 
# of draco_0
import fmdt.truth
import fmdt
import numpy as np

vid = "Draco_0.avi"

# human = fmdt.truth.HumanDetection(vid, 45, 59, 240, 226, 125, 264)

# for x in np.linspace(25, 240):
#     # print("Running fmdt.detec")
#     res = fmdt.detect(vid, ccl_hyst_hi=255, ccl_hyst_lo=int(x), trk_out_path="draco_tmp.txt", log=True)
#     if fmdt.truth.is_meteor_detected(human, res.tracking_list):
#         print("Human meteor detected iwth ccl_hyst_lo:", x)

for x in [226, 231, 235]:
    # print("Running fmdt.detec")
    res = fmdt.detect(vid, ccl_hyst_hi=255, ccl_hyst_lo=int(x), trk_out_path="draco_tmp.txt", log=True)

    print(res.tracking_list)

vid = "draco1.avi"

for lm in np.linspace(50, 220, 10):
    res = fmdt.detect(vid, ccl_hyst_hi=225, ccl_hyst_lo=int(lm), trk_out_path="draco_tmp.txt", log=True)
    print(res.tracking_list)

    # if fmdt.truth.is_meteor_detected(human, res.tracking_list):
        # print("Human meteor detected iwth ccl_hyst_lo:", x)
