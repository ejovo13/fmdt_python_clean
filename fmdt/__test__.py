"""Unit tests for fmdt
"""
import unittest
import fmdt
import numpy as np
import os

# TODO Consider how to test conversion functions. Unfortunately, converting between 
# a video and a ndarray then back to a video is not one-to-one. Some pixels are altered
# by a small amount (brightness of 1-2) whereas others are altered by up to 80.
# It would be interesting to study the distribution of altered pixels

def assert_conversion_correctness(filename="demo.mp4") -> bool: 
    """Assert that the conversion functions between a video and ndarray are lossless
    """
    #! Conversion between ndarray and video is NOT EXACT
    #! Conversion between ndarray and video is NOT EXACT
    #! Conversion between ndarray and video is NOT EXACT
    name, ext = fmdt.__decompose_video_filename(filename)
    filename_conv = f"{name}_conv.{ext}"

    # video -> frames; frames -> video'; video' -> frames'
    frames = fmdt.__convert_video_to_ndarray(filename, log=True)
    fmdt.__convert_ndarray_to_video(filename_conv, frames, fmdt.__get_avg_frame_rate(filename), log=True)
    conv_frames = fmdt.__convert_video_to_ndarray(filename_conv, log=True)
    os.remove(filename_conv)

    # See how many frames are close
    nframes, _, _, _ = frames.shape

    # f and fprime are ndarrays of dtype uint8
    def are_frames_close(f, fprime, dist=5):
        f_int = np.asarray(f, dtype=int)
        fprime_int = np.asarray(fprime, dtype=int)
        return np.all(np.abs(f_int - fprime_int) <= dist)
    close_frames = np.zeros(nframes, dtype=bool)
    for i in range(nframes):
        close_frames[i] = are_frames_close(conv_frames[i,:,:,:], frames[i,:,:,:], 100)

    print(f"Num close frames: {np.sum(close_frames)}/{nframes}")

    return False


class TestVideoMethods(unittest.TestCase):

    def test_conversion(self):
        self.assertTrue(assert_conversion_correctness())

if __name__ == '__main__':
    unittest.main()
