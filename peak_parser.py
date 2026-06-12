from peak import Peak

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
        if len(parts) < len(col_map):
            continue

        assignment = parts[col_map["assignment"]]
        w1 = float(parts[col_map["w1"]])
        w2 = float(parts[col_map["w2"]])
        
        volume = None
        if "volume" in col_map:
            volume = float(parts[col_map["volume"]])

        data_height = None
        if "data_height" in col_map:
            data_height = float(parts[col_map["data_height"]])

        peak = Peak(
            assignment=assignment,
            w1=w1,
            w2=w2,
            volume=volume,
            data_height=data_height
        )
        
        peaks.append(peak)
    return peaks



