"""Load up a configuration of fmdt-detect commands to run, and expect to find a specific meteor"""

import fmdt.truth
import fmdt

DATA_BASE_FILE = "human_detections.csv"
# DATA_BASE_FILE = "human_detection.csv"

humans = fmdt.HumanDetection.init_ground_truth(DATA_BASE_FILE)

# watec6 = None
# watec12 = None
watec6  = "/home/ejovo/Videos/Watec6mm"
watec12 = "/home/ejovo/Videos/Watec12mm"

# I actually think that I might want to 

# Need to load in the configs 
# Load them in as Args