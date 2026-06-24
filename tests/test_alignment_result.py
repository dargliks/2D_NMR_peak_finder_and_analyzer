from core.alignment_result import  AlignmentResult
from core.peak import Peak


def test_alignmentresult_stores_required_fields():
    original = Peak(
        assignment="A1",
        w1=120.5,
        w2=8.1,
    )

    aligned = Peak(
        assignment="A1",
        w1=120.3,
        w2=8.0,
    )

    result = AlignmentResult(
        original_peak = original,
        aligned_peak = aligned,
        status = "CONVERGED"
    )

    assert result.original_peak is original
    assert result.aligned_peak is aligned
    assert result.status == "CONVERGED"


def test_alignementresult_default_collision_list_is_empty():
    original = Peak(
        assignment="A1",
        w1=120.5,
        w2=8.1,
    )

    aligned = Peak(
        assignment="A1",
        w1=120.3,
        w2=8.0,
    )

    result = AlignmentResult(
        original_peak = original,
        aligned_peak = aligned,
        status = "CONVERGED"
    )

    assert result.collision_with == []


def test_alignmentresult_collision_lists_are_independant():
    original1 = Peak(
        assignment="A1",
        w1=120.5,
        w2=8.1,
    )

    aligned1 = Peak(
        assignment="A1",
        w1=120.3,
        w2=8.0,
    )

    result1 = AlignmentResult(
        original_peak = original1,
        aligned_peak = aligned1,
        status = "CONVERGED"
    )

    original2 = Peak(
        assignment="A2",
        w1=119.5,
        w2=9.1,
    )

    aligned2 = Peak(
        assignment="A1",
        w1=119.3,
        w2=9.2,
    )

    result2 = AlignmentResult(
        original_peak = original2,
        aligned_peak = aligned2,
        status = "CONVERGED"
    )

    result1.collision_with.append("Peak42")

    assert result1.collision_with == ["Peak42"]
    assert result2.collision_with == []