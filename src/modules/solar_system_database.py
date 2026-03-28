"""
Comprehensive Solar System Database for Space AI Assistant.
Complete encyclopedia of planets, moons, asteroids, comets, and other solar system objects.
"""

import sqlite3
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

class SolarSystemDatabase:
    """Comprehensive database of all solar system objects."""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("Solar_System_Database")
        
        # Database setup
        self.db_path = config.knowledge_dir / "solar_system_database.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize solar system database
        self._initialize_database()
        self._populate_data()
        
    def _initialize_database(self):
        """Initialize solar system database tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Planets table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS planets (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        type TEXT,
                        distance_from_sun_au REAL,
                        distance_from_sun_km REAL,
                        orbital_period_days REAL,
                        orbital_period_years REAL,
                        rotation_period_hours REAL,
                        diameter_km REAL,
                        mass_kg REAL,
                        mass_earth_ratio REAL,
                        density_g_cm3 REAL,
                        surface_gravity_ms2 REAL,
                        escape_velocity_ms REAL,
                        surface_temperature_min_k REAL,
                        surface_temperature_max_k REAL,
                        surface_temperature_avg_k REAL,
                        atmosphere_composition TEXT,
                        atmosphere_pressure_kpa REAL,
                        magnetic_field BOOLEAN DEFAULT 0,
                        ring_system BOOLEAN DEFAULT 0,
                        moon_count INTEGER DEFAULT 0,
                        discovery_date TEXT,
                        discovered_by TEXT,
                        notable_features TEXT,
                        description TEXT
                    )
                ''')
                
                # Moons table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS moons (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        parent_planet TEXT NOT NULL,
                        diameter_km REAL,
                        mass_kg REAL,
                        orbital_distance_km REAL,
                        orbital_period_days REAL,
                        rotation_period_hours REAL,
                        surface_gravity_ms2 REAL,
                        surface_temperature_k REAL,
                        atmosphere TEXT,
                        composition TEXT,
                        discovery_date TEXT,
                        discovered_by TEXT,
                        notable_features TEXT,
                        description TEXT,
                        FOREIGN KEY (parent_planet) REFERENCES planets (name)
                    )
                ''')
                
                # Asteroids table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS asteroids (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        designation TEXT,
                        type TEXT,
                        diameter_km REAL,
                        mass_kg REAL,
                        orbital_distance_au REAL,
                        orbital_period_years REAL,
                        rotation_period_hours REAL,
                        composition TEXT,
                        albedo REAL,
                        discovery_date TEXT,
                        discovered_by TEXT,
                        notable_features TEXT,
                        description TEXT
                    )
                ''')
                
                # Comets table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS comets (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        designation TEXT,
                        type TEXT,
                        nucleus_diameter_km REAL,
                        orbital_period_years REAL,
                        perihelion_au REAL,
                        aphelion_au REAL,
                        eccentricity REAL,
                        inclination_deg REAL,
                        last_perihelion TEXT,
                        next_perihelion TEXT,
                        composition TEXT,
                        discovery_date TEXT,
                        discovered_by TEXT,
                        notable_features TEXT,
                        description TEXT
                    )
                ''')
                
                # Dwarf planets table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS dwarf_planets (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        location TEXT,
                        diameter_km REAL,
                        mass_kg REAL,
                        orbital_distance_au REAL,
                        orbital_period_years REAL,
                        rotation_period_hours REAL,
                        surface_gravity_ms2 REAL,
                        surface_temperature_k REAL,
                        atmosphere TEXT,
                        moon_count INTEGER DEFAULT 0,
                        discovery_date TEXT,
                        discovered_by TEXT,
                        notable_features TEXT,
                        description TEXT
                    )
                ''')
                
                conn.commit()
                self.logger.info("Solar system database initialized")
                
        except Exception as e:
            self.logger.error(f"Solar system database initialization failed: {e}")
            raise
    
    def _populate_data(self):
        """Populate solar system database with comprehensive data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if data exists
                cursor.execute("SELECT COUNT(*) FROM planets")
                if cursor.fetchone()[0] > 0:
                    return
                
                self._populate_planets(cursor)
                self._populate_moons(cursor)
                self._populate_asteroids(cursor)
                self._populate_comets(cursor)
                self._populate_dwarf_planets(cursor)
                
                conn.commit()
                self.logger.info("Solar system data populated")
                
        except Exception as e:
            self.logger.error(f"Solar system data population failed: {e}")
    
    def _populate_planets(self, cursor):
        """Populate planets data."""
        planets = [
            # name, type, dist_au, dist_km, orb_period_days, orb_period_years, rot_period_hrs, diameter_km, mass_kg, mass_earth, density, gravity, escape_vel, temp_min, temp_max, temp_avg, atmosphere, pressure, magnetic, rings, moons, discovery, discoverer, features, description
            ('Mercury', 'Terrestrial', 0.387, 57910000, 87.97, 0.241, 1407.6, 4879, 3.3011e23, 0.055, 5.427, 3.7, 4250, 100, 700, 340, 'Extremely thin (oxygen, sodium, hydrogen, helium, potassium)', 0.000000001, 1, 0, 0, 'Ancient times', 'Ancient civilizations', 'Extreme temperature variations, heavily cratered surface, no atmosphere', 'Smallest planet, closest to Sun with extreme temperature variations'),
            
            ('Venus', 'Terrestrial', 0.723, 108200000, 224.7, 0.615, -5832.5, 12104, 4.8675e24, 0.815, 5.243, 8.87, 10360, 737, 737, 737, 'Dense carbon dioxide (96.5%), nitrogen (3.5%)', 9200, 0, 0, 0, 'Ancient times', 'Ancient civilizations', 'Hottest planet, retrograde rotation, thick atmosphere, volcanic surface', 'Hottest planet due to extreme greenhouse effect from dense CO2 atmosphere'),
            
            ('Earth', 'Terrestrial', 1.0, 149600000, 365.26, 1.0, 23.93, 12756, 5.972e24, 1.0, 5.514, 9.8, 11180, 184, 330, 288, 'Nitrogen (78%), oxygen (21%), argon (0.93%)', 101.325, 1, 0, 1, 'N/A', 'N/A', 'Only known planet with life, liquid water, protective magnetic field', 'Our home planet, only known world harboring life with liquid water oceans'),
            
            ('Mars', 'Terrestrial', 1.524, 227900000, 686.98, 1.881, 24.62, 6792, 6.4171e23, 0.107, 3.933, 3.71, 5030, 130, 308, 210, 'Carbon dioxide (95.3%), nitrogen (2.7%), argon (1.6%)', 0.636, 0, 0, 2, 'Ancient times', 'Ancient civilizations', 'Polar ice caps, largest volcano in solar system, evidence of ancient water', 'Red planet with evidence of ancient water activity and potential for past life'),
            
            ('Jupiter', 'Gas Giant', 5.204, 778500000, 4332.59, 11.862, 9.93, 142984, 1.8982e27, 317.8, 1.326, 24.79, 59500, 165, 165, 165, 'Hydrogen (89%), helium (10%), traces of methane, ammonia', 0, 1, 1, 95, 'Ancient times', 'Ancient civilizations', 'Great Red Spot, largest planet, strong magnetic field, many moons', 'Largest planet, gas giant with Great Red Spot storm and extensive moon system'),
            
            ('Saturn', 'Gas Giant', 9.582, 1432000000, 10759.22, 29.457, 10.66, 120536, 5.6834e26, 95.2, 0.687, 10.44, 35500, 134, 134, 134, 'Hydrogen (96%), helium (3%), traces of ammonia, methane', 0, 1, 1, 146, 'Ancient times', 'Ancient civilizations', 'Prominent ring system, lowest density planet, hexagonal polar storm', 'Gas giant famous for its spectacular ring system and lowest density of all planets'),
            
            ('Uranus', 'Ice Giant', 19.201, 2867000000, 30688.5, 84.011, -17.24, 51118, 8.6810e25, 14.5, 1.27, 8.69, 21300, 76, 76, 76, 'Hydrogen (83%), helium (15%), methane (2%)', 0, 1, 1, 28, '1781', 'William Herschel', 'Tilted 98 degrees, faint rings, extreme seasons, methane atmosphere', 'Ice giant tilted on its side with extreme 84-year seasons and faint ring system'),
            
            ('Neptune', 'Ice Giant', 30.047, 4515000000, 60182, 164.8, 16.11, 49528, 1.02413e26, 17.1, 1.638, 11.15, 23500, 72, 72, 72, 'Hydrogen (80%), helium (19%), methane (1%)', 0, 1, 1, 16, '1846', 'Urbain Le Verrier, John Couch Adams', 'Strongest winds in solar system, Great Dark Spot, deep blue color', 'Outermost planet with strongest winds in solar system and deep blue methane atmosphere')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO planets 
            (name, type, distance_from_sun_au, distance_from_sun_km, orbital_period_days, 
             orbital_period_years, rotation_period_hours, diameter_km, mass_kg, mass_earth_ratio, 
             density_g_cm3, surface_gravity_ms2, escape_velocity_ms, surface_temperature_min_k, 
             surface_temperature_max_k, surface_temperature_avg_k, atmosphere_composition, 
             atmosphere_pressure_kpa, magnetic_field, ring_system, moon_count, discovery_date, 
             discovered_by, notable_features, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', planets)
    
    def _populate_moons(self, cursor):
        """Populate major moons data."""
        moons = [
            # name, parent_planet, diameter_km, mass_kg, orbital_distance_km, orbital_period_days, rotation_period_hrs, gravity, temp_k, atmosphere, composition, discovery, discoverer, features, description
            ('Moon', 'Earth', 3474, 7.342e22, 384400, 27.32, 655.7, 1.62, 250, 'Extremely thin', 'Rocky silicate', 'Ancient times', 'Ancient civilizations', 'Synchronous rotation, maria and highlands, tidal locking', 'Earth\'s only natural satellite, responsible for tides and stabilizing Earth\'s axial tilt'),
            
            ('Phobos', 'Mars', 22.5, 1.0659e16, 9376, 0.32, 7.6, 0.0057, 233, 'None', 'Carbonaceous rock', '1877', 'Asaph Hall', 'Irregular shape, grooved surface, orbital decay', 'Larger and inner moon of Mars, irregularly shaped and slowly spiraling toward Mars'),
            
            ('Deimos', 'Mars', 12.4, 1.4762e15, 23463, 1.26, 30.3, 0.003, 233, 'None', 'Carbonaceous rock', '1877', 'Asaph Hall', 'Smooth surface, small size, distant orbit', 'Smaller and outer moon of Mars with smooth, dust-covered surface'),
            
            ('Io', 'Jupiter', 3643, 8.932e22, 421700, 1.77, 42.5, 1.796, 130, 'Sulfur dioxide', 'Silicate rock, sulfur', '1610', 'Galileo Galilei', 'Most volcanically active body, sulfur volcanoes, no impact craters', 'Most volcanically active body in solar system with sulfur volcanoes and colorful surface'),
            
            ('Europa', 'Jupiter', 3122, 4.800e22, 671034, 3.55, 85.2, 1.314, 102, 'Thin oxygen', 'Water ice over rocky core', '1610', 'Galileo Galilei', 'Subsurface ocean, smooth ice surface, potential for life', 'Ice-covered moon with subsurface ocean and potential for extraterrestrial life'),
            
            ('Ganymede', 'Jupiter', 5268, 1.482e23, 1070412, 7.15, 171.7, 1.428, 110, 'Thin oxygen', 'Water ice and rock', '1610', 'Galileo Galilei', 'Largest moon in solar system, own magnetic field, subsurface ocean', 'Largest moon in solar system with its own magnetic field and subsurface ocean'),
            
            ('Callisto', 'Jupiter', 4821, 1.076e23, 1882709, 16.69, 400.5, 1.235, 134, 'Thin carbon dioxide', 'Water ice and rock', '1610', 'Galileo Galilei', 'Most cratered body, ancient surface, subsurface ocean', 'Most heavily cratered body in solar system with ancient surface and subsurface ocean'),
            
            ('Titan', 'Saturn', 5150, 1.345e23, 1221830, 15.95, 382.7, 1.352, 94, 'Dense nitrogen with methane', 'Water ice and rock', '1655', 'Christiaan Huygens', 'Dense atmosphere, methane lakes, Earth-like processes', 'Only moon with dense atmosphere and liquid lakes, showing Earth-like geological processes'),
            
            ('Enceladus', 'Saturn', 504, 1.080e20, 238020, 1.37, 32.9, 0.0113, 75, 'Water vapor', 'Water ice', '1789', 'William Herschel', 'Ice geysers, subsurface ocean, smooth south pole', 'Ice moon with geysers erupting from south pole, harboring subsurface ocean'),
            
            ('Mimas', 'Saturn', 396, 3.75e19, 185539, 0.94, 22.6, 0.064, 64, 'None', 'Water ice and rock', '1789', 'William Herschel', 'Large Herschel crater, Death Star appearance', 'Small moon with large crater giving it Death Star-like appearance'),
            
            ('Triton', 'Neptune', 2707, 2.14e22, 354759, -5.88, 141.0, 0.779, 38, 'Thin nitrogen', 'Nitrogen ice and rock', '1846', 'William Lassell', 'Retrograde orbit, nitrogen geysers, captured Kuiper Belt object', 'Largest moon of Neptune with retrograde orbit and nitrogen geysers, likely captured Kuiper Belt object'),
            
            ('Charon', 'Pluto', 1212, 1.586e21, 19591, 6.39, 153.3, 0.288, 53, 'None', 'Water ice and rock', '1978', 'James Christy', 'Tidally locked system, large relative size', 'Largest moon of dwarf planet Pluto, forming tidally locked binary system')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO moons 
            (name, parent_planet, diameter_km, mass_kg, orbital_distance_km, orbital_period_days, 
             rotation_period_hours, surface_gravity_ms2, surface_temperature_k, atmosphere, 
             composition, discovery_date, discovered_by, notable_features, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', moons)
    
    def _populate_asteroids(self, cursor):
        """Populate major asteroids data."""
        asteroids = [
            # name, designation, type, diameter_km, mass_kg, orbital_distance_au, orbital_period_years, rotation_hrs, composition, albedo, discovery, discoverer, features, description
            ('Ceres', '1 Ceres', 'Dwarf Planet/Asteroid', 939, 9.1e20, 2.77, 4.60, 9.07, 'Water ice, carbonates, clay minerals', 0.09, '1801', 'Giuseppe Piazzi', 'Largest asteroid, dwarf planet status, possible subsurface ocean', 'Largest object in asteroid belt, classified as dwarf planet with possible subsurface ocean'),
            
            ('Vesta', '4 Vesta', 'V-type', 525, 2.59e20, 2.36, 3.63, 5.34, 'Basaltic rock, iron-nickel core', 0.42, '1807', 'Heinrich Olbers', 'Differentiated structure, large impact crater, HED meteorites source', 'Second largest asteroid with differentiated structure and source of HED meteorites'),
            
            ('Pallas', '2 Pallas', 'B-type', 512, 2.04e20, 2.77, 4.62, 7.81, 'Carbonaceous chondrite', 0.16, '1802', 'Heinrich Olbers', 'Highly inclined orbit, irregular shape, low density', 'Large asteroid with highly inclined orbit and irregular, heavily cratered surface'),
            
            ('Hygiea', '10 Hygiea', 'C-type', 434, 8.32e19, 3.14, 5.56, 27.6, 'Carbonaceous material', 0.07, '1849', 'Annibale de Gasparis', 'Spherical shape, dark surface, C-type composition', 'Fourth largest asteroid with nearly spherical shape and dark carbonaceous surface'),
            
            ('Eros', '433 Eros', 'S-type', 16.8, 6.69e15, 1.46, 1.76, 5.27, 'Silicate rock, nickel-iron', 0.25, '1898', 'Gustav Witt', 'First asteroid orbited by spacecraft, elongated shape, near-Earth asteroid', 'Near-Earth asteroid first to be orbited and landed on by spacecraft (NEAR Shoemaker)'),
            
            ('Bennu', '101955 Bennu', 'B-type', 0.492, 7.8e10, 1.13, 1.20, 4.29, 'Carbonaceous material, organics', 0.04, '1999', 'LINEAR', 'Sample return target, rubble pile structure, potential Earth impact risk', 'Carbon-rich asteroid targeted by OSIRIS-REx mission for sample return'),
            
            ('Ryugu', '162173 Ryugu', 'C-type', 0.87, 4.5e11, 1.19, 1.30, 7.63, 'Carbonaceous chondrite', 0.05, '1999', 'LINEAR', 'Diamond shape, sample return by Hayabusa2, spinning top structure', 'Diamond-shaped asteroid successfully sampled by Japan\'s Hayabusa2 mission'),
            
            ('Apophis', '99942 Apophis', 'S-type', 0.37, 6.1e10, 0.92, 0.89, 30.4, 'Silicate rock', 0.23, '2004', 'Roy Tucker, David Tholen, Fabrizio Bernardi', 'Potentially hazardous asteroid, close Earth approaches', 'Potentially hazardous asteroid making close approaches to Earth in 2029 and 2036'),
            
            ('Itokawa', '25143 Itokawa', 'S-type', 0.54, 3.51e10, 1.32, 1.52, 12.1, 'Silicate rock, metal', 0.53, '1998', 'LINEAR', 'Rubble pile structure, sample return by Hayabusa, peanut shape', 'Peanut-shaped asteroid first successfully sampled and returned by Japan\'s Hayabusa mission')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO asteroids 
            (name, designation, type, diameter_km, mass_kg, orbital_distance_au, orbital_period_years, 
             rotation_period_hours, composition, albedo, discovery_date, discovered_by, notable_features, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', asteroids)
    
    def _populate_comets(self, cursor):
        """Populate major comets data."""
        comets = [
            # name, designation, type, nucleus_diameter, orbital_period, perihelion, aphelion, eccentricity, inclination, last_perihelion, next_perihelion, composition, discovery, discoverer, features, description
            ('Halley\'s Comet', '1P/Halley', 'Short-period', 15, 75.3, 0.586, 35.08, 0.967, 162.3, '1986-02-09', '2061-07-28', 'Water ice, dust, rocky material', '240 BC', 'Ancient Chinese astronomers', 'Most famous comet, predictable orbit, visible to naked eye', 'Most famous comet with 75-year orbit, last visible in 1986, next appearance in 2061'),
            
            ('Hale-Bopp', 'C/1995 O1', 'Long-period', 40, 2533, 0.914, 371, 0.995, 89.4, '1997-04-01', '4530 AD', 'Water ice, carbon monoxide, dust', '1995', 'Alan Hale, Thomas Bopp', 'Great Comet of 1997, visible for 18 months, dual tails', 'Spectacular comet visible for record 18 months in 1990s with distinctive dual tails'),
            
            ('Hyakutake', 'C/1996 B2', 'Long-period', 4.2, 72000, 0.230, 3410, 0.999, 124.9, '1996-05-01', '74000 AD', 'Water ice, methanol, ethane', '1996', 'Yuji Hyakutake', 'Longest measured comet tail, close Earth approach', 'Comet with longest measured tail (570 million km) and close approach to Earth in 1996'),
            
            ('Shoemaker-Levy 9', 'D/1993 F2', 'Disrupted', 2, 0, 0, 0, 0, 0, 'Fragmented', 'Impacted Jupiter 1994', 'Water ice, rocky material', '1993', 'Carolyn Shoemaker, Eugene Shoemaker, David Levy', 'Fragmented comet, Jupiter impact, string of pearls appearance', 'Fragmented comet that spectacularly impacted Jupiter in 1994, providing insights into comet composition'),
            
            ('Wild 2', '81P/Wild', 'Short-period', 5.5, 5.5, 1.59, 5.77, 0.54, 3.2, '2022-05-27', '2028-01-16', 'Pristine materials, organics', '1960', 'Paul Wild', 'Stardust sample return target, pristine materials', 'Comet targeted by Stardust mission for sample return, containing pristine solar system materials'),
            
            ('Tempel 1', '9P/Tempel', 'Short-period', 7.6, 5.5, 1.50, 4.73, 0.52, 10.5, '2022-07-27', '2028-02-18', 'Water ice, silicates, organics', '1867', 'Wilhelm Tempel', 'Deep Impact target, artificial crater created', 'Target of Deep Impact mission which created artificial crater to study interior composition'),
            
            ('Churyumov-Gerasimenko', '67P/Churyumov-Gerasimenko', 'Short-period', 4.1, 6.4, 1.24, 5.68, 0.64, 7.0, '2021-11-02', '2028-04-21', 'Water ice, organics, complex molecules', '1969', 'Klim Churyumov, Svetlana Gerasimenko', 'Rosetta mission target, rubber duck shape, surface landing', 'Target of ESA\'s Rosetta mission with successful Philae lander, revealing comet structure and composition'),
            
            ('NEOWISE', 'C/2020 F3', 'Long-period', 5, 6800, 0.295, 715, 0.999, 128.9, '2020-07-03', '8820 AD', 'Water ice, dust, sodium', '2020', 'NEOWISE space telescope', 'Brightest comet of 2020s, visible to naked eye', 'Brightest comet of the 2020s, discovered by NEOWISE telescope and visible to naked eye'),
            
            ('Encke', '2P/Encke', 'Short-period', 4.8, 3.3, 0.336, 4.09, 0.85, 11.8, '2023-10-22', '2027-01-17', 'Depleted volatiles, dust', '1818', 'Pierre Méchain (rediscovered by Johann Encke)', 'Shortest known orbital period, parent of Taurid meteors', 'Comet with shortest known orbital period (3.3 years) and parent body of Taurid meteor showers')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO comets 
            (name, designation, type, nucleus_diameter_km, orbital_period_years, perihelion_au, 
             aphelion_au, eccentricity, inclination_deg, last_perihelion, next_perihelion, 
             composition, discovery_date, discovered_by, notable_features, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', comets)
    
    def _populate_dwarf_planets(self, cursor):
        """Populate dwarf planets data."""
        dwarf_planets = [
            # name, location, diameter_km, mass_kg, orbital_distance_au, orbital_period_years, rotation_hrs, gravity, temp_k, atmosphere, moons, discovery, discoverer, features, description
            ('Pluto', 'Kuiper Belt', 2374, 1.309e22, 39.48, 248.1, 153.3, 0.62, 44, 'Thin nitrogen, methane, carbon monoxide', 5, '1930', 'Clyde Tombaugh', 'Former ninth planet, binary system with Charon, heart-shaped feature', 'Former ninth planet, now classified as dwarf planet with complex geology and atmosphere'),
            
            ('Eris', 'Scattered Disk', 2326, 1.66e22, 67.7, 557, 25.9, 0.82, 30, 'Thin nitrogen (seasonal)', 1, '2005', 'Mike Brown, Chad Trujillo, David Rabinowitz', 'Most massive dwarf planet, highly reflective surface, distant orbit', 'Most massive known dwarf planet with highly reflective icy surface in distant orbit'),
            
            ('Makemake', 'Kuiper Belt', 1434, 3.1e21, 45.8, 309.9, 22.5, 0.4, 30, 'Extremely thin (possible)', 1, '2005', 'Mike Brown, Chad Trujillo, David Rabinowitz', 'Reddish surface, methane ice, classical Kuiper Belt object', 'Reddish dwarf planet with methane ice surface in classical Kuiper Belt region'),
            
            ('Haumea', 'Kuiper Belt', 1632, 4.01e21, 43.1, 284.1, 3.9, 0.44, 32, 'None detected', 2, '2004', 'Mike Brown (disputed with José Luis Ortiz)', 'Elongated shape, fast rotation, ring system, crystalline water ice', 'Elongated dwarf planet with fastest rotation and ring system, covered in crystalline water ice'),
            
            ('Ceres', 'Asteroid Belt', 939, 9.1e20, 2.77, 4.60, 9.07, 0.27, 168, 'Thin water vapor', 0, '1801', 'Giuseppe Piazzi', 'Largest asteroid belt object, possible subsurface ocean, bright spots', 'Largest object in asteroid belt with possible subsurface ocean and mysterious bright spots')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO dwarf_planets 
            (name, location, diameter_km, mass_kg, orbital_distance_au, orbital_period_years, 
             rotation_period_hours, surface_gravity_ms2, surface_temperature_k, atmosphere, 
             moon_count, discovery_date, discovered_by, notable_features, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', dwarf_planets)
    
    def query_planet(self, query: str) -> Dict[str, Any]:
        """Query planet information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM planets 
                    WHERE LOWER(name) LIKE LOWER(?) 
                    OR LOWER(type) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    planets = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'planet_info',
                        'planets': planets,
                        'count': len(planets)
                    }
                
                return {'type': 'no_results', 'message': f'No planets found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Planet query failed: {e}")
            return {'type': 'error', 'message': 'Planet query failed'}
    
    def query_moon(self, query: str) -> Dict[str, Any]:
        """Query moon information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM moons 
                    WHERE LOWER(name) LIKE LOWER(?) 
                    OR LOWER(parent_planet) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    moons = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'moon_info',
                        'moons': moons,
                        'count': len(moons)
                    }
                
                return {'type': 'no_results', 'message': f'No moons found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Moon query failed: {e}")
            return {'type': 'error', 'message': 'Moon query failed'}
    
    def format_solar_system_info(self, data: Dict[str, Any]) -> str:
        """Format solar system information for display."""
        if data['type'] == 'planet_info':
            output = []
            for planet in data['planets']:
                info = [f"**{planet['name']} - {planet['type']} Planet**"]
                
                if planet['distance_from_sun_au']:
                    info.append(f"Distance from Sun: {planet['distance_from_sun_au']:.3f} AU ({planet['distance_from_sun_km']:,.0f} km)")
                
                if planet['diameter_km']:
                    info.append(f"Diameter: {planet['diameter_km']:,.0f} km")
                
                if planet['mass_earth_ratio']:
                    info.append(f"Mass: {planet['mass_earth_ratio']:.3f} Earth masses")
                
                if planet['orbital_period_years']:
                    info.append(f"Orbital Period: {planet['orbital_period_years']:.2f} years")
                
                if planet['rotation_period_hours']:
                    info.append(f"Day Length: {planet['rotation_period_hours']:.1f} hours")
                
                if planet['surface_temperature_avg_k']:
                    celsius = planet['surface_temperature_avg_k'] - 273.15
                    info.append(f"Average Temperature: {planet['surface_temperature_avg_k']:.0f} K ({celsius:.0f}°C)")
                
                if planet['atmosphere_composition']:
                    info.append(f"Atmosphere: {planet['atmosphere_composition']}")
                
                if planet['moon_count']:
                    info.append(f"Moons: {planet['moon_count']}")
                
                if planet['notable_features']:
                    info.append(f"Notable Features: {planet['notable_features']}")
                
                if planet['description']:
                    info.append(f"Description: {planet['description']}")
                
                output.append('\n'.join(info))
            
            return '\n\n'.join(output)
        
        elif data['type'] == 'moon_info':
            output = []
            for moon in data['moons']:
                info = [f"**{moon['name']} - Moon of {moon['parent_planet']}**"]
                
                if moon['diameter_km']:
                    info.append(f"Diameter: {moon['diameter_km']:,.0f} km")
                
                if moon['orbital_distance_km']:
                    info.append(f"Distance from Planet: {moon['orbital_distance_km']:,.0f} km")
                
                if moon['orbital_period_days']:
                    info.append(f"Orbital Period: {moon['orbital_period_days']:.2f} days")
                
                if moon['surface_temperature_k']:
                    celsius = moon['surface_temperature_k'] - 273.15
                    info.append(f"Surface Temperature: {moon['surface_temperature_k']:.0f} K ({celsius:.0f}°C)")
                
                if moon['atmosphere']:
                    info.append(f"Atmosphere: {moon['atmosphere']}")
                
                if moon['composition']:
                    info.append(f"Composition: {moon['composition']}")
                
                if moon['discovery_date'] and moon['discovered_by']:
                    info.append(f"Discovered: {moon['discovery_date']} by {moon['discovered_by']}")
                
                if moon['notable_features']:
                    info.append(f"Notable Features: {moon['notable_features']}")
                
                if moon['description']:
                    info.append(f"Description: {moon['description']}")
                
                output.append('\n'.join(info))
            
            return '\n\n'.join(output)
        
        elif data['type'] == 'asteroid_info':
            output = []
            for asteroid in data['asteroids']:
                info = [f"**{asteroid['name']} ({asteroid['designation']}) - {asteroid['type']} Asteroid**"]
                
                if asteroid['diameter_km']:
                    info.append(f"Diameter: {asteroid['diameter_km']:.2f} km")
                
                if asteroid['mass_kg']:
                    info.append(f"Mass: {asteroid['mass_kg']:.2e} kg")
                
                if asteroid['orbital_distance_au']:
                    info.append(f"Orbital Distance: {asteroid['orbital_distance_au']:.3f} AU")
                
                if asteroid['orbital_period_years']:
                    info.append(f"Orbital Period: {asteroid['orbital_period_years']:.2f} years")
                
                if asteroid['rotation_period_hours']:
                    info.append(f"Rotation Period: {asteroid['rotation_period_hours']:.1f} hours")
                
                if asteroid['composition']:
                    info.append(f"Composition: {asteroid['composition']}")
                
                if asteroid['albedo']:
                    info.append(f"Albedo: {asteroid['albedo']:.2f}")
                
                if asteroid['discovery_date'] and asteroid['discovered_by']:
                    info.append(f"Discovered: {asteroid['discovery_date']} by {asteroid['discovered_by']}")
                
                if asteroid['notable_features']:
                    info.append(f"Notable Features: {asteroid['notable_features']}")
                
                if asteroid['description']:
                    info.append(f"Description: {asteroid['description']}")
                
                output.append('\n'.join(info))
            
            return '\n\n'.join(output)
        
        elif data['type'] == 'comet_info':
            output = []
            for comet in data['comets']:
                info = [f"**{comet['name']} ({comet['designation']}) - {comet['type']} Comet**"]
                
                if comet['nucleus_diameter_km']:
                    info.append(f"Nucleus Diameter: {comet['nucleus_diameter_km']:.1f} km")
                
                if comet['orbital_period_years']:
                    info.append(f"Orbital Period: {comet['orbital_period_years']:.1f} years")
                
                if comet['perihelion_au'] and comet['aphelion_au']:
                    info.append(f"Orbit: {comet['perihelion_au']:.3f} - {comet['aphelion_au']:.1f} AU")
                
                if comet['eccentricity']:
                    info.append(f"Eccentricity: {comet['eccentricity']:.3f}")
                
                if comet['inclination_deg']:
                    info.append(f"Inclination: {comet['inclination_deg']:.1f}°")
                
                if comet['last_perihelion']:
                    info.append(f"Last Perihelion: {comet['last_perihelion']}")
                
                if comet['next_perihelion']:
                    info.append(f"Next Perihelion: {comet['next_perihelion']}")
                
                if comet['composition']:
                    info.append(f"Composition: {comet['composition']}")
                
                if comet['discovery_date'] and comet['discovered_by']:
                    info.append(f"Discovered: {comet['discovery_date']} by {comet['discovered_by']}")
                
                if comet['notable_features']:
                    info.append(f"Notable Features: {comet['notable_features']}")
                
                if comet['description']:
                    info.append(f"Description: {comet['description']}")
                
                output.append('\n'.join(info))
            
            return '\n\n'.join(output)
        
        elif data['type'] == 'dwarf_planet_info':
            output = []
            for dwarf_planet in data['dwarf_planets']:
                info = [f"**{dwarf_planet['name']} - Dwarf Planet ({dwarf_planet['location']})**"]
                
                if dwarf_planet['diameter_km']:
                    info.append(f"Diameter: {dwarf_planet['diameter_km']:,.0f} km")
                
                if dwarf_planet['mass_kg']:
                    info.append(f"Mass: {dwarf_planet['mass_kg']:.2e} kg")
                
                if dwarf_planet['orbital_distance_au']:
                    info.append(f"Orbital Distance: {dwarf_planet['orbital_distance_au']:.2f} AU")
                
                if dwarf_planet['orbital_period_years']:
                    info.append(f"Orbital Period: {dwarf_planet['orbital_period_years']:.1f} years")
                
                if dwarf_planet['rotation_period_hours']:
                    info.append(f"Rotation Period: {dwarf_planet['rotation_period_hours']:.1f} hours")
                
                if dwarf_planet['surface_gravity_ms2']:
                    info.append(f"Surface Gravity: {dwarf_planet['surface_gravity_ms2']:.2f} m/s²")
                
                if dwarf_planet['surface_temperature_k']:
                    celsius = dwarf_planet['surface_temperature_k'] - 273.15
                    info.append(f"Surface Temperature: {dwarf_planet['surface_temperature_k']:.0f} K ({celsius:.0f}°C)")
                
                if dwarf_planet['atmosphere']:
                    info.append(f"Atmosphere: {dwarf_planet['atmosphere']}")
                
                if dwarf_planet['moon_count']:
                    info.append(f"Moons: {dwarf_planet['moon_count']}")
                
                if dwarf_planet['discovery_date'] and dwarf_planet['discovered_by']:
                    info.append(f"Discovered: {dwarf_planet['discovery_date']} by {dwarf_planet['discovered_by']}")
                
                if dwarf_planet['notable_features']:
                    info.append(f"Notable Features: {dwarf_planet['notable_features']}")
                
                if dwarf_planet['description']:
                    info.append(f"Description: {dwarf_planet['description']}")
                
                output.append('\n'.join(info))
            
            return '\n\n'.join(output)
        
        elif data['type'] == 'no_results':
            return data['message']
        
        elif data['type'] == 'error':
            return f"Error: {data['message']}"
        
        else:
            return "Unknown solar system data format"
    
    def query_asteroid(self, query: str) -> Dict[str, Any]:
        """Query asteroid information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM asteroids 
                    WHERE LOWER(name) LIKE LOWER(?) 
                    OR LOWER(designation) LIKE LOWER(?)
                    OR LOWER(type) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    asteroids = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'asteroid_info',
                        'asteroids': asteroids,
                        'count': len(asteroids)
                    }
                
                return {'type': 'no_results', 'message': f'No asteroids found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Asteroid query failed: {e}")
            return {'type': 'error', 'message': 'Asteroid query failed'}
    
    def query_comet(self, query: str) -> Dict[str, Any]:
        """Query comet information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM comets 
                    WHERE LOWER(name) LIKE LOWER(?) 
                    OR LOWER(designation) LIKE LOWER(?)
                    OR LOWER(type) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    comets = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'comet_info',
                        'comets': comets,
                        'count': len(comets)
                    }
                
                return {'type': 'no_results', 'message': f'No comets found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Comet query failed: {e}")
            return {'type': 'error', 'message': 'Comet query failed'}
    
    def query_dwarf_planet(self, query: str) -> Dict[str, Any]:
        """Query dwarf planet information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM dwarf_planets 
                    WHERE LOWER(name) LIKE LOWER(?) 
                    OR LOWER(location) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    dwarf_planets = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'dwarf_planet_info',
                        'dwarf_planets': dwarf_planets,
                        'count': len(dwarf_planets)
                    }
                
                return {'type': 'no_results', 'message': f'No dwarf planets found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Dwarf planet query failed: {e}")
            return {'type': 'error', 'message': 'Dwarf planet query failed'}
    
    def query_solar_system(self, query: str) -> Dict[str, Any]:
        """General solar system query that searches across all object types."""
        try:
            # Try each object type
            planet_result = self.query_planet(query)
            if planet_result['type'] != 'no_results':
                return planet_result
            
            moon_result = self.query_moon(query)
            if moon_result['type'] != 'no_results':
                return moon_result
            
            asteroid_result = self.query_asteroid(query)
            if asteroid_result['type'] != 'no_results':
                return asteroid_result
            
            comet_result = self.query_comet(query)
            if comet_result['type'] != 'no_results':
                return comet_result
            
            dwarf_planet_result = self.query_dwarf_planet(query)
            if dwarf_planet_result['type'] != 'no_results':
                return dwarf_planet_result
            
            return {'type': 'no_results', 'message': f'No solar system objects found matching "{query}"'}
            
        except Exception as e:
            self.logger.error(f"Solar system query failed: {e}")
            return {'type': 'error', 'message': 'Solar system query failed'}
