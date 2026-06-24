from dataclasses import replace

from alignment.collision_detector import detect_collisions
from core.alignment_result import AlignmentResult
from core.peak import Peak


def test_collision_detector_colliding_peaks(simple_peak):
    
    result_a = AlignmentResult(
        original_peak = simple_peak,
        aligned_peak = simple_peak,
        status = "CONVERGED"
    )

    result_b = AlignmentResult(
        original_peak = replace (simple_peak, assignment = "B1"),
        aligned_peak = replace (simple_peak, assignment = "B1"),
        status = "CONVERGED"
    )

    results = [result_a, result_b]
    detect_collisions(results)

    assert result_a.collision_with == ["B1"]
    assert result_b.collision_with == ["A1"]


def test_detect_collisions_separated_peaks(simple_peak,another_peak):
    
    result_a = AlignmentResult(
            original_peak = simple_peak,
            aligned_peak = simple_peak,
            status = "CONVERGED"
        )
    
    result_b = AlignmentResult(
        original_peak = another_peak,
        aligned_peak = another_peak,
        status = "CONVERGED"
    )

    results = [result_a, result_b]
    detect_collisions(results)

    assert result_a.collision_with == []
    assert result_b.collision_with == []


def test_detect_collisions_multiple_cases(simple_peak, another_peak):

    result_a = AlignmentResult(
        original_peak = simple_peak,
        aligned_peak = simple_peak,
        status = "CONVERGED"
    )

    result_b = AlignmentResult(
        original_peak = replace (simple_peak, assignment = "B1"),
        aligned_peak = replace (simple_peak, assignment = "B1"),
        status = "CONVERGED"
    )

    result_c = AlignmentResult(
        original_peak = another_peak,
        aligned_peak = another_peak,
        status = "CONVERGED"
    )

    results = [result_a, result_b, result_c]
    detect_collisions(results)

    assert result_a.collision_with == ["B1"]
    assert result_b.collision_with == ["A1"]
    assert result_c.collision_with == []    

