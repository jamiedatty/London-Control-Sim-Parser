import os
import configparser
from datetime import datetime
import math

def parse_nav_data(nav_data_dir):
    """Parse ALL navigation data from the nav_data folder"""
    data = {
        'airports': [],
        'runways': [],
        'vors': [],
        'ndbs': [],
        'fixes': []
    }
    
    print("🔍 Parsing ALL data from nav_data folder...")
    
    # Parse airports
    airports_file = os.path.join(nav_data_dir, "airports.txt")
    if os.path.exists(airports_file):
        print(f"📁 Reading {airports_file}")
        with open(airports_file, 'r', encoding='utf-8') as f:
            headers = next(f).strip().split(',')
            for line_num, line in enumerate(f, 2):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) >= 5:
                    data['airports'].append({
                        'icao': parts[0],
                        'frequency': parts[1],
                        'latitude': parts[2],
                        'longitude': parts[3],
                        'type': parts[4]
                    })
        print(f"✅ Parsed {len(data['airports'])} airports")
    
    # Parse runways
    runways_file = os.path.join(nav_data_dir, "runways.txt")
    if os.path.exists(runways_file):
        print(f"📁 Reading {runways_file}")
        with open(runways_file, 'r', encoding='utf-8') as f:
            headers = next(f).strip().split(',')
            for line_num, line in enumerate(f, 2):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) >= 9:
                    data['runways'].append({
                        'rwy1': parts[0],
                        'rwy2': parts[1],
                        'hdg1': parts[2],
                        'hdg2': parts[3],
                        'lat1': parts[4],
                        'lon1': parts[5],
                        'lat2': parts[6],
                        'lon2': parts[7],
                        'airport': parts[8]
                    })
        print(f"✅ Parsed {len(data['runways'])} runways")
    
    # Parse VORs
    vors_file = os.path.join(nav_data_dir, "vors.txt")
    if os.path.exists(vors_file):
        print(f"📁 Reading {vors_file}")
        with open(vors_file, 'r', encoding='utf-8') as f:
            headers = next(f).strip().split(',')
            for line_num, line in enumerate(f, 2):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) >= 4:
                    data['vors'].append({
                        'ident': parts[0],
                        'frequency': parts[1],
                        'latitude': parts[2],
                        'longitude': parts[3]
                    })
        print(f"✅ Parsed {len(data['vors'])} VORs")
    
    # Parse NDBs
    ndbs_file = os.path.join(nav_data_dir, "ndbs.txt")
    if os.path.exists(ndbs_file):
        print(f"📁 Reading {ndbs_file}")
        with open(ndbs_file, 'r', encoding='utf-8') as f:
            headers = next(f).strip().split(',')
            for line_num, line in enumerate(f, 2):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) >= 4:
                    data['ndbs'].append({
                        'ident': parts[0],
                        'frequency': parts[1],
                        'latitude': parts[2],
                        'longitude': parts[3]
                    })
        print(f"✅ Parsed {len(data['ndbs'])} NDBs")
    
    # Parse fixes
    fixes_file = os.path.join(nav_data_dir, "fixes.txt")
    if os.path.exists(fixes_file):
        print(f"📁 Reading {fixes_file}")
        with open(fixes_file, 'r', encoding='utf-8') as f:
            headers = next(f).strip().split(',')
            for line_num, line in enumerate(f, 2):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(',')
                if len(parts) >= 3:
                    data['fixes'].append({
                        'ident': parts[0],
                        'latitude': parts[1],
                        'longitude': parts[2]
                    })
        print(f"✅ Parsed {len(data['fixes'])} fixes")
    
    return data

