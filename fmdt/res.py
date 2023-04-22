"""Store the results of a run to fmdt-detect"""
import os
import re
import pandas as pd
import fmdt.args
import fmdt.core

def retrieve_all_nroi(log_path: str) -> list[int]:
    """
    Assumes the format: '# Frame n°00247 (t) -- Regions of interest (RoI) [64]: \n'
    """

    if not os.path.exists(log_path):
        return []
    
    frames = os.listdir(log_path)
    rxp = r'\[(\d*)\]'

    rxp_comp = re.compile(rxp)

    def contains_roi(line: str) -> bool:
        return "(RoI)" in line

    def retrieve_single_nroi(frame: str):
        with open(log_path + "/" + frame, "r") as file:
            lines = file.readlines()
            rois = [l for l in lines if contains_roi(l) and "(t)" in l]
            tokens = rois[0].split() 
            n_roi = [n for n in tokens if rxp_comp.search(n)]
            return int(n_roi[0][1:-2])

    return [retrieve_single_nroi(f) for f in frames]

def retrieve_all_nassociations(log_path: str) -> list[int]:

    if not os.path.exists(log_path):
        return []

    frames = os.listdir(log_path)[1:]

    rxp = r'\[\d*\]'

    rxp_comp = re.compile(rxp)

    def retrieve_single_nassociations(frame: str):
        with open(log_path + "/" + frame, "r") as file:
            lines = file.readlines()
            assocs = [l for l in lines if "Associations" in l]
            tokens = assocs[0].split() 
            n_roi = [n for n in tokens if rxp_comp.search(n)]
            return int(n_roi[0][1:-2])

    return [retrieve_single_nassociations(f) for f in frames]

def retrieve_mean_err_std_dev(filename: str) -> tuple[float, float]:
    """This function is JANK. It only depends on the fact that in a log file the only things that have 19
    columns are the rows containing the mean_err and std_dev!"""
    with open(filename) as file:
        lines = file.readlines()
        for l in lines:
            l_split = l.split()
            if len(l_split) == 19:
                mean_err = float(l_split[-3])
                std_dev  = float(l_split[-1])
                return (mean_err, std_dev)
            
def retrieve_all_mean_errs(log_path: str) -> list[float]:

    if not os.path.exists(log_path):
        return []

    frames = os.listdir(log_path)[1:]

    def mean_err(filename) -> float:
        m, _ = retrieve_mean_err_std_dev(log_path + "/" + filename)
        return m
    
    return [mean_err(f) for f in frames]

def retrieve_all_std_devs(log_path: str) -> list[float]:

    if not os.path.exists(log_path):
        return []

    frames = os.listdir(log_path)[1:]

    def mean_err(filename) -> float:
        _, s = retrieve_mean_err_std_dev(log_path + "/" + filename)
        return s
    
    return [mean_err(f) for f in frames]

def retrieve_log_info(log_path: str) -> tuple[list[int], list[int], list[float], list[float]]:
    """Return [nrois], [nassocs], [mean_errs], [std_devs]"""

    print(f"Trying to retrieve log info here: {log_path}")

    nrois = retrieve_all_nroi(log_path)
    nassocs = retrieve_all_nassociations(log_path)
    mean_errs = retrieve_all_mean_errs(log_path)
    std_devs = retrieve_all_std_devs(log_path)

    return nrois, nassocs, mean_errs, std_devs


def retrieve_log_df(log_path: str) -> pd.DataFrame:

    assert os.path.exists(log_path), f"log_path {log_path} does not exist"

    nroi, nassoc, mean_err, std_dev = retrieve_log_info(log_path)

    return pd.DataFrame({
        "nroi": nroi,
        "nassoc": [0] + nassoc,
        "mean_err": [0.0] + mean_err,
        "std_dev": [0.0] + std_dev
    })

