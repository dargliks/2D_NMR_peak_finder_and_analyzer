import pytest
import numpy as np

from core.spectrum import Spectrum


@pytest.fixture
def simple_spectrum():
    intensities = np.array([
        [1.0, 2.0, 3.0],
        [4.0, 5.0, 6.0],
        [7.0, 8.0, 9.0],
    ])

    w1_axis = np.array([10.0, 11.0, 12.0])
    w2_axis = np.array([20.0, 21.0, 22.0])

    return Spectrum(
        intensities = intensities,
        w1_axis = w1_axis,
        w2_axis = w2_axis,
        w1_nucleus = "15N",
        w2_nucleus = "1H",
    )


def test_ppm_to_index(simple_spectrum):
    w1_idx, w2_idx = simple_spectrum.ppm_to_index(11.0, 21.0)

    assert w1_idx == 1
    assert w2_idx == 1


def test_index_to_ppm(simple_spectrum):
    w1, w2 = simple_spectrum.index_to_ppm(2, 0)

    assert w1 == 12.0
    assert w2 == 20.0


def test_get_intensity(simple_spectrum):
    value = simple_spectrum.get_intensity(11.0, 21.0)

    assert value == 5.0

def test_apply_shift(simple_spectrum):
    simple_spectrum.apply_shift(1.0, -2.0)

    assert simple_spectrum.w1_axis[0] == 11.0
    assert simple_spectrum.w2_axis[0] == 18.0


@pytest.fixture
def large_spectrum():
    intensities = np.arange(100).reshape(10, 10).astype(float)

    w1_axis = np.arange(10, 20)   # 10 points
    w2_axis = np.arange(20, 30)   # 10 points

    return Spectrum(
        intensities=intensities,
        w1_axis=w1_axis,
        w2_axis=w2_axis,
        w1_nucleus="15N",
        w2_nucleus="1H",
    )


def test_extract_region_basic(large_spectrum):
    region = large_spectrum.extract_region(
        center_w1=14,
        center_w2=24,
        radius_w1=2,
        radius_w2=2,
    )

    assert len(region.w1_axis) == 5
    assert len(region.w2_axis) == 5
    assert region.intensities.shape == (5, 5)


def test_extract_region_too_small_raises(large_spectrum):
    with pytest.raises(ValueError):
        large_spectrum.extract_region(
            center_w1=14,
            center_w2=24,
            radius_w1=0.01,
            radius_w2=0.01,
        )
