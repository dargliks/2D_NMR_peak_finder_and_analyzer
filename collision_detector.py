import numpy as np
from alignment_result import AlignmentResult

def detect_collisions(results) -> None:
    for i in range(len(results)):
        for j in range(i + 1, len(results)):
            p1 = results[i].aligned_peak
            p2 = results[j].aligned_peak
            eps_w1 = 1e-3
            eps_w2 = 1e-3
            if (
                np.isclose(p1.w1, p2.w1, atol=eps_w1)
                and np.isclose(p1.w2, p2.w2, atol=eps_w2)
            ):
                results[i].collision_with.append(p2.assignment)
                results[j].collision_with.append(p1.assignment)