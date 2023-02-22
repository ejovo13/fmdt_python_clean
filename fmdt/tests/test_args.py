import unittest
import shutil
import fmdt.args

class TestARGS(unittest.TestCase):

    def test_fmdt_detect_args(self):
        args = fmdt.args.handle_detect_args(vid_in_path="vid.mp4")
        print(args)

        # Here we should programmatically verify the correctness of the command 
        # that is output
        



def main() -> None:
    unittest.main()    

if __name__ == '__main__':
    main()