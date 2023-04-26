import fmdt
import fmdt.truth

lst = fmdt.truth.load_meteors_file("meteors.txt", "2022_05_31_tauh_34_meteors.mp4")

fmdt.truth.save_meteors_file("meteors_copy.txt", lst)