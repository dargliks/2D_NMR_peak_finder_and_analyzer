import numpy as np
from dataclasses import replace
from spectrum import Spectrum
from peak import Peak
from alignment_config import AlignmentConfig
from alignment_result import AlignmentResult


def _align_once(peak: Peak, spectrum: Spectrum, config: AlignmentConfig,) -> Peak:
    
    # 1. Extract local region around the peak
    region = spectrum.extract_region(
        center_w1=peak.w1,
        center_w2=peak.w2,
        radius_w1=config.radius_w1,
        radius_w2=config.radius_w2,
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


def align_peak(peak: Peak, spectrum: Spectrum, config: AlignmentConfig) -> AlignmentResult:

    current_peak = peak

    for i in range(config.max_iterations):

        new_peak = _align_once(
            current_peak,
            spectrum,
            config,
        )

        if (
            new_peak.w1 == current_peak.w1
            and new_peak.w2 == current_peak.w2
        ):
            print ("iteration count:", i)
            return AlignmentResult(
                peak=new_peak,
                status="CONVERGED"
            )
            
        current_peak = new_peak

    return AlignmentResult(
        peak=current_peak,
        status="FAILED_TO_CONVERGE"
    )
