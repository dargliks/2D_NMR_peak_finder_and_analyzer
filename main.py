from spectrum_loader import load_ucsf
from peak_parser import load_peaks
from default_settings import get_default_config
from dataclasses import replace
from spectrum import Spectrum
from alignment_engine import align_peak
from collision_detector import detect_collisions
from output_writer import write_sparky, write_report

def main():
    print("2D NMR Peak Finder and Analyzer")

    spectrum_filename = input("please enter the spectrum filename:")
    spectrum = load_ucsf(filename=spectrum_filename)

    print("Spectrum loaded successfully.")
    print(f"Detected experiment: {spectrum.w1_nucleus}/{spectrum.w2_nucleus}")

    peaklist_filename = input("please enter the peak list filename:")
    peaks=load_peaks(peaklist_filename)

    print(f"{len(peaks)} peaks loaded successfully")

    default_config = get_default_config(spectrum)
    config = replace(default_config)



    while True:

        print()
        print("current settings:")
        print(f"1. Global w1 shift:              {config.global_w1_shift:.3f}ppm")
        print(f"2. Global w2 shift:              {config.global_w2_shift:.3f}ppm")
        print(f"3. Refinement radius w1:         {config.radius_w1:.3f}ppm")
        print(f"4. Refinement radius w2:         {config.radius_w2:.3f}ppm")
        print(f"5. maximum iterations:           {config.max_iterations}")
        print(f"6. minimun intensity threshold:  {config.minimum_peak_intensity:.1e}")
        print()
        print("99. reset default settings")
        print()
        print("0. start alignment")
        print()
        print("selection:")
        selection = int(input(">"))

        if selection == 0:
            break

        if selection == 1:
            config.global_w1_shift = float(input("apply global w1 shift (in ppm):"))

        elif selection == 2:
            config.global_w2_shift = float(input("apply global w2 shift (in ppm):"))

        elif selection == 3:
            config.radius_w1 = float(input("Insert new w1 refinement radius:"))

        elif selection == 4:
            config.radius_w2 = float(input("Insert new w2 refinement radius:"))

        elif selection == 5:
            config.max_iterations = int(input("Insert new maximum iterations:"))

        elif selection == 6:
            config.minimum_peak_intensity = float(input("Insert new minimum intensity threshold:"))            

        elif selection == 99:
            config = replace(default_config)

        else:
            print ("Invalid choice")

    spectrum.apply_shift(config.global_w1_shift, config.global_w2_shift)

    results = []

    for peak in peaks:
        result=align_peak(
            peak = peak,
            spectrum = spectrum,
            config = config,
        )

        results.append(result)
    
    detect_collisions(results)

    write_sparky(results, "aligned_peaks.list")
    write_report(results, "alignment_report.csv")
    





if __name__ == "__main__":
    main()