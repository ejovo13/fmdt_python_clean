import unittest
import os
import fmdt.args
import fmdt.api
import fmdt.res
import fmdt.core
import fmdt.download

from fmdt.utils import stderr


class TestDatabase(unittest.TestCase):

    # Constant numbers pulled from SQL requests
    DEMO_NAME = '2022_05_31_tauh_34_meteors.mp4'
    DEMO_NB_METEORS = 34
    NB_DRACO6_TOTAL = 52
    NB_DRACO6_WITH_METEORS = 38
    NB_DRACO12_TOTAL = 41
    NB_DRACO12_WITH_METEORS = 37
    NB_WINDOW = 7

    def test_demo(self):

        demo = fmdt.load_demo()
        self.assertEqual(demo.name, self.DEMO_NAME)
        self.assertEqual(demo.nb_meteors(), self.DEMO_NB_METEORS)

    def test_draco6(self):

        d6 = fmdt.load_draco6()
        d6_gt = fmdt.load_draco6(require_gt=True)
        d6_det = fmdt.load_draco6(require_best_det=True)

        self.assertEqual(len(d6), self.NB_DRACO6_TOTAL)
        self.assertEqual(len(d6_gt), self.NB_DRACO6_WITH_METEORS)

        for d in d6_gt:
            self.assertTrue(d.has_meteors())

        for d in d6_det:
            self.assertTrue(d.has_best_detection())


    def test_draco12(self):

        d12 = fmdt.load_draco12()
        d12_gt = fmdt.load_draco12(require_gt=True)
        d12_det = fmdt.load_draco12(require_best_det=True)

        self.assertEqual(len(d12), self.NB_DRACO12_TOTAL)
        self.assertEqual(len(d12_gt), self.NB_DRACO12_WITH_METEORS)

        for d in d12_gt:
            self.assertTrue(d.has_meteors())

        for d in d12_det:
            self.assertTrue(d.has_best_detection())

    def test_window(self):

        window = fmdt.load_window()
        self.assertEqual(len(window), self.NB_WINDOW)

    def test_window_clips(self):

        window_clips = fmdt.load_window_clips()

        for w in window_clips:
            self.assertTrue(w.has_meteors())

    def test_report(self):
        stderr("Database successfully tested")


class TestDetect(unittest.TestCase):

    # Assert that a simple detection works
    TRACK_PATH = "these_tracks.txt"
    DEMO = fmdt.load_draco6()[0]

    def test_detect_demo_default_trk_path(self):

        res = self.DEMO.detect()
        res.cleanup()

    def test_detect_demo_verbose_default_trk_path(self):

        res = self.DEMO.detect(verbose=True)
        res.cleanup()


    def test_detect_demo_verbose_trk_path(self):

        res = self.DEMO.detect(verbose=True, trk_path=self.TRACK_PATH)

        self.assertTrue(os.path.exists(self.TRACK_PATH))
        os.remove(self.TRACK_PATH)

        res.cleanup()


    def test_detect_demo_no_trk_path(self):

        res = self.DEMO.detect(trk_path=None, verbose=True)
        res.cleanup()

class TestVisu(unittest.TestCase):

    DEMO = fmdt.load_demo()

    def test_simple_visu(self):

        self.DEMO.detect(log_path="log").log_parser().visu()


class TestArgs(unittest.TestCase):

    """This TestCase deals with the creation of Args objects and verifies that the shell commands have
    their parameters set appropriately.
    """

    CCL_HYST_LO = 150
    CCL_HYST_HI = 155

    def test_cmd_production(self):

        args = fmdt.Args.new(ccl_hyst_lo=self.CCL_HYST_LO, ccl_hyst_hi=self.CCL_HYST_HI)

        cmd = args.command()

        self.assertTrue(f"--ccl-hyst-lo {self.CCL_HYST_LO}" in cmd)
        self.assertTrue(f"--ccl-hyst-hi {self.CCL_HYST_HI}" in cmd)

    def test_args_creation(self):

        def try_bad_detect():
            fmdt.detect_args(vid_out_path='demo_visu.mp4')

        self.assertRaises(Exception, try_bad_detect)




