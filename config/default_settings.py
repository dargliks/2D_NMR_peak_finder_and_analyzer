"""
Provides alignment default settings based on experiment type.
"""

from core.alignment_config import AlignmentConfig
from core.spectrum import Spectrum


def get_default_config(spectrum: Spectrum) -> AlignmentConfig:
    """
    Detects experiment type based on nuclei, and returns default alignment settings,
    including global spectrum shift, max refinement search radius, max refinement iterations
    and minimal peak intensity threshold.
    """

    if (
        spectrum.w1_nucleus == "15N" 
        and spectrum.w2_nucleus == "1H"
    ):
        # Standard NH-HSQC experiment. Default settings calibrated to a representative spectrum. 
        config = AlignmentConfig(
            global_w1_shift = 0.0,
            global_w2_shift = 0.0,
            radius_w1 = 0.2,
            radius_w2 = 0.02,
            max_iterations = 3,
            minimum_peak_intensity = 1e11
        )

    elif (
        spectrum.w1_nucleus == "13C" 
        and spectrum.w2_nucleus == "1H"
    ):
        # Methyl-TROSY HMQC experiment. Defaults currently use the generic settings until calibrated.
        config = AlignmentConfig(
            global_w1_shift = 0.0,
            global_w2_shift = 0.0,             
            radius_w1 = 0.2,
            radius_w2 = 0.02,
            max_iterations = 3,
            minimum_peak_intensity = 1e11
        )
         
    else:
        # unrecognized experiment type. Use generic default settings. 
        print("Unknown experiment type.")
        print("Using general default settings.")

        config = AlignmentConfig(
            global_w1_shift = 0.0,
            global_w2_shift = 0.0,
            radius_w1 = 0.2,
            radius_w2 = 0.02,
            max_iterations = 3,
            minimum_peak_intensity = 1e11
        )
         
    return config