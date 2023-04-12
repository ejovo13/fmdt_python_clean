import fmdt

ints = [(785, 790), (1222, 1250), (1426, 1439), (2288, 2323), (2836, 2850), (2810, 2888), (2928, 2933), (3426, 3434), (3857, 3862), (4155, 4179), (4262, 4268), (4447, 4460), (5323, 5330), (6790, 6811), (7199, 7207)]

print(ints)

win = fmdt.load_window()

v = win[0]

print(v)
print(v.exists())

fmdt.split_video_at_intervals(v.full_path(), ints, nframes_before=-15, nframes_after=50, overwrite=True)
