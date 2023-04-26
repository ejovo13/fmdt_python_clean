"""Module dedicated to reporting the statistics of the current database"""

import fmdt.db

from fmdt.download import (
    get_db_dir
)

from fmdt.utils import (
    join
)

import sqlite3
import pandas as pd

def num_videos(
    db_file = "videos.db",
    db_dir = get_db_dir()
) -> pd.DataFrame:

    con = sqlite3.connect(join(db_dir, db_file))

    df = pd.read_sql_query("""
            SELECT type, count(*)
            FROM video
            GROUP BY type;
        """,
        con
    )

    df.rename(
        columns={"count(*)": "n_clips"},
        inplace=True
    )

    con.close()

    return df


def num_meteors(
    db_file = "videos.db",
    db_dir = get_db_dir()
) -> pd.DataFrame:

    con = sqlite3.connect(join(db_dir, db_file))

    df = pd.read_sql_query("""
        SELECT type, count(*) 
        FROM video
        INNER JOIN human_detections as hd
        ON video.name = hd.video_name
        GROUP BY type;
        """,
        con
    )

    df.rename(
        columns={"count(*)": "n_clips"},
        inplace=True
    )

    con.close()

    return df