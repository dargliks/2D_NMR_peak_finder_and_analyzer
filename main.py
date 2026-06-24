"""
Command-line interface for the 2D NMR Peak Finder and Analyzer.

Loads the spectrum and peak list, allows the user to adjust alignment
parameters, runs the alignment, and writes the output files.
"""

import os
from dataclasses import replace

from alignment.alignment_engine import align_peak
from alignment.collision_detector import detect_collisions
from config.default_settings import get_default_config
from file_io.output_writer import write_report, write_sparky
from file_io.peak_parser import load_peaks
from file_io.spectrum_loader import load_ucsf


def main():
    """
    Run the command-line interface for the peak alignment workflow.
    """
    print("2D NMR Peak Finder and Analyzer")

    # Load input files
    while True:
        spectrum_filename = input("Please enter the spectrum filename:")
        try:
            spectrum = load_ucsf(filename=spectrum_filename)
            print("Spectrum loaded successfully.")
            print(f"Detected experiment: {spectrum.w1_nucleus}/{spectrum.w2_nucleus}")
            break
        except FileNotFoundError:
            print("File not found. Please type valid file name.")
        except Exception:
            print("File could not be parsed. Please check format.")

    while True:
        peaklist_filename = input("Please enter the peak list filename:")
        try:
            peaks = load_peaks(peaklist_filename)
            print(f"{len(peaks)} peaks loaded successfully")
            break
        except FileNotFoundError:
            print("File not found. Please type valid file name.")
        except Exception:
            print("File could not be parsed. Please check format.")

    # Configure alignment settings
    default_config = get_default_config(spectrum)
    config = replace(default_config)

    while True:
        print()
        print("Current settings:")
        print(f"1. Global w1 shift:              {config.global_w1_shift:.3f}ppm")
        print(f"2. Global w2 shift:              {config.global_w2_shift:.3f}ppm")
        print(f"3. Refinement radius w1:         {config.radius_w1:.3f}ppm")
        print(f"4. Refinement radius w2:         {config.radius_w2:.3f}ppm")
        print(f"5. Maximum iterations:           {config.max_iterations}")
        print(f"6. Minimum intensity threshold:  {config.minimum_peak_intensity:.1e}")
        print()
        print("99. Reset default settings")
        print()
        print("0. Start alignment")
        print()
        print("Selection:")

        while True:
            selection_text = input(">")
            try: 
                selection = int(selection_text)
                break
            except ValueError:
                print("Invalid input. Please enter a number.")

        if selection == 0:
            break

        if selection == 1:
            while True:
                w1_shift_input = input("Apply global w1 shift (in ppm):")
                try:
                    config.global_w1_shift = float(w1_shift_input)
                    print(f"Updated w1 global shift: {w1_shift_input} ppm")
                    break
                except ValueError:
                    print("Invalid input. Please insert valid w1 global shift value (number only, in ppm)")

        elif selection == 2:
            while True:
                w2_shift_input = input("Apply global w2 shift (in ppm):")
                try:
                    config.global_w2_shift = float(w2_shift_input)
                    print(f"Updated w2 global shift: {w2_shift_input} ppm")
                    break
                except ValueError:
                    print("Invalid input. Please insert valid w2 global shift value (number only, in ppm)")


        elif selection == 3:
            while True:
                w1_radius_input = input("Insert new w1 refinement radius (in ppm):")
                try:
                    config.radius_w1 = float(w1_radius_input)
                    print(f"Updated w1 refinement radius: {w1_radius_input} ppm")
                    break
                except ValueError:
                    print("Invalid input. Please insert valid w1 refinement radius value (number only, in ppm)")


        elif selection == 4:
            while True:
                w2_radius_input = input("Insert new w2 refinement radius (in ppm):")
                try:
                    config.radius_w2 = float(w2_radius_input)
                    print(f"Updated w2 refinement radius: {w2_radius_input} ppm")
                    break
                except ValueError:
                    print("Invalid input. Please insert valid w2 refinement radius value (number only, in ppm)")

        elif selection == 5:
            while True:
                max_iterations_input = input("Insert new maximum iterations:")
                try: 
                    config.max_iterations = int(max_iterations_input)
                    print(f"Updated maximum iterations: {max_iterations_input}")
                    break
                except ValueError:
                    print("Invalid input. Please insert valid max iterations value (whole number only)")

        elif selection == 6:
            while True:
                min_intensity_input = input("Insert new minimum intensity threshold:")
                try:
                    config.minimum_peak_intensity = float(min_intensity_input)
                    print(f"Updated minimum intensity threshold: {min_intensity_input}")
                    break
                except ValueError:
                    print("Invalid input. Please insert valid minimum intensity threshold value (number only)")

        elif selection == 99:
            config = replace(default_config)

        else:
            print ("Invalid choice")

    spectrum.apply_shift(config.global_w1_shift, config.global_w2_shift)

    results = []

    # Run peak alignment
    for peak in peaks:
        result = align_peak(
            peak = peak,
            spectrum = spectrum,
            config = config,
        )

        results.append(result)

    # Summarize alignment results
    converged = 0
    low = 0
    failed = 0

    for result in results:
        if result.status == "CONVERGED":
            converged += 1

        elif result.status == "LOW_SIGNAL":
            low += 1
        
        elif result.status == "FAILED_TO_CONVERGE":
            failed += 1
    
    print("Alignment complete.")
    print()
    print(f"{len(results)} peaks processed.")
    print()
    print("Status summary:")
    print(f"CONVERGED:            {converged}")
    print(f"LOW_SIGNAL:           {low}")
    print(f"FAILED_TO_CONVERGE:   {failed}")
    
    # Detect collisions
    detect_collisions(results)

    collision_count = 0
    for result in results:
        if result.collision_with:
            collision_count += 1

    print()
    print(f"{collision_count} peaks involved in collisions.")

    # Write output files
    os.makedirs("outputs", exist_ok=True)
    write_sparky(results, "outputs/aligned_peaks.list")
    write_report(results, "outputs/alignment_report.csv")

    print()
    print("Output files written to outputs/.")


if __name__ == "__main__":
    main()