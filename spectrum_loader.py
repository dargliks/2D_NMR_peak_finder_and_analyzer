import nmrglue as ng
from spectrum import Spectrum

def load_ucsf(filename: str) -> Spectrum:
    dic, data = ng.sparky.read(filename)

    uc_w1 = ng.sparky.make_uc(dic, data, dim=0)
    uc_w2 = ng.sparky.make_uc(dic, data, dim=1)

    w1_axis = uc_w1.ppm_scale()
    w2_axis = uc_w2.ppm_scale()

    w1_nucleus = dic["w1"]["nucleus"]
    w2_nucleus = dic["w2"]["nucleus"]

    return Spectrum (
        intensities=data,
        w1_axis=w1_axis,
        w2_axis=w2_axis,
        w1_nucleus=w1_nucleus,
        w2_nucleus=w2_nucleus
    )