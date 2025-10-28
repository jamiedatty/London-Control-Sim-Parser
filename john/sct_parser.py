#!/usr/bin/env python3
"""
EuroScope .SCT File Parser for FASA London Control Adaptation
Parses VORs, NDBs, Fixes, and Airports from .sct files
"""

import re
import os
import tkinter as tk
from tkinter import filedialog, messagebox
import sys

def convert_coordinates(coord_string):
    """
    Convert coordinates from various formats to DDMMSSH format
    Input examples: 
    - S028.34.14.350 E016.32.01.798
    - S028.34.23.941 E016.32.03.609
    Returns: DDMMSSH DDMMSSH format
    """
    if not coord_string or coord_string.strip() == '':
        return None
        
    # Extract latitude and longitude parts
    lat_match = re.search(r'([NS])(\d{2,3})\.(\d{2})\.(\d{2})\.(\d{2,3})', coord_string)
    lon_match = re.search(r'([EW])(\d{2,3})\.(\d{2})\.(\d{2})\.(\d{2,3})', coord_string)
    
    if lat_match and lon_match:
        lat_hemi, lat_deg, lat_min, lat_sec, lat_frac = lat_match.groups()
        lon_hemi, lon_deg, lon_min, lon_sec, lon_frac = lon_match.groups()
        
        # Ensure consistent formatting (2-digit seconds)
        lat_sec = lat_sec.zfill(2)
        lon_sec = lon_sec.zfill(2)
        
        # Format as DDMMSSH (degrees, minutes, seconds, hemisphere)
        lat_formatted = f"{lat_deg}{lat_min}{lat_sec}{lat_hemi}"
        lon_formatted = f"{lon_deg}{lon_min}{lon_sec}{lon_hemi}"
        
        return f"{lat_formatted} {lon_formatted}"
    
    return None

def parse_section(section_name, lines, data_type):
    """Parse a specific section from the .sct file"""
    results = []
    current_section = False
    
    for line in lines:
        line = line.strip()
        
        # Check if we've entered our target section
        if line.upper() == f"[{section_name.upper()}]":
            current_section = True
            continue
        # Check if we've left our target section
        elif line.startswith('[') and current_section:
            break
        # Skip empty lines and comments
        elif not line or line.startswith(';') or not current_section:
            continue
        
        # Parse the line based on data type
        if data_type == "VOR":
            # VOR format: ABV  112.100 S028.34.14.350 E016.32.01.798
            parts = line.split()
            if len(parts) >= 4:
                ident = parts[0]
                coords = ' '.join(parts[2:4])
                formatted_coords = convert_coordinates(coords)
                if formatted_coords:
                    results.append(f"{ident}\t{formatted_coords} v - ")
        
        elif data_type == "NDB":
            # NDB format: BI   233.000 S020.59.50.999 E031.33.54.000
            parts = line.split()
            if len(parts) >= 4:
                ident = parts[0]
                coords = ' '.join(parts[2:4])
                formatted_coords = convert_coordinates(coords)
                if formatted_coords:
                    results.append(f"{ident}\t{formatted_coords} n - ")
        
        elif data_type == "FIXES":
            # FIXES format: 031X  S026.14.14.859 E028.24.04.971
            parts = line.split()
            if len(parts) >= 3:
                ident = parts[0]
                coords = ' '.join(parts[1:3])
                formatted_coords = convert_coordinates(coords)
                if formatted_coords:
                    results.append(f"{ident}\t{formatted_coords} f - ")
        
        elif data_type == "AIRPORT":
            # AIRPORT format: FAAB 000.000 S028.34.23.941 E016.32.03.609 D
            parts = line.split()
            if len(parts) >= 4:
                ident = parts[0]
                # Skip frequency (parts[1]) and use coordinates (parts[2:4])
                coords = ' '.join(parts[2:4])
                formatted_coords = convert_coordinates(coords)
                if formatted_coords:
                    results.append(f"{ident}\t{formatted_coords} a - ")
    
    return results

