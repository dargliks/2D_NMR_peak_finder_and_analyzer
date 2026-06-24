from file_io.peak_parser import load_peaks

def test_peak_parser_basic(tmp_path):
    file = tmp_path / "peaks.list"

    file.write_text(
        """
assignment w1 w2 volume data height

A1 120.0 8.0 50 1000
A2 121.0 9.0 60 2000
"""
    )

    peaks = load_peaks(file)

    assert len(peaks) == 2

    assert peaks[0].assignment == "A1"
    assert peaks[0].w1 == 120.0
    assert peaks[0].w2 == 8.0

    assert peaks[1].assignment == "A2"


def test_peak_parser_missing_volume(tmp_path):
    file = tmp_path / "peaks.list"

    file.write_text(
        """
assignment w1 w2 volume data height

A1 120.0 8.0    50
"""
    )

    peaks = load_peaks(file)

    assert len(peaks) == 1
    assert peaks[0].assignment == "A1"
    assert peaks[0].volume is None
    assert peaks[0].data_height == 50.0


def test_peak_parser_skips_bad_rows(tmp_path):
    file = tmp_path / "peaks.list"

    file.write_text(
        """
assignment w1 w2 volume data height

A1 120.0 8.0 50 1000
BAD ROW HERE
A2 121.0 9.0 60 2000 
"""
    )

    peaks = load_peaks(file)

    assert len(peaks) == 2
    assert peaks[0].assignment == "A1"
    assert peaks[1].assignment == "A2"