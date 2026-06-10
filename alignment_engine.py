import numpy as np
from dataclasses import replace
from spectrum import Spectrum
from peak import Peak

def align_peak(peak: Peak, spectrum: Spectrum) -> Peak:

    # 1. Extract local region around the peak
    region = spectrum.extract_region(
        center_w1=peak.w1,
        center_w2=peak.w2,
        radius_w1=0.2,
        radius_w2=0.2,
    )

    # 2. Find index of strongest intensity in the region
    local_max_idx = np.unravel_index(
        np.argmax(region.intensities),
        region.intensities.shape
    )

    w1_idx, w2_idx = local_max_idx

    # 3. Convert that index back to ppm coordinates
    new_w1, new_w2 = region.index_to_ppm(w1_idx, w2_idx)

    #4. Find intensity at new position
    new_data_height = float(
        region.intensities[w1_idx, w2_idx]
    )

    # 5. Return NEW Peak (do NOT modify original)
    return replace(
        peak,
        w1=new_w1,
        w2=new_w2,
        data_height=new_data_height,
        volume=None,   
    )