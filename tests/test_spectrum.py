import numpy as np
from core.spectrum import Spectrum
from core.peak import Peak
from alignment.alignment_engine import align_peak
from core.alignment_config import AlignmentConfig
from file_io.spectrum_loader import load_ucsf
from file_io.peak_parser import load_peaks
from dev_tools.visualize_alignment import visualize_alignment
from alignment.collision_detector import detect_collisions
from file_io.output_writer import write_sparky, write_report


def main():
    intensities = np.array([
        [10, 20, 30],
        [40, 50, 60],
        [70, 80, 90]
    ])
    w1_axis = np.array([10.0, 9.0, 8.0])
    w2_axis = np.array([1.0, 2.0, 3.0])

    spectrum = Spectrum(
        intensities=intensities,
        w1_axis=w1_axis,
        w2_axis=w2_axis,
        w1_nucleus="15N",
        w2_nucleus="1H",
    )

    print("Spectrum created successfully!")
    print(spectrum)

    w1_ppm = 9.2
    w2_ppm = 2.1

    i, j = spectrum.ppm_to_index(w1_ppm, w2_ppm)

    print("Nearest indices:", i, j)

    intensity = spectrum.get_intensity(9.2, 2.1)

    print("Intensity:", intensity)

    w1_ppm, w2_ppm = spectrum.index_to_ppm(1, 1)

    print("PPM coordinates:", w1_ppm, w2_ppm)

    # region = spectrum.extract_region(
    #      center_w1=9.0,
    #      center_w2=2.0,
    #      radius_w1=0.2,
    #      radius_w2=0.2,
    #)

    # print("Region intensities:")
    # print(region.intensities)

    # print("Region w1 axis:")
    # print(region.w1_axis)

    # print("Region w2 axis:")
    # print(region.w2_axis)
    
    peak = Peak(
        assignment="2ALAN-H",
        w1=9.2,
        w2=2.1,
        volume=None,
        data_height=None
    )

    config = AlignmentConfig(
        radius_w1=0.2,
        radius_w2=0.02,
        max_iterations=3,
        minimum_peak_intensity=1e11,
    )
    
    # alignment_result = align_peak(peak, spectrum, config)
    # aligned_peak = alignment_result.peak

    # print("Original peak:", peak)
    # print("Aligned peak:", aligned_peak)

    # test_peaks = [
    #     Peak(
    #         assignment="TEST1",
    #         w1=8.0,
    #         w2=3.0,
    #         volume=None,
    #         data_height=None,
    #     ),
    #     Peak(
    #         assignment="TEST2",
    #         w1=8.1,
    #         w2=2.9,
    #         volume=None,
    #         data_height=None,
    #     ),
    #     Peak(
    #         assignment="TEST3",
    #         w1=9.0,
    #         w2=2.0,
    #         volume=None,
    #         data_height=None,
    #     ),
    # ]

    # for peak in test_peaks:
    #     alignment_result = align_peak(peak, spectrum, config)
    #     aligned_peak = alignment_result.peak

    #     print()
    #     print("Original:", peak)
    #     print("Aligned :", aligned_peak)


    real_spectrum = load_ucsf("example_spectrum.ucsf")

    print()
    print("Loaded spectrum successfully!")
    print(real_spectrum.intensities.shape)
    print(real_spectrum.w1_nucleus, real_spectrum.w2_nucleus)

    print()
    peaks = load_peaks("example_file_1.list")
    print(f"Loaded {len(peaks)} peaks.")
    print("First peak:", peaks[0])

    test_indices = [0, 8, 11, 22, 41]

    for Index in test_indices:
        peak=peaks[Index]
        
        alignment_result = align_peak(
            peak=peak,
            spectrum=real_spectrum,
            config=config,   
        )
        aligned_peak = alignment_result.aligned_peak

        print()
        print(f"Peak #{Index}: {peak.assignment}")

        #print(region.intensities.shape)

        print("Original:")
        print(peak)

        print("Aligned:")
        print(aligned_peak)

        visualize_alignment(
            spectrum=real_spectrum,
            original_peak=peak,
            aligned_peak=aligned_peak,
            alignment_config=config,
            plot_radius_w1=0.8,
            plot_radius_w2=0.4,
        )

    # original_first_w1 = real_spectrum.w1_axis[0]
    # original_first_w2 = real_spectrum.w2_axis[0]
    # real_spectrum.apply_shift (
    #     w1_shift = 0.5,
    #     w2_shift = -0.03,
    # )

    # assert real_spectrum.w1_axis[0] == original_first_w1 + 0.5
    # assert real_spectrum.w2_axis[0] == original_first_w2 - 0.03
    # print("Shift test passed!")

    peaks = load_peaks("example_file_2.list")
    results = []
    
    for peak in peaks:
        original_w1 = peak.w1
        oringinal_w2 = peak.w2
        result=align_peak(peak=peak,
            spectrum=real_spectrum,
            config=config,   
        )

        results.append(result)

        print(result.aligned_peak.assignment) 
        print("original peak:", result.original_peak.w1, result.original_peak.w2)
        print("aligned peak:", result.aligned_peak.w1, result.aligned_peak.w2) 
        print(result.status)
        print()

    test_indices = [0, 32, 34, 37]
    
    for Index in test_indices:
    
        peak=peaks[Index]
            
        alignment_result = align_peak(
            peak=peak,
            spectrum=real_spectrum,
            config=config,   
        )
        aligned_peak = alignment_result.aligned_peak
        visualize_alignment(
            spectrum=real_spectrum,
            original_peak=peak,
            aligned_peak=aligned_peak,
            alignment_config=config,
            plot_radius_w1=0.8,
            plot_radius_w2=0.4,
        )
    
    detect_collisions(results)

    write_sparky(
        results=results,
        filepath="aligned_peaks.list",
    )

    write_report(
        results=results,
        filepath="alignment_report.csv"
    )

    



        






if __name__ == "__main__":
    main()