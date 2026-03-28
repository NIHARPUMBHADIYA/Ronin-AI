"""
Exoplanet Database for Space AI Assistant.
Comprehensive database of confirmed exoplanets and planetary systems.
"""

import sqlite3
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

class ExoplanetDatabase:
    """Comprehensive database of exoplanets and planetary systems."""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("Exoplanet_Database")
        
        # Database setup
        self.db_path = config.knowledge_dir / "exoplanet_database.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize exoplanet database
        self._initialize_exoplanet_database()
        self._populate_exoplanet_data()
        
    def _initialize_exoplanet_database(self):
        """Initialize exoplanet database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Exoplanets table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS exoplanets (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        host_star TEXT NOT NULL,
                        planet_type TEXT,
                        discovery_method TEXT,
                        discovery_year INTEGER,
                        discovered_by TEXT,
                        mass_earth_masses REAL,
                        radius_earth_radii REAL,
                        orbital_period_days REAL,
                        semi_major_axis_au REAL,
                        eccentricity REAL,
                        inclination_deg REAL,
                        equilibrium_temp_k REAL,
                        stellar_distance_ly REAL,
                        habitable_zone BOOLEAN DEFAULT 0,
                        confirmed BOOLEAN DEFAULT 1,
                        atmosphere_detected BOOLEAN DEFAULT 0,
                        water_detected BOOLEAN DEFAULT 0,
                        notable_features TEXT,
                        description TEXT
                    )
                ''')
                
                # Host stars table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS host_stars (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        stellar_type TEXT,
                        mass_solar_masses REAL,
                        radius_solar_radii REAL,
                        temperature_k REAL,
                        metallicity REAL,
                        age_gyr REAL,
                        distance_ly REAL,
                        constellation TEXT,
                        coordinates_ra TEXT,
                        coordinates_dec TEXT,
                        apparent_magnitude REAL,
                        planet_count INTEGER DEFAULT 0,
                        habitable_zone_inner_au REAL,
                        habitable_zone_outer_au REAL,
                        notable_features TEXT
                    )
                ''')
                
                # Planetary systems table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS planetary_systems (
                        id INTEGER PRIMARY KEY,
                        system_name TEXT UNIQUE NOT NULL,
                        host_star TEXT NOT NULL,
                        planet_count INTEGER,
                        confirmed_planets INTEGER,
                        candidate_planets INTEGER,
                        discovery_year INTEGER,
                        distance_ly REAL,
                        system_age_gyr REAL,
                        habitable_planets INTEGER DEFAULT 0,
                        notable_features TEXT,
                        description TEXT
                    )
                ''')
                
                conn.commit()
                self.logger.info("Exoplanet database initialized")
                
        except Exception as e:
            self.logger.error(f"Exoplanet database initialization failed: {e}")
            raise
    
    def _populate_exoplanet_data(self):
        """Populate exoplanet database with comprehensive data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if data exists
                cursor.execute("SELECT COUNT(*) FROM exoplanets")
                if cursor.fetchone()[0] > 0:
                    return
                
                self._populate_notable_exoplanets(cursor)
                self._populate_host_stars(cursor)
                self._populate_planetary_systems(cursor)
                
                conn.commit()
                self.logger.info("Exoplanet data populated")
                
        except Exception as e:
            self.logger.error(f"Exoplanet data population failed: {e}")
    
    def _populate_notable_exoplanets(self, cursor):
        """Populate notable exoplanets data."""
        exoplanets = [
            # name, host_star, planet_type, discovery_method, discovery_year, discovered_by, mass_earth, radius_earth, orbital_period, semi_major_axis, eccentricity, inclination, eq_temp, stellar_distance, habitable_zone, confirmed, atmosphere, water, notable_features, description
            ('Proxima Centauri b', 'Proxima Centauri', 'Terrestrial', 'Radial Velocity', 2016, 'Anglada-Escudé et al.', 1.17, 1.1, 11.186, 0.0485, 0.11, 89.7, 234, 4.24, 1, 1, 0, 0, 'Closest known exoplanet, potentially habitable', 'Closest exoplanet to Earth, located in the habitable zone of Proxima Centauri'),
            
            ('Kepler-452b', 'Kepler-452', 'Super-Earth', 'Transit', 2015, 'Kepler Space Telescope', 5.0, 1.6, 384.8, 1.04, 0.0, 89.8, 265, 1402, 1, 1, 0, 0, 'Earth\'s cousin, similar orbital period', 'Super-Earth in the habitable zone with Earth-like orbital characteristics'),
            
            ('TRAPPIST-1e', 'TRAPPIST-1', 'Terrestrial', 'Transit', 2017, 'Gillon et al.', 0.77, 0.91, 6.1, 0.029, 0.0, 89.7, 251, 40.7, 1, 1, 1, 0, 'Part of 7-planet system, potentially habitable', 'One of seven Earth-sized planets in the TRAPPIST-1 system'),
            
            ('HD 209458 b', 'HD 209458', 'Hot Jupiter', 'Transit', 1999, 'Charbonneau et al.', 220, 1.38, 3.52, 0.047, 0.0, 86.6, 1130, 159, 0, 1, 1, 1, 'First exoplanet with detected atmosphere and water vapor', 'Historic hot Jupiter, first exoplanet with atmospheric detection'),
            
            ('51 Eridani b', '51 Eridani', 'Super-Jupiter', 'Direct Imaging', 2014, 'Macintosh et al.', 760, 1.22, 11000, 13, 0.45, 0, 700, 28.1, 0, 1, 0, 0, 'Directly imaged young exoplanet', 'Young Jupiter-like planet directly imaged using coronagraphy'),
            
            ('Kepler-186f', 'Kepler-186', 'Terrestrial', 'Transit', 2014, 'Kepler Space Telescope', 1.44, 1.11, 129.9, 0.432, 0.0, 89.9, 188, 582, 1, 1, 0, 0, 'First Earth-size planet in habitable zone', 'First Earth-sized planet discovered in the habitable zone of another star'),
            
            ('TOI-715 b', 'TOI-715', 'Super-Earth', 'Transit', 2024, 'TESS', 3.02, 1.55, 19.3, 0.083, 0.0, 89.0, 280, 137, 1, 1, 0, 0, 'Recently discovered potentially habitable super-Earth', 'Super-Earth in the conservative habitable zone discovered by TESS'),
            
            ('K2-18 b', 'K2-18', 'Sub-Neptune', 'Transit', 2015, 'Kepler K2', 8.6, 2.3, 33.0, 0.143, 0.0, 89.6, 255, 124, 1, 1, 1, 1, 'Water vapor and possible clouds detected', 'Sub-Neptune with confirmed water vapor in its atmosphere'),
            
            ('WASP-121b', 'WASP-121', 'Hot Jupiter', 'Transit', 2015, 'Delrez et al.', 370, 1.87, 1.27, 0.025, 0.0, 87.6, 2359, 850, 0, 1, 1, 1, 'Extremely hot with metal clouds and rain', 'Ultra-hot Jupiter with exotic atmospheric chemistry'),
            
            ('LHS 1140 b', 'LHS 1140', 'Super-Earth', 'Transit', 2017, 'Dittmann et al.', 6.6, 1.4, 24.7, 0.095, 0.0, 89.7, 230, 41, 1, 1, 0, 0, 'Dense rocky planet in habitable zone', 'Dense super-Earth with potential for retaining atmosphere'),
            
            ('GJ 1214 b', 'GJ 1214', 'Sub-Neptune', 'Transit', 2009, 'Charbonneau et al.', 6.26, 2.68, 1.58, 0.014, 0.0, 89.1, 555, 48, 0, 1, 1, 0, 'Water world or thick atmosphere', 'Sub-Neptune with mysterious atmosphere composition'),
            
            ('55 Cancri e', '55 Cancri A', 'Super-Earth', 'Radial Velocity', 2004, 'McArthur et al.', 8.63, 2.0, 0.74, 0.016, 0.0, 83.4, 2573, 41, 0, 1, 1, 0, 'Lava world with extreme temperatures', 'Super-Earth with molten surface and possible lava rain'),
            
            ('Kepler-442b', 'Kepler-442', 'Super-Earth', 'Transit', 2015, 'Kepler Space Telescope', 2.3, 1.34, 112.3, 0.409, 0.0, 89.8, 233, 1206, 1, 1, 0, 0, 'Highly potentially habitable super-Earth', 'Super-Earth with high Earth Similarity Index'),
            
            ('TRAPPIST-1d', 'TRAPPIST-1', 'Terrestrial', 'Transit', 2017, 'Gillon et al.', 0.39, 0.77, 4.05, 0.022, 0.0, 89.7, 288, 40.7, 1, 1, 1, 0, 'Potentially habitable with possible water', 'Earth-sized planet in TRAPPIST-1 system with potential habitability'),
            
            ('TOI-849b', 'TOI-849', 'Chthonian Planet', 'Transit', 2020, 'Armstrong et al.', 120, 1.25, 0.77, 0.014, 0.0, 89.2, 1800, 730, 0, 1, 0, 0, 'Exposed planetary core', 'Rare exposed planetary core, remnant of gas giant'),
            
            ('KELT-9b', 'KELT-9', 'Ultra-Hot Jupiter', 'Transit', 2017, 'Gaudi et al.', 880, 1.89, 1.48, 0.034, 0.0, 86.8, 4050, 670, 0, 1, 1, 0, 'Hottest known exoplanet', 'Ultra-hot Jupiter hotter than most stars'),
            
            ('CoRoT-7b', 'CoRoT-7', 'Super-Earth', 'Transit', 2009, 'Léger et al.', 4.8, 1.68, 0.85, 0.017, 0.0, 80.1, 2573, 489, 0, 1, 0, 0, 'First rocky exoplanet discovered', 'Historic first confirmed rocky exoplanet'),
            
            ('Kepler-16b', 'Kepler-16', 'Gas Giant', 'Transit', 2011, 'Kepler Space Telescope', 333, 8.5, 228.8, 0.7, 0.007, 90.0, 200, 245, 0, 1, 0, 0, 'Circumbinary planet (Tatooine-like)', 'Gas giant orbiting two stars like Luke Skywalker\'s Tatooine')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO exoplanets 
            (name, host_star, planet_type, discovery_method, discovery_year, discovered_by, 
             mass_earth_masses, radius_earth_radii, orbital_period_days, semi_major_axis_au, 
             eccentricity, inclination_deg, equilibrium_temp_k, stellar_distance_ly, 
             habitable_zone, confirmed, atmosphere_detected, water_detected, notable_features, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', exoplanets)
    
    def _populate_host_stars(self, cursor):
        """Populate host stars data."""
        host_stars = [
            # name, stellar_type, mass_solar, radius_solar, temp_k, metallicity, age_gyr, distance_ly, constellation, ra, dec, app_mag, planet_count, hz_inner, hz_outer, notable_features
            ('Proxima Centauri', 'M5.5V', 0.123, 0.154, 3042, -0.07, 4.85, 4.24, 'Centaurus', '14h 29m 43s', '-62° 40\' 46"', 11.13, 1, 0.023, 0.054, 'Closest star to Sun, red dwarf with flares'),
            ('Kepler-452', 'G2V', 1.04, 1.11, 5757, 0.21, 6.0, 1402, 'Cygnus', '19h 44m 00s', '+44° 16\' 39"', 13.4, 1, 1.0, 1.8, 'Sun-like star, slightly older and larger'),
            ('TRAPPIST-1', 'M8V', 0.089, 0.121, 2559, 0.04, 7.6, 40.7, 'Aquarius', '23h 06m 29s', '-05° 02\' 29"', 18.8, 7, 0.011, 0.054, 'Ultra-cool dwarf with 7 Earth-sized planets'),
            ('HD 209458', 'G0V', 1.148, 1.203, 6091, 0.02, 4.0, 159, 'Pegasus', '22h 03m 11s', '+18° 53\' 04"', 7.65, 1, 1.2, 2.2, 'Sun-like star, first transiting exoplanet host'),
            ('51 Eridani', 'F0V', 1.75, 1.45, 7331, -0.15, 0.02, 28.1, 'Eridanus', '04h 37m 36s', '-02° 28\' 25"', 5.22, 1, 2.4, 4.8, 'Young F-type star with debris disk'),
            ('Kepler-186', 'M1V', 0.544, 0.507, 3755, -0.28, 4.0, 582, 'Cygnus', '19h 54m 36s', '+43° 57\' 18"', 14.6, 5, 0.22, 0.4, 'M-dwarf with Earth-sized planets'),
            ('TOI-715', 'M4V', 0.139, 0.374, 3450, 0.0, 6.6, 137, 'Volans', '06h 35m 15s', '-66° 17\' 09"', 16.4, 1, 0.05, 0.09, 'Nearby red dwarf with super-Earth'),
            ('K2-18', 'M2.5V', 0.359, 0.411, 3457, 0.12, 2.3, 124, 'Leo', '11h 30m 14s', '+07° 35\' 18"', 13.0, 2, 0.095, 0.18, 'Red dwarf with sub-Neptune in habitable zone'),
            ('WASP-121', 'F6V', 1.353, 1.458, 6460, 0.13, 1.7, 850, 'Puppis', '06h 31m 11s', '-39° 05\' 50"', 10.4, 1, 1.8, 3.2, 'Hot F-type star with ultra-hot Jupiter'),
            ('LHS 1140', 'M4.5V', 0.146, 0.186, 3131, -0.24, 5.0, 41, 'Cetus', '00h 44m 59s', '-15° 16\' 17"', 15.0, 2, 0.037, 0.07, 'Quiet red dwarf ideal for habitability studies')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO host_stars 
            (name, stellar_type, mass_solar_masses, radius_solar_radii, temperature_k, 
             metallicity, age_gyr, distance_ly, constellation, coordinates_ra, coordinates_dec, 
             apparent_magnitude, planet_count, habitable_zone_inner_au, habitable_zone_outer_au, notable_features)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', host_stars)
    
    def _populate_planetary_systems(self, cursor):
        """Populate planetary systems data."""
        systems = [
            # system_name, host_star, planet_count, confirmed, candidates, discovery_year, distance_ly, age_gyr, habitable_planets, notable_features, description
            ('Proxima Centauri System', 'Proxima Centauri', 1, 1, 0, 2016, 4.24, 4.85, 1, 'Closest planetary system to Earth', 'Nearest known planetary system with potentially habitable world'),
            ('TRAPPIST-1 System', 'TRAPPIST-1', 7, 7, 0, 2017, 40.7, 7.6, 3, 'Seven Earth-sized planets, multiple in habitable zone', 'Remarkable system with seven terrestrial planets'),
            ('Kepler-452 System', 'Kepler-452', 1, 1, 0, 2015, 1402, 6.0, 1, 'Earth\'s cousin system', 'Sun-like star with Earth-analog planet'),
            ('Alpha Centauri System', 'Alpha Centauri A/B', 1, 1, 0, 2012, 4.37, 4.85, 0, 'Triple star system with planets', 'Closest star system to Earth with confirmed planets'),
            ('TOI-715 System', 'TOI-715', 1, 1, 0, 2024, 137, 6.6, 1, 'Recently discovered habitable super-Earth', 'Newly confirmed system with potentially habitable world'),
            ('Kepler-186 System', 'Kepler-186', 5, 5, 0, 2014, 582, 4.0, 1, 'First Earth-size planet in habitable zone', 'M-dwarf system with multiple terrestrial planets'),
            ('55 Cancri System', '55 Cancri A', 5, 5, 0, 2004, 41, 7.4, 0, 'Multiple planet system with hot super-Earth', 'Well-studied multi-planet system around Sun-like star'),
            ('HD 40307 System', 'HD 40307', 6, 3, 3, 2008, 42, 4.2, 1, 'Super-Earth in habitable zone', 'Nearby system with potentially habitable super-Earth'),
            ('Gliese 667C System', 'Gliese 667C', 3, 2, 1, 2011, 23.6, 2.0, 2, 'Multiple potentially habitable planets', 'Triple star system with habitable zone planets'),
            ('Kepler-442 System', 'Kepler-442', 1, 1, 0, 2015, 1206, 2.9, 1, 'Highly Earth-like conditions', 'System with one of most Earth-like exoplanets known')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO planetary_systems 
            (system_name, host_star, planet_count, confirmed_planets, candidate_planets, 
             discovery_year, distance_ly, system_age_gyr, habitable_planets, notable_features, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', systems)
    
    def query_exoplanet(self, query: str) -> Dict[str, Any]:
        """Query exoplanet information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM exoplanets 
                    WHERE LOWER(name) LIKE LOWER(?) 
                    OR LOWER(host_star) LIKE LOWER(?)
                    OR LOWER(planet_type) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    exoplanets = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'exoplanet_info',
                        'exoplanets': exoplanets,
                        'count': len(exoplanets)
                    }
                
                return {'type': 'no_results', 'message': f'No exoplanets found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Exoplanet query failed: {e}")
            return {'type': 'error', 'message': 'Exoplanet query failed'}
    
    def query_host_star(self, query: str) -> Dict[str, Any]:
        """Query host star information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM host_stars 
                    WHERE LOWER(name) LIKE LOWER(?) 
                    OR LOWER(stellar_type) LIKE LOWER(?)
                    OR LOWER(constellation) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    stars = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'host_star_info',
                        'stars': stars,
                        'count': len(stars)
                    }
                
                return {'type': 'no_results', 'message': f'No host stars found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Host star query failed: {e}")
            return {'type': 'error', 'message': 'Host star query failed'}
    
    def query_planetary_system(self, query: str) -> Dict[str, Any]:
        """Query planetary system information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM planetary_systems 
                    WHERE LOWER(system_name) LIKE LOWER(?) 
                    OR LOWER(host_star) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    systems = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'planetary_system_info',
                        'systems': systems,
                        'count': len(systems)
                    }
                
                return {'type': 'no_results', 'message': f'No planetary systems found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Planetary system query failed: {e}")
            return {'type': 'error', 'message': 'Planetary system query failed'}
    
    def get_habitable_exoplanets(self) -> Dict[str, Any]:
        """Get potentially habitable exoplanets."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM exoplanets 
                    WHERE habitable_zone = 1
                    ORDER BY stellar_distance_ly
                ''')
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    exoplanets = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'habitable_exoplanets',
                        'exoplanets': exoplanets,
                        'count': len(exoplanets)
                    }
                
                return {'type': 'no_results', 'message': 'No habitable exoplanets in database'}
                
        except Exception as e:
            self.logger.error(f"Habitable exoplanets query failed: {e}")
            return {'type': 'error', 'message': 'Habitable exoplanets query failed'}
    
    def get_nearest_exoplanets(self, limit: int = 10) -> Dict[str, Any]:
        """Get nearest exoplanets to Earth."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM exoplanets 
                    WHERE stellar_distance_ly IS NOT NULL
                    ORDER BY stellar_distance_ly 
                    LIMIT ?
                ''', (limit,))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    exoplanets = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'nearest_exoplanets',
                        'exoplanets': exoplanets,
                        'count': len(exoplanets)
                    }
                
                return {'type': 'no_results', 'message': 'No exoplanet distance data available'}
                
        except Exception as e:
            self.logger.error(f"Nearest exoplanets query failed: {e}")
            return {'type': 'error', 'message': 'Nearest exoplanets query failed'}
    
    def get_exoplanets_by_type(self, planet_type: str) -> Dict[str, Any]:
        """Get exoplanets by type."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM exoplanets 
                    WHERE LOWER(planet_type) LIKE LOWER(?)
                    ORDER BY discovery_year DESC
                ''', (f'%{planet_type}%',))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    exoplanets = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'exoplanets_by_type',
                        'exoplanets': exoplanets,
                        'planet_type': planet_type,
                        'count': len(exoplanets)
                    }
                
                return {'type': 'no_results', 'message': f'No exoplanets found of type "{planet_type}"'}
                
        except Exception as e:
            self.logger.error(f"Exoplanets by type query failed: {e}")
            return {'type': 'error', 'message': 'Exoplanets by type query failed'}
    
    def format_exoplanet_info(self, exoplanet_data: Dict[str, Any]) -> str:
        """Format exoplanet information for display."""
        if exoplanet_data['type'] == 'exoplanet_info':
            output = []
            for planet in exoplanet_data['exoplanets']:
                info = [f"**{planet['name']}**"]
                info.append(f"Host Star: {planet['host_star']}")
                info.append(f"Type: {planet['planet_type']}")
                
                if planet['discovery_year']:
                    info.append(f"Discovered: {planet['discovery_year']} by {planet.get('discovered_by', 'Unknown')}")
                
                info.append(f"Discovery Method: {planet['discovery_method']}")
                
                if planet['mass_earth_masses']:
                    info.append(f"Mass: {planet['mass_earth_masses']:.2f} Earth masses")
                
                if planet['radius_earth_radii']:
                    info.append(f"Radius: {planet['radius_earth_radii']:.2f} Earth radii")
                
                if planet['orbital_period_days']:
                    info.append(f"Orbital Period: {planet['orbital_period_days']:.1f} days")
                
                if planet['stellar_distance_ly']:
                    info.append(f"Distance from Earth: {planet['stellar_distance_ly']:.1f} light-years")
                
                if planet['equilibrium_temp_k']:
                    info.append(f"Equilibrium Temperature: {planet['equilibrium_temp_k']:.0f} K ({planet['equilibrium_temp_k']-273:.0f}°C)")
                
                if planet['habitable_zone']:
                    info.append("✅ Located in Habitable Zone")
                
                if planet['atmosphere_detected']:
                    info.append("🌫️ Atmosphere Detected")
                
                if planet['water_detected']:
                    info.append("💧 Water Vapor Detected")
                
                if planet['notable_features']:
                    info.append(f"Notable Features: {planet['notable_features']}")
                
                if planet['description']:
                    info.append(f"Description: {planet['description']}")
                
                output.append('\n'.join(info))
            
            return '\n\n'.join(output)
        
        elif exoplanet_data['type'] == 'host_star_info':
            output = []
            for star in exoplanet_data['stars']:
                info = [f"**{star['name']} (Host Star)**"]
                info.append(f"Stellar Type: {star['stellar_type']}")
                info.append(f"Constellation: {star['constellation']}")
                
                if star['distance_ly']:
                    info.append(f"Distance: {star['distance_ly']:.1f} light-years")
                
                if star['mass_solar_masses']:
                    info.append(f"Mass: {star['mass_solar_masses']:.2f} solar masses")
                
                if star['temperature_k']:
                    info.append(f"Temperature: {star['temperature_k']:.0f} K")
                
                if star['age_gyr']:
                    info.append(f"Age: {star['age_gyr']:.1f} billion years")
                
                if star['planet_count']:
                    info.append(f"Known Planets: {star['planet_count']}")
                
                if star['notable_features']:
                    info.append(f"Notable Features: {star['notable_features']}")
                
                output.append('\n'.join(info))
            
            return '\n\n'.join(output)
        
        elif exoplanet_data['type'] == 'planetary_system_info':
            output = []
            for system in exoplanet_data['systems']:
                info = [f"**{system['system_name']}**"]
                info.append(f"Host Star: {system['host_star']}")
                
                if system['distance_ly']:
                    info.append(f"Distance: {system['distance_ly']:.1f} light-years")
                
                if system['confirmed_planets']:
                    info.append(f"Confirmed Planets: {system['confirmed_planets']}")
                
                if system['habitable_planets']:
                    info.append(f"Potentially Habitable Planets: {system['habitable_planets']}")
                
                if system['discovery_year']:
                    info.append(f"Discovery Year: {system['discovery_year']}")
                
                if system['notable_features']:
                    info.append(f"Notable Features: {system['notable_features']}")
                
                if system['description']:
                    info.append(f"Description: {system['description']}")
                
                output.append('\n'.join(info))
            
            return '\n\n'.join(output)
        
        elif exoplanet_data['type'] == 'no_results':
            return exoplanet_data['message']
        
        elif exoplanet_data['type'] == 'error':
            return f"Error: {exoplanet_data['message']}"
        
        else:
            return "Unknown exoplanet data format"
