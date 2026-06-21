"""
Detects collisions between aligned NMR peaks based on proximity in ppm space.

Marks peaks as colliding when their final aligned positions are within
a small tolerance in both dimensions.
"""

import numpy as np

from core.alignment_result import AlignmentResult


def detect_collisions(results) -> None:
    """
    Detects collisions between aligned peaks based on proximity in ppm space.
    If two aligned peaks fall within a small tolerance in both w1 and w2,
    they are marked as colliding in both corresponding results.
    """

    eps_w1 = 1e-3  # collision tolerance in ppm (w1 axis)
    eps_w2 = 1e-3  # collision tolerance in ppm (w2 axis)
    
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            p1 = results[i].aligned_peak
            p2 = results[j].aligned_peak
            if (
                np.isclose(p1.w1, p2.w1, atol=eps_w1)
                and np.isclose(p1.w2, p2.w2, atol=eps_w2)
            ):
                results[i].collision_with.append(p2.assignment)
                results[j].collision_with.append(p1.assignment)