import fmdt
# import fmdt.truth
# import pandas as pd

# df = pd.read_csv("human_de ")
# humans = fmdt.truth.read_human_detection_csv("human_detections.csv")

# fmdt.truth.HumanDetection.init_ground_truth("human_detection.csv")
humans = fmdt.HumanDetection.init_ground_truth("human_detections.csv")

file = "Draconids-6mm1.14-1400-170300.avi"

meteors_in_file = [m for m in humans if m.video_name == file]

# print(humans)

for h in humans:
    print(h)

print(meteors_in_file)
for m in meteors_in_file:
    print(m)