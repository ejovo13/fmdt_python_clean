"""
Core functions used in the processing of output for fmdt: https://github.com/alsoc/fmdt

Public API:
    extract_key_information
    extract_all_information
    split_video_at_meteors
"""

import fmdt.utils as utils
from enum import Enum

# Structure of tracking output table of fmdt-detect after 
# each line gets stripped using whitespace as a delimiter
class TrackingTable:

    OBJECT_ID   = 0
    START_FRAME = 2
    START_X     = 4
    START_Y     = 6
    END_FRAME   = 8
    END_X       = 10
    END_Y       = 12
    OBJECT_TYPE = 14


class ObjectType(Enum):
    METEOR = 0
    STAR   = 1
    NOISE  = 2

    @staticmethod
    def from_str(s: str):
        slow = s.lower()
        if slow == "meteor":
            return ObjectType.METEOR
        elif slow == "star":
            return ObjectType.STAR
        else:
            return ObjectType.NOISE


    
class TrackedObject:

    def __init__(
        self,
        id: int,
        start_frame: int,
        start_x: float,
        start_y: float,
        end_frame: int,
        end_x: float,
        end_y: float,
        type: ObjectType
        ): 

        self.id = id
        self.start_frame = start_frame
        self.start_x = start_x
        self.start_y = start_y
        self.end_frame = end_frame
        self.end_x = end_x
        self.end_y = end_y
        self.type = type
        
    def is_meteor(self) -> bool:
        return self.type == ObjectType.METEOR

    def is_star(self) -> bool:
        return self.type == ObjectType.STAR

    def is_noise(self) -> bool:
        return self.type == ObjectType.NOISE
    
    def type_str(self) -> str:
        if self.is_meteor():
            return "Meteor" 
        elif self.is_star():
            return "Star" 
        else:
            return "Noise" 
    
    def __str__(self) -> str:

        return f"<{self.type_str()} ({self.start_frame}, {self.end_frame}), pos0: ({self.start_x, self.start_y}), posT: ({self.end_x}, {self.end_y})>"
    
    def __repr__(self) -> str:
        return f"<{self.type_str()} ({self.start_frame}, {self.end_frame})>"
    
    # @staticmethod
    # def from_tracking_file(filename: str):
    #     pass
    #     # all_info = extract_all_information()

# class TrackingList:
#     """A list of TrackedObjects"""

def read_tracks_file(tracks_filename: str) -> list[TrackedObject]:
    return extract_all_information(tracks_filename)


def extract_key_information(detect_tracks_in: str) -> list[dict]:
    """Extract key information from a detect_tracks.txt file.

    "Key" information refers to the start frame, end frame, and type of 
    object detected

    Parameters
    ----------
    detect_tracks_in (str): The name of a file whose content is the output
        of fmdt_detect

    Returns
    -------
    dict_array (list[dict]): A list of dictionaries of the form
        { 
            "type": <"meteor" | "noise" | "start">
            "frame_start": <int>
            "frame_end": <int>
        }
        where each item in the list corresponds to a single object detected by 
        `fmdt-detect`
    """

    # Utility function to convert a line of interest to a dictionary
    def line_to_dict(split_line: list[str]):

        return {
            "type":         split_line[TrackingTable.OBJECT_TYPE],
            "start_frame":  int(split_line[TrackingTable.START_FRAME]),
            "end_frame":    int(split_line[TrackingTable.END_FRAME])
        }

    # Utility boolean function to extract only the important lines
    interesting_line = lambda line: (
        (" meteor" in line) or (" star" in line) or (" noise" in line)
    )
    
    # Processing of the actual file
    file_tracks = open(detect_tracks_in)
    file_lines  = file_tracks.readlines()
    dict_array = []

    for line in file_lines:
        if interesting_line(line):
            dict_array.append(line_to_dict(line.split()))

    return dict_array

