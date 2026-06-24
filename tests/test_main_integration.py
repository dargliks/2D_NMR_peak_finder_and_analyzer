from core.alignment_result import AlignmentResult
from main import main


def test_main_happy_path(monkeypatch, simple_peak, testing_config):

    calls = {
        "align": 0,
        "collisions": 0,
        "sparky": 0,
        "report": 0,
    }

    class FakeSpectrum:
        w1_nucleus = "15N"
        w2_nucleus = "1H"

        def apply_shift(self, w1, w2):
            pass

    def fake_load_ucsf(filename):
        return FakeSpectrum()

    def fake_load_peaks(filename):
        return [simple_peak]

    def fake_get_default_config(spectrum):
        return testing_config

    def fake_align_peak(peak, spectrum, config):
        calls["align"] += 1

        return AlignmentResult(
            original_peak=peak,
            aligned_peak=peak,
            status="CONVERGED",
        )

    def fake_detect_collisions(results):
        calls["collisions"] += 1

    def fake_write_sparky(results, filename):
        calls["sparky"] += 1

    def fake_write_report(results, filename):
        calls["report"] += 1

    inputs = iter([
        "fake.ucsf",
        "fake.list",
        "0",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda prompt="": next(inputs),
    )

    monkeypatch.setattr(
        "main.load_ucsf",
        fake_load_ucsf,
    )

    monkeypatch.setattr(
        "main.load_peaks",
        fake_load_peaks,
    )

    monkeypatch.setattr(
        "main.get_default_config",
        fake_get_default_config,
    )

    monkeypatch.setattr(
        "main.align_peak",
        fake_align_peak,
    )

    monkeypatch.setattr(
        "main.detect_collisions",
        fake_detect_collisions,
    )

    monkeypatch.setattr(
        "main.write_sparky",
        fake_write_sparky,
    )

    monkeypatch.setattr(
        "main.write_report",
        fake_write_report,
    )

    main()

    assert calls["align"] == 1
    assert calls["collisions"] == 1
    assert calls["sparky"] == 1
    assert calls["report"] == 1