import numpy as np
from spectrum import Spectrum


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


if __name__ == "__main__":
    main()