"""
Data model representing the result of aligning a single NMR peak.
"""

from dataclasses import dataclass, field

from core.peak import Peak


@dataclass
class AlignmentResult:
    """
    Represents the result of aligning a single NMR peak, including the original peak,
    the aligned peak, the alignment status, and any detected collisions.
    """
    original_peak: Peak
    aligned_peak: Peak
    status: str  # "CONVERGED" or "FAILED_TO_CONVERGE" or "LOW_SIGNAL"
    collision_with: list[str] = field(default_factory=list)  # Assignments of peaks that occupy the same final position