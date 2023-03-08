import fmdt

f_start = [785, 1222, 1426, 2288, 2836, 2862, 2928, 3426, 3857, 4155, 4262, 4447, 5323, 6790, 7199]
f_end   = [790, 1250, 1439, 2323, 2850, 2888, 2933, 3434, 3862, 4179, 4268, 4460, 5330, 6811, 7207]

# Now make the pairs
pairs = []
for i in range(len(f_start)):
    pairs.append((f_start[i], f_end[i]))

print(pairs)

condensed_pairs = fmdt.condense_start_end(pairs, 5)

print(f"Converting\n{pairs}\n\tto\n{condensed_pairs}")

# Now go through and separate videos at these segments