class DetectionResult:

    def __init__(self, nframes: int, df: pd.DataFrame, args: fmdt.args.Args, trk_list: list[fmdt.core.TrackedObject], video = None):

        self.nframes = nframes
        self.df = df
        self.args = args 
        self.trk_list = trk_list
        self.video = video

    def detect(self):
        return self.args.detect()

    def visu(self):
        return self.args.visu()

    def n_meteors_detected(self) -> int:
        return len([m for m in self.trk_list if m.is_meteor()])

    def n_stars_detected(self) -> int:
        return len([s for s in self.trk_list if s.is_star()])

    def n_noise_detected(self) -> int:
        return len([n for n in self.trk_list if n.is_noise()])

    def trk_list_summary(self) -> str:
        return f"objects in trk_list: {self.n_meteors_detected()} meteor(s), {self.n_stars_detected()} star(s), {self.n_noise_detected()} noise"
    
    def __str__(self) -> str:
        a = f"fmdt.res.DetectionResult with args digest: {self.args.detect_args.digest()[0:16]}"
        b = f"\n{self.trk_list_summary()}"
        
        c = ""
        if not self.df is None:
            c = f"\n{str(self.df)}"

        return a + b + c
    
    def check(self, gt_path: str = None, stdout: str = "check.txt", log = False):
        """Call fmdt-check with these results
        
        Parameters
        ----------
        gt_path (str): Full path to ground truth file. Used when dealing with a call to fmdt.detect directly and not
            interfacing with a Video object. When calling with the function chain Video.detect().check(), we don't need
            to pass in the gt_path
        
        """

        assert not self.args.detect_args.trk_out_path is None, "To call fmdt.check we must specify the `trk_out_path`"

        if gt_path is None:
            # If we dont have ground truth meteors, assure that the meteor acutally exists
            assert not self.video is None, "When calling DetectionResult.check() specify the gt_path or use a video like v.detect().check()"

            assert self.video.has_meteors(), f"Video {self.video} has no gts in our data base. Specify a meteors file with the `gt_path` argument"

            return self.video.evaluate_args(self.args, self.video.meteors(), stdout=stdout, log=log)

        else:
            return fmdt.check(self.args.detect_args.trk_out_path, gt_path, stdout=stdout, log=log)

    # @staticmethod
    # def from_file(trk_path: str, log_path: str):

    
    # @staticmethod
    # def from_detect(args: fmdt.args.Args):

    #     trk_path = args.detect_args.trk_out_path
    #     log_path = args.detect_args.log_path

    #     if trk_path is None:
    #         trk_list = []
    #     else:
    #         trk_list = fmdt.extract_all_information(trk_path)

    #     if not log_path is None:
    #         rois, nassocs, mean_errs, std_devs = retrieve_log_info(log_path) 
    #     else:
    #         rois = []
    #         nassocs = []
    #         mean_errs = []
    #         std_devs = []

    #     return DetectionResult(rois, [0] + nassocs, [0.0] + mean_errs, [0.0] + std_devs, args, trk_list)

    def roa(self) -> pd.Series:
        """Rate of Association (ROA) is the ratio nassoc / nroi"""

        assert not self.df is None, f"Cannot compute the roa of {self} because the field df is missing. Consider rerunning your detection with `save_df=True`"
        
        return self.df["nassoc"] / self.df["nroi"]

    def mean_roa(self) -> float:
        return self.roa().mean()

    def mean_nroi(self) -> float:
        return self.df["nroi"].mean()

    def mean_nassoc(self) -> float:
        return self.df["nassoc"].mean()

    def mean_mean_err(self) -> float:
        return self.df["mean_err"].mean()
    
    def mean_std_dev(self) -> float:
        return self.df["std_dev"].mean()
    
# load a DetectionResult object from a trk_path and a log_path
def load_det_result(trk_path: str, log_path: str) -> DetectionResult:
    """Load a det_result object whose content is stored in trk_path and log_path"""

    if os.path.exists(trk_path):
        trk_list = fmdt.core.extract_all_information(trk_path) 
        n_frames = fmdt.core.nframes_processed(trk_path)
    else:
        trk_list = []
        n_frames = 0

    if os.path.exists(log_path):
        df = retrieve_log_df(log_path)
    else:
        df = None

    return DetectionResult(n_frames, df, None, trk_list)

#===================== Fonctions dealing with check ============================

# I want to parse the file.
# Let's start off by parsing the first table

# start after Id|    Type 
# end at Statistics

CHECK_TABLE_HEADER = "#   Id |    Type || Detect |  GT || Start |  Stop ||      #"

CTBL_ID = 0
CTBL_TYPE = 2
CTBL_DETECT = 4
CTBL_GT = 6
CTBL_START = 8
CTBL_STOP = 10
CTBL_TRACKS = 12

def load_check_gt_table(check_stdout: str) -> pd.DataFrame:


    with open(check_stdout) as file:
        lines = file.readlines()

        hdr_line_nmbr  = -1
        stat_line_nmbr = -1

        # iterate through lines until the we get to the Id line
        for (i, el) in enumerate(lines):
            if el.strip() == CHECK_TABLE_HEADER:
                hdr_line_nmbr = i
                break

        for (i, el) in enumerate(lines):
            if "Statistics:" in el:
                stat_line_nmbr= i 

        table = lines[(hdr_line_nmbr + 2):stat_line_nmbr] 


        ids = []
        types = []
        detects = []
        gts = []
        starts = []
        stops = []
        tracks = []

        for line in table:
            s = line.split()

            ids.append(int(s[CTBL_ID]))
            types.append(s[CTBL_TYPE])
            detects.append(int(s[CTBL_DETECT]))
            gts.append(int(s[CTBL_GT]))
            starts.append(int(s[CTBL_START]))
            stops.append(int(s[CTBL_STOP]))
            tracks.append(int(s[CTBL_TRACKS]))
        
    return pd.DataFrame({
        "id": ids,
        "types": types,
        "detects": detects,
        "gts": gts,
        "starts": starts,
        "stops": stops,
        "tracks": tracks
    })