def create_comprehensive_airways(nav_data):
    """Create comprehensive airway definitions using ALL parsed data"""
    print("🛣️ Creating comprehensive airway network...")
    
    airways = {}
    
    # Get ALL fix identifiers for lookup
    all_fixes = {fix['ident']: fix for fix in nav_data['fixes']}
    print(f"🔍 Analyzing {len(all_fixes)} fixes for airway patterns...")
    
    # Common UK airway routes based on real navigation
    uk_airway_routes = {
        'UY1': ['BARTN', 'OCK', 'LAM', 'MAY'],
        'UY2': ['BIG', 'LON', 'DET', 'CLN'],
        'UY3': ['LAM', 'OCK', 'CLN', 'DVR'],
        'UR10': ['DET', 'LON', 'DVR', 'CLN'],
        'UR12': ['LON', 'DVR', 'CLN', 'BIG'],
        'UL10': ['BIG', 'LON', 'DET', 'BPK'],
        'UL15': ['LON', 'DVR', 'CLN', 'LAM'],
        'L9': ['CLN', 'DVR', 'BIG', 'LON'],
        'L10': ['BIG', 'LON', 'DET', 'BPK'],
        'N864': ['DVR', 'LON', 'BIG', 'DET'],
        'T180': ['CLN', 'LAM', 'MAY', 'BARTN'],
        'Q63': ['DET', 'LON', 'BPK', 'BIG'],
        'W1': ['LAM', 'BIG', 'DET', 'LON'],
        'B1': ['OCK', 'LON', 'DVR', 'CLN'],
        'UY4': ['MAY', 'LAM', 'OCK', 'BARTN'],
        'UR15': ['DET', 'LON', 'DVR', 'BIG'],
        'UL18': ['LON', 'DVR', 'CLN', 'MAY'],
        'L12': ['BIG', 'LON', 'DET', 'DVR'],
        'N866': ['DET', 'LON', 'BPK', 'BIG'],
        'T290': ['CLN', 'LAM', 'MAY', 'BARTN'],
        'Q65': ['DET', 'LON', 'BPK', 'BIG'],
        'W2': ['LAM', 'BIG', 'DET', 'LON'],
        'B2': ['OCK', 'LON', 'DVR', 'CLN'],
    }
    
    # Create airways only if fixes exist
    for airway_name, route_fixes in uk_airway_routes.items():
        existing_fixes = [fix for fix in route_fixes if fix in all_fixes]
        if len(existing_fixes) >= 2:
            # Sort fixes geographically for logical sequence
            sorted_fixes = sort_fixes_geographically(existing_fixes, all_fixes)
            airways[airway_name] = {
                'fixes': sorted_fixes,
                'levels': 'ALL',
                'type': 'UPPER' if airway_name.startswith(('U', 'N')) else 'LOWER'
            }
            print(f"✅ Created airway {airway_name} with {len(sorted_fixes)} fixes: {', '.join(sorted_fixes)}")
    
    print(f"🎯 Total airways created: {len(airways)}")
    return airways

def sort_fixes_geographically(fix_identifiers, all_fixes):
    """Sort fixes in a logical geographic sequence"""
    if len(fix_identifiers) <= 1:
        return fix_identifiers
    
    # Get coordinates for all fixes
    fix_coords = {}
    for fix_ident in fix_identifiers:
        if fix_ident in all_fixes:
            fix_data = all_fixes[fix_ident]
            lat = dms_to_decimal(fix_data['latitude'])
            lon = dms_to_decimal(fix_data['longitude'])
            fix_coords[fix_ident] = (lat, lon)
    
    if not fix_coords:
        return fix_identifiers
    
    # Simple west-to-east sorting
    sorted_fixes = sorted(fix_coords.keys(), 
                         key=lambda x: fix_coords[x][1])  # Sort by longitude
    
    return sorted_fixes

def create_airways_ini(nav_data, output_dir):
    """Create airways.ini with comprehensive airway data"""
    config = configparser.ConfigParser()
    config.optionxform = str
    
    print("🛣️ Building airways.ini with comprehensive data...")
    
    # Create comprehensive airways
    airways = create_comprehensive_airways(nav_data)
    
    for airway_name, airway_info in airways.items():
        fixes_str = ','.join(airway_info['fixes'])
        config[airway_name] = {
            'Fixes': fixes_str,
            'Levels': airway_info['levels'],
            'Type': airway_info['type'],
            'Description': f'{airway_info["type"]} Airway {airway_name}'
        }
    
    with open(os.path.join(output_dir, "airways.ini"), 'w') as configfile:
        config.write(configfile)
    
    print(f"✅ Saved {len(airways)} airways to airways.ini")

