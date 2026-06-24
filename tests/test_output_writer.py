from dataclasses import replace

from core.alignment_result import AlignmentResult
from file_io.output_writer import write_report, write_sparky

def test_write_sparky_basic (tmp_path, simple_peak):
    output_file = tmp_path / "aligned.list"

    result = AlignmentResult(
        original_peak = simple_peak,
        aligned_peak = simple_peak,
        status = "CONVERGED"
    )

    write_sparky([result],output_file)

    contents = output_file.read_text()

    assert "assignment w1 w2" in contents
    assert "A1" in contents
    assert "120.000" in contents
    assert "8.000" in contents


def test_write_sparky_failed_peak_uses_original_position(tmp_path, simple_peak):
    output_file = tmp_path / "aligned.list"

    aligned_peak = replace(
        simple_peak,
        w1=121.0,
        w2=9.0,
    )

    result = AlignmentResult(
        original_peak = simple_peak,
        aligned_peak = aligned_peak,
        status = "FAILED_TO_CONVERGE",
    )
    
    write_sparky([result], output_file)

    contents = output_file.read_text()

    assert "120.000" in contents
    assert "8.000" in contents

    assert "121.000" not in contents
    assert "9.000" not in contents


def test_write_report_basic(tmp_path, simple_peak):
    output_file = tmp_path / "report.csv"

    result = AlignmentResult(
        original_peak=simple_peak,
        aligned_peak=simple_peak,
        status="CONVERGED",
    )

    write_report([result], output_file)

    contents = output_file.read_text()

    # header
    assert "assignment,original w1,original w2,aligned w1,aligned w2,status,collisions" in contents

    # data
    assert "A1" in contents
    assert "120.000" in contents
    assert "8.000" in contents
    assert "CONVERGED" in contents


def test_write_report_collision_field(tmp_path, simple_peak):
    output_file = tmp_path / "report.csv"

    result = AlignmentResult(
        original_peak=simple_peak,
        aligned_peak=simple_peak,
        status="CONVERGED",
        collision_with=["B1", "C2"],
    )

    write_report([result], output_file)

    contents = output_file.read_text()

    assert "B1;C2" in contents