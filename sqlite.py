"""Learn how to play around with sql lite"""

import os
import fmdt
import fmdt.config

con = fmdt.config.load_config()
print(con)

files = os.listdir(con.d6)

all_vids = fmdt.config.get_local_vids()

print(all_vids)
print(len(all_vids))