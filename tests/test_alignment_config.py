from core.alignment_config import AlignmentConfig

def test_alignmentconfig_stores_values():
    config = AlignmentConfig(
        global_w1_shift = 0.15,
        global_w2_shift = -0.03,
        radius_w1 = 0.2,
        radius_w2 = 0.02,
        max_iterations = 5,
        minimum_peak_intensity = 1e11,
    )

    assert config.global_w1_shift == 0.15
    assert config.global_w2_shift == -0.03
    assert config.radius_w1 == 0.2
    assert config.radius_w2 == 0.02
    assert config.max_iterations == 5
    assert config.minimum_peak_intensity == 1e11