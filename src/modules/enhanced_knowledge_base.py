"""
Enhanced Knowledge Base for Space AI Assistant.
Comprehensive astronomical database covering the entire universe.
"""

import json
import sqlite3
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import math

class EnhancedSpaceKnowledgeBase:
    """Comprehensive astronomical knowledge base covering the entire universe."""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("Enhanced_Knowledge_Base")
        
        # Database setup
        self.db_path = config.knowledge_dir / "enhanced_space_knowledge.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize enhanced database
        self._initialize_enhanced_database()
        self._populate_comprehensive_data()
        
        # Cache for frequently accessed data
        self.cache = {}
        
    def _initialize_enhanced_database(self):
        """Initialize comprehensive astronomical database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Enhanced celestial bodies table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS celestial_bodies (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        type TEXT NOT NULL,
                        parent_system TEXT,
                        mass_kg REAL,
                        radius_km REAL,
                        orbital_period_days REAL,
                        distance_from_parent_au REAL,
                        surface_gravity_ms2 REAL,
                        escape_velocity_ms REAL,
                        atmosphere TEXT,
                        temperature_k REAL,
                        moons INTEGER DEFAULT 0,
                        rings BOOLEAN DEFAULT 0,
                        magnetic_field BOOLEAN DEFAULT 0,
                        discovery_date TEXT,
                        discovered_by TEXT,
                        description TEXT,
                        composition TEXT,
                        albedo REAL,
                        axial_tilt_degrees REAL,
                        rotation_period_hours REAL
                    )
                ''')
                
                # Stars and stellar objects
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS stars (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        catalog_names TEXT,
                        constellation TEXT,
                        stellar_class TEXT,
                        mass_solar REAL,
                        radius_solar REAL,
                        luminosity_solar REAL,
                        temperature_k REAL,
                        distance_ly REAL,
                        magnitude_apparent REAL,
                        magnitude_absolute REAL,
                        metallicity REAL,
                        age_years REAL,
                        coordinates_ra TEXT,
                        coordinates_dec TEXT,
                        proper_motion_ra REAL,
                        proper_motion_dec REAL,
                        radial_velocity REAL,
                        binary_system BOOLEAN DEFAULT 0,
                        variable_star BOOLEAN DEFAULT 0,
                        exoplanets INTEGER DEFAULT 0,
                        description TEXT
                    )
                ''')
                
                # Exoplanets
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS exoplanets (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        host_star TEXT,
                        discovery_method TEXT,
                        discovery_year INTEGER,
                        mass_earth REAL,
                        radius_earth REAL,
                        orbital_period_days REAL,
                        semi_major_axis_au REAL,
                        eccentricity REAL,
                        temperature_k REAL,
                        habitable_zone BOOLEAN DEFAULT 0,
                        atmosphere_detected BOOLEAN DEFAULT 0,
                        water_detected BOOLEAN DEFAULT 0,
                        description TEXT
                    )
                ''')
                
                # Galaxies
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS galaxies (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        catalog_names TEXT,
                        galaxy_type TEXT,
                        constellation TEXT,
                        distance_mly REAL,
                        diameter_ly REAL,
                        mass_solar REAL,
                        stars_count REAL,
                        magnitude_apparent REAL,
                        redshift REAL,
                        coordinates_ra TEXT,
                        coordinates_dec TEXT,
                        central_black_hole BOOLEAN DEFAULT 0,
                        active_nucleus BOOLEAN DEFAULT 0,
                        description TEXT
                    )
                ''')
                
                # Deep space objects
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS deep_space_objects (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        catalog_names TEXT,
                        object_type TEXT,
                        constellation TEXT,
                        distance_ly REAL,
                        diameter_ly REAL,
                        magnitude_apparent REAL,
                        coordinates_ra TEXT,
                        coordinates_dec TEXT,
                        age_years REAL,
                        temperature_k REAL,
                        description TEXT,
                        formation_process TEXT
                    )
                ''')
                
                # Constellations
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS constellations (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        abbreviation TEXT,
                        genitive TEXT,
                        area_square_degrees REAL,
                        brightest_star TEXT,
                        mythology TEXT,
                        visible_latitudes TEXT,
                        best_viewing_month TEXT,
                        notable_objects TEXT,
                        description TEXT
                    )
                ''')
                
                conn.commit()
                self.logger.info("Enhanced database initialized successfully")
                
        except Exception as e:
            self.logger.error(f"Enhanced database initialization failed: {e}")
            raise
    
    def _populate_comprehensive_data(self):
        """Populate database with comprehensive astronomical data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if data already exists
                cursor.execute("SELECT COUNT(*) FROM celestial_bodies")
                if cursor.fetchone()[0] > 0:
                    return  # Data already populated
                
                # Populate all data
                self._populate_solar_system_data(cursor)
                self._populate_star_data(cursor)
                self._populate_exoplanet_data(cursor)
                self._populate_galaxy_data(cursor)
                self._populate_deep_space_data(cursor)
                self._populate_constellation_data(cursor)
                
                conn.commit()
                self.logger.info("Comprehensive astronomical data populated")
                
        except Exception as e:
            self.logger.error(f"Data population failed: {e}")
    
    def _populate_solar_system_data(self, cursor):
        """Populate comprehensive solar system data."""
        solar_system_data = [
            # name, type, parent_system, mass_kg, radius_km, orbital_period_days, distance_au, surface_gravity, escape_velocity, atmosphere, temp_k, moons, rings, magnetic_field, discovery, discoverer, description, composition, albedo, axial_tilt, rotation_period
            ('Sun', 'Star', 'Solar System', 1.989e30, 696340, 0, 0, 274, 617500, 'Hydrogen/Helium plasma', 5778, 0, 0, 1, 'Ancient', 'Ancient civilizations', 'G-type main-sequence star, center of our solar system', 'Hydrogen 73%, Helium 25%', 0.0, 7.25, 609.12),
            
            # Inner planets
            ('Mercury', 'Planet', 'Solar System', 3.301e23, 2439.7, 87.97, 0.387, 3.7, 4250, 'Trace', 440, 0, 0, 1, 'Ancient', 'Ancient civilizations', 'Closest planet to the Sun, heavily cratered', 'Iron core, silicate mantle', 0.142, 0.034, 1407.6),
            ('Venus', 'Planet', 'Solar System', 4.867e24, 6051.8, 224.7, 0.723, 8.87, 10360, 'CO2 (96.5%)', 737, 0, 0, 0, 'Ancient', 'Ancient civilizations', 'Hottest planet, extreme greenhouse effect', 'Silicate rocks, metallic core', 0.689, 177.4, -5832.5),
            ('Earth', 'Planet', 'Solar System', 5.972e24, 6371, 365.25, 1.0, 9.81, 11180, 'N2 (78%), O2 (21%)', 288, 1, 0, 1, 'Ancient', 'Ancient civilizations', 'Only known planet with life', 'Silicate rocks, iron core', 0.367, 23.44, 23.93),
            ('Mars', 'Planet', 'Solar System', 6.417e23, 3389.5, 686.98, 1.524, 3.71, 5030, 'CO2 (95.3%)', 210, 2, 0, 0, 'Ancient', 'Ancient civilizations', 'The Red Planet, polar ice caps', 'Iron oxide surface, basalt', 0.170, 25.19, 24.62),
            
            # Outer planets
            ('Jupiter', 'Planet', 'Solar System', 1.898e27, 69911, 4332.59, 5.204, 24.79, 59500, 'H2 (89%), He (10%)', 165, 95, 1, 1, 'Ancient', 'Ancient civilizations', 'Largest planet, Great Red Spot', 'Hydrogen and helium', 0.538, 3.13, 9.93),
            ('Saturn', 'Planet', 'Solar System', 5.683e26, 58232, 10759.22, 9.573, 10.44, 35500, 'H2 (96%), He (3%)', 134, 146, 1, 1, 'Ancient', 'Ancient civilizations', 'Prominent ring system', 'Hydrogen and helium', 0.499, 26.73, 10.66),
            ('Uranus', 'Planet', 'Solar System', 8.681e25, 25362, 30688.5, 19.165, 8.69, 21300, 'H2 (83%), He (15%)', 76, 27, 1, 1, '1781', 'William Herschel', 'Ice giant, tilted on its side', 'Water, methane, ammonia ices', 0.488, 97.77, -17.24),
            ('Neptune', 'Planet', 'Solar System', 1.024e26, 24622, 60182, 30.178, 11.15, 23500, 'H2 (80%), He (19%)', 72, 16, 1, 1, '1846', 'Urbain Le Verrier', 'Windiest planet, deep blue color', 'Water, methane, ammonia ices', 0.442, 28.32, 16.11),
            
            # Major moons
            ('Moon', 'Natural Satellite', 'Earth', 7.342e22, 1737.4, 27.32, 0.00257, 1.62, 2380, 'None', 220, 0, 0, 0, 'Ancient', 'Ancient civilizations', 'Earth\'s only natural satellite', 'Anorthosite highlands, basalt maria', 0.136, 6.68, 655.72),
            ('Io', 'Natural Satellite', 'Jupiter', 8.932e22, 1821.6, 1.77, 0.00282, 1.796, 2558, 'SO2', 110, 0, 0, 0, '1610', 'Galileo Galilei', 'Most volcanically active body', 'Sulfur compounds, silicate rock', 0.63, 0, 42.46),
            ('Europa', 'Natural Satellite', 'Jupiter', 4.8e22, 1560.8, 3.55, 0.00449, 1.314, 2025, 'Trace oxygen', 102, 0, 0, 0, '1610', 'Galileo Galilei', 'Subsurface ocean, potential for life', 'Water ice, rocky mantle', 0.67, 0.1, 85.23),
            ('Ganymede', 'Natural Satellite', 'Jupiter', 1.482e23, 2634.1, 7.15, 0.00716, 1.428, 2741, 'Trace oxygen', 110, 0, 0, 1, '1610', 'Galileo Galilei', 'Largest moon in solar system', 'Water ice, rock', 0.43, 0.2, 171.7),
            ('Callisto', 'Natural Satellite', 'Jupiter', 1.076e23, 2410.3, 16.69, 0.01259, 1.235, 2440, 'Trace CO2', 134, 0, 0, 0, '1610', 'Galileo Galilei', 'Heavily cratered, ancient surface', 'Water ice, rock', 0.22, 0, 400.5),
            ('Titan', 'Natural Satellite', 'Saturn', 1.345e23, 2574, 15.95, 0.00817, 1.352, 2639, 'N2 (98.4%)', 94, 0, 0, 0, '1655', 'Christiaan Huygens', 'Thick atmosphere, methane lakes', 'Water ice, hydrocarbons', 0.22, 0, 382.69),
            ('Enceladus', 'Natural Satellite', 'Saturn', 1.08e20, 252.1, 1.37, 0.00238, 0.0113, 239, 'Water vapor', 75, 0, 0, 0, '1789', 'William Herschel', 'Ice geysers from south pole', 'Water ice', 0.81, 0, 32.9),
            
            # Dwarf planets
            ('Pluto', 'Dwarf Planet', 'Solar System', 1.303e22, 1188.3, 90560, 39.482, 0.62, 1210, 'N2, CH4, CO', 44, 5, 0, 0, '1930', 'Clyde Tombaugh', 'Largest known dwarf planet', 'Rock and ice', 0.49, 122.53, -153.3),
            ('Ceres', 'Dwarf Planet', 'Solar System', 9.1e20, 473, 1682, 2.766, 0.27, 510, 'Water vapor', 168, 0, 0, 0, '1801', 'Giuseppe Piazzi', 'Largest asteroid, dwarf planet', 'Rock and ice', 0.09, 4, 9.07),
            ('Eris', 'Dwarf Planet', 'Solar System', 1.66e22, 1163, 203830, 67.67, 0.82, 1380, 'N2, CH4', 30, 1, 0, 0, '2005', 'Mike Brown', 'Most massive dwarf planet', 'Rock and ice', 0.96, 0, 25.9),
            ('Makemake', 'Dwarf Planet', 'Solar System', 3e21, 715, 112897, 45.79, 0.5, 850, 'CH4, N2', 30, 1, 0, 0, '2005', 'Mike Brown', 'Classical Kuiper Belt object', 'Rock and ice', 0.77, 0, 22.5),
            ('Haumea', 'Dwarf Planet', 'Solar System', 4.01e21, 816, 103410, 43.13, 0.44, 910, 'None detected', 32, 2, 1, 0, '2004', 'Mike Brown', 'Elongated shape, fast rotation', 'Rock and ice', 0.51, 0, 3.92),
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO celestial_bodies 
            (name, type, parent_system, mass_kg, radius_km, orbital_period_days, distance_from_parent_au,
             surface_gravity_ms2, escape_velocity_ms, atmosphere, temperature_k, moons, rings, magnetic_field,
             discovery_date, discovered_by, description, composition, albedo, axial_tilt_degrees, rotation_period_hours)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', solar_system_data)
