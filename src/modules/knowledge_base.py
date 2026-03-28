"""
Space Knowledge Base for Space AI Assistant.
Contains comprehensive astronomical and space mission data.
"""

import json
import sqlite3
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path
import math

class SpaceKnowledgeBase:
    """Offline knowledge base for astronomical and space mission data."""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("Knowledge_Base")
        
        # Database setup
        self.db_path = config.knowledge_dir / "space_knowledge.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._initialize_database()
        self._populate_initial_data()
        
        # In-memory cache for frequently accessed data
        self.cache = {}
        
    def _initialize_database(self):
        """Initialize SQLite database with required tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Celestial bodies table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS celestial_bodies (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        type TEXT NOT NULL,
                        mass_kg REAL,
                        radius_km REAL,
                        orbital_period_days REAL,
                        distance_from_sun_au REAL,
                        surface_gravity_ms2 REAL,
                        escape_velocity_ms REAL,
                        atmosphere TEXT,
                        temperature_k REAL,
                        moons INTEGER DEFAULT 0,
                        description TEXT
                    )
                ''')
                
                # Spacecraft and missions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS spacecraft (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        type TEXT NOT NULL,
                        launch_date TEXT,
                        mission_status TEXT,
                        agency TEXT,
                        mass_kg REAL,
                        power_watts REAL,
                        orbit_altitude_km REAL,
                        description TEXT
                    )
                ''')
                
                # Physical constants table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS constants (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        symbol TEXT,
                        value REAL NOT NULL,
                        unit TEXT NOT NULL,
                        description TEXT
                    )
                ''')
                
                # Emergency procedures table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS emergency_procedures (
                        id INTEGER PRIMARY KEY,
                        emergency_type TEXT NOT NULL,
                        severity TEXT NOT NULL,
                        immediate_actions TEXT NOT NULL,
                        detailed_procedure TEXT NOT NULL,
                        equipment_needed TEXT,
                        time_critical BOOLEAN DEFAULT 0
                    )
                ''')
                
                # Stellar objects table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS stellar_objects (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        object_type TEXT NOT NULL,
                        constellation TEXT,
                        distance_ly REAL,
                        magnitude REAL,
                        spectral_class TEXT,
                        mass_solar REAL,
                        radius_solar REAL,
                        temperature_k REAL,
                        luminosity_solar REAL,
                        description TEXT
                    )
                ''')
                
                # Deep space objects table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS deep_space_objects (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        object_type TEXT NOT NULL,
                        constellation TEXT,
                        distance_ly REAL,
                        magnitude REAL,
                        size_arcmin REAL,
                        mass_solar REAL,
                        age_years REAL,
                        description TEXT
                    )
                ''')
                
                # Space physics formulas table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS physics_formulas (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        category TEXT NOT NULL,
                        formula TEXT NOT NULL,
                        variables TEXT NOT NULL,
                        units TEXT NOT NULL,
                        description TEXT,
                        applications TEXT
                    )
                ''')
                
                # Astronaut procedures table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS astronaut_procedures (
                        id INTEGER PRIMARY KEY,
                        procedure_name TEXT UNIQUE NOT NULL,
                        category TEXT NOT NULL,
                        duration_minutes INTEGER,
                        crew_size INTEGER,
                        equipment_required TEXT,
                        safety_considerations TEXT,
                        step_by_step TEXT NOT NULL,
                        contingencies TEXT
                    )
                ''')
                
                # Space weather table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS space_weather (
                        id INTEGER PRIMARY KEY,
                        phenomenon TEXT UNIQUE NOT NULL,
                        source TEXT NOT NULL,
                        frequency TEXT,
                        intensity_scale TEXT,
                        effects_on_spacecraft TEXT,
                        effects_on_humans TEXT,
                        mitigation_strategies TEXT,
                        warning_signs TEXT
                    )
                ''')
                
                # Space technology table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS space_technology (
                        id INTEGER PRIMARY KEY,
                        technology_name TEXT UNIQUE NOT NULL,
                        category TEXT NOT NULL,
                        specifications TEXT,
                        operating_conditions TEXT,
                        power_requirements TEXT,
                        maintenance_schedule TEXT,
                        failure_modes TEXT,
                        description TEXT
                    )
                ''')
                
                # Constellations table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS constellations (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        abbreviation TEXT,
                        area_sq_degrees REAL,
                        brightest_star TEXT,
                        mythology TEXT,
                        visibility TEXT,
                        notable_objects TEXT,
                        description TEXT
                    )
                ''')
                
                # Exoplanets table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS exoplanets (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        host_star TEXT NOT NULL,
                        discovery_year INTEGER,
                        discovery_method TEXT,
                        distance_ly REAL,
                        mass_earth REAL,
                        radius_earth REAL,
                        orbital_period_days REAL,
                        equilibrium_temp_k REAL,
                        habitable_zone BOOLEAN,
                        atmosphere TEXT,
                        description TEXT
                    )
                ''')
                
                # Space exploration history table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS space_history (
                        id INTEGER PRIMARY KEY,
                        event_name TEXT UNIQUE NOT NULL,
                        date TEXT NOT NULL,
                        agency TEXT,
                        mission_type TEXT,
                        significance TEXT,
                        participants TEXT,
                        outcome TEXT,
                        description TEXT
                    )
                ''')
                
                # Cosmology table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS cosmology (
                        id INTEGER PRIMARY KEY,
                        concept_name TEXT UNIQUE NOT NULL,
                        category TEXT NOT NULL,
                        value_measurement TEXT,
                        uncertainty TEXT,
                        discovery_date TEXT,
                        evidence TEXT,
                        implications TEXT,
                        description TEXT
                    )
                ''')
                
                # Astrobiology table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS astrobiology (
                        id INTEGER PRIMARY KEY,
                        topic_name TEXT UNIQUE NOT NULL,
                        category TEXT NOT NULL,
                        location TEXT,
                        evidence_level TEXT,
                        detection_method TEXT,
                        significance TEXT,
                        research_status TEXT,
                        description TEXT
                    )
                ''')
                
                # Space medicine table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS space_medicine (
                        id INTEGER PRIMARY KEY,
                        condition_name TEXT UNIQUE NOT NULL,
                        category TEXT NOT NULL,
                        symptoms TEXT,
                        causes TEXT,
                        duration TEXT,
                        countermeasures TEXT,
                        severity TEXT,
                        description TEXT
                    )
                ''')
                
                conn.commit()
                self.logger.info("Database initialized successfully")
                
        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            raise
    
    def _populate_initial_data(self):
        """Populate database with initial astronomical data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if data already exists
                cursor.execute("SELECT COUNT(*) FROM celestial_bodies")
                if cursor.fetchone()[0] > 0:
                    return  # Data already populated
                
                # Populate celestial bodies
                celestial_data = self._get_celestial_bodies_data()
                cursor.executemany('''
                    INSERT OR REPLACE INTO celestial_bodies 
                    (name, type, mass_kg, radius_km, orbital_period_days, distance_from_sun_au,
                     surface_gravity_ms2, escape_velocity_ms, atmosphere, temperature_k, moons, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', celestial_data)
                
                # Populate spacecraft data
                spacecraft_data = self._get_spacecraft_data()
                cursor.executemany('''
                    INSERT OR REPLACE INTO spacecraft
                    (name, type, launch_date, mission_status, agency, mass_kg, power_watts, orbit_altitude_km, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', spacecraft_data)
                
                # Populate physical constants
                constants_data = self._get_physical_constants()
                cursor.executemany('''
                    INSERT OR REPLACE INTO constants
                    (name, symbol, value, unit, description)
                    VALUES (?, ?, ?, ?, ?)
                ''', constants_data)
                
                # Populate emergency procedures
                emergency_data = self._get_emergency_procedures()
                cursor.executemany('''
                    INSERT OR REPLACE INTO emergency_procedures
                    (emergency_type, severity, immediate_actions, detailed_procedure, equipment_needed, time_critical)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', emergency_data)
                
                # Populate stellar objects
                stellar_data = self._get_stellar_objects_data()
                cursor.executemany('''
                    INSERT OR REPLACE INTO stellar_objects
                    (name, object_type, constellation, distance_ly, magnitude, spectral_class, mass_solar, radius_solar, temperature_k, luminosity_solar, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', stellar_data)
                
                # Populate deep space objects
                deep_space_data = self._get_deep_space_objects_data()
                cursor.executemany('''
                    INSERT OR REPLACE INTO deep_space_objects
                    (name, object_type, constellation, distance_ly, magnitude, size_arcmin, mass_solar, age_years, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', deep_space_data)
                
                # Populate physics formulas
                physics_data = self._get_physics_formulas_data()
                cursor.executemany('''
                    INSERT OR REPLACE INTO physics_formulas
                    (name, category, formula, variables, units, description, applications)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', physics_data)
                
                # Populate astronaut procedures
                procedures_data = self._get_astronaut_procedures_data()
                cursor.executemany('''
                    INSERT OR REPLACE INTO astronaut_procedures
                    (procedure_name, category, duration_minutes, crew_size, equipment_required, safety_considerations, step_by_step, contingencies)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', procedures_data)
                
                # Populate space weather
                weather_data = self._get_space_weather_data()
                cursor.executemany('''
                    INSERT OR REPLACE INTO space_weather
                    (phenomenon, source, frequency, intensity_scale, effects_on_spacecraft, effects_on_humans, mitigation_strategies, warning_signs)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', weather_data)
                
                # Populate space technology
                technology_data = self._get_space_technology_data()
                cursor.executemany('''
                    INSERT OR REPLACE INTO space_technology
                    (technology_name, category, specifications, operating_conditions, power_requirements, maintenance_schedule, failure_modes, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', technology_data)
                
                # Populate constellations
                constellation_data = self._get_constellations_data()
                cursor.executemany('''
                    INSERT OR REPLACE INTO constellations
                    (name, abbreviation, area_sq_degrees, brightest_star, mythology, visibility, notable_objects, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', constellation_data)
                
                # Populate exoplanets
                exoplanet_data = self._get_exoplanets_data()
                cursor.executemany('''
                    INSERT OR REPLACE INTO exoplanets
                    (name, host_star, discovery_year, discovery_method, distance_ly, mass_earth, radius_earth, orbital_period_days, equilibrium_temp_k, habitable_zone, atmosphere, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', exoplanet_data)
                
                # Populate space history
                history_data = self._get_space_history_data()
                cursor.executemany('''
                    INSERT OR REPLACE INTO space_history
                    (event_name, date, agency, mission_type, significance, participants, outcome, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', history_data)
                
                # Populate cosmology
                cosmology_data = self._get_cosmology_data()
                cursor.executemany('''
                    INSERT OR REPLACE INTO cosmology
                    (concept_name, category, value_measurement, uncertainty, discovery_date, evidence, implications, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', cosmology_data)
                
                # Populate astrobiology
                astrobiology_data = self._get_astrobiology_data()
                cursor.executemany('''
                    INSERT OR REPLACE INTO astrobiology
                    (topic_name, category, location, evidence_level, detection_method, significance, research_status, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', astrobiology_data)
                
                # Populate space medicine
                medicine_data = self._get_space_medicine_data()
                cursor.executemany('''
                    INSERT OR REPLACE INTO space_medicine
                    (condition_name, category, symptoms, causes, duration, countermeasures, severity, description)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', medicine_data)
                
                conn.commit()
                self.logger.info("Initial data populated successfully")
                
        except Exception as e:
            self.logger.error(f"Data population failed: {e}")
    
    def _get_celestial_bodies_data(self) -> List[Tuple]:
        """Get comprehensive celestial bodies data for database population."""
        return [
            # name, type, mass_kg, radius_km, orbital_period_days, distance_from_sun_au, surface_gravity_ms2, escape_velocity_ms, atmosphere, temperature_k, moons, description
            
            # STARS
            ('Sun', 'Star', 1.989e30, 696340, 0, 0, 274, 617500, 'Hydrogen/Helium plasma', 5778, 0, 'The central star of our solar system, a G-type main-sequence star'),
            ('Proxima Centauri', 'Star', 2.446e29, 107280, 0, 4.24, 0, 0, 'Stellar atmosphere', 3042, 3, 'Closest star to the Sun, red dwarf in Alpha Centauri system'),
            ('Alpha Centauri A', 'Star', 2.2e30, 854000, 0, 4.37, 0, 0, 'Stellar atmosphere', 5790, 0, 'Sun-like star in closest star system'),
            ('Alpha Centauri B', 'Star', 1.8e30, 602000, 0, 4.37, 0, 0, 'Stellar atmosphere', 5260, 0, 'Orange dwarf star in Alpha Centauri system'),
            ('Sirius A', 'Star', 4.02e30, 1190000, 0, 8.6, 0, 0, 'Stellar atmosphere', 9940, 0, 'Brightest star in night sky, binary system'),
            ('Betelgeuse', 'Star', 2.188e31, 617100000, 0, 548, 0, 0, 'Stellar atmosphere', 3500, 0, 'Red supergiant in Orion, semi-regular variable star'),
            ('Vega', 'Star', 4.25e30, 1728000, 0, 25.04, 0, 0, 'Stellar atmosphere', 9602, 0, 'Former pole star, standard for magnitude scale'),
            
            # PLANETS
            ('Mercury', 'Planet', 3.301e23, 2439.7, 87.97, 0.387, 3.7, 4250, 'Trace (O2, Na, H, He, K)', 440, 0, 'Closest planet to Sun, extreme temperature variations, heavily cratered'),
            ('Venus', 'Planet', 4.867e24, 6051.8, 224.7, 0.723, 8.87, 10360, 'CO2 (96.5%), N2 (3.5%)', 737, 0, 'Hottest planet, runaway greenhouse effect, retrograde rotation'),
            ('Earth', 'Planet', 5.972e24, 6371, 365.25, 1.0, 9.81, 11180, 'N2 (78%), O2 (21%), Ar (0.93%)', 288, 1, 'Only known planet with life, liquid water, protective magnetosphere'),
            ('Mars', 'Planet', 6.417e23, 3389.5, 686.98, 1.524, 3.71, 5030, 'CO2 (95.3%), N2 (2.7%), Ar (1.6%)', 210, 2, 'Red planet due to iron oxide, polar ice caps, largest volcano Olympus Mons'),
            ('Jupiter', 'Planet', 1.898e27, 69911, 4332.59, 5.204, 24.79, 59500, 'H2 (89%), He (10%), CH4, NH3', 165, 95, 'Largest planet, Great Red Spot storm, strong radiation belts'),
            ('Saturn', 'Planet', 5.683e26, 58232, 10759.22, 9.573, 10.44, 35500, 'H2 (96%), He (3%), CH4, NH3', 134, 146, 'Prominent ring system, lowest density planet, hexagonal polar storm'),
            ('Uranus', 'Planet', 8.681e25, 25362, 30688.5, 19.165, 8.69, 21300, 'H2 (83%), He (15%), CH4 (2%)', 76, 27, 'Ice giant tilted 98°, faint rings, extreme seasons lasting 21 years'),
            ('Neptune', 'Planet', 1.024e26, 24622, 60182, 30.178, 11.15, 23500, 'H2 (80%), He (19%), CH4 (1%)', 72, 16, 'Windiest planet (2100 km/h), Great Dark Spot, strongest magnetic field tilt'),
            
            # DWARF PLANETS
            ('Pluto', 'Dwarf Planet', 1.309e22, 1188.3, 90560, 39.48, 0.62, 1210, 'N2, CH4, CO', 44, 5, 'Largest known dwarf planet, binary system with Charon, New Horizons flyby 2015'),
            ('Eris', 'Dwarf Planet', 1.66e22, 1163, 203830, 67.7, 0.82, 1384, 'CH4 frost', 30, 1, 'Most massive dwarf planet, highly reflective surface, extreme elliptical orbit'),
            ('Ceres', 'Dwarf Planet', 9.39e20, 473, 1682, 2.77, 0.27, 510, 'Water vapor', 168, 0, 'Largest asteroid belt object, water ice detected, Dawn mission target'),
            ('Makemake', 'Dwarf Planet', 3.1e21, 715, 112897, 45.79, 0.5, 850, 'CH4, N2', 30, 1, 'Classical Kuiper Belt object, reddish surface, no atmosphere detected'),
            ('Haumea', 'Dwarf Planet', 4.01e21, 816, 103774, 43.13, 0.44, 910, 'None detected', 32, 2, 'Elongated shape due to rapid rotation, ring system, crystalline water ice'),
            
            # MAJOR MOONS - EARTH
            ('Moon', 'Natural Satellite', 7.342e22, 1737.4, 27.32, 1.0, 1.62, 2380, 'Trace (Ar, He, Na, K, Rn)', 220, 0, 'Earth\'s only natural satellite, tidally locked, Apollo landing sites'),
            
            # MAJOR MOONS - MARS
            ('Phobos', 'Natural Satellite', 1.072e16, 11.1, 0.32, 1.524, 0.0057, 11.3, 'None', 233, 0, 'Largest moon of Mars, irregular shape, grooved surface, orbital decay'),
            ('Deimos', 'Natural Satellite', 1.48e15, 6.2, 1.26, 1.524, 0.003, 5.6, 'None', 233, 0, 'Outer moon of Mars, smoother surface than Phobos, may be captured asteroid'),
            
            # MAJOR MOONS - JUPITER
            ('Io', 'Natural Satellite', 8.932e22, 1821.6, 1.77, 5.204, 1.796, 2558, 'SO2, trace others', 110, 0, 'Most volcanically active body, sulfur surface, tidal heating from Jupiter'),
            ('Europa', 'Natural Satellite', 4.8e22, 1560.8, 3.55, 5.204, 1.314, 2025, 'O2 (trace)', 102, 0, 'Subsurface ocean beneath ice crust, potential for life, smooth surface'),
            ('Ganymede', 'Natural Satellite', 1.482e23, 2634.1, 7.15, 5.204, 1.428, 2741, 'O2 (trace)', 110, 0, 'Largest moon in solar system, own magnetosphere, grooved terrain'),
            ('Callisto', 'Natural Satellite', 1.076e23, 2410.3, 16.69, 5.204, 1.235, 2440, 'CO2, O2 (trace)', 134, 0, 'Most heavily cratered body, subsurface ocean, low radiation environment'),
            ('Amalthea', 'Natural Satellite', 2.08e18, 83.5, 0.498, 5.204, 0.02, 58, 'None', 122, 0, 'Irregular shape, red coloration, within Jupiter\'s main ring'),
            
            # MAJOR MOONS - SATURN
            ('Titan', 'Natural Satellite', 1.345e23, 2574, 15.95, 9.573, 1.352, 2639, 'N2 (98.4%), CH4 (1.6%)', 94, 0, 'Dense atmosphere, methane lakes, organic chemistry, Cassini-Huygens mission'),
            ('Enceladus', 'Natural Satellite', 1.08e20, 252.1, 1.37, 9.573, 0.113, 239, 'Water vapor, N2, CO2', 75, 0, 'Ice geysers from south pole, subsurface ocean, tiger stripes'),
            ('Mimas', 'Natural Satellite', 3.75e19, 198.2, 0.94, 9.573, 0.064, 159, 'None', 64, 0, 'Herschel crater gives Death Star appearance, low density'),
            ('Iapetus', 'Natural Satellite', 1.81e21, 734.5, 79.33, 9.573, 0.223, 573, 'None', 110, 0, 'Two-tone coloration, equatorial ridge, walnut shape'),
            ('Rhea', 'Natural Satellite', 2.31e21, 763.8, 4.52, 9.573, 0.264, 635, 'O2, CO2 (trace)', 53, 0, 'Icy surface, possible ring system, wispy terrain'),
            ('Dione', 'Natural Satellite', 1.1e21, 561.4, 2.74, 9.573, 0.232, 510, 'O2 (trace)', 87, 0, 'Bright wispy streaks, co-orbital with Helene'),
            
            # MAJOR MOONS - URANUS
            ('Miranda', 'Natural Satellite', 6.59e19, 235.8, 1.41, 19.165, 0.079, 193, 'None', 60, 0, 'Extreme geological features, coronae and chasmata, patchwork appearance'),
            ('Ariel', 'Natural Satellite', 1.35e21, 578.9, 2.52, 19.165, 0.269, 558, 'None', 60, 0, 'Youngest surface among Uranus moons, extensive valley systems'),
            ('Umbriel', 'Natural Satellite', 1.17e21, 584.7, 4.14, 19.165, 0.234, 526, 'None', 75, 0, 'Darkest of major Uranian moons, ancient cratered surface'),
            ('Titania', 'Natural Satellite', 3.53e21, 788.4, 8.71, 19.165, 0.367, 773, 'None', 70, 0, 'Largest Uranian moon, rift valleys, possible subsurface ocean'),
            ('Oberon', 'Natural Satellite', 3.01e21, 761.4, 13.46, 19.165, 0.347, 734, 'None', 75, 0, 'Outermost major Uranian moon, heavily cratered, high albedo features'),
            
            # MAJOR MOONS - NEPTUNE
            ('Triton', 'Natural Satellite', 2.14e22, 1353.4, 5.88, 30.178, 0.779, 1455, 'N2, CH4 (trace)', 38, 0, 'Retrograde orbit, nitrogen geysers, captured Kuiper Belt object'),
            ('Nereid', 'Natural Satellite', 3.1e19, 170, 360.14, 30.178, 0.07, 150, 'None', 50, 0, 'Highly eccentric orbit, irregular shape, possible captured object'),
            
            # MAJOR ASTEROIDS
            ('Vesta', 'Asteroid', 2.59e20, 262.7, 1325.75, 2.36, 0.25, 360, 'None', 85, 0, 'Second most massive asteroid, differentiated interior, Dawn mission target'),
            ('Pallas', 'Asteroid', 2.04e20, 272.5, 1686.4, 2.77, 0.2, 320, 'None', 164, 0, 'Second largest asteroid, highly inclined orbit, silicate composition'),
            ('Hygiea', 'Asteroid', 8.32e19, 217, 2029.5, 3.14, 0.14, 245, 'None', 164, 0, 'Fourth largest asteroid, spherical shape, C-type composition'),
            
            # KUIPER BELT OBJECTS
            ('Sedna', 'Trans-Neptunian Object', 1e21, 497, 4015760, 76, 0.33, 544, 'CH4, N2 (seasonal)', 12, 0, 'Extremely distant orbit, reddish surface, detached object'),
            ('Quaoar', 'Trans-Neptunian Object', 1.4e21, 555, 104845, 43.4, 0.125, 276, 'None detected', 44, 1, 'Classical Kuiper Belt object, crystalline water ice, ring system'),
            ('Orcus', 'Trans-Neptunian Object', 6.32e20, 458.5, 90465, 39.17, 0.23, 450, 'None detected', 44, 1, 'Pluto analog, water ice surface, binary system with Vanth'),
            
            # COMETS (FAMOUS ONES)
            ('Halley', 'Comet', 2.2e14, 5.5, 27375, 17.8, 0.0003, 3, 'H2O, CO2, CO, dust', 47, 0, 'Most famous comet, 76-year orbit, last perihelion 1986, next 2061'),
            ('Hale-Bopp', 'Comet', 1.3e16, 30, 912500, 186, 0.005, 17, 'H2O, CO2, CO, dust', 225, 0, 'Great Comet of 1997, unusually large nucleus, visible for 18 months'),
            
            # EXOPLANETS (NOTABLE ONES)
            ('Kepler-452b', 'Exoplanet', 1.9e25, 8500, 384.8, 1.05, 19.6, 0, 'Unknown', 265, 0, 'Earth\'s cousin, habitable zone of Sun-like star, 1400 light-years away'),
            ('Proxima Centauri b', 'Exoplanet', 7.58e24, 7160, 11.19, 0.05, 11, 0, 'Unknown', 234, 0, 'Closest exoplanet, potentially habitable, tidally locked'),
            ('TRAPPIST-1e', 'Exoplanet', 4.31e24, 5740, 6.1, 0.029, 9.2, 0, 'Unknown', 251, 0, 'Potentially habitable, seven-planet system, 40 light-years away'),
        ]
    
    def _get_spacecraft_data(self) -> List[Tuple]:
        """Get comprehensive spacecraft and mission data for database population."""
        return [
            # name, type, launch_date, mission_status, agency, mass_kg, power_watts, orbit_altitude_km, description
            
            # SPACE STATIONS
            ('International Space Station', 'Space Station', '1998-11-20', 'Active', 'NASA/ESA/Roscosmos/JAXA/CSA', 420000, 84000, 408, 'Largest human-made object in space, continuous human presence since 2000'),
            ('Mir', 'Space Station', '1986-02-20', 'Deorbited', 'Soviet Union/Russia', 124340, 28000, 393, 'First modular space station, operated for 15 years'),
            ('Skylab', 'Space Station', '1973-05-14', 'Deorbited', 'NASA', 77000, 12400, 435, 'First American space station, three crewed missions'),
            ('Salyut 1', 'Space Station', '1971-04-19', 'Deorbited', 'Soviet Union', 18900, 4000, 200, 'First space station in history'),
            ('Tiangong Space Station', 'Space Station', '2021-04-29', 'Active', 'CNSA', 66000, 27000, 340, 'Chinese space station, three-module configuration'),
            
            # SPACE TELESCOPES
            ('Hubble Space Telescope', 'Observatory', '1990-04-24', 'Active', 'NASA/ESA', 11110, 2800, 547, 'Revolutionary visible light telescope, over 1.5 million observations'),
            ('James Webb Space Telescope', 'Observatory', '2021-12-25', 'Active', 'NASA/ESA/CSA', 6161, 2000, 1500000, 'Largest space telescope, infrared observations, L2 Lagrange point'),
            ('Spitzer Space Telescope', 'Observatory', '2003-08-25', 'Retired', 'NASA', 950, 750, 0, 'Infrared space telescope, studied cool objects in space'),
            ('Kepler Space Telescope', 'Observatory', '2009-03-07', 'Retired', 'NASA', 1052, 1100, 0, 'Exoplanet hunter, discovered thousands of planets'),
            ('Chandra X-ray Observatory', 'Observatory', '1999-07-23', 'Active', 'NASA', 4790, 2350, 139000, 'X-ray telescope studying high-energy phenomena'),
            ('TESS', 'Observatory', '2018-04-18', 'Active', 'NASA', 362, 290, 0, 'Transiting Exoplanet Survey Satellite, all-sky planet search'),
            ('Euclid', 'Observatory', '2023-07-01', 'Active', 'ESA', 2160, 2000, 1500000, 'Dark matter and dark energy survey telescope'),
            
            # DEEP SPACE PROBES
            ('Voyager 1', 'Deep Space Probe', '1977-09-05', 'Active', 'NASA', 825, 420, 0, 'Farthest human-made object, entered interstellar space 2012'),
            ('Voyager 2', 'Deep Space Probe', '1977-08-20', 'Active', 'NASA', 825, 420, 0, 'Only spacecraft to visit all four outer planets, Grand Tour mission'),
            ('Pioneer 10', 'Deep Space Probe', '1972-03-03', 'Contact Lost', 'NASA', 270, 155, 0, 'First spacecraft to Jupiter, first to leave solar system'),
            ('Pioneer 11', 'Deep Space Probe', '1973-04-06', 'Contact Lost', 'NASA', 270, 155, 0, 'First spacecraft to Saturn, studied rings and moons'),
            ('New Horizons', 'Deep Space Probe', '2006-01-19', 'Active', 'NASA', 478, 228, 0, 'Pluto flyby mission, now exploring Kuiper Belt'),
            ('Parker Solar Probe', 'Deep Space Probe', '2018-08-12', 'Active', 'NASA', 685, 384, 0, 'Closest approach to Sun, studying solar corona and wind'),
            
            # PLANETARY MISSIONS
            ('Cassini', 'Planetary Probe', '1997-10-15', 'Completed', 'NASA/ESA/ASI', 5712, 885, 0, 'Comprehensive Saturn system study, Huygens Titan lander'),
            ('Galileo', 'Planetary Probe', '1989-10-18', 'Completed', 'NASA', 2223, 570, 0, 'Jupiter orbiter, atmospheric probe, discovered subsurface oceans'),
            ('Juno', 'Planetary Probe', '2011-08-05', 'Active', 'NASA', 3625, 486, 0, 'Jupiter polar orbiter, studying interior and magnetosphere'),
            ('MESSENGER', 'Planetary Probe', '2004-08-03', 'Completed', 'NASA', 1107, 640, 0, 'First Mercury orbiter, mapped entire surface'),
            ('BepiColombo', 'Planetary Probe', '2018-10-20', 'En Route', 'ESA/JAXA', 4081, 1000, 0, 'Dual Mercury orbiters, arrival 2025'),
            ('Akatsuki', 'Planetary Probe', '2010-05-21', 'Active', 'JAXA', 517, 700, 0, 'Venus climate orbiter, studying atmospheric dynamics'),
            
            # MARS MISSIONS
            ('Mars Perseverance Rover', 'Rover', '2020-07-30', 'Active', 'NASA', 1025, 125, 0, 'Astrobiology mission, sample collection for future return'),
            ('Mars Curiosity Rover', 'Rover', '2011-11-26', 'Active', 'NASA', 899, 45, 0, 'Nuclear-powered rover, studying Martian geology and climate'),
            ('Mars Opportunity Rover', 'Rover', '2003-07-07', 'Completed', 'NASA', 185, 20, 0, 'Operated 15 years, found evidence of past water activity'),
            ('Mars Spirit Rover', 'Rover', '2003-06-10', 'Completed', 'NASA', 185, 20, 0, 'Twin of Opportunity, studied Gusev Crater geology'),
            ('Mars Ingenuity Helicopter', 'Aircraft', '2020-07-30', 'Active', 'NASA', 1.8, 6, 0, 'First powered flight on another planet, technology demonstrator'),
            ('Mars Reconnaissance Orbiter', 'Orbiter', '2005-08-12', 'Active', 'NASA', 2180, 2000, 0, 'High-resolution Mars imaging and communication relay'),
            ('MAVEN', 'Orbiter', '2013-11-18', 'Active', 'NASA', 2454, 1135, 0, 'Mars atmospheric evolution study, upper atmosphere analysis'),
            
            # CREW VEHICLES
            ('Dragon Crew', 'Crew Vehicle', '2020-05-30', 'Active', 'SpaceX/NASA', 12519, 4000, 408, 'Commercial crew transportation, autonomous docking capability'),
            ('Soyuz', 'Crew Vehicle', '1967-04-23', 'Active', 'Roscosmos', 7220, 1000, 408, 'Most reliable crew vehicle, over 140 crewed flights'),
            ('Space Shuttle', 'Crew Vehicle', '1981-04-12', 'Retired', 'NASA', 78000, 21000, 408, 'Reusable spaceplane, 135 missions over 30 years'),
            ('Apollo Command Module', 'Crew Vehicle', '1968-10-11', 'Retired', 'NASA', 5560, 1420, 0, 'Moon landing program, 11 crewed flights'),
            ('Artemis Orion', 'Crew Vehicle', '2022-11-16', 'Development', 'NASA', 26520, 11000, 0, 'Next-generation deep space crew vehicle for Moon and Mars'),
            ('Starliner', 'Crew Vehicle', '2019-12-20', 'Development', 'Boeing/NASA', 13000, 2900, 408, 'Commercial crew vehicle, autonomous and manual flight modes'),
            ('Shenzhou', 'Crew Vehicle', '1999-11-20', 'Active', 'CNSA', 7840, 1500, 343, 'Chinese crew vehicle, based on Soyuz design'),
            
            # CARGO VEHICLES
            ('Dragon Cargo', 'Cargo Vehicle', '2010-12-08', 'Active', 'SpaceX/NASA', 6000, 4000, 408, 'First commercial cargo vehicle, reusable capsule'),
            ('Cygnus', 'Cargo Vehicle', '2013-09-18', 'Active', 'Northrop Grumman/NASA', 7500, 3500, 408, 'Expendable cargo vehicle, enhanced capacity versions'),
            ('Progress', 'Cargo Vehicle', '1978-01-20', 'Active', 'Roscosmos', 7020, 1000, 408, 'Reliable cargo delivery, propellant transfer capability'),
            ('HTV', 'Cargo Vehicle', '2009-09-11', 'Retired', 'JAXA', 10500, 4500, 408, 'Japanese cargo vehicle, large pressurized volume'),
            ('ATV', 'Cargo Vehicle', '2008-03-09', 'Retired', 'ESA', 20750, 4800, 408, 'European cargo vehicle, ISS reboost capability'),
            
            # FUTURE MISSIONS
            ('Artemis III', 'Lunar Mission', '2026-01-01', 'Planned', 'NASA', 0, 0, 0, 'First crewed Moon landing since Apollo, South Pole target'),
            ('Europa Clipper', 'Planetary Probe', '2024-10-01', 'Planned', 'NASA', 6065, 620, 0, 'Jupiter moon Europa study, multiple flybys'),
            ('Dragonfly', 'Planetary Probe', '2027-01-01', 'Planned', 'NASA', 450, 110, 0, 'Titan rotorcraft lander, astrobiology investigation'),
            ('Mars Sample Return', 'Sample Return', '2028-01-01', 'Planned', 'NASA/ESA', 0, 0, 0, 'Return Perseverance samples to Earth for analysis'),
            ('Breakthrough Starshot', 'Interstellar Probe', '2030-01-01', 'Concept', 'Breakthrough Initiatives', 0.000001, 0, 0, 'Light sail nanocraft to Proxima Centauri'),
        ]
    
    def _get_physical_constants(self) -> List[Tuple]:
        """Get physical constants data."""
        return [
            # name, symbol, value, unit, description
            ('Speed of Light', 'c', 299792458, 'm/s', 'Speed of light in vacuum'),
            ('Gravitational Constant', 'G', 6.67430e-11, 'm³/kg⋅s²', 'Universal gravitational constant'),
            ('Planck Constant', 'h', 6.62607015e-34, 'J⋅s', 'Quantum of electromagnetic action'),
            ('Boltzmann Constant', 'k', 1.380649e-23, 'J/K', 'Relates energy and temperature'),
            ('Avogadro Number', 'NA', 6.02214076e23, '1/mol', 'Number of particles per mole'),
            ('Stefan-Boltzmann Constant', 'σ', 5.670374419e-8, 'W/m²⋅K⁴', 'Blackbody radiation constant'),
            ('Astronomical Unit', 'AU', 149597870.7, 'km', 'Average Earth-Sun distance'),
            ('Light Year', 'ly', 9.4607304725808e12, 'km', 'Distance light travels in one year'),
            ('Parsec', 'pc', 3.0857e13, 'km', 'Parallax arcsecond distance unit'),
            ('Solar Mass', 'M☉', 1.98847e30, 'kg', 'Mass of the Sun'),
            ('Earth Mass', 'M⊕', 5.9722e24, 'kg', 'Mass of Earth'),
            ('Standard Gravity', 'g', 9.80665, 'm/s²', 'Standard gravitational acceleration'),
        ]
    
    def _get_emergency_procedures(self) -> List[Tuple]:
        """Get emergency procedures data."""
        return [
            # emergency_type, severity, immediate_actions, detailed_procedure, equipment_needed, time_critical
            ('Fire', 'Critical', 'Alert crew, isolate power, use fire extinguisher', 
             '1. Sound alarm\n2. Don breathing apparatus\n3. Isolate electrical power\n4. Use CO2 extinguisher\n5. Ventilate area\n6. Monitor for re-ignition',
             'Fire extinguisher, breathing apparatus, emergency lighting', True),
            
            ('Depressurization', 'Critical', 'Don emergency oxygen, seal breach, move to safe area',
             '1. Emergency oxygen masks\n2. Locate breach\n3. Apply emergency patch\n4. Isolate affected compartment\n5. Monitor pressure\n6. Prepare for EVA repair if needed',
             'Emergency oxygen, patch kit, pressure suits', True),
            
            ('Medical Emergency', 'High', 'Assess patient, provide first aid, contact ground',
             '1. Ensure scene safety\n2. Check vital signs\n3. Apply appropriate first aid\n4. Administer medication if trained\n5. Contact mission control\n6. Prepare for emergency return if needed',
             'Medical kit, defibrillator, medications, communication equipment', True),
            
            ('Power Failure', 'High', 'Switch to backup power, check systems, conserve energy',
             '1. Activate backup power\n2. Check critical systems status\n3. Reduce non-essential power usage\n4. Diagnose main power failure\n5. Implement repair procedures\n6. Monitor battery levels',
             'Backup batteries, diagnostic tools, repair equipment', False),
            
            ('Communication Loss', 'Medium', 'Check equipment, try backup systems, reposition antennas',
             '1. Verify equipment status\n2. Check all connections\n3. Switch to backup communication\n4. Adjust antenna orientation\n5. Try different frequencies\n6. Implement communication schedule',
             'Backup radio, diagnostic equipment, antenna controls', False),
            
            ('Radiation Exposure', 'High', 'Move to shielded area, monitor exposure, limit EVA',
             '1. Move to most shielded compartment\n2. Monitor radiation levels\n3. Check personal dosimeters\n4. Cancel non-essential EVAs\n5. Contact medical for guidance\n6. Document exposure levels',
             'Radiation detectors, dosimeters, shielding materials', True),
        ]
    
    def _get_stellar_objects_data(self) -> List[Tuple]:
        """Get stellar objects data for database population."""
        return [
            # name, object_type, constellation, distance_ly, magnitude, spectral_class, mass_solar, radius_solar, temperature_k, luminosity_solar, description
            ('Sirius', 'Binary Star', 'Canis Major', 8.6, -1.46, 'A1V', 2.063, 1.711, 9940, 25.4, 'Brightest star in night sky, white main sequence with white dwarf companion'),
            ('Canopus', 'Supergiant', 'Carina', 310, -0.74, 'A9II', 8.0, 71, 5310, 10700, 'Second brightest star, navigation star for spacecraft'),
            ('Arcturus', 'Giant Star', 'Boötes', 36.7, -0.05, 'K1.5III', 1.08, 25.4, 4290, 170, 'Red giant, fourth brightest star, high proper motion'),
            ('Vega', 'Main Sequence', 'Lyra', 25.04, 0.03, 'A0V', 2.135, 2.362, 9602, 40.12, 'Former pole star, photometric standard, debris disk'),
            ('Capella', 'Multiple Star', 'Auriga', 42.9, 0.08, 'G5III+G0III', 2.69, 11.98, 4970, 78.7, 'Spectroscopic binary giants, sixth brightest star'),
            ('Rigel', 'Supergiant', 'Orion', 860, 0.13, 'B8Ia', 21, 78.9, 12100, 120000, 'Blue supergiant, most luminous star in Orion'),
            ('Procyon', 'Binary Star', 'Canis Minor', 11.46, 0.34, 'F5IV-V', 1.499, 2.048, 6530, 6.93, 'Subgiant with white dwarf companion, eighth brightest star'),
            ('Betelgeuse', 'Supergiant', 'Orion', 548, 0.50, 'M1-2Ia-ab', 16.5, 764, 3590, 90000, 'Red supergiant, semi-regular variable, potential supernova candidate'),
            ('Achernar', 'Be Star', 'Eridanus', 139, 0.46, 'B6Vep', 6.7, 11.4, 20000, 3150, 'Fastest rotating star, oblate shape due to rotation'),
            ('Hadar', 'Multiple Star', 'Centaurus', 390, 0.61, 'B1III', 10.5, 8.6, 22000, 41700, 'Beta Centauri, triple star system, navigation star'),
            ('Altair', 'Main Sequence', 'Aquila', 16.73, 0.77, 'A7V', 1.79, 1.63, 7550, 10.6, 'Fast rotator, oblate shape, twelfth brightest star'),
            ('Aldebaran', 'Giant Star', 'Taurus', 65.3, 0.85, 'K5III', 1.16, 44.13, 3910, 518, 'Red giant, appears in Hyades cluster but not member'),
            ('Antares', 'Supergiant', 'Scorpius', 550, 1.09, 'M1.5Iab-Ib', 12, 700, 3570, 57500, 'Red supergiant, rival of Mars, semi-regular variable'),
            ('Spica', 'Binary Star', 'Virgo', 250, 0.97, 'B1III-IV', 11.43, 7.47, 22400, 20512, 'Rotating ellipsoidal variable, close binary system'),
            ('Pollux', 'Giant Star', 'Gemini', 33.78, 1.14, 'K0III', 1.91, 8.8, 4666, 43, 'Orange giant, has confirmed exoplanet, brightest in Gemini'),
            ('Fomalhaut', 'Main Sequence', 'Piscis Austrinus', 25.13, 1.16, 'A3V', 1.92, 1.842, 8590, 16.6, 'Young star with debris disk and controversial exoplanet'),
            ('Deneb', 'Supergiant', 'Cygnus', 2615, 1.25, 'A2Ia', 19, 203, 8525, 200000, 'Most distant first-magnitude star, part of Summer Triangle'),
            ('Regulus', 'Multiple Star', 'Leo', 79.3, 1.35, 'B8IVn', 3.8, 3.092, 12460, 288, 'Fast rotator, quadruple star system, heart of Leo'),
            ('Adhara', 'Giant Star', 'Canis Major', 430, 1.50, 'B2II', 12.6, 14, 22200, 38700, 'Blue giant, second brightest in Canis Major'),
            ('Shaula', 'Multiple Star', 'Scorpius', 570, 1.63, 'B1.5IV', 14.5, 8.8, 25000, 35000, 'Lambda Scorpii, multiple star system, stinger of scorpion'),
        ]
    
    def _get_deep_space_objects_data(self) -> List[Tuple]:
        """Get deep space objects data for database population."""
        return [
            # name, object_type, constellation, distance_ly, magnitude, size_arcmin, mass_solar, age_years, description
            ('Andromeda Galaxy', 'Spiral Galaxy', 'Andromeda', 2537000, 3.44, 178, 1.5e12, 10.01e9, 'Nearest major galaxy, will collide with Milky Way in 4.5 billion years'),
            ('Orion Nebula', 'Emission Nebula', 'Orion', 1344, 4.0, 85, 2000, 1e6, 'Stellar nursery, trapezium cluster, visible to naked eye'),
            ('Eagle Nebula', 'Emission Nebula', 'Serpens', 7000, 6.0, 7, 15000, 5.5e6, 'Pillars of Creation, active star formation region'),
            ('Crab Nebula', 'Supernova Remnant', 'Taurus', 6500, 8.4, 6, 4.6, 968, 'Remnant of supernova observed in 1054 AD, contains pulsar'),
            ('Ring Nebula', 'Planetary Nebula', 'Lyra', 2300, 8.8, 1.4, 0.2, 20000, 'Famous planetary nebula, white dwarf surrounded by ionized gas'),
            ('Horsehead Nebula', 'Dark Nebula', 'Orion', 1500, 0, 8, 0, 5e6, 'Dark nebula silhouetted against bright emission nebula'),
            ('Pleiades', 'Open Cluster', 'Taurus', 444, 1.6, 110, 800, 100e6, 'Seven Sisters, young hot blue stars with reflection nebulae'),
            ('Beehive Cluster', 'Open Cluster', 'Cancer', 577, 3.7, 95, 500, 600e6, 'Praesepe, visible to naked eye, contains red giants and white dwarfs'),
            ('Globular Cluster M13', 'Globular Cluster', 'Hercules', 25100, 5.8, 20, 600000, 11.65e9, 'Great Hercules Cluster, contains over 300,000 stars'),
            ('Whirlpool Galaxy', 'Spiral Galaxy', 'Canes Venatici', 23000000, 8.4, 11, 160e9, 13e9, 'Face-on spiral galaxy, interacting with companion galaxy'),
            ('Sombrero Galaxy', 'Spiral Galaxy', 'Virgo', 29350000, 8.0, 9, 800e9, 13.25e9, 'Edge-on spiral with prominent dust lane and large central bulge'),
            ('Centaurus A', 'Elliptical Galaxy', 'Centaurus', 13700000, 6.84, 25, 1000e9, 12e9, 'Radio galaxy with prominent dust lane, active galactic nucleus'),
            ('Magellanic Clouds', 'Irregular Galaxy', 'Dorado/Tucana', 160000, 0.9, 650, 20e9, 13e9, 'Satellite galaxies of Milky Way, visible from Southern Hemisphere'),
            ('Rosette Nebula', 'Emission Nebula', 'Monoceros', 5200, 9.0, 80, 10000, 4e6, 'Skull-shaped nebula, central cavity carved by stellar winds'),
            ('Cat\'s Eye Nebula', 'Planetary Nebula', 'Draco', 3300, 8.1, 0.3, 0.65, 1000, 'Complex planetary nebula with intricate knots and jets'),
            ('Veil Nebula', 'Supernova Remnant', 'Cygnus', 2100, 7.0, 180, 0, 8000, 'Large supernova remnant, filamentary structure visible in H-alpha'),
            ('Double Cluster', 'Open Cluster', 'Perseus', 7500, 4.3, 60, 3700, 12.8e6, 'NGC 869 and 884, young massive star clusters'),
            ('Coal Sack Nebula', 'Dark Nebula', 'Crux', 600, 0, 420, 0, 0, 'Prominent dark nebula visible to naked eye, Southern Cross region'),
            ('Sagittarius A*', 'Black Hole', 'Sagittarius', 26000, 0, 0, 4.15e6, 13.6e9, 'Supermassive black hole at center of Milky Way galaxy'),
            ('Alpha Centauri System', 'Multiple Star', 'Centaurus', 4.37, -0.27, 0, 2.2, 4.85e9, 'Closest star system, triple star with potentially habitable exoplanet'),
        ]
    
    def _get_physics_formulas_data(self) -> List[Tuple]:
        """Get space physics formulas data for database population."""
        return [
            # name, category, formula, variables, units, description, applications
            ('Escape Velocity', 'Orbital Mechanics', 'v_e = sqrt(2GM/r)', 'v_e=escape velocity, G=gravitational constant, M=mass, r=radius', 'm/s', 'Minimum velocity to escape gravitational field', 'Rocket launches, interplanetary missions'),
            ('Orbital Velocity', 'Orbital Mechanics', 'v = sqrt(GM/r)', 'v=orbital velocity, G=gravitational constant, M=central mass, r=orbital radius', 'm/s', 'Velocity needed for circular orbit', 'Satellite deployment, space station operations'),
            ('Orbital Period', 'Orbital Mechanics', 'T = 2π*sqrt(r³/GM)', 'T=period, r=semi-major axis, G=gravitational constant, M=central mass', 's', 'Time for one complete orbit', 'Mission planning, satellite constellations'),
            ('Hohmann Transfer', 'Orbital Mechanics', 'Δv = sqrt(GM/r1)*(sqrt(2r2/(r1+r2)) - 1) + sqrt(GM/r2)*(1 - sqrt(2r1/(r1+r2)))', 'Δv=velocity change, r1=initial radius, r2=final radius', 'm/s', 'Most efficient two-impulse transfer between circular orbits', 'Interplanetary transfers, orbit changes'),
            ('Rocket Equation', 'Propulsion', 'Δv = v_e * ln(m0/mf)', 'Δv=velocity change, v_e=exhaust velocity, m0=initial mass, mf=final mass', 'm/s', 'Relationship between mass ratio and velocity change', 'Rocket design, mission planning'),
            ('Specific Impulse', 'Propulsion', 'Isp = v_e/g0', 'Isp=specific impulse, v_e=exhaust velocity, g0=standard gravity', 's', 'Efficiency measure of rocket engines', 'Engine performance comparison'),
            ('Gravitational Force', 'Gravity', 'F = GMm/r²', 'F=force, G=gravitational constant, M,m=masses, r=distance', 'N', 'Force between two masses', 'Orbital calculations, tidal forces'),
            ('Tidal Force', 'Gravity', 'F_t = 2GMmr/d³', 'F_t=tidal force, M=primary mass, m=secondary mass, r=radius, d=distance', 'N', 'Differential gravitational force', 'Roche limit, tidal heating'),
            ('Relativistic Velocity Addition', 'Relativity', 'v = (v1 + v2)/(1 + v1*v2/c²)', 'v=combined velocity, v1,v2=individual velocities, c=speed of light', 'm/s', 'Velocity addition at high speeds', 'High-speed spacecraft, particle physics'),
            ('Time Dilation', 'Relativity', 't = t0/sqrt(1 - v²/c²)', 't=dilated time, t0=proper time, v=velocity, c=speed of light', 's', 'Time passes slower at high velocities', 'GPS satellites, high-speed missions'),
            ('Schwarzschild Radius', 'Black Holes', 'rs = 2GM/c²', 'rs=Schwarzschild radius, G=gravitational constant, M=mass, c=speed of light', 'm', 'Event horizon radius of black hole', 'Black hole physics, general relativity'),
            ('Synodic Period', 'Orbital Mechanics', '1/Ps = |1/P1 - 1/P2|', 'Ps=synodic period, P1,P2=orbital periods', 's', 'Time between successive oppositions', 'Launch windows, planetary alignments'),
            ('Vis-Viva Equation', 'Orbital Mechanics', 'v² = GM(2/r - 1/a)', 'v=velocity, G=gravitational constant, M=central mass, r=distance, a=semi-major axis', 'm²/s²', 'Energy conservation in orbital mechanics', 'Orbit determination, trajectory analysis'),
            ('Radiation Pressure', 'Space Environment', 'P = I/c', 'P=pressure, I=intensity, c=speed of light', 'Pa', 'Pressure exerted by electromagnetic radiation', 'Solar sails, attitude perturbations'),
            ('Doppler Shift', 'Physics', 'f = f0(1 ± v/c)', 'f=observed frequency, f0=source frequency, v=relative velocity, c=wave speed', 'Hz', 'Frequency change due to relative motion', 'Communications, navigation, astronomy'),
        ]
    
    def _get_astronaut_procedures_data(self) -> List[Tuple]:
        """Get astronaut procedures data for database population."""
        return [
            # procedure_name, category, duration_minutes, crew_size, equipment_required, safety_considerations, step_by_step, contingencies
            ('EVA Suit Donning', 'EVA Operations', 120, 2, 'EMU suit, PLSS, gloves, helmet, tools', 'Pressure checks, leak tests, communication verification', 
             '1. Medical check and pre-breathing\n2. Don liquid cooling garment\n3. Enter suit through back hatch\n4. Connect life support systems\n5. Pressure and leak checks\n6. Communication tests\n7. Tool and tether attachment\n8. Final systems verification',
             'Suit malfunction: abort EVA, emergency ingress procedures\nLife support issues: immediate return to airlock\nCommunication loss: use backup systems, visual signals'),
            
            ('Spacecraft Docking', 'Flight Operations', 45, 2, 'Docking system, RCS thrusters, cameras, sensors', 'Approach corridor maintenance, contact dynamics', 
             '1. Approach target at 0.1 m/s\n2. Align docking ports using cameras\n3. Monitor closure rate and alignment\n4. Contact and capture at <0.03 m/s\n5. Verify hard dock indicators\n6. Pressurize vestibule\n7. Leak checks and hatch opening\n8. Post-docking configuration',
             'Misalignment: abort and retry approach\nHard contact: assess damage, consider manual backup\nLeak detection: isolate and repair before hatch opening'),
            
            ('Emergency Deorbit', 'Emergency Procedures', 30, 3, 'Deorbit engines, navigation system, heat shield', 'Trajectory verification, thermal protection integrity', 
             '1. Crew strapped in and secured\n2. Configure spacecraft for reentry\n3. Calculate deorbit burn parameters\n4. Execute deorbit burn\n5. Jettison unnecessary modules\n6. Orient for reentry attitude\n7. Monitor thermal protection system\n8. Deploy parachutes at designated altitude',
             'Engine failure: use backup propulsion or RCS\nNavigation failure: use backup systems, ground guidance\nThermal protection damage: adjust reentry profile'),
            
            ('ISS Emergency Evacuation', 'Emergency Procedures', 15, 6, 'Soyuz spacecraft, emergency supplies, communication equipment', 'Rapid egress, crew accountability, life support duration', 
             '1. Sound evacuation alarm\n2. Secure critical systems\n3. Gather emergency supplies\n4. Enter Soyuz vehicles (3 crew each)\n5. Seal hatches and undock\n6. Maintain formation flight\n7. Communicate with ground\n8. Execute emergency landing if required',
             'Soyuz malfunction: use backup vehicle or shelter in place\nRapid depressurization: immediate evacuation\nFire: fight fire first if safe, then evacuate'),
            
            ('Robotic Arm Operations', 'Robotics', 180, 2, 'Robotic arm, end effector, cameras, workstation', 'Collision avoidance, load limits, joint constraints', 
             '1. Power up arm and run diagnostics\n2. Configure cameras and lighting\n3. Plan trajectory avoiding obstacles\n4. Execute slow, controlled movements\n5. Monitor joint angles and loads\n6. Grapple target with end effector\n7. Verify secure capture\n8. Move payload to destination\n9. Release and stow arm',
             'Arm malfunction: switch to backup mode or manual control\nCollision risk: emergency stop and assess\nEnd effector failure: attempt manual grapple or abort operation'),
            
            ('Science Experiment Setup', 'Science Operations', 90, 1, 'Experiment hardware, data storage, power connections', 'Contamination control, proper handling procedures', 
             '1. Review experiment procedures\n2. Prepare workspace and tools\n3. Install experiment hardware\n4. Connect power and data cables\n5. Initialize software and calibrate\n6. Run system checks\n7. Begin data collection\n8. Monitor experiment progress\n9. Document any anomalies',
             'Hardware failure: switch to backup equipment\nData corruption: restart and recalibrate\nContamination: clean and sterilize affected areas'),
            
            ('Water Recovery System Maintenance', 'Life Support', 240, 2, 'Replacement filters, tools, cleaning supplies, spare parts', 'Fluid handling safety, contamination prevention', 
             '1. Shut down water recovery system\n2. Isolate fluid lines\n3. Remove and replace filters\n4. Clean and inspect components\n5. Replace worn parts\n6. Reassemble system\n7. Pressure test all connections\n8. Restart system and verify operation\n9. Sample and test water quality',
             'Leak detection: immediate shutdown and repair\nFilter clogging: emergency bypass mode\nContamination: full system flush and sterilization'),
            
            ('Solar Array Deployment', 'Spacecraft Operations', 60, 2, 'Solar arrays, deployment mechanism, monitoring systems', 'Deployment sequence timing, structural loads', 
             '1. Verify spacecraft attitude and stability\n2. Remove deployment restraints\n3. Initialize deployment sequence\n4. Monitor array extension\n5. Verify panel alignment\n6. Test array articulation\n7. Confirm power generation\n8. Lock arrays in operational position',
             'Deployment jam: attempt manual override\nPartial deployment: assess power impact\nStructural damage: secure arrays and assess mission impact'),
        ]
    
    def _get_space_weather_data(self) -> List[Tuple]:
        """Get space weather phenomena data for database population."""
        return [
            # phenomenon, source, frequency, intensity_scale, effects_on_spacecraft, effects_on_humans, mitigation_strategies, warning_signs
            ('Solar Flares', 'Solar Corona', 'Daily to weekly during solar maximum', 'X-ray flux: A, B, C, M, X classes', 
             'Radio blackouts, GPS errors, satellite charging, solar panel degradation', 
             'Increased radiation exposure, potential DNA damage during EVA', 
             'Shelter in shielded areas, postpone EVAs, use backup communication frequencies', 
             'Sudden radio fadeouts, increased particle counts, aurora activity'),
            
            ('Coronal Mass Ejections', 'Solar Corona', 'Few per week during solar maximum', 'Magnetic field strength and particle density', 
             'Geomagnetic storms, satellite drag increase, power system failures', 
             'Radiation sickness risk, central nervous system effects', 
             'Storm shelters, reduce orbital altitude, power down non-essential systems', 
             'Solar wind speed increase, magnetic field rotation, proton events'),
            
            ('Geomagnetic Storms', 'Earth Magnetosphere', 'Monthly during solar maximum', 'Kp index 0-9, Dst index', 
             'Orbital decay acceleration, attitude control issues, communication disruption', 
             'Disorientation, nausea, potential cardiac effects', 
             'Altitude adjustments, magnetic torquer compensation, medical monitoring', 
             'Aurora expansion, compass deviation, radio interference'),
            
            ('Solar Energetic Particles', 'Solar Flares and CMEs', 'Several per year', 'Proton flux >10 MeV', 
             'Single event upsets, memory corruption, detector noise', 
             'Acute radiation syndrome, skin burns, cataracts', 
             'Immediate shelter, medical countermeasures, system resets', 
             'Sudden particle flux increase, neutron monitor alerts'),
            
            ('Galactic Cosmic Rays', 'Deep Space', 'Constant background', 'Particle energy and flux', 
             'Gradual component degradation, background noise increase', 
             'Chronic radiation exposure, cancer risk, cognitive effects', 
             'Passive shielding, active shielding research, medical monitoring', 
             'Gradual increase with solar minimum, high-energy particle detection'),
            
            ('Micrometeoroid Impacts', 'Asteroid Belt and Comets', 'Continuous', 'Size and velocity distribution', 
             'Hull penetration, system damage, debris creation', 
             'Suit puncture risk during EVA, habitat depressurization', 
             'Whipple shields, debris tracking, impact-resistant design', 
             'Sudden pressure loss, impact signatures, debris field encounters'),
            
            ('Plasma Irregularities', 'Ionosphere', 'Daily variations', 'Total electron content variations', 
             'GPS signal scintillation, communication phase errors', 
             'Navigation errors during critical operations', 
             'Multiple GPS receivers, inertial navigation backup', 
             'Signal amplitude variations, phase fluctuations, loss of lock'),
            
            ('Atmospheric Drag Variations', 'Thermosphere', 'Solar cycle dependent', 'Atmospheric density changes', 
             'Orbital decay rate changes, mission lifetime reduction', 
             'Unplanned reentry risk, mission duration impact', 
             'Propulsive orbit maintenance, atmospheric density monitoring', 
             'Solar activity increase, thermosphere heating, density models'),
        ]
    
    def _get_space_technology_data(self) -> List[Tuple]:
        """Get space technology specifications for database population."""
        return [
            # technology_name, category, specifications, operating_conditions, power_requirements, maintenance_schedule, failure_modes, description
            ('Life Support System (ECLSS)', 'Life Support', 'O2 generation: 5.5 kg/day, CO2 removal: 9 kg/day, Water recovery: 93% efficiency', 
             'Temperature: 18-27°C, Humidity: 25-75%, Pressure: 101.3 kPa', '6-8 kW continuous power', 
             'Filter replacement: 90 days, Component inspection: 180 days', 
             'Filter clogging, pump failure, sensor drift, contamination', 
             'Environmental Control and Life Support System maintaining breathable atmosphere'),
            
            ('Extravehicular Mobility Unit (EMU)', 'EVA Equipment', 'Operating pressure: 29.6 kPa, Life support: 8 hours, Mass: 113 kg', 
             'Vacuum to 1 atm, Temperature: -157°C to +121°C', '16.8V DC, 550W peak', 
             'Pre-EVA checkout: each use, Major service: 25 EVAs', 
             'Pressure loss, cooling failure, communication loss, joint lock-up', 
             'Spacesuit providing life support and mobility for spacewalks'),
            
            ('Reaction Control System (RCS)', 'Propulsion', 'Thrust: 25-490 N per thruster, Propellant: MMH/N2O4, Isp: 290s', 
             'Operating temperature: -40°C to +70°C, Vacuum operation', '28V DC, 50W per valve', 
             'Thruster inspection: 100 cycles, Valve replacement: 1000 cycles', 
             'Thruster clogging, valve leakage, propellant contamination', 
             'Small thrusters for attitude control and orbital maneuvering'),
            
            ('Solar Array System', 'Power Generation', 'Power output: 84-120 kW, Efficiency: 14.2%, Area: 2500 m²', 
             'Temperature: -157°C to +121°C, Space environment', 'Self-generating', 
             'Visual inspection: monthly, Electrical test: quarterly', 
             'Cell degradation, micrometeoroid damage, wiring failure, tracking error', 
             'Photovoltaic arrays converting sunlight to electrical power'),
            
            ('Canadarm2 (SSRMS)', 'Robotics', 'Length: 17.6m, Payload: 116,000 kg, Joints: 7 DOF', 
             'Temperature: -157°C to +121°C, Vacuum operation', '28V DC, 2.5 kW peak', 
             'Joint lubrication: 6 months, End effector service: 12 months', 
             'Joint seizure, end effector failure, wire harness damage', 
             'Space Station Remote Manipulator System for cargo handling'),
            
            ('Ku-Band Communication System', 'Communications', 'Data rate: 300 Mbps down, 25 Mbps up, Frequency: 13.775-14.5 GHz', 
             'Antenna pointing accuracy: ±0.2°, Space environment', '28V DC, 1.2 kW', 
             'Antenna alignment: weekly, Amplifier check: monthly', 
             'Antenna pointing error, amplifier failure, signal interference', 
             'High-speed data communication with ground stations'),
            
            ('Thermal Control System', 'Thermal Management', 'Heat rejection: 35 kW, Coolant: ammonia, Operating range: -157°C to +121°C', 
             'Radiator area: 1680 m², Pump flow rate: 180 kg/hr', '28V DC, 800W pumps', 
             'Pump inspection: 6 months, Radiator cleaning: annually', 
             'Pump failure, coolant leak, radiator damage, valve malfunction', 
             'Active and passive thermal control maintaining operating temperatures'),
            
            ('Guidance Navigation Control (GNC)', 'Navigation', 'GPS accuracy: ±5m, IMU drift: <0.1°/hr, Star tracker accuracy: 1 arcsec', 
             'Operating temperature: -40°C to +70°C, Radiation hardened', '28V DC, 200W', 
             'Calibration: monthly, Software update: as needed', 
             'Sensor failure, software corruption, actuator malfunction', 
             'Integrated system for spacecraft position, attitude, and control'),
            
            ('Pressurized Mating Adapter (PMA)', 'Docking Systems', 'Diameter: 1.27m, Pressure rating: 103.4 kPa, Leak rate: <0.1 kg/day', 
             'Docking loads: 67 kN, Temperature: -40°C to +50°C', 'Passive system', 
             'Seal inspection: before each docking, Mechanism test: quarterly', 
             'Seal degradation, mechanism jam, structural damage', 
             'Interface adapter for spacecraft docking operations'),
        ]
    
    def query(self, nlu_result: Dict, context: Dict = None) -> Dict[str, Any]:
        """Enhanced query method with ChatGPT-level understanding."""
        query_text = nlu_result.get('processed_text', '').lower()
        original_text = nlu_result.get('original_text', '')
        entities = nlu_result.get('entities', {})
        
        try:
            # Enhanced pattern matching for better understanding
            # Direct celestial body queries with basic responses
            celestial_info = {
                'mars': "Mars is the fourth planet from the Sun, known as the Red Planet due to iron oxide on its surface. It has two small moons, Phobos and Deimos, and is a primary target for human exploration.",
                'jupiter': "Jupiter is the largest planet in our solar system, a gas giant with over 80 known moons including the four Galilean moons. It has a Great Red Spot storm and acts as a cosmic vacuum cleaner.",
                'saturn': "Saturn is famous for its spectacular ring system made of ice and rock particles. It's a gas giant with over 80 moons, including Titan which has a thick atmosphere.",
                'earth': "Earth is our home planet, the third from the Sun. It's the only known planet with life, has one natural satellite (the Moon), and 71% of its surface is covered by water.",
                'moon': "The Moon is Earth's only natural satellite, formed about 4.5 billion years ago. It influences Earth's tides and has been the target of human exploration since 1969.",
                'sun': "The Sun is a G-type main-sequence star at the center of our solar system. It contains 99.86% of the system's mass and generates energy through nuclear fusion.",
                'venus': "Venus is the second planet from the Sun and the hottest planet in our solar system due to its thick atmosphere of carbon dioxide. It rotates backwards compared to most planets.",
                'mercury': "Mercury is the smallest planet and closest to the Sun. It has extreme temperature variations and no atmosphere to retain heat.",
                'uranus': "Uranus is an ice giant that rotates on its side. It has a faint ring system and 27 known moons.",
                'neptune': "Neptune is the farthest planet from the Sun, known for its deep blue color and the fastest winds in the solar system.",
                'pluto': "Pluto is a dwarf planet in the Kuiper Belt, formerly considered the ninth planet until 2006."
            }
            
            for body, info in celestial_info.items():
                if body in query_text:
                    return {
                        'answer': info,
                        'confidence': 0.8,
                        'source': 'celestial_knowledge',
                        'category': 'space_knowledge'
                    }
            
            # Direct entity-based routing
            if 'celestial_body' in entities:
                return self._query_celestial_body(entities['celestial_body'], query_text)
            elif 'spacecraft' in entities:
                return self._query_spacecraft(entities['spacecraft'], query_text)
            
            # Check for specific knowledge areas
            elif any(word in query_text for word in ['constellation', 'zodiac', 'asterism']):
                return self._query_constellations(query_text)
            elif any(word in query_text.lower() for word in ['exoplanet', 'habitable', 'kepler', 'trappist']):
                return self._query_exoplanets(query_text)
            elif any(word in query_text.lower() for word in ['history', 'mission', 'apollo', 'sputnik', 'launch']):
                return self._query_space_history(query_text)
            elif any(word in query_text.lower() for word in ['cosmology', 'universe', 'dark matter', 'big bang']):
                return self._query_cosmology(query_text)
            elif any(word in query_text.lower() for word in ['astrobiology', 'life', 'biosignature', 'extremophile']):
                return self._query_astrobiology(query_text)
            elif any(word in query_text.lower() for word in ['medicine', 'health', 'bone loss', 'radiation']):
                return self._query_space_medicine(query_text)
            elif any(word in query_text.lower() for word in ['star', 'galaxy', 'nebula', 'cluster']):
                return self._query_stellar_objects(query_text)
            elif any(word in query_text.lower() for word in ['formula', 'equation', 'physics', 'orbital', 'velocity']):
                return self._query_physics_formulas(query_text)
            elif any(word in query_text.lower() for word in ['procedure', 'eva', 'docking', 'maintenance']):
                return self._query_astronaut_procedures(query_text)
            elif any(word in query_text.lower() for word in ['weather', 'solar', 'storm']):
                return self._query_space_weather(query_text)
            elif any(word in query_text.lower() for word in ['technology', 'equipment', 'system', 'life support']):
                return self._query_space_technology(query_text)
            elif any(word in query_text.lower() for word in ['constant', 'value', 'speed of light', 'gravity']):
                return self._query_constants(query_text)
            elif 'emergency' in query_text.lower():
                return self._query_emergency_procedures(query_text)
            else:
                return self._comprehensive_search(query_text)
                
        except Exception as e:
            self.logger.error(f"Knowledge query error: {e}")
            return {
                'answer': f"I encountered an error searching the knowledge base: {str(e)}",
                'confidence': 0.0,
                'source': 'error'
            }
    
    def _query_celestial_body(self, entities: List[Dict], query_text: str) -> Dict[str, Any]:
        """Query information about celestial bodies."""
        try:
            body_name = entities[0]['value']
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM celestial_bodies 
                    WHERE name LIKE ? OR name LIKE ?
                ''', (f'%{body_name}%', f'{body_name}%'))
                
                result = cursor.fetchone()
                
                if result:
                    columns = [desc[0] for desc in cursor.description]
                    body_data = dict(zip(columns, result))
                    
                    answer = f"**{body_data.get('name', 'Unknown')}**\n\n"
                    answer += f"Type: {body_data.get('type', 'Unknown')}\n"
                    answer += f"This is a celestial body in our knowledge database."
                    
                    return {
                        'answer': answer,
                        'confidence': 0.9,
                        'source': 'celestial_bodies_db',
                        'data': body_data
                    }
                else:
                    return {
                        'answer': f"I don't have information about {body_name} in my knowledge base.",
                        'confidence': 0.1,
                        'source': 'celestial_bodies_db'
                    }
        except Exception as e:
            return {
                'answer': f"Error querying celestial body: {str(e)}",
                'confidence': 0.0,
                'source': 'error'
            }
    
    def _comprehensive_search(self, query_text: str) -> Dict[str, Any]:
        """Perform comprehensive search across all knowledge areas."""
        try:
            # Simple fallback response for now
            return {
                'answer': "I understand you're asking about space or science topics. I can help with information about planets, spacecraft, physics calculations, and scientific concepts. Could you be more specific about what you'd like to know?",
                'confidence': 0.3,
                'source': 'fallback_search'
            }
        except Exception as e:
            return {
                'answer': f"Search error: {str(e)}",
                'confidence': 0.0,
                'source': 'error'
            }
    
    def _query_spacecraft(self, entities: List[Dict], query_text: str) -> Dict[str, Any]:
        """Query information about spacecraft."""
        try:
            spacecraft_name = entities[0]['value']
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM spacecraft 
                    WHERE name LIKE ? OR name LIKE ?
                ''', (f'%{spacecraft_name}%', f'{spacecraft_name}%'))
                
                result = cursor.fetchone()
                
                if result:
                    columns = [desc[0] for desc in cursor.description]
                    spacecraft_data = dict(zip(columns, result))
                    
                    answer = self._format_spacecraft_info(spacecraft_data, query_text)
                    
                    return {
                        'answer': answer,
                        'confidence': 0.9,
                        'source': 'spacecraft_db',
                        'data': spacecraft_data
                    }
                else:
                    return {
                        'answer': f"I don't have information about {spacecraft_name} in my knowledge base.",
                        'confidence': 0.1,
                        'source': 'spacecraft_db'
                    }
                    
        except Exception as e:
            return {
                'answer': f"Error querying spacecraft information: {str(e)}",
                'confidence': 0.0,
                'source': 'error'
            }
    
    def _format_spacecraft_info(self, data: Dict, query_text: str) -> str:
        """Format spacecraft information for display."""
        name = data['name']
        spacecraft_type = data['type']
        
        info = [f"{name} is a {spacecraft_type.lower()}."]
        
        if data['description']:
            info.append(data['description'])
        
        if data['launch_date']:
            info.append(f"Launch date: {data['launch_date']}")
        
        if data['mission_status']:
            info.append(f"Mission status: {data['mission_status']}")
        
        if data['agency']:
            info.append(f"Agency: {data['agency']}")
        
        if 'mass' in query_text and data['mass_kg']:
            info.append(f"Mass: {data['mass_kg']:,} kg")
        
        if 'power' in query_text and data['power_watts']:
            info.append(f"Power: {data['power_watts']:,} watts")
        
        if 'orbit' in query_text and data['orbit_altitude_km']:
            info.append(f"Orbital altitude: {data['orbit_altitude_km']:,} km")
        
        return " ".join(info)
    
    def _query_constants(self, query_text: str) -> Dict[str, Any]:
        """Query physical constants."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Search for constants by name or symbol
                search_terms = query_text.split()
                conditions = []
                params = []
                
                for term in search_terms:
                    conditions.append("(name LIKE ? OR symbol LIKE ? OR description LIKE ?)")
                    params.extend([f'%{term}%', f'%{term}%', f'%{term}%'])
                
                query = f"SELECT * FROM constants WHERE {' OR '.join(conditions)}"
                cursor.execute(query, params)
                
                results = cursor.fetchall()
                
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    constants = [dict(zip(columns, row)) for row in results]
                    
                    answer = self._format_constants_info(constants)
                    
                    return {
                        'answer': answer,
                        'confidence': 0.8,
                        'source': 'constants_db',
                        'data': constants
                    }
                else:
                    return {
                        'answer': "I couldn't find any matching physical constants.",
                        'confidence': 0.1,
                        'source': 'constants_db'
                    }
                    
        except Exception as e:
            return {
                'answer': f"Error querying constants: {str(e)}",
                'confidence': 0.0,
                'source': 'error'
            }
    
    def _format_constants_info(self, constants: List[Dict]) -> str:
        """Format physical constants information."""
        if len(constants) == 1:
            const = constants[0]
            return f"{const['name']} ({const['symbol']}): {const['value']} {const['unit']}. {const['description']}"
        else:
            info = ["Here are the matching physical constants:"]
            for const in constants[:5]:  # Limit to 5 results
                info.append(f"• {const['name']} ({const['symbol']}): {const['value']} {const['unit']}")
            return "\n".join(info)
    
    def _query_emergency_procedures(self, query_text: str) -> Dict[str, Any]:
        """Query emergency procedures."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Search for emergency procedures
                cursor.execute('''
                    SELECT * FROM emergency_procedures 
                    WHERE emergency_type LIKE ? OR immediate_actions LIKE ? OR detailed_procedure LIKE ?
                ''', (f'%{query_text}%', f'%{query_text}%', f'%{query_text}%'))
                
                results = cursor.fetchall()
                
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    procedures = [dict(zip(columns, row)) for row in results]
                    
                    answer = self._format_emergency_procedures(procedures)
                    
                    return {
                        'answer': answer,
                        'confidence': 0.9,
                        'source': 'emergency_procedures_db',
                        'data': procedures
                    }
                else:
                    return {
                        'answer': "I couldn't find specific emergency procedures for that situation. Please contact mission control immediately for any emergency.",
                        'confidence': 0.3,
                        'source': 'emergency_procedures_db'
                    }
                    
        except Exception as e:
            return {
                'answer': f"Error querying emergency procedures: {str(e)}",
                'confidence': 0.0,
                'source': 'error'
            }
    
    def _format_emergency_procedures(self, procedures: List[Dict]) -> str:
        """Format emergency procedures information."""
        if len(procedures) == 1:
            proc = procedures[0]
            info = [f"🚨 EMERGENCY: {proc['emergency_type']} (Severity: {proc['severity']})"]
            info.append(f"\nIMMEDIATE ACTIONS: {proc['immediate_actions']}")
            info.append(f"\nDETAILED PROCEDURE:\n{proc['detailed_procedure']}")
            if proc['equipment_needed']:
                info.append(f"\nEQUIPMENT NEEDED: {proc['equipment_needed']}")
            if proc['time_critical']:
                info.append("\n⚠️ TIME CRITICAL - Act immediately!")
            return "\n".join(info)
        else:
            info = ["Multiple emergency procedures found:"]
            for proc in procedures:
                critical = " (TIME CRITICAL)" if proc['time_critical'] else ""
                info.append(f"• {proc['emergency_type']} - {proc['severity']} severity{critical}")
            return "\n".join(info)
    
    def _query_stellar_objects(self, query_text: str) -> Dict[str, Any]:
        """Query stellar objects database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                search_terms = query_text.split()
                conditions = []
                params = []
                
                for term in search_terms:
                    conditions.append("(name LIKE ? OR object_type LIKE ? OR constellation LIKE ? OR description LIKE ?)")
                    params.extend([f'%{term}%', f'%{term}%', f'%{term}%', f'%{term}%'])
                
                query = f"SELECT * FROM stellar_objects WHERE {' OR '.join(conditions)} LIMIT 5"
                cursor.execute(query, params)
                results = cursor.fetchall()
                
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    stellar_objects = [dict(zip(columns, row)) for row in results]
                    answer = self._format_stellar_objects_info(stellar_objects)
                    
                    return {
                        'answer': answer,
                        'confidence': 0.8,
                        'source': 'stellar_objects_db',
                        'data': stellar_objects
                    }
                else:
                    return {
                        'answer': "I couldn't find matching stellar objects. Try searching for specific star names, constellations, or object types.",
                        'confidence': 0.2,
                        'source': 'stellar_objects_db'
                    }
        except Exception as e:
            return {
                'answer': f"Error querying stellar objects: {str(e)}",
                'confidence': 0.0,
                'source': 'error'
            }
    
    def _query_physics_formulas(self, query_text: str) -> Dict[str, Any]:
        """Query physics formulas database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                search_terms = query_text.split()
                conditions = []
                params = []
                
                for term in search_terms:
                    conditions.append("(name LIKE ? OR category LIKE ? OR description LIKE ? OR applications LIKE ?)")
                    params.extend([f'%{term}%', f'%{term}%', f'%{term}%', f'%{term}%'])
                
                query = f"SELECT * FROM physics_formulas WHERE {' OR '.join(conditions)} LIMIT 5"
                cursor.execute(query, params)
                results = cursor.fetchall()
                
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    formulas = [dict(zip(columns, row)) for row in results]
                    answer = self._format_physics_formulas_info(formulas)
                    
                    return {
                        'answer': answer,
                        'confidence': 0.9,
                        'source': 'physics_formulas_db',
                        'data': formulas
                    }
                else:
                    return {
                        'answer': "I couldn't find matching physics formulas. Try searching for specific physics concepts or formula names.",
                        'confidence': 0.2,
                        'source': 'physics_formulas_db'
                    }
        except Exception as e:
            return {
                'answer': f"Error querying physics formulas: {str(e)}",
                'confidence': 0.0,
                'source': 'error'
            }
    
    def _query_astronaut_procedures(self, query_text: str) -> Dict[str, Any]:
        """Query astronaut procedures database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                search_terms = query_text.split()
                conditions = []
                params = []
                
                for term in search_terms:
                    conditions.append("(procedure_name LIKE ? OR category LIKE ? OR step_by_step LIKE ?)")
                    params.extend([f'%{term}%', f'%{term}%', f'%{term}%'])
                
                query = f"SELECT * FROM astronaut_procedures WHERE {' OR '.join(conditions)} LIMIT 3"
                cursor.execute(query, params)
                results = cursor.fetchall()
                
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    procedures = [dict(zip(columns, row)) for row in results]
                    answer = self._format_astronaut_procedures_info(procedures)
                    
                    return {
                        'answer': answer,
                        'confidence': 0.9,
                        'source': 'astronaut_procedures_db',
                        'data': procedures
                    }
                else:
                    return {
                        'answer': "I couldn't find matching procedures. Try searching for specific operations like EVA, docking, or maintenance.",
                        'confidence': 0.2,
                        'source': 'astronaut_procedures_db'
                    }
        except Exception as e:
            return {
                'answer': f"Error querying astronaut procedures: {str(e)}",
                'confidence': 0.0,
                'source': 'error'
            }
    
    def _query_space_weather(self, query_text: str) -> Dict[str, Any]:
        """Query space weather database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                search_terms = query_text.split()
                conditions = []
                params = []
                
                for term in search_terms:
                    conditions.append("(phenomenon LIKE ? OR source LIKE ? OR effects_on_spacecraft LIKE ? OR effects_on_humans LIKE ?)")
                    params.extend([f'%{term}%', f'%{term}%', f'%{term}%', f'%{term}%'])
                
                query = f"SELECT * FROM space_weather WHERE {' OR '.join(conditions)} LIMIT 5"
                cursor.execute(query, params)
                results = cursor.fetchall()
                
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    weather_data = [dict(zip(columns, row)) for row in results]
                    answer = self._format_space_weather_info(weather_data)
                    
                    return {
                        'answer': answer,
                        'confidence': 0.8,
                        'source': 'space_weather_db',
                        'data': weather_data
                    }
                else:
                    return {
                        'answer': "I couldn't find matching space weather information. Try searching for solar flares, radiation, or geomagnetic storms.",
                        'confidence': 0.2,
                        'source': 'space_weather_db'
                    }
        except Exception as e:
            return {
                'answer': f"Error querying space weather: {str(e)}",
                'confidence': 0.0,
                'source': 'error'
            }
    
    def _query_space_technology(self, query_text: str) -> Dict[str, Any]:
        """Query space technology database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                search_terms = query_text.split()
                conditions = []
                params = []
                
                for term in search_terms:
                    conditions.append("(technology_name LIKE ? OR category LIKE ? OR specifications LIKE ? OR description LIKE ?)")
                    params.extend([f'%{term}%', f'%{term}%', f'%{term}%', f'%{term}%'])
                
                query = f"SELECT * FROM space_technology WHERE {' OR '.join(conditions)} LIMIT 5"
                cursor.execute(query, params)
                results = cursor.fetchall()
                
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    technology_data = [dict(zip(columns, row)) for row in results]
                    answer = self._format_space_technology_info(technology_data)
                    
                    return {
                        'answer': answer,
                        'confidence': 0.8,
                        'source': 'space_technology_db',
                        'data': technology_data
                    }
                else:
                    return {
                        'answer': "I couldn't find matching space technology information. Try searching for specific systems or equipment.",
                        'confidence': 0.2,
                        'source': 'space_technology_db'
                    }
        except Exception as e:
            return {
                'answer': f"Error querying space technology: {str(e)}",
                'confidence': 0.0,
                'source': 'error'
            }
    
    def _comprehensive_search(self, query_text: str) -> Dict[str, Any]:
        """Perform comprehensive search across all knowledge databases."""
        try:
            all_results = []
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                search_terms = query_text.split()
                
                # Search all tables
                tables_to_search = [
                    ('celestial_bodies', ['name', 'type', 'description']),
                    ('spacecraft', ['name', 'type', 'description']),
                    ('stellar_objects', ['name', 'object_type', 'description']),
                    ('deep_space_objects', ['name', 'object_type', 'description']),
                    ('physics_formulas', ['name', 'category', 'description']),
                    ('astronaut_procedures', ['procedure_name', 'category']),
                    ('space_weather', ['phenomenon', 'source']),
                    ('space_technology', ['technology_name', 'category', 'description'])
                ]
                
                for table_name, columns in tables_to_search:
                    for term in search_terms:
                        conditions = [f"{col} LIKE ?" for col in columns]
                        params = [f'%{term}%'] * len(columns)
                        
                        query = f"SELECT {', '.join(columns)} FROM {table_name} WHERE {' OR '.join(conditions)} LIMIT 2"
                        cursor.execute(query, params)
                        
                        for row in cursor.fetchall():
                            result_text = f"{row[0]} ({row[1]})"
                            if len(row) > 2 and row[2]:
                                result_text += f": {row[2][:100]}..."
                            all_results.append(result_text)
            
            if all_results:
                # Remove duplicates and limit results
                unique_results = list(dict.fromkeys(all_results))[:5]
                answer = "Here's what I found across all knowledge areas:\n" + "\n".join(f"• {result}" for result in unique_results)
                
                return {
                    'answer': answer,
                    'confidence': 0.6,
                    'source': 'comprehensive_search'
                }
            else:
                return {
                    'answer': "I couldn't find specific information about that topic in my knowledge base. Could you be more specific or try rephrasing your question?",
                    'confidence': 0.2,
                    'source': 'comprehensive_search'
                }
                
        except Exception as e:
            return {
                'answer': f"Error performing comprehensive search: {str(e)}",
                'confidence': 0.0,
                'source': 'error'
            }
    
    def _format_stellar_objects_info(self, objects: List[Dict]) -> str:
        """Format stellar objects information for display."""
        if len(objects) == 1:
            obj = objects[0]
            info = [f"{obj['name']} is a {obj['object_type'].lower()}"]
            if obj['constellation']:
                info.append(f"in the constellation {obj['constellation']}")
            if obj['distance_ly']:
                info.append(f"Distance: {obj['distance_ly']:,} light-years")
            if obj['magnitude']:
                info.append(f"Magnitude: {obj['magnitude']}")
            if obj['description']:
                info.append(obj['description'])
            return ". ".join(info) + "."
        else:
            info = ["Stellar objects found:"]
            for obj in objects:
                info.append(f"• {obj['name']} ({obj['object_type']}) - {obj['description'][:80]}...")
            return "\n".join(info)
    
    def _format_physics_formulas_info(self, formulas: List[Dict]) -> str:
        """Format physics formulas information for display."""
        if len(formulas) == 1:
            formula = formulas[0]
            info = [f"**{formula['name']}** ({formula['category']})"]
            info.append(f"Formula: {formula['formula']}")
            info.append(f"Variables: {formula['variables']}")
            info.append(f"Units: {formula['units']}")
            if formula['description']:
                info.append(f"Description: {formula['description']}")
            if formula['applications']:
                info.append(f"Applications: {formula['applications']}")
            return "\n".join(info)
        else:
            info = ["Physics formulas found:"]
            for formula in formulas:
                info.append(f"• **{formula['name']}**: {formula['formula']} - {formula['description']}")
            return "\n".join(info)
    
    def _format_astronaut_procedures_info(self, procedures: List[Dict]) -> str:
        """Format astronaut procedures information for display."""
        if len(procedures) == 1:
            proc = procedures[0]
            info = [f"**{proc['procedure_name']}** ({proc['category']})"]
            if proc['duration_minutes']:
                info.append(f"Duration: {proc['duration_minutes']} minutes")
            if proc['crew_size']:
                info.append(f"Crew size: {proc['crew_size']}")
            if proc['equipment_required']:
                info.append(f"Equipment: {proc['equipment_required']}")
            if proc['safety_considerations']:
                info.append(f"Safety: {proc['safety_considerations']}")
            info.append(f"\nSteps:\n{proc['step_by_step']}")
            if proc['contingencies']:
                info.append(f"\nContingencies:\n{proc['contingencies']}")
            return "\n".join(info)
        else:
            info = ["Astronaut procedures found:"]
            for proc in procedures:
                duration = f" ({proc['duration_minutes']} min)" if proc['duration_minutes'] else ""
                info.append(f"• **{proc['procedure_name']}**{duration} - {proc['category']}")
            return "\n".join(info)
    
    def _format_space_weather_info(self, weather_data: List[Dict]) -> str:
        """Format space weather information for display."""
        if len(weather_data) == 1:
            weather = weather_data[0]
            info = [f"**{weather['phenomenon']}**"]
            info.append(f"Source: {weather['source']}")
            if weather['frequency']:
                info.append(f"Frequency: {weather['frequency']}")
            if weather['intensity_scale']:
                info.append(f"Scale: {weather['intensity_scale']}")
            if weather['effects_on_spacecraft']:
                info.append(f"Spacecraft effects: {weather['effects_on_spacecraft']}")
            if weather['effects_on_humans']:
                info.append(f"Human effects: {weather['effects_on_humans']}")
            if weather['mitigation_strategies']:
                info.append(f"Mitigation: {weather['mitigation_strategies']}")
            if weather['warning_signs']:
                info.append(f"Warning signs: {weather['warning_signs']}")
            return "\n".join(info)
        else:
            info = ["Space weather phenomena found:"]
            for weather in weather_data:
                info.append(f"• **{weather['phenomenon']}** - {weather['source']}")
            return "\n".join(info)
    
    def _format_space_technology_info(self, technology_data: List[Dict]) -> str:
        """Format space technology information for display."""
        if len(technology_data) == 1:
            tech = technology_data[0]
            info = [f"**{tech['technology_name']}**"]
            info.append(f"Category: {tech['category']}")
            if tech['specifications']:
                info.append(f"Specifications: {tech['specifications']}")
            if tech['operating_conditions']:
                info.append(f"Operating conditions: {tech['operating_conditions']}")
            if tech['power_requirements']:
                info.append(f"Power: {tech['power_requirements']}")
            if tech['maintenance_schedule']:
                info.append(f"Maintenance: {tech['maintenance_schedule']}")
            if tech['failure_modes']:
                info.append(f"Failure modes: {tech['failure_modes']}")
            if tech['description']:
                info.append(f"Description: {tech['description']}")
            return "\n".join(info)
        else:
            info = ["Space technology found:"]
            for tech in technology_data:
                info.append(f"• **{tech['technology_name']}** ({tech['category']}) - {tech['description'][:60]}...")
            return "\n".join(info)
    
    def get_random_fact(self) -> str:
        """Get a random space fact from any knowledge area."""
        try:
            import random
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Randomly choose a table to get fact from
                fact_queries = [
                    'SELECT name, description FROM celestial_bodies WHERE description IS NOT NULL ORDER BY RANDOM() LIMIT 1',
                    'SELECT name, description FROM stellar_objects WHERE description IS NOT NULL ORDER BY RANDOM() LIMIT 1',
                    'SELECT name, description FROM deep_space_objects WHERE description IS NOT NULL ORDER BY RANDOM() LIMIT 1',
                    'SELECT name, description FROM spacecraft WHERE description IS NOT NULL ORDER BY RANDOM() LIMIT 1'
                ]
                
                query = random.choice(fact_queries)
                cursor.execute(query)
                result = cursor.fetchone()
                
                if result:
                    return f"Space fact about {result[0]}: {result[1]}"
                else:
                    return "Did you know that the observable universe contains over 2 trillion galaxies?"
                    
        except Exception as e:
            return "I couldn't retrieve a space fact right now."
    
    def get_knowledge_stats(self) -> Dict[str, int]:
        """Get statistics about the knowledge base content."""
        try:
            stats = {}
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                tables = [
                    'celestial_bodies', 'spacecraft', 'constants', 'emergency_procedures',
                    'stellar_objects', 'deep_space_objects', 'physics_formulas',
                    'astronaut_procedures', 'space_weather', 'space_technology'
                ]
                
                for table in tables:
                    cursor.execute(f'SELECT COUNT(*) FROM {table}')
                    stats[table] = cursor.fetchone()[0]
                    
            return stats
        except Exception as e:
            self.logger.error(f"Error getting knowledge stats: {e}")
            return {}
    
    def _get_constellations_data(self) -> List[Tuple]:
        """Get comprehensive constellation data for database population."""
        return [
            # name, abbreviation, area_sq_degrees, brightest_star, mythology, visibility, notable_objects, description
            ('Andromeda', 'And', 722.3, 'Alpheratz', 'Princess chained to rock as sacrifice to sea monster', 'Northern hemisphere autumn', 'Andromeda Galaxy (M31), NGC 7662', 'Large constellation containing the nearest major galaxy to the Milky Way'),
            ('Aquarius', 'Aqr', 979.9, 'Sadalsuud', 'Water-bearer, cup-bearer to the gods', 'Southern sky autumn', 'Helix Nebula, Aquarius Dwarf Galaxy', 'Zodiacal constellation known for meteor showers and water symbolism'),
            ('Aquila', 'Aql', 652.5, 'Altair', 'Eagle carrying Zeus thunderbolts', 'Summer northern hemisphere', 'Altair (12th brightest star), Wild Duck Cluster', 'Contains Altair, one of the vertices of the Summer Triangle'),
            ('Aries', 'Ari', 441.4, 'Hamal', 'Golden ram with fleece sought by Jason', 'Northern autumn/winter', 'NGC 772 galaxy', 'First constellation of the zodiac, marking vernal equinox in ancient times'),
            ('Auriga', 'Aur', 657.4, 'Capella', 'Charioteer holding goat and kids', 'Northern winter', 'Capella (6th brightest star), M36, M37, M38 clusters', 'Contains brilliant Capella and several prominent star clusters'),
            ('Boötes', 'Boo', 906.8, 'Arcturus', 'Herdsman or bear driver', 'Northern spring/summer', 'Arcturus (4th brightest star), NGC 5466', 'Contains Arcturus, easily found by following Big Dipper handle'),
            ('Cancer', 'Cnc', 505.9, 'Tarf', 'Crab sent by Hera to distract Hercules', 'Northern spring', 'Beehive Cluster (M44), M67', 'Faintest zodiacal constellation, home to the famous Beehive Cluster'),
            ('Canis Major', 'CMa', 380.1, 'Sirius', 'Greater dog following Orion', 'Northern winter', 'Sirius (brightest star), M41 cluster', 'Contains Sirius, the brightest star in the night sky'),
            ('Canis Minor', 'CMi', 183.4, 'Procyon', 'Lesser dog, companion to Canis Major', 'Northern winter', 'Procyon (8th brightest star)', 'Small constellation with the bright star Procyon'),
            ('Capricornus', 'Cap', 413.9, 'Deneb Algedi', 'Sea-goat, half goat half fish', 'Southern summer', 'Globular cluster M30', 'Zodiacal constellation representing the sea-goat'),
            ('Cassiopeia', 'Cas', 598.4, 'Gamma Cassiopeiae', 'Vain queen punished by Poseidon', 'Northern circumpolar', 'Heart Nebula, Soul Nebula, M52, M103', 'Distinctive W-shaped constellation, circumpolar from northern latitudes'),
            ('Centaurus', 'Cen', 1060.4, 'Alpha Centauri', 'Centaur, half man half horse', 'Southern hemisphere', 'Alpha Centauri system, Omega Centauri, Proxima Centauri', 'Contains the closest star system to Earth and largest globular cluster'),
            ('Cygnus', 'Cyg', 803.9, 'Deneb', 'Swan flying along Milky Way', 'Northern summer', 'Deneb (19th brightest star), North America Nebula, Veil Nebula', 'Prominent summer constellation lying along the Milky Way'),
            ('Draco', 'Dra', 1082.9, 'Gamma Draconis', 'Dragon guarding golden apples', 'Northern circumpolar', 'Cat\'s Eye Nebula, Spindle Galaxy', 'Large circumpolar constellation wrapping around the north celestial pole'),
            ('Gemini', 'Gem', 513.8, 'Pollux', 'Twins Castor and Pollux', 'Northern winter', 'Castor and Pollux stars, M35 cluster, Eskimo Nebula', 'Zodiacal constellation with prominent twin stars'),
            ('Leo', 'Leo', 946.9, 'Regulus', 'Lion killed by Hercules', 'Northern spring', 'Regulus (21st brightest star), Leo Triplet galaxies', 'Prominent zodiacal constellation resembling a lion'),
            ('Libra', 'Lib', 538.1, 'Zubeneschamali', 'Scales of justice', 'Southern spring', 'Gliese 581 system', 'Zodiacal constellation representing scales or balance'),
            ('Lyra', 'Lyr', 286.5, 'Vega', 'Lyre of Orpheus', 'Northern summer', 'Vega (5th brightest star), Ring Nebula', 'Small but prominent constellation containing brilliant Vega'),
            ('Orion', 'Ori', 594.1, 'Rigel', 'Hunter with belt and sword', 'Winter worldwide', 'Orion Nebula, Horsehead Nebula, Betelgeuse, Rigel', 'Most recognizable constellation with prominent nebulae and bright stars'),
            ('Pegasus', 'Peg', 1120.8, 'Enif', 'Winged horse of Greek mythology', 'Northern autumn', 'Great Square of Pegasus, M15 globular cluster', 'Large constellation featuring the prominent Great Square asterism'),
            ('Perseus', 'Per', 614.9, 'Mirfak', 'Hero who slayed Medusa', 'Northern autumn/winter', 'Double Cluster, California Nebula, Algol variable star', 'Contains the famous variable star Algol and rich star fields'),
            ('Pisces', 'Psc', 889.4, 'Kullat Nunu', 'Two fish tied together', 'Northern autumn', 'M74 galaxy, Van Maanen\'s Star', 'Large but faint zodiacal constellation'),
            ('Sagittarius', 'Sgr', 867.4, 'Kaus Australis', 'Archer aiming at Scorpius', 'Southern summer', 'Galactic center, Lagoon Nebula, Trifid Nebula', 'Points toward galactic center, rich in nebulae and star clusters'),
            ('Scorpius', 'Sco', 496.8, 'Antares', 'Scorpion that killed Orion', 'Southern summer', 'Antares (15th brightest star), Butterfly Cluster', 'Distinctive scorpion shape with red supergiant Antares'),
            ('Taurus', 'Tau', 797.2, 'Aldebaran', 'Bull charging at Orion', 'Northern winter', 'Pleiades, Hyades, Aldebaran, Crab Nebula', 'Contains two of the most famous star clusters'),
            ('Ursa Major', 'UMa', 1279.7, 'Alioth', 'Great Bear, also Big Dipper', 'Northern circumpolar', 'Big Dipper asterism, M81, M82 galaxies, Owl Nebula', 'Third largest constellation, contains the famous Big Dipper'),
            ('Ursa Minor', 'UMi', 255.9, 'Polaris', 'Little Bear, contains North Star', 'Northern circumpolar', 'Polaris (North Star), Little Dipper asterism', 'Contains Polaris, the current north pole star'),
            ('Virgo', 'Vir', 1294.4, 'Spica', 'Maiden holding wheat sheaf', 'Northern spring', 'Spica (16th brightest star), Virgo Cluster, M87 galaxy', 'Largest zodiacal constellation, contains massive galaxy cluster'),
            ('Crux', 'Cru', 68.4, 'Acrux', 'Southern Cross', 'Southern hemisphere', 'Jewel Box Cluster, Coalsack Nebula', 'Smallest constellation, prominent southern navigation aid'),
            ('Vela', 'Vel', 499.6, 'Gamma Velorum', 'Sails of Argo ship', 'Southern hemisphere', 'Vela Supernova Remnant, IC 2391', 'Part of the ancient Argo Navis constellation'),
            ('Carina', 'Car', 494.2, 'Canopus', 'Keel of Argo ship', 'Southern hemisphere', 'Canopus (2nd brightest star), Eta Carinae Nebula', 'Contains Canopus and the spectacular Eta Carinae Nebula')
        ]
    
    def _get_exoplanets_data(self) -> List[Tuple]:
        """Get comprehensive exoplanet data for database population."""
        return [
            # name, host_star, discovery_year, discovery_method, distance_ly, mass_earth, radius_earth, orbital_period_days, equilibrium_temp_k, habitable_zone, atmosphere, description
            ('Proxima Centauri b', 'Proxima Centauri', 2016, 'Radial velocity', 4.24, 1.17, 1.1, 11.2, 234, True, 'Unknown', 'Closest known exoplanet to Earth, potentially habitable'),
            ('Kepler-452b', 'Kepler-452', 2015, 'Transit', 1402, 5.0, 1.6, 384.8, 265, True, 'Unknown', 'Earth\'s cousin in the habitable zone of a Sun-like star'),
            ('TRAPPIST-1e', 'TRAPPIST-1', 2017, 'Transit', 39.5, 0.77, 0.92, 6.1, 251, True, 'Thin', 'One of seven Earth-sized planets in TRAPPIST-1 system'),
            ('TRAPPIST-1f', 'TRAPPIST-1', 2017, 'Transit', 39.5, 1.04, 1.05, 9.2, 219, True, 'Thin', 'Another potentially habitable TRAPPIST-1 planet'),
            ('TRAPPIST-1g', 'TRAPPIST-1', 2017, 'Transit', 39.5, 1.32, 1.13, 12.4, 199, True, 'Thin', 'Outermost potentially habitable TRAPPIST-1 planet'),
            ('K2-18b', 'K2-18', 2015, 'Transit', 124, 8.6, 2.3, 33.0, 265, True, 'Water vapor detected', 'Super-Earth with confirmed water vapor in atmosphere'),
            ('TOI-715b', 'TOI-715', 2024, 'Transit', 137, 3.02, 1.55, 19.3, 280, True, 'Unknown', 'Recently discovered super-Earth in habitable zone'),
            ('Gliese 581g', 'Gliese 581', 2010, 'Radial velocity', 20.4, 3.1, 1.5, 36.6, 228, True, 'Unknown', 'Controversial potentially habitable super-Earth'),
            ('Kepler-186f', 'Kepler-186', 2014, 'Transit', 582, 1.4, 1.1, 129.9, 188, True, 'Unknown', 'First Earth-size planet found in habitable zone'),
            ('Kepler-442b', 'Kepler-442', 2015, 'Transit', 1206, 2.3, 1.3, 112.3, 233, True, 'Unknown', 'Super-Earth with high Earth Similarity Index'),
            ('Wolf 1061c', 'Wolf 1061', 2015, 'Radial velocity', 13.8, 4.3, 1.6, 17.9, 223, True, 'Unknown', 'Nearby potentially habitable super-Earth'),
            ('HD 40307g', 'HD 40307', 2012, 'Radial velocity', 42, 7.1, 2.0, 197.8, 227, True, 'Unknown', 'Super-Earth in the habitable zone of orange dwarf'),
            ('Kepler-22b', 'Kepler-22', 2011, 'Transit', 620, 36, 2.4, 289.9, 262, True, 'Unknown', 'First confirmed planet in habitable zone by Kepler'),
            ('51 Eridani b', '51 Eridani', 2014, 'Direct imaging', 28.1, 760, 12.0, 11000, 700, False, 'Methane', 'Young Jupiter-like planet imaged directly'),
            ('HD 209458b', 'HD 209458', 1999, 'Transit', 159, 220, 1.4, 3.5, 1130, False, 'Hydrogen, sodium', 'First exoplanet with detected atmosphere'),
            ('WASP-12b', 'WASP-12', 2008, 'Transit', 871, 450, 1.8, 1.1, 2516, False, 'Water vapor, carbon monoxide', 'Ultra-hot Jupiter being consumed by its star'),
            ('55 Cancri e', '55 Cancri A', 2004, 'Radial velocity', 41, 8.6, 2.0, 0.7, 2573, False, 'Hydrogen, helium', 'Super-Earth with possible lava surface'),
            ('GJ 1214b', 'GJ 1214', 2009, 'Transit', 48, 6.6, 2.7, 1.6, 555, False, 'Water vapor or haze', 'Mini-Neptune with thick atmosphere'),
            ('Kepler-16b', 'Kepler-16', 2011, 'Transit', 245, 105, 8.5, 228.8, 200, False, 'Unknown', 'First confirmed circumbinary planet (Tatooine-like)'),
            ('PSR B1257+12 b', 'PSR B1257+12', 1992, 'Pulsar timing', 2300, 0.02, 0.5, 25.3, 0, False, 'None', 'First confirmed exoplanet, orbiting a pulsar'),
            ('CoRoT-7b', 'CoRoT-7', 2009, 'Transit', 489, 4.8, 1.6, 0.9, 2573, False, 'Rocky surface', 'First confirmed rocky exoplanet'),
            ('Kepler-438b', 'Kepler-438', 2015, 'Transit', 473, 1.4, 1.1, 35.2, 276, True, 'Unknown', 'Earth-size planet with 70% chance of being rocky'),
            ('Kepler-296e', 'Kepler-296', 2014, 'Transit', 1042, 1.5, 1.8, 34.1, 269, True, 'Unknown', 'Super-Earth in multi-planet system'),
            ('LHS 1140b', 'LHS 1140', 2017, 'Transit', 41, 6.6, 1.4, 24.7, 230, True, 'Thin or none', 'Dense rocky planet ideal for atmospheric studies'),
            ('Ross 128b', 'Ross 128', 2017, 'Radial velocity', 11.0, 1.4, 1.1, 9.9, 269, True, 'Unknown', 'Temperate planet around quiet red dwarf'),
            ('Tau Ceti e', 'Tau Ceti', 2012, 'Radial velocity', 11.9, 4.3, 1.6, 168.1, 205, True, 'Unknown', 'Super-Earth around nearby Sun-like star'),
            ('Gliese 667Cc', 'Gliese 667C', 2011, 'Radial velocity', 23.6, 3.8, 1.5, 28.1, 277, True, 'Unknown', 'Super-Earth in triple star system'),
            ('Kepler-62f', 'Kepler-62', 2013, 'Transit', 1200, 2.8, 1.4, 267.3, 208, True, 'Unknown', 'Super-Earth in five-planet system'),
            ('TOI-849b', 'TOI-849', 2020, 'Transit', 730, 40.8, 3.4, 0.8, 1800, False, 'Stripped core', 'Exposed planetary core, densest Neptune-size planet'),
            ('WASP-76b', 'WASP-76', 2013, 'Transit', 640, 92, 1.8, 1.8, 2227, False, 'Iron rain', 'Ultra-hot Jupiter with iron precipitation')
        ]
    
    def _get_space_history_data(self) -> List[Tuple]:
        """Get comprehensive space exploration history data."""
        return [
            # event_name, date, agency, mission_type, significance, participants, outcome, description
            ('Sputnik 1 Launch', '1957-10-04', 'Soviet Union', 'Satellite', 'First artificial satellite', 'Sergei Korolev team', 'Success', 'Marked beginning of Space Age and triggered Space Race'),
            ('Yuri Gagarin First Human in Space', '1961-04-12', 'Soviet Union', 'Human spaceflight', 'First human in space', 'Yuri Gagarin', 'Success', 'First human to orbit Earth, proving human spaceflight possible'),
            ('Apollo 11 Moon Landing', '1969-07-20', 'NASA', 'Lunar landing', 'First humans on Moon', 'Neil Armstrong, Buzz Aldrin, Michael Collins', 'Success', 'First human lunar landing, fulfilling Kennedy\'s goal'),
            ('Voyager 1 Launch', '1977-09-05', 'NASA', 'Deep space probe', 'Interstellar exploration', 'NASA JPL team', 'Success', 'First human-made object to enter interstellar space'),
            ('Space Shuttle First Flight', '1981-04-12', 'NASA', 'Reusable spacecraft', 'Reusable space transportation', 'John Young, Robert Crippen', 'Success', 'First reusable orbital spacecraft, revolutionized space access'),
            ('Hubble Space Telescope Launch', '1990-04-24', 'NASA/ESA', 'Space telescope', 'Deep space observation', 'Discovery crew', 'Success', 'Transformed our understanding of the universe'),
            ('International Space Station First Module', '1998-11-20', 'International', 'Space station', 'Permanent human presence', 'Multiple nations', 'Success', 'Largest human-made object in space, continuous habitation since 2000'),
            ('Mars Pathfinder Landing', '1997-07-04', 'NASA', 'Mars exploration', 'First Mars rover', 'NASA JPL team', 'Success', 'First successful Mars rover mission, proved concept'),
            ('SpaceX Falcon Heavy First Flight', '2018-02-06', 'SpaceX', 'Heavy lift rocket', 'Commercial heavy lift', 'SpaceX team', 'Success', 'Most powerful operational rocket, commercial space milestone'),
            ('James Webb Space Telescope Launch', '2021-12-25', 'NASA/ESA/CSA', 'Space telescope', 'Infrared astronomy', 'International team', 'Success', 'Most powerful space telescope ever built, successor to Hubble'),
            ('Perseverance Mars Landing', '2021-02-18', 'NASA', 'Mars exploration', 'Search for ancient life', 'NASA JPL team', 'Success', 'Most advanced Mars rover, includes Ingenuity helicopter'),
            ('Chang\'e 4 Far Side Landing', '2019-01-03', 'CNSA', 'Lunar exploration', 'First far side landing', 'Chinese space team', 'Success', 'First soft landing on Moon\'s far side'),
            ('Parker Solar Probe Launch', '2018-08-12', 'NASA', 'Solar exploration', 'Closest approach to Sun', 'NASA team', 'Success', 'Fastest human-made object, studying solar corona'),
            ('New Horizons Pluto Flyby', '2015-07-14', 'NASA', 'Outer planet exploration', 'First Pluto close-up', 'NASA team', 'Success', 'Revealed Pluto\'s complex geology and atmosphere'),
            ('Cassini Saturn Arrival', '2004-07-01', 'NASA/ESA', 'Outer planet exploration', 'Saturn system study', 'International team', 'Success', '13-year mission revealed Saturn\'s moons and rings in detail'),
            ('SpaceX Dragon First Crewed Flight', '2020-05-30', 'SpaceX/NASA', 'Commercial crew', 'Commercial human spaceflight', 'Doug Hurley, Bob Behnken', 'Success', 'First commercial crew mission to ISS'),
            ('Artemis 1 Launch', '2022-11-16', 'NASA', 'Lunar program', 'Return to Moon preparation', 'Uncrewed test', 'Success', 'First step in returning humans to Moon'),
            ('DART Asteroid Impact', '2022-09-26', 'NASA', 'Planetary defense', 'Asteroid deflection test', 'NASA team', 'Success', 'First successful asteroid deflection mission'),
            ('BepiColombo Mercury Launch', '2018-10-20', 'ESA/JAXA', 'Mercury exploration', 'Mercury orbit study', 'European/Japanese team', 'Success', 'Joint mission to study Mercury\'s mysteries'),
            ('Ingenuity Mars Helicopter', '2021-04-19', 'NASA', 'Mars exploration', 'First powered flight on Mars', 'NASA JPL team', 'Success', 'First helicopter to fly on another planet')
        ]
    
    def _get_cosmology_data(self) -> List[Tuple]:
        """Get comprehensive cosmology data for database population."""
        return [
            # concept_name, category, value_measurement, uncertainty, discovery_date, evidence, implications, description
            ('Hubble Constant', 'Cosmic Parameters', '70 km/s/Mpc', '±2.2', '1929', 'Type Ia supernovae, Cepheid variables', 'Universe expansion rate', 'Rate of cosmic expansion, fundamental cosmological parameter'),
            ('Dark Matter', 'Cosmic Components', '26.8% of universe', '±1.1%', '1933', 'Galaxy rotation curves, gravitational lensing', 'Invisible matter dominates universe', 'Unknown form of matter that interacts gravitationally but not electromagnetically'),
            ('Dark Energy', 'Cosmic Components', '68.3% of universe', '±1.2%', '1998', 'Type Ia supernovae observations', 'Accelerating cosmic expansion', 'Mysterious energy causing accelerated expansion of universe'),
            ('Cosmic Microwave Background', 'Early Universe', '2.725 K', '±0.002 K', '1965', 'COBE, WMAP, Planck satellites', 'Big Bang afterglow', 'Relic radiation from early universe, provides cosmic baby picture'),
            ('Age of Universe', 'Cosmic Parameters', '13.8 billion years', '±0.02 Gyr', '2013', 'CMB analysis, stellar ages', 'Time since Big Bang', 'Fundamental age of cosmos determined from multiple observations'),
            ('Observable Universe Diameter', 'Cosmic Scale', '93 billion light-years', 'Theoretical calculation', '2003', 'Light travel time + expansion', 'Limit of observable cosmos', 'Maximum distance we can observe due to finite light speed and cosmic age'),
            ('Critical Density', 'Cosmic Parameters', '9.47×10^-27 kg/m³', 'Theoretical', '1922', 'General relativity predictions', 'Flat universe geometry', 'Density required for flat spacetime geometry'),
            ('Baryon Acoustic Oscillations', 'Large Scale Structure', '150 Mpc scale', '±2%', '2005', 'Galaxy surveys', 'Standard ruler for cosmos', 'Sound waves from early universe frozen into matter distribution'),
            ('Inflation Theory', 'Early Universe', 'Exponential expansion', 'Theoretical', '1980', 'CMB uniformity, flatness', 'Solves horizon problem', 'Rapid expansion in first fraction of second after Big Bang'),
            ('Big Bang Nucleosynthesis', 'Early Universe', 'First 20 minutes', 'Theoretical + observational', '1948', 'Light element abundances', 'Origin of hydrogen, helium', 'Formation of lightest elements in early hot universe'),
            ('Cosmic Web', 'Large Scale Structure', 'Filamentary structure', 'Observational', '1980s', 'Galaxy surveys, simulations', 'Universe architecture', 'Largest scale structure with filaments and voids'),
            ('Redshift', 'Observational Cosmology', 'z = Δλ/λ', 'Measurement dependent', '1912', 'Spectroscopic observations', 'Distance and recession', 'Stretching of light due to cosmic expansion'),
            ('Planck Era', 'Quantum Cosmology', '10^-43 seconds', 'Theoretical limit', '1899', 'Quantum gravity theory', 'Physics breakdown', 'Earliest moment when known physics applies'),
            ('Multiverse Theory', 'Theoretical Cosmology', 'Infinite universes', 'Speculative', '1957', 'Quantum mechanics, inflation', 'Reality beyond observation', 'Hypothetical ensemble of multiple universes'),
            ('Heat Death', 'Cosmic Fate', '10^100+ years', 'Theoretical projection', '1850s', 'Thermodynamics', 'Ultimate cosmic fate', 'Maximum entropy state as universe\'s final destiny')
        ]
    
    def _get_astrobiology_data(self) -> List[Tuple]:
        """Get comprehensive astrobiology data for database population."""
        return [
            # topic_name, category, location, evidence_level, detection_method, significance, research_status, description
            ('Extremophiles on Earth', 'Life Detection', 'Earth extreme environments', 'Confirmed', 'Direct sampling', 'Expands habitable zone concepts', 'Ongoing research', 'Organisms thriving in extreme conditions, models for alien life'),
            ('Mars Methane Detection', 'Biosignatures', 'Mars atmosphere', 'Controversial', 'Spectroscopy', 'Possible biological activity', 'Under investigation', 'Seasonal methane variations could indicate microbial life'),
            ('Europa Subsurface Ocean', 'Habitable Environments', 'Jupiter\'s moon Europa', 'Strong evidence', 'Magnetic field analysis', 'Potential habitat for life', 'Mission planning', 'Liquid water ocean beneath ice shell, twice Earth\'s ocean volume'),
            ('Enceladus Hydrothermal Vents', 'Habitable Environments', 'Saturn\'s moon Enceladus', 'Confirmed', 'Cassini observations', 'Active hydrothermal system', 'Confirmed discovery', 'Subsurface ocean with hydrothermal activity, organic compounds detected'),
            ('Titan Organic Chemistry', 'Prebiotic Chemistry', 'Saturn\'s moon Titan', 'Confirmed', 'Cassini-Huygens mission', 'Complex organic synthesis', 'Ongoing analysis', 'Methane cycle creates complex organic molecules in thick atmosphere'),
            ('Phosphine in Venus Atmosphere', 'Biosignatures', 'Venus atmosphere', 'Disputed', 'Radio telescope detection', 'Possible biological origin', 'Controversial', 'Potential biosignature gas detected in Venus clouds, heavily debated'),
            ('Panspermia Hypothesis', 'Origin of Life', 'Interplanetary/interstellar', 'Theoretical', 'Meteorite analysis', 'Life distribution mechanism', 'Speculative research', 'Theory that life spreads between planets via meteoroids or comets'),
            ('SETI Radio Searches', 'Technosignatures', 'Galactic', 'No confirmed detection', 'Radio telescopes', 'Search for intelligence', 'Ongoing monitoring', 'Systematic search for artificial radio signals from extraterrestrial civilizations'),
            ('Kepler Habitable Zone Planets', 'Exoplanet Habitability', 'Various star systems', 'Statistical analysis', 'Transit photometry', 'Frequency of Earth-like worlds', 'Catalog analysis', 'Thousands of planets in habitable zones around other stars'),
            ('Amino Acids in Meteorites', 'Prebiotic Chemistry', 'Carbonaceous chondrites', 'Confirmed', 'Mass spectrometry', 'Organic compounds from space', 'Established science', 'Complex organic molecules including amino acids found in meteorites'),
            ('Tardigrades in Space', 'Astrobiology Experiments', 'Low Earth orbit', 'Confirmed survival', 'Space exposure experiments', 'Life survival in space', 'Experimental confirmation', 'Microscopic animals survive vacuum and radiation of space'),
            ('Biosignature Gases', 'Detection Methods', 'Exoplanet atmospheres', 'Theoretical framework', 'Atmospheric spectroscopy', 'Remote life detection', 'Method development', 'Gases like oxygen and methane that could indicate biological activity'),
            ('Hydrothermal Vent Life', 'Extreme Environments', 'Earth\'s ocean floors', 'Confirmed', 'Deep sea exploration', 'Chemosynthetic ecosystems', 'Well-established', 'Life thriving on chemical energy without sunlight, model for alien biospheres'),
            ('Mars Subsurface Water', 'Habitable Environments', 'Mars subsurface', 'Strong evidence', 'Radar, orbital imaging', 'Current liquid water habitat', 'Recent discoveries', 'Liquid water lakes and aquifers beneath Martian surface'),
            ('Goldilocks Zone Calculation', 'Habitability Theory', 'Stellar systems', 'Theoretical model', 'Stellar physics modeling', 'Habitable planet prediction', 'Refined calculations', 'Orbital distance range where liquid water can exist on planet surface'),
            ('Astrobiology Missions', 'Space Exploration', 'Solar system', 'Mission planning', 'Robotic exploration', 'Direct life search', 'Multiple missions planned', 'Dedicated missions to search for life on Mars, Europa, Enceladus'),
            ('Fermi Paradox', 'SETI Theory', 'Galaxy-wide', 'Theoretical problem', 'Statistical analysis', 'Great Silence mystery', 'Ongoing debate', 'Contradiction between high probability of alien life and lack of contact'),
            ('Chirality in Space', 'Prebiotic Chemistry', 'Interstellar medium', 'Observational evidence', 'Polarimetry', 'Molecular handedness origin', 'Research frontier', 'Preference for left-handed amino acids may originate in space'),
            ('Subsurface Biospheres', 'Deep Life', 'Planetary interiors', 'Earth confirmed', 'Deep drilling', 'Hidden life reservoirs', 'Expanding research', 'Vast ecosystems living kilometers below surface, implications for other worlds'),
            ('Atmospheric Escape', 'Planetary Evolution', 'Rocky planets', 'Observational/theoretical', 'Atmospheric modeling', 'Habitability loss mechanism', 'Active research', 'Process by which planets lose their atmospheres and water to space')
        ]
    
    def _get_space_medicine_data(self) -> List[Tuple]:
        """Get comprehensive space medicine data for database population."""
        return [
            # condition_name, category, symptoms, causes, duration, countermeasures, severity, description
            ('Space Motion Sickness', 'Adaptation Syndrome', 'Nausea, vomiting, disorientation', 'Microgravity adaptation', '2-4 days', 'Anti-nausea medication, adaptation training', 'Moderate', 'Common condition affecting 60-80% of astronauts during first days in space'),
            ('Bone Loss', 'Musculoskeletal', 'Decreased bone density, fracture risk', 'Lack of weight-bearing exercise', 'Months to years', 'ARED exercise, bisphosphonates', 'High', 'Astronauts lose 1-2% bone mass per month in microgravity'),
            ('Muscle Atrophy', 'Musculoskeletal', 'Muscle weakness, mass reduction', 'Disuse in microgravity', 'Weeks to months', 'Daily exercise regimen, resistance training', 'High', 'Significant muscle loss without countermeasures, especially in legs and back'),
            ('Cardiovascular Deconditioning', 'Cardiovascular', 'Reduced exercise capacity, orthostatic intolerance', 'Fluid shifts, reduced workload', 'Days to weeks', 'Exercise protocols, fluid loading', 'Moderate', 'Heart becomes deconditioned due to reduced gravitational stress'),
            ('Radiation Exposure', 'Radiation Effects', 'Increased cancer risk, acute radiation syndrome', 'Cosmic rays, solar particles', 'Cumulative over mission', 'Shielding, mission duration limits', 'High', 'Major concern for deep space missions beyond Earth\'s magnetosphere'),
            ('Vision Impairment', 'Neuro-ocular', 'Blurred vision, hyperopic shift', 'Intracranial pressure changes', 'Months', 'Under investigation', 'Moderate', 'SANS (Spaceflight Associated Neuro-ocular Syndrome) affects many astronauts'),
            ('Kidney Stones', 'Renal', 'Pain, urinary obstruction', 'Bone demineralization, dehydration', 'Variable', 'Hydration, dietary modifications', 'Moderate', 'Increased risk due to calcium release from bones and fluid shifts'),
            ('Sleep Disorders', 'Neurological', 'Insomnia, circadian disruption', '16 sunrises/sunsets per day', 'Throughout mission', 'Light therapy, sleep hygiene, melatonin', 'Moderate', 'Disrupted sleep-wake cycles due to rapid day-night transitions'),
            ('Psychological Stress', 'Behavioral Health', 'Anxiety, depression, interpersonal conflict', 'Isolation, confinement, workload', 'Variable', 'Psychological support, recreation time', 'Variable', 'Mental health challenges from extreme environment and social isolation'),
            ('Fluid Shifts', 'Physiological Adaptation', 'Facial puffiness, nasal congestion', 'Absence of gravity', 'First days to weeks', 'Lower body negative pressure', 'Mild', 'Body fluids redistribute toward head in microgravity'),
            ('Immune System Suppression', 'Immunological', 'Increased infection susceptibility', 'Stress, radiation, microgravity', 'Throughout mission', 'Nutrition, exercise, stress management', 'Moderate', 'Weakened immune response increases risk of infections'),
            ('Vestibular Dysfunction', 'Sensory', 'Spatial disorientation, balance problems', 'Otolith organ adaptation', 'Days to weeks', 'Adaptation training, visual cues', 'Moderate', 'Inner ear changes cause balance and orientation difficulties'),
            ('Wound Healing Impairment', 'Tissue Repair', 'Slower healing, altered scarring', 'Microgravity effects on cells', 'Variable', 'Proper wound care, nutrition', 'Moderate', 'Wounds heal more slowly and differently in microgravity environment'),
            ('Medication Effectiveness Changes', 'Pharmacological', 'Altered drug response', 'Changed metabolism, distribution', 'Variable', 'Dosage adjustments, monitoring', 'Variable', 'Medications may work differently in space due to physiological changes'),
            ('Decompression Sickness', 'Pressure-related', 'Joint pain, neurological symptoms', 'Rapid pressure changes', 'Hours', 'Gradual decompression, oxygen pre-breathing', 'High', 'Risk during EVAs or emergency decompression events'),
            ('Thermal Regulation Issues', 'Thermoregulation', 'Overheating or cooling problems', 'Altered heat transfer in microgravity', 'Variable', 'Environmental controls, proper clothing', 'Moderate', 'Body temperature regulation works differently without convection'),
            ('Nutritional Deficiencies', 'Metabolic', 'Various symptoms depending on deficiency', 'Limited food variety, absorption changes', 'Weeks to months', 'Supplementation, balanced diet', 'Moderate', 'Risk of vitamin and mineral deficiencies on long missions'),
            ('Crew Compatibility Issues', 'Behavioral Health', 'Interpersonal conflict, team dysfunction', 'Stress, personality conflicts, cultural differences', 'Variable', 'Team training, conflict resolution', 'Variable', 'Importance of crew selection and team dynamics for mission success'),
            ('Emergency Medical Events', 'Acute Care', 'Various depending on condition', 'Accidents, acute illness', 'Acute', 'Medical training, telemedicine, equipment', 'High', 'Challenge of providing medical care without immediate evacuation capability'),
            ('Readaptation Syndrome', 'Return to Earth', 'Dizziness, weakness, balance problems', 'Readjustment to gravity', 'Days to weeks', 'Gradual activity increase, physical therapy', 'Moderate', 'Difficulty readjusting to Earth gravity after long-duration spaceflight')
        ]

    def shutdown(self):
        """Shutdown the knowledge base."""
        self.logger.info("Knowledge base shutting down")
        self.cache.clear()
