import fmdt

# Specifiy where your videos are stored
fmdt.init(d6_dir = "/home/ejovo/Videos/Watec6mm",
          d12_dir = "/home/ejovo/Videos/Watec12mm",
          win_dir = "/home/ejovo/Videos/Window")

# Load in the database
gt6 = fmdt.load_gt6()
gt12 = fmdt.load_gt12()

# Far cleaner than before!
args = fmdt.detect_args(light_min=254, light_max=255, timeout=1)

success_list = gt6.try_command(args)

print(success_list)
print(sum(success_list))