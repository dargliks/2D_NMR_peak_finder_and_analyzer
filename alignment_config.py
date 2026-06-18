from dataclasses import dataclass


@dataclass
class AlignmentConfig:
    global_w1_shift: float
    global_w2_shift: float
    radius_w1: float
    radius_w2: float
    max_iterations: int
    minimum_peak_intensity: float