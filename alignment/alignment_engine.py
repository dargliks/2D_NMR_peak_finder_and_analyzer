"""
Core alignment engine for 2D NMR peak processing.

Performs iterative peak alignment by searching for local intensity maxima
within a configurable region around each peak. Stops when convergence is
detected or maximum iterations are reached.

Produces structured AlignmentResult objects for downstream analysis.
"""

from dataclasses import replace
import numpy as np

from core.alignment_config import AlignmentConfig
from core.alignment_result import AlignmentResult
from core.peak import Peak
from core.spectrum import Spectrum


def _align_once(peak: Peak, spectrum: Spectrum, config: AlignmentConfig,) -> Peak:
    """
    Performs a single iteration of peak alignment.
    Finds the highest intensity point within a local region around the
    current peak and returns an updated peak positioned at that maximum.
    """
     
    region = spectrum.extract_region(
        center_w1 = peak.w1,
        center_w2 = peak.w2,
        radius_w1 = config.radius_w1,
        radius_w2 = config.radius_w2,
    )

    local_max_idx = np.unravel_index(
        np.argmax(region.intensities),
        region.intensities.shape
    )
    # Find coordinates of maximum intensity in local region grid

    w1_idx, w2_idx = local_max_idx

    new_w1, new_w2 = region.index_to_ppm(w1_idx, w2_idx)

    new_data_height = float(
        region.intensities[w1_idx, w2_idx]
    )

    return replace(
        peak,
        w1 = new_w1,
        w2 = new_w2,
        data_height = new_data_height,
        volume = None, # not computed in V1 alignment; intensity-based alignment only  
    )


def align_peak(peak: Peak, spectrum: Spectrum, config: AlignmentConfig) -> AlignmentResult:
    """
    Iteratively aligns a peak to local intensity maxima until convergence.
    Stops when peak position stabilizes or maximum iterations are reached.
    """

    original_peak = peak
    current_peak = peak

    for i in range(config.max_iterations):

        new_peak = _align_once(
            current_peak,
            spectrum,
            config,
        )

        if (
             np.isclose(new_peak.w1, current_peak.w1, atol = 1e-6)
            and np.isclose(new_peak.w2, current_peak.w2, atol = 1e-6)
        ):
            if (new_peak.data_height < config.minimum_peak_intensity):
                return AlignmentResult(
                    original_peak = original_peak,
                    aligned_peak = new_peak, 
                    status = "LOW_SIGNAL"
                )
                
            else:
                return AlignmentResult(
                    original_peak=original_peak,
                    aligned_peak=new_peak,
                    status = "CONVERGED"
                )
            
        current_peak = new_peak

    return AlignmentResult(
        original_peak = original_peak,
        aligned_peak = current_peak,
        status = "FAILED_TO_CONVERGE"
    )
