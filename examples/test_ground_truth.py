"""Companion script for https://fmdt-python-clean.readthedocs.io/en/latest/howto/2_test_db/

    !========== Attention ============!
    You must change the d6_dir, d12_dir, and win_dir variables
    to where the videos are stored on your machine

"""
import fmdt
import time


#! ================== Need to change these variables =============== !#
d6_dir  = None # ex: "/home/ejovo/Videos/Watec6mm"
d12_dir = None #     "/home/ejovo/Videos/Watec12mm"
win_dir = None #     "/home/ejovo/Videos"
#! ================== Need to change these variables =============== !#

assert not d6_dir is None, "Change the directory to where the videos are locally stored"

fmdt.init(d6_dir, d12_dir, win_dir)
fmdt.download_csvs()

gt6 = fmdt.load_gt6()
gt12 = fmdt.load_gt12()

args = fmdt.detect_args(light_min=253, light_max=255)
success_list = gt6.try_command(args)

print(success_list)
print(f"GroundTruths detected: {sum(success_list)}")

print("Finished applying args to ground truth videos.")
time.sleep(2)

gt6.draw_heatmap(246, 255, 3)