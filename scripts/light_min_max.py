import fmdt
import fmdt.utils
import numpy as np
import os
import sys
import fmdt.truth

# dir = "/run/media/ejovo/Seagate Portable Drive/Meteors/Watec12mm/Meteor/"

# name = "Draconids-12mm2.00.09-1450-202900.avi"
# vid = "Draconids-6mm1.00-2750-163200.avi"; human = fmdt.truth.HumanDetection(vid, 45, 59, 240, 226, 125, 264)
vid = "draco1.avi"; human = fmdt.truth.HumanDetection(vid, 45, 59, 240, 226, 125, 264)
# vid = "Draconids-6mm1.05-0750-164200.avi"; human = fmdt.truth.HumanDetection(vid, 16, 26, 12, 339, 4, 360)
# vid = "Draconids-6mm1.14-1400-170300.avi"; human = fmdt.truth.HumanDetection(vid, 11, 24, 11, 233, 14, 273)
# vid = "Draconids-6mm1.20-2350-171600.avi" ; human = fmdt.truth.HumanDetection(vid, 22, 38, 232, 368, 237, 396)

# vid = dir + name

if vid is None and len(sys.argv) < 2:
    assert False, "No video selected. Pass the path of a video as an argument or change the variable `vid` in this script"

human.test_detection_vary_light(vid, offset=25, light_min_start=150, light_min_end=235, k_trials=15, log=True)
