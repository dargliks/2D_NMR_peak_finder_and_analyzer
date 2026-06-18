from dataclasses import dataclass, field
from peak import Peak

@dataclass
class AlignmentResult:
    original_peak: Peak
    aligned_peak: Peak
    status: str  # "CONVERGED" or "FAILED_TO_CONVERGE" or "LOW SIGNAL"
    collision_with: list[str] = field(default_factory=list)