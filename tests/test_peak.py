from core.peak import Peak

def test_peak_stores_required_fields():

    peak = Peak(
        assignment = "A1",
        w1 = 120.5,
        w2 = 8.15,
    )

    assert peak.assignment == "A1"
    assert peak.w1 == 120.5
    assert peak.w2 == 8.15


def test_peak_optional_fields_default_to_none():

    peak = Peak(
        assignment = "A1",
        w1 = 120.5,
        w2 = 8.15,
    )

    assert peak.volume is None
    assert peak.data_height is None


def test_peak_accepts_optional_values():

    peak = Peak (
        assignment="A1",
        w1=120.5,
        w2=8.15,
        volume=2.3e8,
        data_height=5.1e7,
    )

    assert peak.volume == 2.3e8
    assert peak.data_height == 5.1e7


