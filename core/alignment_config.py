"""
Data model representing the configuration parameters for peak alignment.
"""

from dataclasses import dataclass


@dataclass
class AlignmentConfig:
    """
    Represents the configuration parameters for peak alignment, including global spectrum 
    shift, permitted refinement radius, maximum number of refinement iterations and minimal
    peak intensity threshold.
    """
    global_w1_shift: float
    global_w2_shift: float
    radius_w1: float           # max allowed shift during refinement (w1)
    radius_w2: float           # max allowed shift during refinement (w2)
    max_iterations: int        
    minimum_peak_intensity: float  # Intensity threshold based on peak height