def parse_sct_file(filename):
    """Parse entire .sct file and extract all navigation data"""
    try:
        with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
            lines = file.readlines()
    except Exception as e:
        return None, f"Error reading file: {str(e)}"
    
    # Parse each section
    vors = parse_section("VOR", lines, "VOR")
    ndbs = parse_section("NDB", lines, "NDB")
    fixes = parse_section("FIXES", lines, "FIXES")
    airports = parse_section("AIRPORT", lines, "AIRPORT")
    
    # Combine all data
    all_data = []
    all_data.append("; London Control Adaptation - Parsed Navigation Data")
    all_data.append("; Generated from EuroScope .SCT file")
    all_data.append("")
    
    if vors:
        all_data.append("; VORs")
        all_data.extend(vors)
        all_data.append("")
    
    if ndbs:
        all_data.append("; NDBs")
        all_data.extend(ndbs)
        all_data.append("")
    
    if fixes:
        all_data.append("; Fixes")
        all_data.extend(fixes)
        all_data.append("")
    
    if airports:
        all_data.append("; Airports")
        all_data.extend(airports)
    
    stats = {
        'vors': len(vors),
        'ndbs': len(ndbs),
        'fixes': len(fixes),
        'airports': len(airports),
        'total': len(vors) + len(ndbs) + len(fixes) + len(airports)
    }
    
    return all_data, stats

def save_output(data, output_filename):
    """Save parsed data to output file"""
    try:
        with open(output_filename, 'w') as file:
            for line in data:
                file.write(line + '\n')
        return True
    except Exception as e:
        return False, str(e)

def select_and_parse_file():
    """GUI function to select .sct file and parse it"""
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    
    # Select input file
    input_file = filedialog.askopenfilename(
        title="Select EuroScope .SCT file",
        filetypes=[("SCT files", "*.sct"), ("All files", "*.*")]
    )
    
    if not input_file:
        print("No file selected. Exiting.")
        return
    
    # Parse the file
    print(f"Parsing {os.path.basename(input_file)}...")
    data, stats = parse_sct_file(input_file)
    
    if data is None:
        messagebox.showerror("Error", stats)
        return
    
    # Generate output filename
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}_parsed.txt"
    
    # Save output
    if save_output(data, output_file):
        # Show results
        result_message = (
            f"Successfully parsed {os.path.basename(input_file)}!\n\n"
            f"Statistics:\n"
            f"- VORs: {stats['vors']}\n"
            f"- NDBs: {stats['ndbs']}\n"
            f"- Fixes: {stats['fixes']}\n"
            f"- Airports: {stats['airports']}\n"
            f"- Total: {stats['total']} navigation points\n\n"
            f"Output saved to:\n{output_file}"
        )
        
        messagebox.showinfo("Parsing Complete", result_message)
        print(f"\nParsing complete! Output saved to: {output_file}")
        print(f"Processed: {stats['vors']} VORs, {stats['ndbs']} NDBs, {stats['fixes']} fixes, {stats['airports']} airports")
    else:
        messagebox.showerror("Error", "Failed to save output file")

def main():
    """Main function with command line and GUI options"""
    print("EuroScope .SCT File Parser for FASA London Control")
    print("=" * 60)
    
    if len(sys.argv) > 1:
        # Command line mode
        input_file = sys.argv[1]
        if os.path.exists(input_file):
            print(f"Parsing {input_file}...")
            data, stats = parse_sct_file(input_file)
            
            if data:
                output_file = f"{os.path.splitext(input_file)[0]}_parsed.txt"
                if save_output(data, output_file):
                    print(f"Success! Output saved to: {output_file}")
                    print(f"Statistics: {stats['vors']} VORs, {stats['ndbs']} NDBs, "
                          f"{stats['fixes']} fixes, {stats['airports']} airports "
                          f"({stats['total']} total)")
                else:
                    print("Error saving output file")
            else:
                print(f"Error: {stats}")
        else:
            print(f"File not found: {input_file}")
            print("Usage: python sct_parser.py [filename.sct]")
    else:
        # GUI mode
        print("No file specified. Opening file selector...")
        print("Please select your EuroScope .SCT file")
        select_and_parse_file()

if __name__ == "__main__":
    main()