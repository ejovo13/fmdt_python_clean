import unittest
import shutil
# import fmdt.api
import os
import fmdt.args
import fmdt.api
import fmdt.res
import fmdt.core
import fmdt.download
import pandas as pd

class TestAPI(unittest.TestCase):

    def test_fmdt_detect_existence(self):
        fmdt_detect_exe = shutil.which("fmdt-detect")
        self.assertTrue(not fmdt_detect_exe is None, "Executable 'fmdt-detect' not found on the path")

    
class TestARGS(unittest.TestCase):

    #================= Creation of Args type ==============
    def test_detect_arg_creation(self):

        args = fmdt.detect_args("demo.mp4")

        self.assertTrue(args.detect_args.vid_in_path == "demo.mp4")
        self.assertTrue(args.visu_args.vid_out_path == "demo_visu.mp4")

    def test_arg_creation(self):

        args = fmdt.Args.new(vid_in_path="demo.mp4", vid_out_path="demo_out.mp4", vid_in_start=10)

        self.assertTrue(args.visu_args.vid_out_path == "demo_out.mp4")
        self.assertTrue(args.visu_args.vid_in_start == 10)
        self.assertTrue(args.detect_args.vid_in_start == 10)

        args2 = fmdt.Args.new(vid_in_path="demo.mp4", timeout=4, log=True)

        self.assertTrue(args2.timeout == 4)
        self.assertTrue(args2.log)

class TestDetections(unittest.TestCase):

    def test_demo_plain(self):

        if not os.path.exists("demo.mp4"):
            print("Cannot run detection tests on demo.mp4 because it was not found")
            exit(2)
        res = fmdt.detect("demo.mp4")

        """Needs to be run with "demo.mp4" in the current working directory"""

        self.assertTrue(isinstance(res, fmdt.res.DetectionResult))
        self.assertTrue(isinstance(res.trk_list[0], fmdt.core.TrackedObject))

        self.assertTrue(len(res.trk_list) == 38)
        self.assertTrue(res.trk_list[0].type_str() == "Meteor")
        self.assertTrue(res.nframes == 256)

        # Since we haven't passed the log_path parameter, we expect no data to be stored
        self.assertTrue(len(res.nrois) == 0)

    def test_demo_log(self):

        if not os.path.exists("demo.mp4"):
            print("Cannot run detection tests on demo.mp4 because it was not found")
            exit(2)
        res = fmdt.detect("demo.mp4", log_path="log")

        self.assertTrue(len(res.nrois) == 256)

        df = res.to_dataframe()

        self.assertTrue(len(df) == 256)

    def test_demo_log_all(self):

        if not os.path.exists("demo.mp4"):
            print("Cannot run detection tests on demo.mp4 because it was not found")
            exit(2)
        res = fmdt.detect("demo.mp4", log_path="log", trk_all=True)


        self.assertTrue(len(res.trk_list) == 82)
        self.assertTrue(len(res.nrois) == 256)
        

        df = res.to_dataframe()

        self.assertTrue(len(df) == 256)


class TestGroundTruth(unittest.TestCase):

    def test_downloads(self):
        """Download all the csvs associated with our data base"""

        fmdt.download.download_csvs(overwrite=True)

        # Now I should be able to load in the values using pandas I guess
        # We want to load in some ground truth values as well
        gt6 = fmdt.GroundTruth("human_detections_draco6.csv")
        gt12 = fmdt.GroundTruth("human_detections_draco12.csv")
        gtall = fmdt.GroundTruth("human_detections.csv")

        self.assertTrue(len(gt6) == 38)
        self.assertTrue(len(gt12) == 39)
        self.assertTrue(len(gtall) == 77)

# class TestKnownResults(unittest.TestCase):

#     def test_


def main() -> None:
    unittest.main()    

if __name__ == '__main__':
    main()