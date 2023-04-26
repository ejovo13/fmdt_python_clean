from fmdt.core import (
    extract_all_information,
    extract_key_information,
    split_video_at_meteors,
    split_video_at_intervals,
) 

from fmdt.api import (
    detect,
    visu,
    count,
    detect_directory,
    check
)

from fmdt.args import (
    Args,
    DetectArgs,
    VisuArgs,
    detect_args,
    set_exec_path,
    get_exec_path
)

from fmdt.utils import (
    condense_start_end
)

from fmdt.truth import (
    WATEC6_DIR,
    WATEC12_DIR,
    HumanDetection,
    read_human_detection_csv,
    init_ground_truth,
    GroundTruth
)

from fmdt.download import (
    download_csvs,
    download_demo_mp4,
    download_dbs,
    get_db_dir
)

from fmdt.config import (
    init,
    load_gt12,
    load_gt6,
    load_config,
    listdir_draco12,
    listdir_draco6,
    listdir_window,
    setdir_draco6,
    setdir_draco12,
    setdir_window,
    init_cache,
    clear_cache,
    cache_dir,
    cache_info,
    listdir_cache,
    size_cache,
    bytes_format
)

from fmdt.db import (
    Video,
    VideoType,
    VideoClip,
    retrieve_videos,
    load_draco6,
    load_draco12,
    load_window,
    load_demo,
    load_window_clips,
    load_all,
    get_video,
    info as local_info,
    retrieve_table_video,
    retrieve_table_video_clips,
    retrieve_table_best_detections,
    retrieve_table_detect_args,
    retrieve_table_human_detections
)

from fmdt.stats import (
    num_videos,
    num_meteors
)

init_cache()



# from fmdt.truth import HumanDetection

MAJOR_VERSION = 0
MINOR_VERSION = 0
PATCH         = 42 

VERSION = str(MAJOR_VERSION) + "." + str(MINOR_VERSION) + "." + str(PATCH)