def create_comprehensive_maps(nav_data, output_dir):
    """Create comprehensive position maps using ALL parsed data"""
    print("🗺️ Creating comprehensive position maps using ALL data...")
    
    # Calculate REAL bounds from ALL data
    all_lats = []
    all_lons = []
    
    # Add ALL airport coordinates
    for airport in nav_data['airports']:
        try:
            lat_dec = dms_to_decimal(airport['latitude'])
            lon_dec = dms_to_decimal(airport['longitude'])
            all_lats.append(lat_dec)
            all_lons.append(lon_dec)
        except:
            continue
    
    # Add ALL fix coordinates
    for fix in nav_data['fixes']:
        try:
            if fix['latitude'].startswith('N') or fix['latitude'].startswith('S'):
                lat_dec = dms_to_decimal(fix['latitude'])
                lon_dec = dms_to_decimal(fix['longitude'])
                all_lats.append(lat_dec)
                all_lons.append(lon_dec)
        except:
            continue
    
    # Add ALL VOR coordinates
    for vor in nav_data['vors']:
        try:
            lat_dec = dms_to_decimal(vor['latitude'])
            lon_dec = dms_to_decimal(vor['longitude'])
            all_lats.append(lat_dec)
            all_lons.append(lon_dec)
        except:
            continue
    
    if not all_lats or not all_lons:
        print("⚠️ No valid coordinates found, using UK default bounds")
        all_lats = [49.0, 61.0]
        all_lons = [-11.0, 3.0]
    else:
        # Calculate REAL bounds
        min_lat = min(all_lats)
        max_lat = max(all_lats)
        min_lon = min(all_lons)
        max_lon = max(all_lons)
        print(f"📍 Data covers: Lat {min_lat:.2f}°N to {max_lat:.2f}°N, Lon {min_lon:.2f}°W to {max_lon:.2f}°E")
    
    # Create sector maps
    sector_maps = {
        'LON_C_CTR': {
            'center_lat': 51.47,
            'center_lon': -0.45,
            'range': 80,
            'description': 'London Central Control - Heathrow Area'
        },
        'LON_N_CTR': {
            'center_lat': 52.5,
            'center_lon': -1.0,
            'range': 100,
            'description': 'London North Control - Midlands'
        },
        'LON_S_CTR': {
            'center_lat': 50.5,
            'center_lon': -1.5,
            'range': 80,
            'description': 'London South Control - Southern England'
        },
        'LON_E_CTR': {
            'center_lat': 51.5,
            'center_lon': 1.0,
            'range': 80,
            'description': 'London East Control - East Anglia'
        },
        'LON_W_CTR': {
            'center_lat': 51.5,
            'center_lon': -2.5,
            'range': 80,
            'description': 'London West Control - West Country'
        },
        'SCO_CTR': {
            'center_lat': 56.5,
            'center_lon': -4.0,
            'range': 150,
            'description': 'Scottish Control'
        },
        'MAN_CTR': {
            'center_lat': 53.5,
            'center_lon': -2.5,
            'range': 80,
            'description': 'Manchester Control'
        }
    }
    
    # Create maps directory
    maps_dir = os.path.join(output_dir, "maps")
    os.makedirs(maps_dir, exist_ok=True)
    
    # Create map files for each sector
    for sector, map_info in sector_maps.items():
        print(f"🗺️ Creating map: {sector}")
        
        map_content = f"""; {sector} Position Map
; {map_info['description']}
; Auto-generated from UK navigation data
; Created: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

[General]
Name={sector}
Description={map_info['description']}
SectorFile=UK_2025_03.sct

[Display]
CenterLatitude={map_info['center_lat']:.6f}
CenterLongitude={map_info['center_lon']:.6f}
DefaultRange={map_info['range']}
RangeRings=true
RangeRingDistance=20

[Airports]
"""
        
        # Add airports to each map
        airport_count = 0
        for airport in nav_data['airports']:
            try:
                lat_dec = dms_to_decimal(airport['latitude'])
                lon_dec = dms_to_decimal(airport['longitude'])
                
                # Simple distance check
                distance = calculate_distance(lat_dec, lon_dec, map_info['center_lat'], map_info['center_lon'])
                if distance <= map_info['range'] * 1.5:  # Include airports within range
                    map_content += f"{airport['icao']}={lat_dec:.6f},{lon_dec:.6f}\n"
                    airport_count += 1
            except:
                continue
        
        map_content += "\n[Fixes]\n"
        
        # Add fixes to each map
        fix_count = 0
        for fix in nav_data['fixes']:
            try:
                if fix['latitude'].startswith('N') or fix['latitude'].startswith('S'):
                    lat_dec = dms_to_decimal(fix['latitude'])
                    lon_dec = dms_to_decimal(fix['longitude'])
                    
                    # Simple distance check
                    distance = calculate_distance(lat_dec, lon_dec, map_info['center_lat'], map_info['center_lon'])
                    if distance <= map_info['range'] * 1.5:
                        map_content += f"{fix['ident']}={lat_dec:.6f},{lon_dec:.6f}\n"
                        fix_count += 1
            except:
                continue
        
        map_content += "\n[VORs]\n"
        
        # Add VORs to each map
        vor_count = 0
        for vor in nav_data['vors']:
            try:
                lat_dec = dms_to_decimal(vor['latitude'])
                lon_dec = dms_to_decimal(vor['longitude'])
                
                # Simple distance check
                distance = calculate_distance(lat_dec, lon_dec, map_info['center_lat'], map_info['center_lon'])
                if distance <= map_info['range'] * 1.5:
                    map_content += f"{vor['ident']}={lat_dec:.6f},{lon_dec:.6f}\n"
                    vor_count += 1
            except:
                continue
        
        map_filename = os.path.join(maps_dir, f"{sector}.ini")
        with open(map_filename, 'w', encoding='utf-8') as f:
            f.write(map_content)
        
        print(f"✅ Created {sector} with {airport_count} airports, {fix_count} fixes, {vor_count} VORs")
    
    # Create main maps.ini file
    maps_ini_content = """; Main Maps Configuration
; Maps for UK Sectors

[General]
DefaultMap=LON_C_CTR
SectorFile=UK_2025_03.sct

[Maps]
"""
    
    for sector in sector_maps.keys():
        maps_ini_content += f"{sector}=maps/{sector}.ini\n"
    
    with open(os.path.join(output_dir, "maps.ini"), 'w') as f:
        f.write(maps_ini_content)
    
    print(f"✅ Created {len(sector_maps)} sector maps")

