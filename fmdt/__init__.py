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
    detect_args
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
    download_dbs
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
    size_cache
)

from fmdt.db import (
    Video,
    VideoType,
    load_in_videos,
    load_draco6,
    load_draco12,
    load_window,
    load_demo,
    info as local_info
)

init_cache()



# from fmdt.truth import HumanDetection

MAJOR_VERSION = 0
MINOR_VERSION = 0
PATCH         = 33 

VERSION = str(MAJOR_VERSION) + "." + str(MINOR_VERSION) + "." + str(PATCH)
