from file_io.peak_parser import get_column_positions, build_columns_from_header, parse_peak_line

example_header = "      Assignment         w1         w2        Volume   Data Height "

example_positions = get_column_positions(example_header)
print(example_positions)

example_names = build_columns_from_header (example_header)
print(example_names)

example_line_1 = "          2ALAN-H    122.289      8.063   2.15e+13 ga 620720029696 "
example_line_2 = "         27ALAN-H    123.013      8.963                -2729510144 " 

parsed_line_1 = parse_peak_line(example_line_1, example_names)
parsed_line_2 = parse_peak_line(example_line_2, example_names)

print(parsed_line_1)
print(parsed_line_2)
