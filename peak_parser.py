from peak import Peak

def load_peaks(file_path):
    peaks = []
    
    with open(file_path, "r") as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()

        if not line:
            continue

        parts = line.split()

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
            
            print(col_map)
            continue

        assignment = parts[col_map["assignment"]]
        w1 = float(parts[col_map["w1"]])
        w2 = float(parts[col_map["w2"]])

        peak = Peak(assignment, w1, w2)
        print(peak)

load_peaks("example_file_1.list")


