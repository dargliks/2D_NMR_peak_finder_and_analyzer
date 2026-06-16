from peak import Peak

def get_column_positions(header_line: str):
    positions = []
    in_column = False

    for i, char in enumerate(header_line):
        if char != " " and not in_column:
            positions.append(i)
            in_column = True

        elif char == " ":
            in_column = False

    return positions

def normalize_data_height(columns):
    normalized = []
    i = 0

    while i < len(columns):
        name, pos = columns[i]

        # Detect "data" followed immediately by "height"
        if (
            name.lower() == "data"
            and i + 1 < len(columns)
            and columns[i + 1][0].lower() == "height"
        ):
            # Merge into single column
            next_name, _ = columns[i + 1]
            normalized.append(("data_height", pos))
            i += 2
            continue

        normalized.append((name, pos))
        i += 1

    return normalized

def build_columns_from_header(header_line: str):
   
    # Step 1: find where each column starts
    starts = get_column_positions(header_line)

    # Step 2: ensure we can slice until end of line
    starts.append(len(header_line))

    columns = []

    for i in range(len(starts) - 1):
        start = starts[i]
        end = starts[i + 1]

        # Step 3: extract raw header text for this column
        raw_name = header_line[start:end].strip()

        columns.append((raw_name, start))

    # Step 4: merge known multi-word column ("Data Height")
    columns = normalize_data_height(columns)

    # Step 5: normalize names (lowercase etc.)
    columns = [(name.lower(), pos) for name, pos in columns]

    return columns

def parse_peak_line(line: str, columns):
    values = {}

    for i in range(len(columns)):
        name, start = columns[i]

        # compute end boundary
        if i + 1 < len(columns):
            end = columns[i + 1][1]
        else:
            end = len(line)

        raw_value = line[start:end].strip()

        values[name] = raw_value

    return values

def load_peaks(file_path):
    col_map = None
    peaks = []
    
    with open(file_path, "r") as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()

        if not line:
            continue

        parts = line.split()
        parts = [p for p in parts if p.lower() != "ga"]

        # detect header
        if parts[0].lower() == "assignment":
            header = parts
            normalized_header = []
            
            i = 0
            while i < len(header):
                if (
                    header[i].lower() == "data"
                    and i + 1 < len(header)
                    and header[i + 1].lower() == "height"
                ):
                    normalized_header.append("data_height")
                    i += 2
                    continue
            
                normalized_header.append(header[i].lower())
                i += 1

            col_map = {}
            for i, name in enumerate(normalized_header):
                col_map[name] = i
            
            continue

        if col_map is None:
            continue


        assignment = parts[col_map["assignment"]]
        w1 = float(parts[col_map["w1"]])
        w2 = float(parts[col_map["w2"]])

        volume = None
        data_height = None

        expected = len(col_map)
        actual = len(parts)

        if actual == expected:
            volume = float(parts[col_map["volume"]]) if "volume" in col_map else None
            data_height = float(parts[col_map["data_height"]]) if "data_height" in col_map else None
        elif actual == expected - 1:
            volume = None
            data_height = float(parts[col_map["data_height"] -1]) if "data_height" in col_map else None
        else:
            continue

        # volume = None
        # if "volume" in col_map:
        #     volume = float(parts[col_map["volume"]])

        # data_height = None
        # if "data_height" in col_map:
        #     data_height = float(parts[col_map["data_height"]])

        peak = Peak(
            assignment=assignment,
            w1=w1,
            w2=w2,
            volume=volume,
            data_height=data_height
        )
        
        peaks.append(peak)
    return peaks



