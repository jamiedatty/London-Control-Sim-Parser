import re

def parse_sector_file(filename):
    sections = {
        'AIRPORT': [],
        'RUNWAY': [],
        'VOR': [],
        'NDB': [],
        'FIXES': []
    }
    
    current_section = None
    
    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            line = line.strip()
            
            # Skip empty lines and comments
            if not line or line.startswith(';'):
                continue
                
            # Check for section headers
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                continue
                
            # Process data lines based on current section
            if current_section in sections:
                sections[current_section].append(line)
    
    return sections

def write_nav_data(sections, output_dir="nav_data"):
    import os
    os.makedirs(output_dir, exist_ok=True)
    
    # Write Airport data
    with open(f"{output_dir}/airports.txt", "w") as f:
        f.write("ICAO,Frequency,Latitude,Longitude,Type\n")
        for line in sections['AIRPORT']:
            parts = line.split()
            if len(parts) >= 5:
                icao = parts[0]
                freq = parts[1]
                lat = parts[2]
                lon = parts[3]
                atype = parts[4]
                f.write(f"{icao},{freq},{lat},{lon},{atype}\n")
    
    # Write Runway data
    with open(f"{output_dir}/runways.txt", "w") as f:
        f.write("Runway1,Runway2,Heading1,Heading2,Lat1,Lon1,Lat2,Lon2,Airport\n")
        for line in sections['RUNWAY']:
            parts = line.split()
            if len(parts) >= 9:
                rwy1 = parts[0]
                rwy2 = parts[1]
                hdg1 = parts[2]
                hdg2 = parts[3]
                lat1 = parts[4]
                lon1 = parts[5]
                lat2 = parts[6]
                lon2 = parts[7]
                airport = parts[8]
                f.write(f"{rwy1},{rwy2},{hdg1},{hdg2},{lat1},{lon1},{lat2},{lon2},{airport}\n")
    
    # Write VOR data
    with open(f"{output_dir}/vors.txt", "w") as f:
        f.write("Identifier,Frequency,Latitude,Longitude\n")
        for line in sections['VOR']:
            parts = line.split()
            if len(parts) >= 4:
                ident = parts[0]
                freq = parts[1]
                lat = parts[2]
                lon = parts[3]
                f.write(f"{ident},{freq},{lat},{lon}\n")
    
    # Write NDB data
    with open(f"{output_dir}/ndbs.txt", "w") as f:
        f.write("Identifier,Frequency,Latitude,Longitude\n")
        for line in sections['NDB']:
            parts = line.split()
            if len(parts) >= 4:
                ident = parts[0]
                freq = parts[1]
                lat = parts[2]
                lon = parts[3]
                f.write(f"{ident},{freq},{lat},{lon}\n")
    
    # Write Fixes data
    with open(f"{output_dir}/fixes.txt", "w") as f:
        f.write("Identifier,Latitude,Longitude\n")
        for line in sections['FIXES']:
            parts = line.split()
            if len(parts) >= 3:
                ident = parts[0]
                lat = parts[1]
                lon = parts[2]
                f.write(f"{ident},{lat},{lon}\n")
            elif len(parts) == 2:
                # Some fixes might have only identifier and coordinates combined
                ident = parts[0]
                # Try to extract coords from the second part
                coords = parts[1]
                if coords.startswith('N') and 'W' in coords or coords.startswith('N') and 'E' in coords:
                    # Simple coordinate format
                    f.write(f"{ident},{coords},\n")
                else:
                    f.write(f"{ident},{coords},\n")

def main():
    input_file = "FASA-Package_20251004101136-251001-0002.sct"
    
    try:
        print("Parsing sector file...")
        sections = parse_sector_file(input_file)
        
        print(f"Found {len(sections['AIRPORT'])} airports")
        print(f"Found {len(sections['RUNWAY'])} runways")
        print(f"Found {len(sections['VOR'])} VORs")
        print(f"Found {len(sections['NDB'])} NDBs")
        print(f"Found {len(sections['FIXES'])} fixes")
        
        print("Writing navigation data to files...")
        write_nav_data(sections)
        
        print("Done! Check the 'nav_data' folder for the output files.")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure the file 'UK_2025_03.txt' is in the same directory as this script.")

if __name__ == "__main__":
    main()