# class TestAPI(unittest.TestCase):

#     def test_fmdt_detect_existence(self):
#         fmdt_detect_exe = shutil.which("fmdt-detect")
#         self.assertTrue(not fmdt_detect_exe is None, "Executable 'fmdt-detect' not found on the path")


# class TestARGS(unittest.TestCase):

#     #================= Creation of Args type ==============
#     def test_detect_arg_creation(self):

#         args = fmdt.detect_args("demo.mp4")

#         self.assertTrue(args.detect_args.vid_in_path == "demo.mp4")
#         self.assertTrue(args.visu_args.vid_out_path == "demo_visu.mp4")

#     def test_arg_creation(self):

#         args = fmdt.Args.new(vid_in_path="demo.mp4", vid_out_path="demo_out.mp4", vid_in_start=10)

#         self.assertTrue(args.visu_args.vid_out_path == "demo_out.mp4")
#         self.assertTrue(args.visu_args.vid_in_start == 10)
#         self.assertTrue(args.detect_args.vid_in_start == 10)

#         args2 = fmdt.Args.new(vid_in_path="demo.mp4", timeout=4, log=True)

#         self.assertTrue(args2.timeout == 4)
#         self.assertTrue(args2.log)

# class TestDetections(unittest.TestCase):

#     def test_demo_plain(self):

#         if not os.path.exists("demo.mp4"):
#             print("Cannot run detection tests on demo.mp4 because it was not found")
#             exit(2)
#         res = fmdt.detect("demo.mp4")

#         """Needs to be run with "demo.mp4" in the current working directory"""

#         self.assertTrue(isinstance(res, fmdt.res.DetectionResult))
#         self.assertTrue(isinstance(res.trk_list[0], fmdt.core.TrackedObject))

#         self.assertTrue(len(res.trk_list) == 38)
#         self.assertTrue(res.trk_list[0].type_str() == "Meteor")
#         self.assertTrue(res.nframes == 256)

#         # Since we haven't passed the log_path parameter, we expect no data to be stored
#         self.assertTrue(len(res.nrois) == 0)

#     def test_demo_log(self):

#         if not os.path.exists("demo.mp4"):
#             print("Cannot run detection tests on demo.mp4 because it was not found")
#             exit(2)
#         res = fmdt.detect("demo.mp4", log_path="log")

#         self.assertTrue(len(res.nrois) == 256)

#         df = res.to_dataframe()

#         self.assertTrue(len(df) == 256)

#     def test_demo_log_all(self):

#         if not os.path.exists("demo.mp4"):
#             print("Cannot run detection tests on demo.mp4 because it was not found")
#             exit(2)
#         res = fmdt.detect("demo.mp4", log_path="log", trk_all=True)


#         self.assertTrue(len(res.trk_list) == 82)
#         self.assertTrue(len(res.nrois) == 256)


#         df = res.to_dataframe()

#         self.assertTrue(len(df) == 256)


# class TestGroundTruth(unittest.TestCase):

#     def test_downloads(self):
#         """Download all the csvs associated with our data base"""

#         fmdt.download.download_csvs(overwrite=True)

#         # Now I should be able to load in the values using pandas I guess
#         # We want to load in some ground truth values as well
#         gt6 = fmdt.GroundTruth("human_detections_draco6.csv")
#         gt12 = fmdt.GroundTruth("human_detections_draco12.csv")
#         gtall = fmdt.GroundTruth("human_detections.csv")

#         self.assertTrue(len(gt6) == 38)
#         self.assertTrue(len(gt12) == 39)
#         self.assertTrue(len(gtall) == 77)

# # class TestKnownResults(unittest.TestCase):

#     def test_


def main() -> None:
    unittest.main()

if __name__ == '__main__':
    main()