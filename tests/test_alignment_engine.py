import pytest
import numpy as np

from alignment.alignment_engine import align_peak
from core.spectrum import Spectrum

@pytest.fixture
def alignment_spectrum_5x5():
    intensities = np.array([
        [0, 0, 0, 0, 0],
        [0, 1, 2, 1, 0],
        [0, 2, 9, 2, 0],
        [0, 1, 2, 1, 0],
        [0, 0, 0, 0, 0],
    ], dtype=float)

    return Spectrum(
        intensities=intensities,
        w1_axis=np.array([118, 119, 120, 121, 122], dtype=float),
        w2_axis=np.array([6, 7, 8, 9, 10], dtype=float),
        w1_nucleus="15N",
        w2_nucleus="1H",
    )


def test_alignment_engine_centered_peak(alignment_spectrum_5x5,simple_peak, testing_config):

    result = align_peak(simple_peak, alignment_spectrum_5x5, testing_config)

    assert np.isclose(result.aligned_peak.w1, 120.0)
    assert np.isclose(result.aligned_peak.w2, 8.0)
    assert result.aligned_peak.data_height == pytest.approx(9.0)
    assert result.status == "CONVERGED"


@pytest.fixture
def alignment_spectrum_move_then_converge():
    intensities = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 1, 2, 2, 2, 1, 1, 0, 0],
        [0, 1, 2, 5, 2, 1, 1, 0, 0],
        [0, 1, 2, 2, 2, 1, 0, 0, 0],
        [0, 1, 1, 1, 9, 1, 0, 0, 0],
        [0, 0, 0, 1, 2, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ], dtype=float)

    return Spectrum(
        intensities=intensities,
        w1_axis=np.arange(118, 127, dtype=float),
        w2_axis=np.arange(6, 15, dtype=float),
        w1_nucleus="15N",
        w2_nucleus="1H",
    )


def test_alignment_engine_moves_then_converges(
    simple_peak,
    testing_config,
    alignment_spectrum_move_then_converge,
):
    result = align_peak(simple_peak, alignment_spectrum_move_then_converge, testing_config)

    # should end up at the true maximum (9 region)
    assert np.isclose(result.aligned_peak.w1, 123.0)
    assert np.isclose(result.aligned_peak.w2, 10.0)
    assert result.aligned_peak.data_height == pytest.approx(9.0)
    assert result.status == "CONVERGED"


def test_alignment_engine_low_signal(simple_peak, testing_config, alignment_spectrum_5x5):

    # Copy spectrum but weaken the peak below threshold (5)
    weak_intensities = alignment_spectrum_5x5.intensities.copy()
    weak_intensities[2, 2] = 3  # was 9, now below threshold

    spectrum = Spectrum(
        intensities=weak_intensities,
        w1_axis=alignment_spectrum_5x5.w1_axis,
        w2_axis=alignment_spectrum_5x5.w2_axis,
        w1_nucleus=alignment_spectrum_5x5.w1_nucleus,
        w2_nucleus=alignment_spectrum_5x5.w2_nucleus,
    )

    result = align_peak(simple_peak, spectrum, testing_config)

    # it still converges geometrically
    assert np.isclose(result.aligned_peak.w1, 120.0)
    assert np.isclose(result.aligned_peak.w2, 8.0)

    # BUT signal is too low → rejected
    assert result.status == "LOW_SIGNAL"

@pytest.fixture
def alignment_spectrum_fail_to_converge():
    intensities = np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 2, 2, 2, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 2, 5, 2, 1, 1, 0, 0, 0, 0, 0],
        [0, 1, 2, 2, 7, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 5, 9, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 1, 2, 1, 11, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 13, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 17, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ], dtype=float)

    return Spectrum(
        intensities=intensities,
        w1_axis=np.arange(118, 130, dtype=float),
        w2_axis=np.arange(6, 18, dtype=float),
        w1_nucleus="15N",
        w2_nucleus="1H",
    )


def test_alignment_engine_fails_to_converge(
    simple_peak,
    testing_config,
    alignment_spectrum_fail_to_converge,
):
    result = align_peak(simple_peak, alignment_spectrum_fail_to_converge, testing_config)
    assert result.status == "FAILED_TO_CONVERGE"
    assert result.aligned_peak.data_height < 17
