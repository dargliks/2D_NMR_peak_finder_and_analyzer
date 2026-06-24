import pytest

from core.alignment_config import AlignmentConfig
from core.peak import Peak


@pytest.fixture
def simple_peak():
    return Peak(
        assignment="A1",
        w1=120.0,
        w2=8.0,
    )


@pytest.fixture
def another_peak():
    return Peak(
        assignment="A2",
        w1=120.1,
        w2=8.1,
    )


@pytest.fixture
def testing_config():
    return AlignmentConfig(
        global_w1_shift=0.0,
        global_w2_shift=0.0,
        radius_w1=2.0,
        radius_w2=2.0,
        max_iterations=3,
        minimum_peak_intensity=5,
    )