def extract_all_information(detect_tracks_in: str) -> list[TrackedObject]:
    """Extract all tracking information from a detect_tracks.txt file.

    Parameters
    ----------
    detect_tracks_in (str): The name of a file whose content is the output
        of fmdt_detect

    Returns
    -------
    dict_array (list[dict]): A list of dictionaries of the form
        { 
            "id":           <int>,
            "start_frame":  <int>,
            "start_x":      <float>,
            "start_y":      <float>,
            "end_frame":    <int>,
            "end_x":        <float>,
            "end_y":        <float>,
            "type":         <"meteor" | "noise" | "start">,
        }
        where each item in the list corresponds to a single object detected by 
        `fmdt-detect`
    """

    # Utility function to convert a line of interest to a dictionary
    # def line_to_dict(split_line: list[str]):

    #     return {
    #         "id":           int(split_line[TrackingTable.OBJECT_ID]),
    #         "start_frame":  int(split_line[TrackingTable.START_FRAME]),
    #         "start_x":      float(split_line[TrackingTable.START_X]),
    #         "start_y":      float(split_line[TrackingTable.START_Y]),
    #         "end_frame":    int(split_line[TrackingTable.END_FRAME]),
    #         "end_x":        float(split_line[TrackingTable.END_X]),
    #         "end_y":        float(split_line[TrackingTable.END_Y]),
    #         "type":         split_line[TrackingTable.OBJECT_TYPE]
    #     }

    def line_to_obj(split_line: list[str]) -> TrackedObject:
        return TrackedObject(int  (split_line[TrackingTable.OBJECT_ID]),
                             int  (split_line[TrackingTable.START_FRAME]),
                             float(split_line[TrackingTable.START_X]),
                             float(split_line[TrackingTable.START_Y]),
                             int  (split_line[TrackingTable.END_FRAME]),
                             float(split_line[TrackingTable.END_X]),
                             float(split_line[TrackingTable.END_Y]),
                             ObjectType.from_str(split_line[TrackingTable.OBJECT_TYPE]))
      
    # Utility boolean function to extract only the important lines
    interesting_line = lambda line: (
        (" meteor" in line) or (" star" in line) or (" noise" in line)
    )
    
    # Processing of the actual file
    file_tracks = open(detect_tracks_in)
    file_lines  = file_tracks.readlines()

    return [line_to_obj(line.split()) for line in file_lines if interesting_line(line)]


def split_video_at_meteors(
        video_filename: str,
        detect_tracks_in: str,
        nframes_before=3,
        nframes_after=3,
        overwrite=False,
        exact_split: bool = False,
        log: bool = False
    ) -> None:
    """
    Split a video into small segments of length (nframes_before + nframes_after + sequence_length) frames
    for each meteor detected 

    Parameters
    ----------
    video_filename (str): Filename of video to split 
    detect_tracks_in (str): Filename of tracks recorded by a call to 
        fmdt.detect(video_filename, out_track_file=detect_tracks_in)
    nframes_before (int): Number of frames to extract before the meteor sequence begins
        (Default value of 3)
    nframes_after (int): Number of frames to extract after the meteor sequence ends
        (Default value of 3)
    overwrite (bool): Tells ffmpeg to overwrite (True) the generated output videos if they already
        exist. If false then ffmpeg will ask for manual confirmation
        (Default value of False)
    exact_split (bool): Determine whether to extract the _exact_ frames requested (True) - which requires loading
        the entire video into memory as a numpy array - or approximate the frames requested using ffmpeg's 
        seeking functionality (False). For long videos with high resolution, use False otherwise the program 
        might crash. 
        (Default value of False)
    log (bool): When True, print to console the current action being performed
    """
    utils.assert_file_exists(video_filename)
    utils.assert_file_exists(detect_tracks_in)

    # Preprocessing of information held in `detect_tracks_in`
    tracking_list = extract_key_information(detect_tracks_in)
    tracking_list = utils.retain_meteors(tracking_list)
    seqs = utils.separate_meteor_sequences(tracking_list)
    video_name, extension = utils.decompose_video_filename(video_filename) 

    # Bookkeeping for formatting the name of the output videos
    max_digits = len(str(seqs[-1][1]))
    format_str = '0' + str(max_digits)

    # Selection of splitting algorithm
    if exact_split:
        
        # Querying of video information, extraction of frames
        frames = utils.convert_video_to_ndarray(video_filename, log=log)
        frame_rate = utils.get_avg_frame_rate(video_filename)
        total_frames, _, _, _ = frames.shape
        seq_video_name = lambda seq: (
            f'{video_name}_f{format(seq[0], format_str)}-{format(seq[1], format_str)}.{extension}'
        )

        def exact_splitting(seq) -> None:
            """Function call that will convert a 'meteor seq' to a frame perfect video sequence"""

            # Ensure that f_start and f_end are valid
            f_start = s[0] - nframes_before if s[0] - nframes_before >= 0 else 0
            f_end   = s[1] + nframes_after  if s[1] + nframes_after  <= total_frames else total_frames
            frames_seq = frames[f_start:f_end, :, :, :]
            utils.convert_ndarray_to_video(seq_video_name(s), frames_seq, frame_rate, log=log)

        splitting_algorithm = exact_splitting
    
    else:

        seq_video_name = lambda seq: (
            f'{video_name}_f{format(seq[0], format_str)}-{format(seq[1], format_str)}_.{extension}'
        )

        def approx_splitting(seq) -> None:
            """Function call that will convert a 'meteor seq' to an approximate video sequence"""

            f_start = s[0] - nframes_before if s[0] - nframes_before >= 0 else 0
            f_end   = s[1] + nframes_after
            utils.extract_video_frames(video_filename, f_start, f_end,
                                       seq_video_name(s), overwrite=overwrite)

        splitting_algorithm = approx_splitting

    for s in seqs:
        splitting_algorithm(s)