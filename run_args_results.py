# Convert the results obtained from `run_args.sh` into a three arrays of the same size:
#
# light_min
# light_max
# n_detected

# file = "draco6_random_lminmax_results.txt"
# file = "data_all_k30j10.txt"
file = "data_all.txt"
# file = "draco12_k30_j10.txt"

# Convert a '[1, 2, 3]' to [1, 2, 3]
def strlist_to_listint(strlist: str) -> list[int]:
    red = strlist[1:-1]
    ints = red.split(',')
    return [int(i.strip()) for i in ints]

print(strlist_to_listint('[1, 2, 3]'))

with open(file) as f:
    lines = [strlist_to_listint(l.strip()) for l in f.readlines()]

    lmins = lines[0::3]
    lmaxs = lines[1::3]
    dets  = lines[2::3]

    lmins = [j for i in lmins for j in i]    
    lmaxs = [j for i in lmaxs for j in i]    
    dets  = [j for i in dets  for j in i]    

    print(lmins)
    print(lmaxs)
    print(dets)