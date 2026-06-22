"""
Converts list of alignment results into output files, including 
a SPARKY peak list and a report for user review.
"""

from core.alignment_result import AlignmentResult


def write_sparky(results: list[AlignmentResult], filepath: str):
    """
    Writes a SPARKY-compatible peak list of aligned peaks.
    Peaks that fail to converge are written at their original positions.
    """

    with open (filepath, "w") as f:
        f.write("assignment w1 w2\n\n")

        for result in results:
            if result.status == "FAILED_TO_CONVERGE":
                f.write(
                    f"{result.original_peak.assignment} {result.original_peak.w1:.3f} {result.original_peak.w2:.3f}\n"
                )
                # Peaks that fail to converge appear in the SPARKY list at their original position. 
                
            else:
                f.write(
                    f"{result.aligned_peak.assignment} {result.aligned_peak.w1:.3f} {result.aligned_peak.w2:.3f}\n"
                )


def write_report(results: list[AlignmentResult], filepath: str):
    """
    Writes a CSV alignment report for inspection.
    Includes original and aligned peak positions, status, and collision information.
    """

    with open (filepath, "w") as f:
        f.write ("assignment,original w1,original w2,aligned w1,aligned w2,status,collisions\n")

        for result in results:
            collision_summary = ";".join(result.collision_with)
            f.write(f"{result.original_peak.assignment},{result.original_peak.w1:.3f},{result.original_peak.w2:.3f},")
            f.write(f"{result.aligned_peak.w1:.3f},{result.aligned_peak.w2:.3f},{result.status},{collision_summary}\n")

