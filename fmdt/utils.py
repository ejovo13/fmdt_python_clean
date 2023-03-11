import ffmpeg
import os
import sys
import numpy as np
import subprocess

def retain_meteors(tracking_list: list[dict]) -> list[dict]:
    """Take a list of dictionaries returned by one of the fmdt.extract_* functions
    and filter out objects that are not meteors
    """
    return [obj for obj in tracking_list if obj["type"] == "meteor"]

def separate_meteor_sequences(tracking_list: list[dict], frame_buffer = 5) -> list[tuple[int, int]]:
    """
    Take a tracking list and compute the disparate sequences of meteors 

    If two meteors are within frame_buffer frames of each other, consider them as part of the
    same sequence
    """

    # Let's convert the tracking list into a list of (start_frame, end_frame) tuples
    start_end = [(obj["start_frame"], obj["end_frame"]) for obj in tracking_list]

    return condense_start_end(start_end, frame_buffer)

def condense_start_end(start_end: list[tuple[int, int]], frame_buffer = 5) -> list[tuple[int, int]]:
    """Condense a list of (f_start, f_end) frame pairs into a small sequence of 
    non-overlapping sequences
    """
    start_end_condensed = [start_end[0]]
    ci = 0 # condensed index, will not always be equal to i
    for i in range(len(start_end) - 1):

        # If the end frame of one meteor is close to the start frame of the next, condense the two sequences
        if (start_end_condensed[ci][1] + frame_buffer > start_end[i + 1][0]):
            start_end_condensed[ci] = (start_end_condensed[ci][0], start_end[i + 1][1])
        else:
            ci = ci + 1
            start_end_condensed.append(start_end[i + 1]) 

    return start_end_condensed


# =============================== Video file functions ========================================
def get_avg_frame_rate(filename: str) -> float:
    """
    Get the average framerate of a video
    
    Adapted from https://github.com/kkroening/ffmpeg-python/blob/master/examples/video_info.py#L15
    """
    probe = ffmpeg.probe(filename)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    frame_rates = video_stream['avg_frame_rate'].split('/')
    return float(frame_rates[0]) / float(frame_rates[1])

def get_video_width(filename: str) -> int:
    probe = ffmpeg.probe(filename)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    return int(video_stream['width'])


def get_video_height(filename: str) -> int:
    probe = ffmpeg.probe(filename)
    video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
    return int(video_stream['height'])

    
def decompose_video_filename(filename: str) -> tuple[str, str]:
    """Separate the name of a video from its extension

    Ex: decompose_video_filename("vid.mp4") returns the pair ("vid", "mp4") 
    """
    sep = filename.split('.')
    # assert len(sep) == 2, "Filename has multiply periods"

    ext = sep[-1]

    if len(sep) >= 2:
        name = ".".join(sep[:-1])

    return (name, ext)

def assert_file_exists(filename: str) -> None:
    assert os.path.exists(filename), f"{filename} not found"

def time_s_to_ffmpeg_format(time: int | float) -> str:

    time_h = int(time // (60 * 60))
    time -= time_h * 60 * 60
    time_m = int(time // 60)
    time -= time_m * 60
    time_s = int(np.floor(time)) 

    return f"{time_h:02}:{time_m:02}:{time_s:02}"

# def frame_number_to_ffmpeg_format(filename: str, frame_number: int, seconds_offset=0) -> str:

#     assert_file_exists(filename)
#     fps = get_avg_frame_rate(filename)
#     start_time = frame_number / fps + seconds_offset

#     return time_s_to_ffmpeg_format(start_time)


def extract_video_frames(
        filename: str,
        start_frame: int,
        end_frame: int,
        out_file: str | None = None,
        quiet = True,
        overwrite = False
    ) -> None:

    assert_file_exists(filename)

    if out_file is None:
        # Then create our own name for the new video
        name, ext = decompose_video_filename(filename)
        out_file = f"{name}_f{start_frame}-{end_frame}.{ext}"

    fps = get_avg_frame_rate(filename)
    start_time = (start_frame / fps) - 1 # offset by at most one second
    start_time = time_s_to_ffmpeg_format(start_time)

    # Calculate the duration.
    duration = (end_frame - start_frame) / fps
    duration = time_s_to_ffmpeg_format(duration + 1) # Add one second to the duration

    # end_time   = frame_number_to_ffmpeg_format(filename, start_frame, seconds_offset=1)

    args = ["ffmpeg", "-ss", start_time, "-i", filename, "-t", duration, out_file]

    if quiet:
        args.extend(["-loglevel", "error"])

    if overwrite:
        args.append("-y")

    print(f"Running command '{' '.join(args)}'")
    subprocess.run(args)



def convert_video_to_ndarray(filename: str, log=False) -> np.ndarray:
    """
    Convert a video file to a numpy array of size [n_frames, height, width, 3] 

    Taken from ffmpeg-python's documentation 
    https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md#convert-video-to-numpy-array
    """

    assert_file_exists(filename)

    if log:
        print(f"converting '{filename}' to ndarray", file=sys.stderr)

    fps = get_avg_frame_rate(filename)
    w   = get_video_width(filename)
    h   = get_video_height(filename)

    out, _ = (
        ffmpeg
        .input(filename)
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .run(capture_stdout=True, quiet=True)
    )
    video = (
        np
        .frombuffer(out, np.uint8)
        .reshape([-1, h, w, 3])
    )

    return video

def convert_video_to_frames(video_filename: str) -> None:

    # We can implement this two ways, one using ffmpeg to write frames to a folder
    vid_name, _ = decompose_video_filename(video_filename)
    os.mkdir(vid_name)
    ffmpeg_cmd = f"ffmpeg -loglevel error -vcodec h264 -i {video_filename} {vid_name}/%05d.png"
    # ffmpeg_cmd = f"ffmpeg -loglevel error -vcodec h264 -i {video_filename} {vid_name}/%05d.png"
    args = ffmpeg_cmd.split(" ")

    subprocess.run(args)
    print(args)


def convert_ndarray_to_video(
        filename_out: str,
        frames: np.ndarray,
        framerate=60,
        vcodec='libx264',
        log=False
    ) -> None:
    """
    Convert a rgb numpy array to video using ffmpeg-python

    Adapted from https://github.com/kkroening/ffmpeg-python/issues/246#issuecomment-520200981 
    """

    if log:
        print(f"converting ndarray to '{filename_out}'", file=sys.stderr)

    _, h, w, _ = frames.shape
    process = (
        ffmpeg
            .input('pipe:', format='rawvideo', pix_fmt='rgb24', s='{}x{}'.format(w, h))
            # .output(filename_out, pix_fmt='yuv420p', vcodec=vcodec, r=framerate)
            # .output(filename_out, pix_fmt='rgb24', vcodec=vcodec, r=framerate)
            .output(filename_out, pix_fmt='rgb24', r=framerate)
            .overwrite_output()
            .run_async(pipe_stdin=True, quiet=True)
    )
    for frame in frames:
        process.stdin.write(
            frame
                .astype(np.uint8)
                .tobytes()
        )
    process.stdin.close()
    process.stdout.close()
    process.stderr.close()
    process.wait()