import os
import fmdt
import sys

# Directory whose videos you would like to view
directory = "/run/media/ejovo/Seagate Portable Drive/Meteors/Watec12mm/Meteor/"

def print_help() -> None:
    print("Type the name of the directory you wish to process:")
    # print(f"Ex: {sys.argv[0]} ~/Videos/Meteors")

if directory is None and len(sys.argv) == 1:
    print_help()
    directory = input()
    # assert False
elif directory is None:
    directory = sys.argv[1]

args = {
    "out_track_file": "tracks.txt",
    "light_min": 190,
    "light_max": 235, # None of the videos fail with _just_ a light max
    "trk_all": True,
    "log": True
}

a = fmdt.Args(detect_args=args)

fmdt.detect_directory(directory, a, True)