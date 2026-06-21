from core.alignment_config import AlignmentConfig


def main():
    config = AlignmentConfig(
        radius_w1=0.2,
        radius_w2=0.2,
        max_iterations=3,
        minimum_peak_intensity=5000
    )

    print(config)


if __name__ == "__main__":
    main()