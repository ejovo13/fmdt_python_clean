"""Convert the contents of `human_detectsions.csv` and `video_list.csv` and "meteors.txt" into a single data base file `videos.db`"""

import sqlite3
import pandas as pd
from fmdt.args import *
import fmdt.db
import fmdt.truth
import fmdt.utils

from fmdt.utils import md5ssl

def create_database_file():
    """Create our database 'videos.db' wiping the previous content"""
    f = open("videos.db", "w")
    f.close()

def create_video_table():

    con = sqlite3.connect("videos.db")
    cur = con.cursor()

    # ============================ Add MD5 hashes for data integrity =================
    # this is a little bit dangerous because we are now working recursively
    # vids = fmdt.retrieve_videos()
    # cur.execute("""CREATE TABLE video(
    #                 id INTEGER NOT NULL PRIMARY KEY,
    #                 name TEXT,
    #                 type TEXT,
    #                 md5 TEXT
    #             )""")

    cur.execute("""CREATE TABLE video(
                id INTEGER NOT NULL PRIMARY KEY,
                name TEXT,
                type TEXT
            )""")

    # Let's load in our csv
    df = pd.read_csv("./data/video_list.csv")

    for i in range(len(df)):
        r = df.iloc[i]

        id = r["id"]
        name = r["name"]
        type = r["type"]

        # cur.execute(f"""
        # INSERT INTO video VALUES
        #     ({id}, '{name}', '{type}', '{md5ssl(vids[i].full_path())}')
        # """)

        cur.execute(f"""
        INSERT INTO video VALUES
            ({id}, '{name}', '{type}')
        """)


        print(f"Finished inserting {name}")

    con.commit()
    con.close()

    print("Created video table from video_list.csv")

def create_human_detections():

    con = sqlite3.connect("videos.db")
    cur = con.cursor()

    #================ GroundTruths ===================
    # fmdt.truth.GroundTruth("")
    # fmdt.truth.init_ground_truth()
    csv_file = "./data/human_detections.csv"

    df_gt = pd.read_csv(csv_file)

    # Pandas DataFrame Ground Truths
    cur.execute("""CREATE TABLE human_detections (
                        id INTEGER NOT NULL PRIMARY KEY,
                        video_name TEXT,
                        start_x INTEGER,
                        start_y INTEGER,
                        start_frame INTEGER,
                        end_x INTEGER,
                        end_y INTEGER,
                        end_frame INTEGER,
                        FOREIGN KEY(video_name) REFERENCES video(name)
                )""")

    con.commit()

    for i in range(len(df_gt)):
        r = df_gt.iloc[i]

        vid_name = r["video_name"]
        start_x = r["start_x"]
        start_y = r["start_y"]
        start_frame = r["start_frame"]
        end_x = r["end_x"]
        end_y = r["end_y"]
        end_frame = r["end_frame"]

        cur.execute(f"""
        INSERT INTO human_detections VALUES
            ({i}, '{vid_name}', {start_x}, {start_y}, {start_frame}, {end_x}, {end_y}, {end_frame})
        """)

    print("Created human_detections table from human_detections.csv")

    con.commit()

    # # ================= Ground Truths in meteors.txt ========
    # meteors = fmdt.truth.load_meteors_file("./data/meteors.txt", "2022_05_31_tauh_34_meteors.mp4")

    # start = i + 1
    # for i in range(start, start + len(meteors)):
    #     m = meteors[i - start]

    #     query = f"""
    #     INSERT INTO human_detections VALUES
    #         ({i}, '{m.video_name}', {m.start_x}, {m.start_y}, {m.start_frame}, {m.end_x}, {m.end_y}, {m.end_frame})
    #     """

    #     cur.execute(query)

    # con.commit()
    con.close()

def create_video_clips():

    con = sqlite3.connect("videos.db")
    cur = con.cursor()

    # =================== Create video_clips from Windows =========================
    windows = fmdt.load_window(require_gt = True, db_dir = "./")

    # Assuming that tau is the last file in our windows list
    windows = [w for w in windows if w.name != "2022_05_31_tauh_34_meteors.mp4"]


    con = sqlite3.connect("videos.db")
    cur = con.cursor()


    cur.execute("""CREATE TABLE video_clips (
                    clip_id INTEGER NOT NULL PRIMARY KEY,
                    parent_id INTEGER NOT NULL,
                    start_frame INTEGER,
                    end_frame INTEGER,
                    FOREIGN KEY(parent_id) REFERENCES video(id))"""
                )

    all_clips = []
    for w in windows:
        all_clips += w.create_clips(db_dir = "./")

    for i, c in enumerate(all_clips):

        sql = f"""INSERT INTO video_clips VALUES (
            {i}, {c.parent_id()}, {c.start_frame}, {c.end_frame}
        )"""

        cur.execute(sql)


    con.commit()
    con.close()

    print("Created video_clips table")

