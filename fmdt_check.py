# Start implementing the functions needed to check fmdt

import fmdt
import fmdt.truth
import subprocess

vid = "demo.mp4"
gt_path = "meteors.txt"
trk_path= "trk.txt"

# def fmdt_check(trk_path: str, gt_path: str):

#     # Literally so simple

#     argv = ["fmdt-check", "--trk-path", trk_path, "--gt-path", gt_path]

#     subprocess.run(argv)


# # res = fmdt.detect(vid, trk_out_path=trk_path)
# # print(res)

# # fmdt_check(trk_path, gt_path)

# import os

# def evaluate_args(args: fmdt.Args, meteors: list[fmdt.truth.HumanDetection], rerun: bool = False, tmp_gt_file = "tmp_meteors.txt"):
#     """Call fmdt-detect and fmdt-check to evaluate how well a given set of arguments detects our ground truth
    
#     Parameters
#     ----------
    
#     args (fmdt.Args): The set of fmdt-detect parameters that we want to evaluate
#     meteors (list[fmdt.HumanDetection]): The list of meteors in our ground truth
#     rerun (bool): Used to determine if we should rerun fmdt-detect when the trk_out_path file
#         already exists
#     """
#     assert not args.detect_args.trk_out_path is None, "Missing `trk_out_path` from `args: fmdt.Args` required for evaluation"
#     assert not args.detect_args.vid_in_path  is None, "Missing `vid_in_path` required to evaluate an fmdt.Args"

#     if rerun:
#         args.detect()

#     # Check if the trk_out_path file already exists
#     if not os.path.exists(args.detect_args.trk_out_path):
#         args.detect()

#     # We guarentee that the file exist at this point

#     # Let's write the data from meteors to a temp file
#     fmdt.truth.save_meteors_file(tmp_gt_file, meteors)

#     # Then call fmdt_check

#     fmdt_check(args.detect_args.trk_out_path, tmp_gt_file)


args = fmdt.detect_args(vid_in_path="demo.mp4", trk_out_path="trk.txt")
meteors = fmdt.truth.load_meteors_file("meteors.txt")

v = fmdt.Video("demo.mp4")

v.evaluate_args(args, meteors)