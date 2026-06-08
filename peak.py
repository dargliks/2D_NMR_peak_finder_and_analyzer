from dataclasses import dataclass
from typing import Optional

@dataclass
class Peak:
    assignment: str
    w1: float
    w2: float

    volume: Optional[float] = None
    data_height: Optional[float] = None