CHECK_NGT = "- Number of GT objs"      
CHECK_NTRACK = "- Number of tracks"
CHECK_TPOS = "- True positives"
CHECK_FPOS = "- False positives"
CHECK_TNEG = "- True negative"
CHECK_FNEG = "- False negative"
CHECK_TRACK_RATE = "- tracking rate"

def check_line_to_tuple(line: str) -> tuple[int, int, int, int]:
    """Convert '- Number of GT objs = ['meteor':   34, 'star':    0, 'noise':    0, 'all':   34]' to a 4-tuple of numbers """

    # Find the first instance of []
    line = line.strip()

    for (i, el) in enumerate(line):
        if line[i] == "[":
            break

    array_interior = line[i + 1:-1] # drop the brackets

    content = array_interior.split()

    m = int(content[1][:-1]) # drop comma at the end
    s = int(content[3][:-1]) # drop comma at the end
    n = int(content[5][:-1])
    a = int(content[7])

    return m, s, n, a

def check_tracking_rate_line(line: str) -> tuple[int, int, int, int]:
    """Convert '- Number of GT objs = ['meteor':   34, 'star':    0, 'noise':    0, 'all':   34]' to a 4-tuple of numbers """

    # Find the first instance of []
    line = line.strip()

    for (i, el) in enumerate(line):
        if line[i] == "[":
            break

    array_interior = line[i + 1:-1] # drop the brackets

    content = array_interior.split()

    m = float(content[1][:-1]) # drop comma at the end
    s = float(content[3][:-1]) # drop comma at the end
    n = float(content[5][:-1])
    a = float(content[7])

    return m, s, n, a


def load_check_stats(check_stdout: str) -> pd.DataFrame:

    with open(check_stdout) as file:
        lines = file.readlines()

        # iterate through lines until the we get to the Id line
        for (i, el) in enumerate(lines):
            if CHECK_NGT in el:
                break

        ms = []; ss = []; ns = []; alls = [];
        mat = [ms, ss, ns, alls] # these are our rows and we need to get the matrix as column

        for j in range(6):
            m, s, n, a = check_line_to_tuple(lines[i + j])
            ms.append(m); ss.append(s); ns.append(n); alls.append(a)
        
        m, s, n, a = check_tracking_rate_line(lines[i + 6])
        ms.append(m); ss.append(s); ns.append(n); alls.append(a)

        ngts = []; ntrks = []; tpos = []; fpos = []; tneg = []; fneg = []; trk_rate = []

        names = ["meteor", "star", "noise", "all"]

        for r in mat:

            ngts.append(r[0])
            ntrks.append(r[1])
            tpos.append(r[2])
            fpos.append(r[3])
            tneg.append(r[4])
            fneg.append(r[5])
            trk_rate.append(r[6])
    
    return pd.DataFrame({
        "type": names,
        "gt": ngts,
        "ntrk": ntrks,
        "tpos": tpos,
        "fpos": fpos,
        "tneg": tneg,
        "fneg": fneg,
        "trk_rate": trk_rate
    })

class CheckResult:

    def __init__(self, gt_table: pd.DataFrame = None, stats: pd.DataFrame = None):
        self.gt_table = gt_table
        self.stats = stats

    def __str__(self) -> str:
        a = "GroundTruth table\n-----------------\n"
        b = str(self.gt_table) + "\n"
        c = "Tracking stats\n--------------\n"
        d = str(self.stats) + "\n"

        return a + b + c + d
    
    def __repr__(self) -> str:
        return self.__str__()

    def meteor_stats(self) -> pd.Series:
        return self.stats[self.stats["type"] == "meteor"].iloc[0]

    def noise_stats(self) -> pd.Series:
        return self.stats[self.stats["type"] == "noise"].iloc[0]

    def star_stats(self) -> pd.Series:
        return self.stats[self.stats["type"] == "star"].iloc[0]

    def all_stats(self) -> pd.Series:
        return self.stats[self.stats["type"] == "all"].iloc[0]
    
    def trk_rate(self) -> float:
        return self.meteor_stats()["trk_rate"]
    
    def gts(self) -> int:
        """Return the number ground truth meteors used when checking"""
        return self.stats["gt"].iloc[0]

    def nb_meteors_detected(self) -> int:
        return sum(self.gt_table["tracks"] != 0)
    
    def detect_rate(self) -> float:
        return self.nb_meteors_detected() / self.gts()
    
    def meteors_detected(self) -> bool:
        """Return True if the tracking rate is greater than 0"""
        return self.trk_rate() > 0.0

def main():
    file = "test_check_one.txt"

    df = load_check_gt_table(file) 


