# Start implementing the functions needed to check fmdt

import fmdt
import fmdt.truth

og = "2022_05_31_tauh_34_meteors.mp4"

args = fmdt.detect_args(trk_out_path="trk.txt")
meteors = fmdt.truth.load_meteors_file("meteors.txt", "2022_05_31_tauh_34_meteors.mp4")

print(meteors)

v = fmdt.Video(og, fmdt.VideoType.WINDOW)
v.evaluate_args(args, meteors)

print(v)
print(v.full_path())
print(v.exists())

v.detect()

print(fmdt.load_config())