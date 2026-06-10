import numpy as np
from spectrum import Spectrum
from peak import Peak
from alignment_engine import align_peak
from alignment_config import AlignmentConfig


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
        w2_axis=w2_axis
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

    region = spectrum.extract_region(
        center_w1=9.0,
        center_w2=2.0,
        radius_w1=0.2,
        radius_w2=0.2,
    )

    print("Region intensities:")
    print(region.intensities)

    print("Region w1 axis:")
    print(region.w1_axis)

    print("Region w2 axis:")
    print(region.w2_axis)
    
    peak = Peak(
        assignment="2ALAN-H",
        w1=9.2,
        w2=2.1,
        volume=None,
        data_height=None
    )

    config = AlignmentConfig(
        radius_w1=0.2,
        radius_w2=0.2,
        max_iterations=3
    )
    
    aligned_peak = align_peak(peak, spectrum, config)

    print("Original peak:", peak)
    print("Aligned peak:", aligned_peak)

    test_peaks = [
        Peak(
            assignment="TEST1",
            w1=8.0,
            w2=3.0,
            volume=None,
            data_height=None,
        ),
        Peak(
            assignment="TEST2",
            w1=8.1,
            w2=2.9,
            volume=None,
            data_height=None,
        ),
        Peak(
            assignment="TEST3",
            w1=9.0,
            w2=2.0,
            volume=None,
            data_height=None,
        ),
    ]

    for peak in test_peaks:
        aligned_peak = align_peak(peak, spectrum, config)

        print()
        print("Original:", peak)
        print("Aligned :", aligned_peak)

if __name__ == "__main__":
    main()