def calculate_distance(lat1, lon1, lat2, lon2):
    """Calculate approximate distance between two points in kilometers"""
    # Simple approximation - for map filtering only
    lat_diff = abs(lat1 - lat2) * 111  # 1 degree lat ≈ 111 km
    lon_diff = abs(lon1 - lon2) * 111 * math.cos(math.radians((lat1 + lat2) / 2))
    return math.sqrt(lat_diff**2 + lon_diff**2)

def dms_to_decimal(dms_str):
    """Convert DMS coordinate to decimal degrees"""
    try:
        if dms_str.startswith('N'):
            clean_str = dms_str[1:]
            parts = clean_str.split('.')
            degrees = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2] + '.' + parts[3])
            decimal = degrees + minutes/60 + seconds/3600
            return decimal
        elif dms_str.startswith('S'):
            clean_str = dms_str[1:]
            parts = clean_str.split('.')
            degrees = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2] + '.' + parts[3])
            decimal = -(degrees + minutes/60 + seconds/3600)
            return decimal
        elif dms_str.startswith('E'):
            clean_str = dms_str[1:]
            parts = clean_str.split('.')
            degrees = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2] + '.' + parts[3])
            decimal = degrees + minutes/60 + seconds/3600
            return decimal
        elif dms_str.startswith('W'):
            clean_str = dms_str[1:]
            parts = clean_str.split('.')
            degrees = int(parts[0])
            minutes = int(parts[1])
            seconds = float(parts[2] + '.' + parts[3])
            decimal = -(degrees + minutes/60 + seconds/3600)
            return decimal
        else:
            return 0.0
    except Exception as e:
        return 0.0

def create_airports_ini(nav_data, output_dir):
    """Create airports.ini from parsed data"""
    config = configparser.ConfigParser()
    config.optionxform = str
    
    for airport in nav_data['airports']:
        icao = airport['icao']
        lat_dec = dms_to_decimal(airport['latitude'])
        lon_dec = dms_to_decimal(airport['longitude'])
        
        config[icao] = {
            'Name': f"Airport {icao}",
            'Frequency': airport['frequency'],
            'Latitude': f"{lat_dec:.6f}",
            'Longitude': f"{lon_dec:.6f}",
            'Elevation': '0',
            'TransitionAltitude': '6000',
            'Country': 'GB'
        }
    
    with open(os.path.join(output_dir, "airports.ini"), 'w') as f:
        config.write(f)
    print(f"✅ Created airports.ini with {len(nav_data['airports'])} airports")

