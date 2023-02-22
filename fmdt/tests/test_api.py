import unittest
import shutil
import fmdt.api

class TestAPI(unittest.TestCase):

    def test_fmdt_detect_existence(self):
        fmdt_detect_exe = shutil.which("fmdt-detect")
        self.assertTrue(not fmdt_detect_exe is None, "Executable 'fmdt-detect' not found on the path")

def main() -> None:
    unittest.main()    

if __name__ == '__main__':
    main()