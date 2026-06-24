import numpy as np

from file_io.spectrum_loader import load_ucsf
from core.spectrum import Spectrum


class FakeUC:
    def __init__(self, scale):
        self.scale = scale

    def ppm_scale(self):
        return self.scale


def test_load_ucsf_returns_spectrum(monkeypatch):

    fake_data = np.array([
        [1.0, 2.0],
        [3.0, 4.0],
    ])

    fake_dic = {
        "w1": {"nucleus": "15N"},
        "w2": {"nucleus": "1H"},
    }

    def fake_read(filename):
        return fake_dic, fake_data

    def fake_make_uc(dic, data, dim):
        if dim == 0:
            return FakeUC(np.array([120.0, 121.0]))

        return FakeUC(np.array([8.0, 9.0]))

    monkeypatch.setattr(
        "file_io.spectrum_loader.ng.sparky.read",
        fake_read,
    )

    monkeypatch.setattr(
        "file_io.spectrum_loader.ng.sparky.make_uc",
        fake_make_uc,
    )

    spectrum = load_ucsf("fake.ucsf")

    assert isinstance(spectrum, Spectrum)


def test_load_ucsf_copies_values(monkeypatch):

    fake_data = np.array([
        [1.0, 2.0],
        [3.0, 4.0],
    ])

    fake_dic = {
        "w1": {"nucleus": "15N"},
        "w2": {"nucleus": "1H"},
    }

    def fake_read(filename):
        return fake_dic, fake_data

    def fake_make_uc(dic, data, dim):
        if dim == 0:
            return FakeUC(np.array([120.0, 121.0]))

        return FakeUC(np.array([8.0, 9.0]))

    monkeypatch.setattr(
        "file_io.spectrum_loader.ng.sparky.read",
        fake_read,
    )

    monkeypatch.setattr(
        "file_io.spectrum_loader.ng.sparky.make_uc",
        fake_make_uc,
    )

    spectrum = load_ucsf("fake.ucsf")

    assert np.array_equal(
        spectrum.intensities,
        fake_data,
    )

    assert np.array_equal(
        spectrum.w1_axis,
        np.array([120.0, 121.0]),
    )

    assert np.array_equal(
        spectrum.w2_axis,
        np.array([8.0, 9.0]),
    )

    assert spectrum.w1_nucleus == "15N"
    assert spectrum.w2_nucleus == "1H"