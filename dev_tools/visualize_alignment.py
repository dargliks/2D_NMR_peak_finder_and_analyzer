import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
# from spectrum import Spectrum
# from peak import Peak

def visualize_alignment(
    spectrum,
    original_peak,
    aligned_peak,
    alignment_config,
    plot_radius_w1,
    plot_radius_w2,
):
    
    region = spectrum.extract_region(
        center_w1=original_peak.w1,
        center_w2=original_peak.w2,
        radius_w1=plot_radius_w1,
        radius_w2=plot_radius_w2,
    )
    
    fig, ax = plt.subplots()
    ax.imshow(
        region.intensities,
        extent = [
            region.w2_axis[0],  
            region.w2_axis[-1],
            region.w1_axis[0],
            region.w1_axis[-1],
        ],
        origin="lower",
    )

    ax.set_xlabel("1H (ppm)")
    ax.set_ylabel("15N (ppm)")
    ax.set_title(original_peak.assignment)

    left = original_peak.w2 - alignment_config.radius_w2
    bottom = original_peak.w1 - alignment_config.radius_w1

    width = 2 * alignment_config.radius_w2
    height = 2 * alignment_config.radius_w1

    search_window = Rectangle(
        (left, bottom),
        width,
        height,
        fill=False,
        edgecolor="lime",
        linewidth=2,
        linestyle="--",
    )

    ax.add_patch(search_window)

    ax.plot(
        original_peak.w2,
        original_peak.w1,
        marker="o",
        color="red",
        markersize=10,
        fillstyle="none",
        label="Original",
    )

    ax.plot(
        aligned_peak.w2,
        aligned_peak.w1,
        marker="x",
        color="blue",
        markersize=10,
        label="Aligned",
    )

    plt.show()