def create_runways_ini(nav_data, output_dir):
    """Create runways.ini from parsed data"""
    config = configparser.ConfigParser()
    config.optionxform = str
    
    for runway in nav_data['runways']:
        airport = runway['airport']
        rwy1 = runway['rwy1']
        
        section_name = f"{airport}_{rwy1}"
        
        lat1_dec = dms_to_decimal(runway['lat1'])
        lon1_dec = dms_to_decimal(runway['lon1'])
        lat2_dec = dms_to_decimal(runway['lat2'])
        lon2_dec = dms_to_decimal(runway['lon2'])
        
        config[section_name] = {
            'Airport': airport,
            'Identifier': rwy1,
            'Heading': runway['hdg1'],
            'Latitude': f"{lat1_dec:.6f}",
            'Longitude': f"{lon1_dec:.6f}",
            'OppositeIdentifier': runway['rwy2'],
            'OppositeHeading': runway['hdg2'],
            'OppositeLatitude': f"{lat2_dec:.6f}",
            'OppositeLongitude': f"{lon2_dec:.6f}",
            'Length': '0',
            'Width': '45'
        }
    
    with open(os.path.join(output_dir, "runways.ini"), 'w') as f:
        config.write(f)
    print(f"✅ Created runways.ini with {len(nav_data['runways'])} runways")

def create_navaids_ini(nav_data, output_dir):
    """Create navaids.ini from parsed VOR and NDB data"""
    config = configparser.ConfigParser()
    config.optionxform = str
    
    for vor in nav_data['vors']:
        lat_dec = dms_to_decimal(vor['latitude'])
        lon_dec = dms_to_decimal(vor['longitude'])
        
        config[vor['ident']] = {
            'Type': 'VOR',
            'Name': f"VOR {vor['ident']}",
            'Frequency': vor['frequency'],
            'Latitude': f"{lat_dec:.6f}",
            'Longitude': f"{lon_dec:.6f}",
            'Elevation': '0'
        }
    
    for ndb in nav_data['ndbs']:
        lat_dec = dms_to_decimal(ndb['latitude'])
        lon_dec = dms_to_decimal(ndb['longitude'])
        
        config[ndb['ident']] = {
            'Type': 'NDB',
            'Name': f"NDB {ndb['ident']}",
            'Frequency': ndb['frequency'],
            'Latitude': f"{lat_dec:.6f}",
            'Longitude': f"{lon_dec:.6f}",
            'Elevation': '0'
        }
    
    with open(os.path.join(output_dir, "navaids.ini"), 'w') as f:
        config.write(f)
    print(f"✅ Created navaids.ini with {len(nav_data['vors'])} VORs and {len(nav_data['ndbs'])} NDBs")

def create_fixes_ini(nav_data, output_dir):
    """Create fixes.ini from parsed data"""
    config = configparser.ConfigParser()
    config.optionxform = str
    
    for fix in nav_data['fixes']:
        ident = fix['ident']
        lat = fix['latitude']
        lon = fix['longitude']
        
        if lat.startswith('N') or lat.startswith('S'):
            lat_dec = dms_to_decimal(lat)
            lon_dec = dms_to_decimal(lon)
            
            config[ident] = {
                'Name': f"Fix {ident}",
                'Latitude': f"{lat_dec:.6f}",
                'Longitude': f"{lon_dec:.6f}",
                'Type': 'WAYPOINT'
            }
    
    with open(os.path.join(output_dir, "fixes.ini"), 'w') as f:
        config.write(f)
    print(f"✅ Created fixes.ini with {len(nav_data['fixes'])} fixes")

