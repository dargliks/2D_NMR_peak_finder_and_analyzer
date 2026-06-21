"""
Data model representing a single assigned NMR peak.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Peak:
    """
    Represents a single assigned NMR peak with its assignment, 
    chemical shift coordinates, and optional intensity values.
    """
    assignment: str
    w1: float
    w2: float

    volume: Optional[float] = None
    data_height: Optional[float] = None