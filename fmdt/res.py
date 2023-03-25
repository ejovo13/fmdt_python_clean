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

    frames = os.listdir(log_path)[1:]

    def mean_err(filename) -> float:
        m, _ = retrieve_mean_err_std_dev(log_path + "/" + filename)
        return m
    
    return [mean_err(f) for f in frames]

def retrieve_all_std_devs(log_path: str) -> list[float]:

    frames = os.listdir(log_path)[1:]

    def mean_err(filename) -> float:
        _, s = retrieve_mean_err_std_dev(log_path + "/" + filename)
        return s
    
    return [mean_err(f) for f in frames]

def retrieve_log_info(log_path: str) -> tuple[list[int], list[int], list[float], list[float]]:
    """Return [nrois], [nassocs], [mean_errs], [std_devs]"""
    nrois = retrieve_all_nroi(log_path)
    nassocs = retrieve_all_nassociations(log_path)
    mean_errs = retrieve_all_mean_errs(log_path)
    std_devs = retrieve_all_std_devs(log_path)

    return nrois, nassocs, mean_errs, std_devs

class CheckingResult:

    def __init__(self):
        pass
 
class DetectionResult:

    def __init__(self, nframes: int, nrois: list[int], nassociations: list[int], mean_errs: list[float],
                 std_devs: list[float], args: fmdt.args.Args, trk_list: list[fmdt.core.TrackedObject]):

        self.nframes = nframes
        self.nrois = nrois
        self.nassociations = nassociations
        self.mean_errs = mean_errs
        self.std_devs = std_devs
        self.args = args 
        self.trk_list = trk_list

    def to_dataframe(self) -> pd.Series:

        if self.nframes == 0:
            return None

        return pd.DataFrame({
            'nrois': self.nrois,
            'nassocs': self.nassociations,
            'mean_errs': self.mean_errs,
            'std_devs': self.std_devs
        })

    def detect(self):
        return self.args.detect()

    def visu(self):
        return self.args.visu()
    
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
        
    

    # I want to be able to 