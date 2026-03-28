"""
Stellar Catalog for Space AI Assistant.
Comprehensive database of stars, stellar classifications, and stellar phenomena.
"""

import sqlite3
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

class StellarCatalog:
    """Comprehensive stellar database and classification system."""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("Stellar_Catalog")
        
        # Database setup
        self.db_path = config.knowledge_dir / "stellar_catalog.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize stellar database
        self._initialize_stellar_database()
        self._populate_stellar_data()
        
    def _initialize_stellar_database(self):
        """Initialize stellar catalog database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Stellar classification table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS stellar_classes (
                        id INTEGER PRIMARY KEY,
                        class_type TEXT UNIQUE NOT NULL,
                        temperature_range TEXT,
                        color TEXT,
                        mass_range TEXT,
                        luminosity_range TEXT,
                        lifespan_range TEXT,
                        characteristics TEXT,
                        examples TEXT
                    )
                ''')
                
                # Major stars catalog
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS major_stars (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        common_names TEXT,
                        catalog_designations TEXT,
                        constellation TEXT,
                        stellar_class TEXT,
                        mass_solar REAL,
                        radius_solar REAL,
                        luminosity_solar REAL,
                        temperature_k REAL,
                        distance_ly REAL,
                        apparent_magnitude REAL,
                        absolute_magnitude REAL,
                        coordinates_ra TEXT,
                        coordinates_dec TEXT,
                        metallicity REAL,
                        age_billion_years REAL,
                        rotational_velocity REAL,
                        binary_system BOOLEAN DEFAULT 0,
                        variable_star BOOLEAN DEFAULT 0,
                        exoplanets INTEGER DEFAULT 0,
                        notable_features TEXT,
                        cultural_significance TEXT,
                        description TEXT
                    )
                ''')
                
                conn.commit()
                self.logger.info("Stellar catalog database initialized")
                
        except Exception as e:
            self.logger.error(f"Stellar database initialization failed: {e}")
            raise
    
    def _populate_stellar_data(self):
        """Populate stellar catalog with comprehensive data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if data exists
                cursor.execute("SELECT COUNT(*) FROM stellar_classes")
                if cursor.fetchone()[0] > 0:
                    return
                
                # Populate stellar classifications
                self._populate_stellar_classes(cursor)
                self._populate_major_stars(cursor)
                
                conn.commit()
                self.logger.info("Stellar catalog data populated")
                
        except Exception as e:
            self.logger.error(f"Stellar data population failed: {e}")
    
    def _populate_stellar_classes(self, cursor):
        """Populate stellar classification data."""
        stellar_classes = [
            # class_type, temperature_range, color, mass_range, luminosity_range, lifespan_range, characteristics, examples
            ('O', '30,000-50,000 K', 'Blue', '15-90 M☉', '30,000-1,000,000 L☉', '1-10 million years', 'Very hot, massive, short-lived stars with strong stellar winds', 'Alnitak, Mintaka, Alnilam'),
            ('B', '10,000-30,000 K', 'Blue-white', '2.1-16 M☉', '25-30,000 L☉', '10-100 million years', 'Hot, luminous stars, often found in young star clusters', 'Rigel, Spica, Regulus, Bellatrix'),
            ('A', '7,500-10,000 K', 'White', '1.4-2.1 M☉', '5-25 L☉', '1-3 billion years', 'White stars with strong hydrogen lines in spectrum', 'Sirius, Vega, Altair, Deneb'),
            ('F', '6,000-7,500 K', 'Yellow-white', '1.04-1.4 M☉', '1.5-5 L☉', '3-7 billion years', 'Yellow-white stars, slightly hotter than the Sun', 'Canopus, Procyon, Polaris'),
            ('G', '5,200-6,000 K', 'Yellow', '0.8-1.04 M☉', '0.6-1.5 L☉', '8-12 billion years', 'Yellow stars like our Sun, stable main sequence', 'Sun, Alpha Centauri A, Capella'),
            ('K', '3,700-5,200 K', 'Orange', '0.45-0.8 M☉', '0.08-0.6 L☉', '15-45 billion years', 'Orange stars, cooler than Sun, very stable', 'Arcturus, Aldebaran, Alpha Centauri B'),
            ('M', '2,400-3,700 K', 'Red', '0.08-0.45 M☉', '0.0001-0.08 L☉', '100+ billion years', 'Red dwarf stars, most common type in galaxy', 'Proxima Centauri, Barnard\'s Star, Wolf 359'),
            ('L', '1,300-2,400 K', 'Dark red', '0.013-0.08 M☉', '0.00001-0.0001 L☉', 'Trillions of years', 'Brown dwarfs, failed stars that cannot sustain fusion', 'Gliese 229B, 2MASS J0523-1403'),
            ('T', '500-1,300 K', 'Infrared', '0.001-0.013 M☉', '<0.00001 L☉', 'Trillions of years', 'Cool brown dwarfs with methane absorption', 'Gliese 570D, 2MASS J0415-0935'),
            ('Y', '<500 K', 'Infrared', '<0.001 M☉', '<0.00001 L☉', 'Trillions of years', 'Ultra-cool brown dwarfs, planet-like temperatures', 'WISE J1828+2650, WISE J0304-2705')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO stellar_classes 
            (class_type, temperature_range, color, mass_range, luminosity_range, lifespan_range, characteristics, examples)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', stellar_classes)
    
    def _populate_major_stars(self, cursor):
        """Populate major stars catalog."""
        major_stars = [
            # name, common_names, catalog_designations, constellation, stellar_class, mass_solar, radius_solar, luminosity_solar, temp_k, distance_ly, app_mag, abs_mag, ra, dec, metallicity, age_gy, rot_vel, binary, variable, exoplanets, notable_features, cultural_significance, description
            ('Sirius', 'Dog Star, Alpha Canis Majoris', 'HD 48915, HR 2491', 'Canis Major', 'A1V', 2.063, 1.711, 25.4, 9940, 8.66, -1.46, -16.716, '02h 06m 23.5s', '-16° 42\' 58.0"', 0.5, 0.242, 16, 1, 0, 0, 'Brightest star in night sky, binary system with white dwarf companion', 'Sacred to ancient Egyptians, used for navigation', 'Brightest star in the night sky, binary system with Sirius B white dwarf'),
            
            ('Canopus', 'Alpha Carinae', 'HD 45348, HR 2326', 'Carina', 'A9II', 7.4, 71, 10700, 5310, 310, -0.74, -5.53, '06h 23m 57.1s', '-52° 41\' 44.4"', -0.2, 0.025, 8, 0, 0, 0, 'Second brightest star, used for spacecraft navigation', 'Important for southern hemisphere navigation', 'Second brightest star in night sky, supergiant used for spacecraft navigation'),
            
            ('Arcturus', 'Alpha Boötis', 'HD 124897, HR 5340', 'Boötes', 'K0III', 1.08, 25.4, 170, 4286, 36.7, -0.05, -0.30, '14h 15m 39.7s', '+19° 10\' 56.7"', -0.52, 7.1, 2.4, 0, 0, 0, 'Fastest moving bright star, metal-poor Population II star', 'Bear Guard in mythology, spring star', 'Red giant star, fourth brightest in night sky, notable for high proper motion'),
            
            ('Vega', 'Alpha Lyrae', 'HD 172167, HR 7001', 'Lyra', 'A0V', 2.135, 2.362, 40.12, 9602, 25.04, 0.026, 0.582, '18h 36m 56.3s', '+38° 47\' 01.3"', -0.5, 0.455, 20.5, 0, 0, 0, 'Former pole star, first star photographed and analyzed spectroscopically', 'Part of Summer Triangle, former northern pole star', 'Fifth brightest star, was northern pole star around 12,000 BCE'),
            
            ('Capella', 'Alpha Aurigae', 'HD 34029, HR 1708', 'Auriga', 'G5III+G0III', 2.69, 11.98, 78.7, 4970, 42.9, 0.08, -0.48, '05h 16m 41.4s', '+45° 59\' 52.8"', -0.07, 0.59, 3, 1, 0, 0, 'Complex quadruple star system, sixth brightest star', 'The Goat Star, important in many cultures', 'Sixth brightest star, complex multiple star system in Auriga'),
            
            ('Rigel', 'Beta Orionis', 'HD 34085, HR 1713', 'Orion', 'B8Ia', 21, 78.9, 120000, 12100, 860, 0.13, -7.84, '05h 14m 32.3s', '-08° 12\' 06.0"', -0.06, 0.008, 25, 1, 1, 0, 'Blue supergiant, most luminous star in Orion', 'Left foot of Orion hunter', 'Blue supergiant, seventh brightest star, extremely luminous'),
            
            ('Procyon', 'Alpha Canis Minoris', 'HD 61421, HR 2943', 'Canis Minor', 'F5IV-V', 1.499, 2.048, 6.93, 6530, 11.46, 0.34, 2.66, '07h 39m 18.1s', '+05° 13\' 30.0"', -0.05, 2.7, 3.16, 1, 0, 0, 'Binary system with white dwarf companion', 'Little Dog Star, part of Winter Triangle', 'Eighth brightest star, binary system with white dwarf Procyon B'),
            
            ('Betelgeuse', 'Alpha Orionis', 'HD 39801, HR 2061', 'Orion', 'M1-2Ia-ab', 11.6, 764, 90000, 3500, 700, 0.50, -5.85, '05h 55m 10.3s', '+07° 24\' 25.4"', 0.05, 0.01, 5, 0, 1, 0, 'Red supergiant, semi-regular variable, candidate for supernova', 'Shoulder of Orion, prominent in winter sky', 'Red supergiant variable star, one of largest known stars, supernova candidate'),
            
            ('Achernar', 'Alpha Eridani', 'HD 10144, HR 472', 'Eridanus', 'Be', 6.7, 11.4, 3150, 20000, 139, 0.46, -2.77, '01h 37m 42.8s', '-57° 14\' 12.3"', 0.16, 0.037, 250, 0, 1, 0, 'Fastest rotating star, oblate shape due to rotation', 'End of the River in Arabic astronomy', 'Fastest rotating star known, extremely flattened due to rapid rotation'),
            
            ('Hadar', 'Beta Centauri, Agena', 'HD 122451, HR 5267', 'Centaurus', 'B1III', 10.7, 8.6, 41700, 25000, 390, 0.61, -5.42, '14h 03m 49.4s', '-60° 22\' 22.9"', -0.23, 0.014, 0, 1, 1, 0, 'Blue giant binary system, Cepheid variable', 'Pointer to Southern Cross', 'Blue giant binary system, tenth brightest star, beta Cepheid variable'),
            
            # Additional bright and notable stars
            ('Altair', 'Alpha Aquilae', 'HD 187642, HR 7557', 'Aquila', 'A7V', 1.79, 1.63, 10.6, 7550, 16.73, 0.77, 2.21, '19h 50m 47.0s', '+08° 52\' 06.0"', -0.2, 1.0, 286, 0, 0, 0, 'Fast rotating star, part of Summer Triangle', 'Eagle star, represents flying eagle', 'Fast-rotating main sequence star, part of Summer Triangle asterism'),
            
            ('Aldebaran', 'Alpha Tauri', 'HD 29139, HR 1457', 'Taurus', 'K5III', 1.16, 44.13, 518, 3910, 65.3, 0.85, -0.63, '04h 35m 55.2s', '+16° 30\' 33.5"', -0.34, 6.4, 1.5, 0, 1, 0, 'Red giant, appears in Hyades cluster but not member', 'Eye of the Bull, royal star in Persian astronomy', 'Orange giant star marking the eye of Taurus the Bull'),
            
            ('Spica', 'Alpha Virginis', 'HD 116658, HR 5056', 'Virgo', 'B1III-IV+B2V', 11.43, 7.47, 20512, 22400, 250, 1.04, -3.55, '13h 25m 11.6s', '-11° 09\' 40.8"', -0.16, 0.01, 199, 1, 1, 0, 'Close binary system, rotating ellipsoidal variable', 'Wheat sheaf star, navigation star', 'Hot blue binary star system, sixteenth brightest star in night sky'),
            
            ('Antares', 'Alpha Scorpii', 'HD 148478, HR 6134', 'Scorpius', 'M1.5Iab-Ib', 12, 700, 75900, 3500, 550, 1.09, -5.28, '16h 29m 24.5s', '-26° 25\' 55.2"', 0.07, 0.011, 3, 1, 1, 0, 'Red supergiant, rival of Mars in brightness', 'Rival of Mars, heart of the Scorpion', 'Red supergiant, one of largest known stars, semiregular variable'),
            
            ('Pollux', 'Beta Geminorum', 'HD 62509, HR 2990', 'Gemini', 'K0III', 1.91, 8.8, 43, 4666, 33.78, 1.14, 1.09, '07h 45m 18.9s', '+28° 01\' 34.3"', 0.07, 0.724, 2.8, 0, 0, 1, 'Orange giant with confirmed exoplanet', 'Twin of Castor, immortal twin in mythology', 'Orange giant star with confirmed exoplanet Pollux b'),
            
            ('Fomalhaut', 'Alpha Piscis Austrini', 'HD 216956, HR 8728', 'Piscis Austrinus', 'A3V', 1.92, 1.842, 16.6, 8590, 25.13, 1.16, 1.72, '22h 57m 39.0s', '-29° 37\' 20.1"', 0.03, 0.44, 93, 0, 0, 1, 'Young star with debris disk and exoplanet', 'Solitary One, autumn star in northern hemisphere', 'Young main sequence star with prominent debris disk and disputed exoplanet'),
            
            ('Deneb', 'Alpha Cygni', 'HD 197345, HR 7924', 'Cygnus', 'A2Ia', 19, 203, 196000, 8525, 2615, 1.25, -8.38, '20h 41m 25.9s', '+45° 16\' 49.2"', -0.05, 0.01, 20, 0, 1, 0, 'Blue-white supergiant, most distant first-magnitude star', 'Tail of the Swan, part of Summer Triangle', 'Luminous blue supergiant, most distant first-magnitude star'),
            
            ('Regulus', 'Alpha Leonis', 'HD 87901, HR 3982', 'Leo', 'B8IVn', 3.8, 3.092, 288, 12460, 79.3, 1.35, -0.52, '10h 08m 22.3s', '+11° 58\' 02.0"', -0.36, 0.001, 347, 1, 0, 0, 'Fast rotating hot star, quadruple system', 'Heart of the Lion, royal star', 'Hot blue main sequence star, fastest rotating first-magnitude star'),
            
            ('Adhara', 'Epsilon Canis Majoris', 'HD 52089, HR 2618', 'Canis Major', 'B2II', 12.6, 14, 38700, 22200, 430, 1.50, -4.11, '06h 58m 37.5s', '-28° 58\' 19.5"', -0.24, 0.022, 20, 1, 0, 0, 'Blue giant binary, second brightest in Canis Major', 'Virgins in Arabic, part of winter sky', 'Hot blue giant binary system, twenty-second brightest star'),
            
            ('Castor', 'Alpha Geminorum', 'HD 60179, HR 2891', 'Gemini', 'A1V+A2Vm', 2.76, 2.4, 49.8, 10286, 51.6, 1.57, 0.59, '07h 34m 35.9s', '+31° 53\' 18.1"', 0.98, 0.37, 18, 1, 0, 0, 'Complex sextuple star system', 'Twin of Pollux, mortal twin in mythology', 'Complex multiple star system with six components'),
            
            ('Shaula', 'Lambda Scorpii', 'HD 158926, HR 6527', 'Scorpius', 'B1.5IV+B2IV', 14.5, 8.8, 36300, 25000, 570, 1.63, -5.05, '17h 33m 36.5s', '-37° 06\' 13.8"', -0.15, 0.01, 0, 1, 1, 0, 'Hot blue binary, stinger of Scorpion', 'The Stinger, raised tail of scorpion', 'Hot blue binary system marking the stinger of Scorpius'),
            
            ('Bellatrix', 'Gamma Orionis', 'HD 35468, HR 1790', 'Orion', 'B2III', 8.6, 5.75, 9211, 21800, 245, 1.64, -2.78, '05h 25m 07.9s', '+06° 20\' 58.9"', -0.07, 0.025, 5, 0, 0, 0, 'Blue giant, left shoulder of Orion', 'Amazon Warrior, shoulder of Orion', 'Hot blue giant star forming the left shoulder of Orion'),
            
            ('Elnath', 'Beta Tauri', 'HD 35497, HR 1791', 'Taurus', 'B7III', 4.5, 4.2, 700, 13824, 134, 1.68, -1.37, '05h 26m 17.5s', '+28° 36\' 27.0"', -0.09, 0.1, 73, 0, 0, 0, 'Blue giant, tip of Taurus horn', 'The Butting One, horn tip of the Bull', 'Hot blue giant marking the northern horn tip of Taurus'),
            
            ('Alnilam', 'Epsilon Orionis', 'HD 37128, HR 1903', 'Orion', 'B0Ia', 64.5, 42, 832000, 27500, 2000, 1.69, -6.38, '05h 36m 12.8s', '-01° 12\' 06.9"', -0.18, 0.004, 40, 0, 1, 0, 'Blue supergiant, middle star of Orion Belt', 'String of Pearls, central belt star', 'Luminous blue supergiant, central star of Orion\'s Belt'),
            
            ('Alnitak', 'Zeta Orionis', 'HD 37742, HR 1948', 'Orion', 'O9.5Ib+B1IV', 33, 20, 250000, 29500, 1260, 1.74, -5.25, '05h 40m 45.5s', '-01° 56\' 34.0"', -0.15, 0.006, 110, 1, 0, 0, 'Blue supergiant binary, easternmost belt star', 'The Girdle, eastern belt star', 'Hot blue supergiant binary system, easternmost star of Orion\'s Belt'),
            
            ('Alnath', 'Beta Aurigae', 'HD 40183, HR 2088', 'Auriga', 'A1mA5-A7', 2.32, 2.77, 48, 9350, 82.1, 1.90, -0.10, '05h 59m 31.7s', '+44° 56\' 50.8"', 0.0, 0.57, 33, 1, 0, 0, 'White subgiant binary system', 'The Driver, charioteer star', 'White subgiant binary system in Auriga constellation'),
            
            ('Alioth', 'Epsilon Ursae Majoris', 'HD 112185, HR 4905', 'Ursa Major', 'A1III-IVp', 2.91, 4.14, 108, 9020, 82.6, 1.77, 0.23, '12h 54m 01.7s', '+55° 57\' 35.4"', -0.09, 0.3, 33, 0, 1, 0, 'Peculiar A-type star, brightest in Big Dipper', 'Fat Tail of the Bear, Big Dipper star', 'Chemically peculiar A-type star, brightest star in Ursa Major'),
            
            ('Dubhe', 'Alpha Ursae Majoris', 'HD 95689, HR 4301', 'Ursa Major', 'K0III+F0V', 4.25, 30.5, 316, 4660, 123, 1.79, -1.08, '11h 03m 43.7s', '+61° 45\' 03.7"', -0.20, 4.6, 2.6, 1, 0, 0, 'Orange giant binary, pointer star', 'The Bear, pointer to Polaris', 'Orange giant binary system, one of the pointer stars to Polaris'),
            
            ('Wezen', 'Delta Canis Majoris', 'HD 54605, HR 2693', 'Canis Major', 'F8Ia', 16.9, 215, 82000, 6390, 1800, 1.83, -6.87, '07h 08m 23.5s', '-26° 23\' 35.5"', 0.11, 0.01, 25, 0, 0, 0, 'Yellow-white supergiant, very luminous', 'Weight, bright star in Canis Major', 'Luminous yellow-white supergiant, one of most luminous stars visible'),
            
            ('Sargas', 'Theta Scorpii', 'HD 159532, HR 6553', 'Scorpius', 'F0II', 5.7, 26, 1834, 7268, 272, 1.87, -2.75, '17h 37m 19.1s', '-42° 59\' 52.2"', 0.18, 0.032, 1, 0, 0, 0, 'Yellow-white giant, part of Scorpius', 'The Babylonian name, tail of scorpion', 'Yellow-white giant star in the tail region of Scorpius'),
            
            ('Kaus Australis', 'Epsilon Sagittarii', 'HD 169022, HR 6879', 'Sagittarius', 'B9.5III', 3.515, 6.8, 363, 9960, 143, 1.85, -1.44, '18h 24m 10.3s', '-34° 23\' 04.6"', 0.12, 0.232, 236, 0, 0, 0, 'Blue-white giant, brightest in Sagittarius', 'Southern part of the Bow', 'Hot blue-white giant, brightest star in Sagittarius constellation'),
            
            ('Avior', 'Epsilon Carinae', 'HD 71129, HR 3307', 'Carina', 'K3III+B2V', 10.5, 130, 4050, 3523, 630, 1.86, -4.58, '08h 22m 30.8s', '-59° 30\' 34.1"', -0.10, 0.66, 0, 1, 0, 0, 'Orange giant binary, part of Southern Cross region', 'Part of False Cross asterism', 'Orange giant binary system, part of the False Cross asterism'),
            
            # Red dwarf and nearby stars
            ('Proxima Centauri', 'Alpha Centauri C', 'GJ 551, HIP 70890', 'Centaurus', 'M5.5Ve', 0.1221, 0.1542, 0.0017, 3042, 4.24, 11.13, 15.60, '14h 29m 42.9s', '-62° 40\' 46.1"', 0.21, 4.85, 2.7, 0, 1, 3, 'Nearest star to Sun, flare star with exoplanets', 'Closest star to our Solar System', 'Nearest known star to the Sun, red dwarf with potentially habitable exoplanet'),
            
            ('Barnard\'s Star', 'Gliese 699', 'HD 173740, HIP 87937', 'Ophiuchus', 'M4.0Ve', 0.144, 0.196, 0.0035, 3134, 5.96, 9.53, 13.22, '17h 57m 48.5s', '+04° 41\' 36.2"', -0.26, 7.0, 2.2, 0, 1, 1, 'High proper motion red dwarf, second nearest star system', 'Named after astronomer E.E. Barnard', 'Red dwarf with highest known proper motion, second nearest star system'),
            
            ('Wolf 359', 'Gliese 406', 'CN Leonis', 'Leo', 'M6.0V', 0.09, 0.16, 0.0014, 2800, 7.86, 13.54, 16.64, '10h 56m 29.2s', '+07° 00\' 53.0"', -0.20, 5.0, 19, 0, 1, 2, 'Flare star, one of faintest known stars', 'Named after German astronomer Max Wolf', 'Very low-mass red dwarf flare star, one of the faintest stars known'),
            
            ('Lalande 21185', 'Gliese 411', 'HD 95735, HIP 54035', 'Ursa Major', 'M2.0V', 0.393, 0.393, 0.026, 3828, 8.29, 7.47, 10.44, '11h 03m 20.2s', '+35° 58\' 11.6"', -0.20, 5.0, 2.2, 0, 1, 2, 'Nearby red dwarf with planetary system', 'Named after French astronomer Lalande', 'Nearby red dwarf star with confirmed planetary system'),
            
            ('Luyten 726-8', 'Gliese 65', 'UV Ceti', 'Cetus', 'M5.5Ve+M6.0Ve', 0.102, 0.14, 0.00006, 2670, 8.73, 12.54, 15.40, '01h 39m 01.3s', '-17° 57\' 01.0"', -1.0, 1.0, 1.4, 1, 1, 0, 'Binary flare star system, prototype UV Ceti variables', 'Prototype of UV Ceti flare stars', 'Binary red dwarf system, prototype of UV Ceti type flare stars'),
            
            # White dwarf stars
            ('Sirius B', 'Alpha Canis Majoris B', 'HD 48915B', 'Canis Major', 'DA2', 0.978, 0.0084, 0.056, 25200, 8.66, 8.44, 11.18, '02h 06m 23.5s', '-16° 42\' 58.0"', 0.0, 0.228, 0, 1, 0, 0, 'White dwarf companion to Sirius, first white dwarf discovered', 'The Pup, companion to Dog Star', 'First white dwarf star discovered, dense companion to Sirius A'),
            
            ('Procyon B', 'Alpha Canis Minoris B', 'HD 61421B', 'Canis Minor', 'DQZ', 0.602, 0.01234, 0.00049, 7740, 11.46, 10.70, 12.98, '07h 39m 18.1s', '+05° 13\' 30.0"', 0.0, 1.37, 0, 1, 0, 0, 'White dwarf companion to Procyon', 'Companion to Little Dog Star', 'White dwarf companion to Procyon A, difficult to observe due to brightness difference'),
            
            # Variable stars
            ('Mira', 'Omicron Ceti', 'HD 10826, HR 681', 'Cetus', 'M7IIIe', 1.18, 332, 8400, 3192, 420, 3.04, -2.53, '02h 19m 20.8s', '-02° 58\' 39.5"', 0.0, 6.0, 0, 0, 1, 0, 'Prototype long-period variable star, pulsating red giant', 'The Wonderful Star, first non-nova variable discovered', 'Prototype long-period variable star, varies from magnitude 2 to 10'),
            
            ('Algol', 'Beta Persei', 'HD 19356, HR 936', 'Perseus', 'B8V+K2IV', 3.17, 2.73, 182, 13000, 90.0, 2.12, -0.18, '03h 08m 10.1s', '+40° 57\' 20.3"', 0.0, 0.570, 0, 1, 1, 0, 'Prototype eclipsing binary, the Demon Star', 'The Demon Star, winking eye of Medusa', 'Famous eclipsing binary star, prototype of Algol-type variables'),
            
            ('Delta Cephei', 'Delta Cephei', 'HD 213306, HR 8571', 'Cepheus', 'F5Ib-G2Ib', 4.5, 44.5, 2000, 5930, 887, 4.07, -3.47, '22h 29m 10.3s', '+58° 24\' 54.7"', 0.09, 0.1, 17, 0, 1, 0, 'Prototype Cepheid variable star, period-luminosity relation', 'Prototype of classical Cepheid variables', 'Prototype classical Cepheid variable, key to cosmic distance scale'),
            
            ('Polaris', 'Alpha Ursae Minoris', 'HD 8890, HR 424', 'Ursa Minor', 'F7Ib-II', 5.4, 37.5, 1260, 6015, 433, 1.98, -3.64, '02h 31m 49.1s', '+89° 15\' 50.8"', 0.05, 0.07, 17, 1, 1, 0, 'Current north pole star, Cepheid variable', 'North Star, Pole Star, navigator\'s star', 'Current northern pole star, classical Cepheid variable star')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO major_stars 
            (name, common_names, catalog_designations, constellation, stellar_class, mass_solar, radius_solar, 
             luminosity_solar, temperature_k, distance_ly, apparent_magnitude, absolute_magnitude, 
             coordinates_ra, coordinates_dec, metallicity, age_billion_years, rotational_velocity, 
             binary_system, variable_star, exoplanets, notable_features, cultural_significance, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', major_stars)
    
    def query_star(self, star_name: str) -> Optional[Dict[str, Any]]:
        """Query information about a specific star."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM major_stars 
                    WHERE name LIKE ? OR common_names LIKE ? OR catalog_designations LIKE ?
                ''', (f'%{star_name}%', f'%{star_name}%', f'%{star_name}%'))
                
                result = cursor.fetchone()
                if result:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, result))
                
        except Exception as e:
            self.logger.error(f"Error querying star {star_name}: {e}")
        
        return None
    
    def query_stellar_class(self, class_type: str) -> Optional[Dict[str, Any]]:
        """Query information about a stellar classification."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM stellar_classes WHERE class_type = ?
                ''', (class_type.upper(),))
                
                result = cursor.fetchone()
                if result:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, result))
                
        except Exception as e:
            self.logger.error(f"Error querying stellar class {class_type}: {e}")
        
        return None
    
    def get_stars_in_constellation(self, constellation: str) -> List[Dict[str, Any]]:
        """Get all major stars in a constellation."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT name, apparent_magnitude, stellar_class, distance_ly, description 
                    FROM major_stars 
                    WHERE constellation LIKE ?
                    ORDER BY apparent_magnitude
                ''', (f'%{constellation}%',))
                
                columns = ['name', 'apparent_magnitude', 'stellar_class', 'distance_ly', 'description']
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
                
        except Exception as e:
            self.logger.error(f"Error querying constellation {constellation}: {e}")
            return []
    
    def get_brightest_stars(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get the brightest stars visible from Earth."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT name, apparent_magnitude, stellar_class, distance_ly, constellation 
                    FROM major_stars 
                    ORDER BY apparent_magnitude 
                    LIMIT ?
                ''', (limit,))
                
                columns = ['name', 'apparent_magnitude', 'stellar_class', 'distance_ly', 'constellation']
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
                
        except Exception as e:
            self.logger.error(f"Error getting brightest stars: {e}")
            return []
