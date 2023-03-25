import fmdt
import fmdt.truth

lst = fmdt.truth.load_meteors_file("meteors.txt")

fmdt.truth.save_meteors_file("meteors_copy.txt", lst)