def read_best_detections():
    """Read detections stored in best_d6.csv, best_d12.csv, best_windows.csv"""

    best_d6  = pd.read_csv("./data/best_d6.csv")
    best_d12 = pd.read_csv("./data/best_d12.csv")
    best_win = pd.read_csv("./data/best_window_new.csv")
    # best_win = pd.read_csv("./data/best_win_clips.csv")

    # The goal is to convert these files into a "best detection"

    # First, I need to create detect_args from these dataframes

    d6_detections:  list[tuple[int, fmdt.DetectArgs]] = []
    d12_detections: list[tuple[int, fmdt.DetectArgs]] = []

    # win_detections will use a clip id instead
    win_detections: list[tuple[int, fmdt.DetectArgs]] = []

    # draco6
    for _, r in best_d6.iterrows():

        if r.trk_rate != 0:

            v = fmdt.get_video(r.video_name)
            d_args = fmdt.Args.new(ccl_hyst_lo=r.lmin, ccl_hyst_hi=r.lmax).detect_args

            d6_detections.append(
                (v.id(db_dir = "./"), d_args, r.n_Tpos, r.trk_rate)
            )

    # draco12
    for _, r in best_d12.iterrows():

        if r.trk_rate != 0:

            v = fmdt.get_video(r.video_name)
            d_args = fmdt.Args.new(ccl_hyst_lo=r.lmin, ccl_hyst_hi=r.lmax).detect_args

            d12_detections.append(
                (v.id(db_dir = "./"), d_args, r.n_Tpos, r.trk_rate)
            )

    for _, r in best_win.iterrows():

        if r.trk_rate != 0:

            # v = fmdt.VideoClip(r.video_name, r.start_frame, r.end_frame)
            v = fmdt.VideoClip(r["name"], r.start_frame, r.end_frame)
            d_args = fmdt.Args.new(ccl_hyst_lo=r.lmin, ccl_hyst_hi=r.lmax, knn_d = 30).detect_args

            win_detections.append(
                # (v.id(db_dir = "./"), d_args, r.n_Tpos, r.trk_rate)
                (v.id(db_dir = "./"), d_args, r.tpos, r.trk_rate)
            )

    print(len(d6_detections))
    print(len(d12_detections))
    print(len(win_detections))


    # Go ahead and construct the new detect args table

    con = sqlite3.connect("videos.db")
    cur = con.cursor()

    cur.execute(fmdt.DetectArgs.sql_create_table())
    con.commit()

    cur.execute(f"""CREATE TABLE best_detections(
        id_video INTEGER,
        id_video_clip INTEGER,
        id_args INTEGER,
        true_pos INTEGER,
        trk_rate NUMERIC,
        FOREIGN KEY(id_args) REFERENCES detect_args(id_args)
    )""")
    con.commit()

    i = 0

    for id_video, dargs, tp, trk in d6_detections:
        cur.execute(dargs.to_sql_insert(i))
        cur.execute(f"INSERT INTO best_detections (id_video, id_args, true_pos, trk_rate) VALUES ({id_video}, {i}, {tp}, {trk})")
        i += 1

    for id_video, dargs, tp, trk in d12_detections:
        cur.execute(dargs.to_sql_insert(i))
        cur.execute(f"INSERT INTO best_detections (id_video, id_args, true_pos, trk_rate) VALUES ({id_video}, {i}, {tp}, {trk})")
        i += 1

    for id_clip, dargs, tp, trk in win_detections:
        cur.execute(dargs.to_sql_insert(i))
        cur.execute(f"INSERT INTO best_detections (id_video_clip, id_args, true_pos, trk_rate) VALUES ({id_clip}, {i}, {tp}, {trk})")
        i += 1

    con.commit()
    con.close()



def main():

    create_database_file()
    create_video_table()
    create_human_detections()
    create_video_clips()
    read_best_detections()

if __name__ == "__main__":
    main()