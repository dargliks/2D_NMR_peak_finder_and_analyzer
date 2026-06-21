"""
Core data structure representing a 2D NMR spectrum and providing
utilities for coordinate conversion, intensity lookup, region extraction,
and global axis shifting.
"""

from dataclasses import dataclass
import numpy as np


@dataclass
class Spectrum:
    """
    Represents a 2D NMR spectrum including intensity data and chemical shift axes.
    Provides utilities for converting between ppm and index space, extracting
    regions, and applying global spectral shifts.
    """
    intensities: np.ndarray
    w1_axis: np.ndarray
    w2_axis: np.ndarray
    w1_nucleus: str
    w2_nucleus: str

    def ppm_to_index(self, w1_ppm: float, w2_ppm: float) -> tuple[int, int]:
        w1_idx = int(np.argmin(np.abs(self.w1_axis - w1_ppm)))
        w2_idx = int(np.argmin(np.abs(self.w2_axis - w2_ppm)))
        return w1_idx, w2_idx
    
    def get_intensity(self, w1_ppm: float, w2_ppm: float) -> float:
        w1_idx, w2_idx = self.ppm_to_index(w1_ppm, w2_ppm)
        return float(self.intensities[w1_idx, w2_idx])
    
    def index_to_ppm(self, w1_idx: int, w2_idx: int) -> tuple[float, float]:
        w1_ppm = float(self.w1_axis[w1_idx])
        w2_ppm = float(self.w2_axis[w2_idx])
        return w1_ppm, w2_ppm
    
    def extract_region(
        self,
        center_w1: float,
        center_w2: float,
        radius_w1: float,
        radius_w2: float
        ) -> "Spectrum":
        lower_w1 = center_w1 - radius_w1
        upper_w1 = center_w1 + radius_w1

        lower_w2 = center_w2 - radius_w2
        upper_w2 = center_w2 + radius_w2

        w1_mask = (
            (self.w1_axis >= lower_w1)
            & (self.w1_axis <= upper_w1)
        )

        w2_mask = (
            (self.w2_axis >= lower_w2)
            & (self.w2_axis <= upper_w2)
        )

        min_size_w1 = 5  # minimum number of points required for valid region
        min_size_w2 = 5  # minimum number of points required for valid region

        if np.sum(w1_mask) < min_size_w1:
            raise ValueError(
                f"The selected w1 search radius ({radius_w1} ppm) "
                f"contains only {np.sum(w1_mask)} data points. "
                f"Please increase the search radius."
            )

        if np.sum(w2_mask) < min_size_w2:
            raise ValueError(
                f"The selected w2 search radius ({radius_w2} ppm) "
                f"contains only {np.sum(w2_mask)} data points. "
                f"Please increase the search radius."
            )

        region_intensities = self.intensities[
            np.ix_(w1_mask, w2_mask)
        ]

        region_w1_axis = self.w1_axis[w1_mask]
        region_w2_axis = self.w2_axis[w2_mask]

        return Spectrum(
            intensities=region_intensities,
            w1_axis=region_w1_axis,
            w2_axis=region_w2_axis,
            w1_nucleus=self.w1_nucleus,
            w2_nucleus=self.w2_nucleus,
        )
    
    def apply_shift(
        self,
        w1_shift,
        w2_shift,
    ):
        self.w1_axis += w1_shift
        self.w2_axis += w2_shift
        # Applies global shift in-place (original spectrum is not preserved in V1 design)