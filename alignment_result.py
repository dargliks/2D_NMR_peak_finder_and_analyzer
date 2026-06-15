from dataclasses import dataclass
from peak import Peak

@dataclass
class AlignmentResult:
    peak: Peak
    status: str  # "CONVERGED" or "FAILED_TO_CONVERGE"