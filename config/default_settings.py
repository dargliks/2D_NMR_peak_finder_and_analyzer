from core.alignment_config import AlignmentConfig

def get_default_config(spectrum):
    if (
        spectrum.w1_nucleus == "15N" 
        and spectrum.w2_nucleus == "1H"
    ):
        config = AlignmentConfig(
            global_w1_shift = 0.0,
            global_w2_shift = 0.0,
            radius_w1=0.2,
            radius_w2=0.02,
            max_iterations=3,
            minimum_peak_intensity=1e11
        )

    elif (
        spectrum.w1_nucleus == "13C" 
        and spectrum.w2_nucleus == "1H"
    ):
        
         config = AlignmentConfig(
            global_w1_shift = 0.0,
            global_w2_shift = 0.0,             
            radius_w1=0.2,
            radius_w2=0.02,
            max_iterations=3,
            minimum_peak_intensity=1e11
        )
         
    else:
        print("Unknown experiment type.")
        print("Using general default settings.")

        config = AlignmentConfig(
            global_w1_shift = 0.0,
            global_w2_shift = 0.0,
            radius_w1=0.2,
            radius_w2=0.02,
            max_iterations=3,
            minimum_peak_intensity=1e11
        )
         
    return config