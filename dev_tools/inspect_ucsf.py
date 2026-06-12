import nmrglue as ng


def main():

    dic, data = ng.sparky.read("example_spectrum.ucsf")
    uc_w1 = ng.sparky.make_uc(dic, data, dim=0)
    uc_w2 = ng.sparky.make_uc(dic, data, dim=1)

    print("Dictionary type:", type(dic))
    print("Data type:", type(data))

    print("Data shape:", data.shape)

    print()
    print("Dictionary keys:")

    for key in dic.keys():
        print(key)
    
    print()
    print("w1 metadata:")
    print(dic["w1"])

    print()
    print("w2 metadata:")
    print(dic["w2"])

    print()
    print(type(uc_w1))
    print(type(uc_w2))

    print()
    print("w1 ppm limits:", uc_w1.ppm_limits())
    print("w2 ppm limits:", uc_w2.ppm_limits())

    w1_axis = uc_w1.ppm_scale()
    w2_axis = uc_w2.ppm_scale()

    print()
    print("First 5 w1 values:", w1_axis[:5])
    print("Last 5 w1 values:", w1_axis[-5:])

    print()
    print("First 5 w2 values:", w2_axis[:5])
    print("Last 5 w2 values:", w2_axis[-5:])


if __name__ == "__main__":
    main()