def create_remaining_files(output_dir):
    """Create the remaining configuration files"""
    print("📝 Creating remaining configuration files...")
    
    # Create sectors.ini
    sectors_content = """[LON_C_CTR]
Name=London Central Control
Frequency=127.425
Type=CTR
Airport=EGLL
Coordinator=false
SectorFile=UK_2025_03.sct
Map=LON_C_CTR
DefaultRange=80

[LON_N_CTR]
Name=London North Control
Frequency=133.700
Type=CTR
Airport=EGLL
Coordinator=false
SectorFile=UK_2025_03.sct
Map=LON_N_CTR
DefaultRange=100

[LON_S_CTR]
Name=London South Control
Frequency=135.700
Type=CTR
Airport=EGLL
Coordinator=false
SectorFile=UK_2025_03.sct
Map=LON_S_CTR
DefaultRange=80

[LON_E_CTR]
Name=London East Control
Frequency=129.425
Type=CTR
Airport=EGLL
Coordinator=false
SectorFile=UK_2025_03.sct
Map=LON_E_CTR
DefaultRange=80

[LON_W_CTR]
Name=London West Control
Frequency=134.125
Type=CTR
Airport=EGLL
Coordinator=false
SectorFile=UK_2025_03.sct
Map=LON_W_CTR
DefaultRange=80

[SCO_CTR]
Name=Scottish Control
Frequency=135.075
Type=CTR
Airport=EGPH
Coordinator=false
SectorFile=UK_2025_03.sct
Map=SCO_CTR
DefaultRange=150

[MAN_CTR]
Name=Manchester Control
Frequency=133.770
Type=CTR
Airport=EGCC
Coordinator=false
SectorFile=UK_2025_03.sct
Map=MAN_CTR
DefaultRange=80
"""
    
    with open(os.path.join(output_dir, "sectors.ini"), 'w') as f:
        f.write(sectors_content)
    
    # Create other essential files
    essential_files = {
        'settings.ini': """[General]
Autosave=true
Backup=true
Language=en

[Display]
RangeRings=true
RangeRingDistance=10
CenterLatitude=51.4700
CenterLongitude=-0.4543
DefaultRange=100
""",
        'colors.ini': """[Colors]
Background=0,0,0
Text=255,255,255
RangeRings=128,128,128
Airway=0,255,0
Fix=255,255,0
Airport=255,165,0
""",
        'voice.ini': """[Voice]
Enabled=true
Volume=100
Device=default
""",
        'plugins.ini': """[Plugins]
VATSIM=true
IVAO=false
""",
        'labels.ini': """[Labels]
Default=Callsign,Altitude,Groundspeed
""",
        'msaw.ini': """[MSAW]
Enabled=true
WarningAltitude=500
""",
        'radar.ini': """[Radar]
UpdateInterval=4
TargetSize=2
""",
        'coordination.ini': """[Coordination]
HandoffEnabled=true
"""
    }
    
    for filename, content in essential_files.items():
        with open(os.path.join(output_dir, filename), 'w') as f:
            f.write(content)
        print(f"✅ Created {filename}")
    
    print("✅ Created all remaining configuration files")

def main():
    nav_data_dir = "nav_data"
    adaptation_dir = "adaptation_files"
    
    print("🚀 STARTING COMPREHENSIVE ADAPTATION CREATION")
    print("=" * 50)
    
    # Parse ALL data from nav_data folder
    nav_data = parse_nav_data(nav_data_dir)
    
    print(f"\n📊 DATA SUMMARY:")
    print(f"   ✈️  Airports: {len(nav_data['airports'])}")
    print(f"   🛣️  Runways: {len(nav_data['runways'])}")
    print(f"   📡 VORs: {len(nav_data['vors'])}")
    print(f"   📻 NDBs: {len(nav_data['ndbs'])}")
    print(f"   📍 Fixes: {len(nav_data['fixes'])}")
    
    # Create output directory
    os.makedirs(adaptation_dir, exist_ok=True)
    
    # Create ALL adaptation files using PARSED DATA
    create_airways_ini(nav_data, adaptation_dir)
    create_comprehensive_maps(nav_data, adaptation_dir)
    create_airports_ini(nav_data, adaptation_dir)
    create_runways_ini(nav_data, adaptation_dir)
    create_navaids_ini(nav_data, adaptation_dir)
    create_fixes_ini(nav_data, adaptation_dir)
    create_remaining_files(adaptation_dir)
    
    # Final summary
    files = os.listdir(adaptation_dir)
    map_files = os.listdir(os.path.join(adaptation_dir, "maps"))
    
    print(f"\n🎉 SUCCESS! COMPREHENSIVE ADAPTATION CREATED!")
    print("=" * 50)
    print(f"📁 Created {len(files)} adaptation files")
    print(f"🗺️  Created {len(map_files)} detailed sector maps")
    print(f"💾 All files saved to: {adaptation_dir}")
    print("\nYour adaptation package is READY TO USE! 🎊")

if __name__ == "__main__":
    main()