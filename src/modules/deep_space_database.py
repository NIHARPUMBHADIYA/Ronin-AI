#!/usr/bin/env python3
"""
Deep Space Objects Database Module for Space AI Assistant.
Handles nebulae, star clusters, quasars, pulsars, and other deep space phenomena.
"""

import sqlite3
import os
from typing import Dict, List, Any, Optional
from ..utils.logger import setup_logger

class DeepSpaceDatabase:
    """Database for deep space objects including nebulae, clusters, quasars, and pulsars."""
    
    def __init__(self, config, logger=None):
        """Initialize the Deep Space Database."""
        self.config = config
        self.logger = logger or setup_logger()
        
        # Database path
        data_dir = config.get('data.knowledge_dir', 'data/knowledge')
        os.makedirs(data_dir, exist_ok=True)
        self.db_path = os.path.join(data_dir, 'deep_space_database.db')
        
        # Initialize database
        self._initialize_database()
        self.logger.info("Deep Space Database initialized successfully")
    
    def _initialize_database(self):
        """Create and populate the deep space database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create tables
            self._create_tables(cursor)
            
            # Populate with data
            self._populate_nebulae(cursor)
            self._populate_star_clusters(cursor)
            self._populate_quasars(cursor)
            self._populate_pulsars(cursor)
            
            conn.commit()
    
    def _create_tables(self, cursor):
        """Create database tables for deep space objects."""
        
        # Nebulae table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS nebulae (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                catalog_designation TEXT,
                type TEXT,
                constellation TEXT,
                distance_ly REAL,
                size_ly REAL,
                apparent_magnitude REAL,
                right_ascension TEXT,
                declination TEXT,
                central_star TEXT,
                composition TEXT,
                temperature_k REAL,
                discovery_date TEXT,
                discovered_by TEXT,
                notable_features TEXT,
                description TEXT
            )
        ''')
        
        # Star clusters table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS star_clusters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                catalog_designation TEXT,
                type TEXT,
                constellation TEXT,
                distance_ly REAL,
                diameter_ly REAL,
                age_million_years REAL,
                star_count INTEGER,
                apparent_magnitude REAL,
                right_ascension TEXT,
                declination TEXT,
                metallicity REAL,
                discovery_date TEXT,
                discovered_by TEXT,
                notable_features TEXT,
                description TEXT
            )
        ''')
        
        # Quasars table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS quasars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                catalog_designation TEXT,
                constellation TEXT,
                redshift REAL,
                distance_billion_ly REAL,
                apparent_magnitude REAL,
                absolute_magnitude REAL,
                luminosity_solar REAL,
                black_hole_mass_solar REAL,
                right_ascension TEXT,
                declination TEXT,
                discovery_date TEXT,
                discovered_by TEXT,
                notable_features TEXT,
                description TEXT
            )
        ''')
        
        # Pulsars table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pulsars (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                catalog_designation TEXT,
                constellation TEXT,
                distance_ly REAL,
                period_ms REAL,
                period_derivative REAL,
                magnetic_field_gauss REAL,
                age_million_years REAL,
                right_ascension TEXT,
                declination TEXT,
                discovery_date TEXT,
                discovered_by TEXT,
                notable_features TEXT,
                description TEXT
            )
        ''')
    
    def _populate_nebulae(self, cursor):
        """Populate nebulae data."""
        nebulae = [
            # name, catalog, type, constellation, distance_ly, size_ly, magnitude, ra, dec, central_star, composition, temp_k, discovery, discoverer, features, description
            ('Orion Nebula', 'M42', 'Emission', 'Orion', 1344, 24, 4.0, '05h 35m 17s', '-05° 23\' 14"', 'Trapezium Cluster', 'Hydrogen, helium, dust', 10000, '1610', 'Nicolas-Claude Fabri de Peiresc', 'Star-forming region, trapezium cluster, stellar nursery', 'One of the brightest nebulae visible to naked eye, active star formation region'),
            
            ('Crab Nebula', 'M1', 'Supernova Remnant', 'Taurus', 6500, 11, 8.4, '05h 34m 32s', '+22° 00\' 52"', 'Crab Pulsar', 'Expanding gas, synchrotron radiation', 1000000, '1054', 'Chinese astronomers', 'Pulsar at center, supernova remnant, expanding at 1500 km/s', 'Remnant of supernova observed by Chinese astronomers in 1054 AD'),
            
            ('Eagle Nebula', 'M16', 'Emission', 'Serpens', 7000, 70, 6.4, '18h 18m 48s', '-13° 49\' 00"', 'Hot young stars', 'Hydrogen, dust pillars', 8000, '1745-46', 'Philippe Loys de Chéseaux', 'Pillars of Creation, star formation, elephant trunk structures', 'Famous for Pillars of Creation, active star-forming region with towering gas columns'),
            
            ('Horsehead Nebula', 'B33', 'Dark', 'Orion', 1500, 3.5, 0, '05h 40m 59s', '-02° 27\' 33"', 'Sigma Orionis', 'Dense dust cloud', 20, '1888', 'Williamina Fleming', 'Distinctive horse head silhouette, dark nebula against bright background', 'Dark nebula creating distinctive horse head silhouette against bright emission nebula'),
            
            ('Ring Nebula', 'M57', 'Planetary', 'Lyra', 2300, 1, 8.8, '18h 53m 36s', '+33° 01\' 45"', 'White dwarf', 'Ionized hydrogen, helium', 70000, '1779', 'Antoine Darquier de Pellepoix', 'Perfect ring shape, white dwarf at center, colorful structure', 'Classic planetary nebula with perfect ring structure, formed by dying star'),
            
            ('Cat\'s Eye Nebula', 'NGC 6543', 'Planetary', 'Draco', 3300, 0.65, 8.1, '17h 58m 33s', '+66° 37\' 59"', 'Central white dwarf', 'Complex ionized gas structure', 80000, '1786', 'William Herschel', 'Complex knots and jets, intricate structure, multiple shells', 'Complex planetary nebula with intricate knots, jets, and multiple concentric shells')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO nebulae 
            (name, catalog_designation, type, constellation, distance_ly, size_ly, apparent_magnitude, 
             right_ascension, declination, central_star, composition, temperature_k, 
             discovery_date, discovered_by, notable_features, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', nebulae)
    
    def query_deep_space(self, query: str) -> Dict[str, Any]:
        """General deep space query across all object types."""
        try:
            # Try nebulae first
            nebula_result = self.query_nebula(query)
            if nebula_result['type'] != 'no_results':
                return nebula_result
            
            # Try star clusters
            cluster_result = self.query_star_cluster(query)
            if cluster_result['type'] != 'no_results':
                return cluster_result
            
            # Try quasars
            quasar_result = self.query_quasar(query)
            if quasar_result['type'] != 'no_results':
                return quasar_result
            
            # Try pulsars
            pulsar_result = self.query_pulsar(query)
            if pulsar_result['type'] != 'no_results':
                return pulsar_result
            
            return {'type': 'no_results', 'message': f'No deep space objects found matching "{query}"'}
            
        except Exception as e:
            self.logger.error(f"Deep space query failed: {e}")
            return {'type': 'error', 'message': 'Deep space query failed'}
    
    def query_nebula(self, query: str) -> Dict[str, Any]:
        """Query nebula information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM nebulae 
                    WHERE LOWER(name) LIKE LOWER(?) 
                    OR LOWER(catalog_designation) LIKE LOWER(?)
                    OR LOWER(type) LIKE LOWER(?)
                    OR LOWER(constellation) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    nebulae = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'nebula_info',
                        'nebulae': nebulae,
                        'count': len(nebulae)
                    }
                
                return {'type': 'no_results', 'message': f'No nebulae found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Nebula query failed: {e}")
            return {'type': 'error', 'message': 'Nebula query failed'}
    
    def _populate_star_clusters(self, cursor):
        """Populate star clusters data."""
        clusters = [
            # name, catalog, type, constellation, distance_ly, diameter_ly, age_million_years, star_count, magnitude, ra, dec, metallicity, discovery, discoverer, features, description
            ('Pleiades', 'M45', 'Open', 'Taurus', 444, 13, 100, 1000, 1.6, '03h 47m 29s', '+24° 07\' 00"', -0.03, 'Ancient', 'Ancient observers', 'Seven Sisters, blue reflection nebulae, hot B-type stars', 'Famous open cluster known as Seven Sisters, young hot stars with reflection nebulae'),
            
            ('Hyades', 'Mel 25', 'Open', 'Taurus', 153, 18, 625, 200, 0.5, '04h 26m 54s', '+15° 52\' 00"', 0.13, 'Ancient', 'Ancient observers', 'Nearest star cluster, V-shaped pattern, red giant Aldebaran nearby', 'Nearest star cluster to Earth forming distinctive V-shape in Taurus constellation'),
            
            ('Beehive Cluster', 'M44', 'Open', 'Cancer', 577, 22.8, 600, 350, 3.7, '08h 40m 06s', '+19° 59\' 00"', 0.0, 'Ancient', 'Ancient observers', 'Praesepe, visible to naked eye, rich in red dwarfs', 'Large open cluster visible to naked eye, also known as Praesepe'),
            
            ('Globular Cluster M13', 'M13', 'Globular', 'Hercules', 25100, 145, 11700, 300000, 5.8, '16h 41m 42s', '+36° 27\' 37"', -1.33, '1714', 'Edmond Halley', 'Great Hercules Cluster, densely packed ancient stars', 'Spectacular globular cluster in Hercules, one of brightest in northern sky'),
            
            ('Omega Centauri', 'NGC 5139', 'Globular', 'Centaurus', 15800, 150, 12000, 10000000, 3.9, '13h 26m 47s', '-47° 28\' 46"', -1.53, '1677', 'Edmond Halley', 'Largest globular cluster, possible stripped galaxy core', 'Largest and brightest globular cluster, possibly remnant core of disrupted galaxy'),
            
            ('Double Cluster', 'NGC 869/884', 'Open', 'Perseus', 7500, 30, 13, 600, 4.3, '02h 20m 00s', '+57° 08\' 00"', -0.05, '964', 'Abd al-Rahman al-Sufi', 'Two adjacent open clusters, young hot stars', 'Spectacular pair of open clusters visible to naked eye in Perseus')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO star_clusters 
            (name, catalog_designation, type, constellation, distance_ly, diameter_ly, age_million_years, 
             star_count, apparent_magnitude, right_ascension, declination, metallicity, 
             discovery_date, discovered_by, notable_features, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', clusters)
    
    def _populate_quasars(self, cursor):
        """Populate quasars data."""
        quasars = [
            # name, catalog, constellation, redshift, distance_billion_ly, app_mag, abs_mag, luminosity_solar, bh_mass_solar, ra, dec, discovery, discoverer, features, description
            ('3C 273', '3C 273', 'Virgo', 0.158, 2.4, 12.9, -26.7, 4e12, 8.86e8, '12h 29m 06s', '+02° 03\' 09"', '1963', 'Maarten Schmidt', 'First quasar identified, brightest quasar, variable luminosity', 'First quasar to be identified, brightest known quasar visible from Earth'),
            
            ('3C 48', '3C 48', 'Triangulum', 0.367, 4.2, 16.2, -25.5, 1e12, 7e8, '01h 37m 41s', '+33° 09\' 35"', '1960', 'Allan Sandage', 'First quasi-stellar radio source discovered, high redshift', 'First quasi-stellar radio source discovered, helped establish quasar nature'),
            
            ('TON 618', 'TON 618', 'Canes Venatici', 2.219, 10.4, 15.9, -30.7, 1.4e13, 6.6e10, '12h 28m 24s', '+31° 28\' 38"', '1957', 'Marie-Hélène Ulrich', 'Most luminous quasar, ultramassive black hole, extremely distant', 'One of most luminous quasars known with ultramassive central black hole'),
            
            ('ULAS J1120+0641', 'ULAS J1120+0641', 'Leo', 7.085, 12.9, 24.5, -27.0, 6.3e13, 2e9, '11h 20m 01s', '+06° 41\' 24"', '2011', 'Daniel Mortlock', 'Most distant quasar, formed 770 million years after Big Bang', 'Most distant quasar known, formed when universe was only 770 million years old')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO quasars 
            (name, catalog_designation, constellation, redshift, distance_billion_ly, apparent_magnitude, 
             absolute_magnitude, luminosity_solar, black_hole_mass_solar, right_ascension, declination, 
             discovery_date, discovered_by, notable_features, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', quasars)
    
    def _populate_pulsars(self, cursor):
        """Populate pulsars data."""
        pulsars = [
            # name, catalog, constellation, distance_ly, period_ms, period_derivative, magnetic_field_gauss, age_million_years, ra, dec, discovery, discoverer, features, description
            ('Crab Pulsar', 'PSR B0531+21', 'Taurus', 6500, 33.085, 4.21e-13, 3.8e12, 1.26, '05h 34m 32s', '+22° 00\' 52"', '1968', 'Jocelyn Bell Burnell team', 'Youngest known pulsar, supernova remnant, lighthouse effect', 'Youngest known pulsar at center of Crab Nebula, remnant of 1054 supernova'),
            
            ('Vela Pulsar', 'PSR B0833-45', 'Vela', 968, 89.33, 1.25e-13, 3.2e12, 11.3, '08h 35m 21s', '-45° 10\' 35"', '1968', 'Large team discovery', 'Glitching pulsar, gamma-ray emission, neutron star', 'Famous for sudden spin-up glitches, strong gamma-ray emitter'),
            
            ('Hulse-Taylor Pulsar', 'PSR B1913+16', 'Aquila', 21000, 59.03, 8.62e-18, 1e12, 108, '19h 15m 28s', '+16° 06\' 27"', '1974', 'Russell Hulse, Joseph Taylor', 'Binary pulsar, gravitational wave evidence, Nobel Prize', 'Binary pulsar that provided first evidence of gravitational waves, Nobel Prize 1993'),
            
            ('Millisecond Pulsar', 'PSR B1937+21', 'Vulpecula', 16000, 1.558, 1.05e-19, 4.1e8, 1570, '19h 39m 39s', '+21° 34\' 59"', '1982', 'Don Backer', 'Fastest spinning pulsar, recycled pulsar, extremely stable', 'First millisecond pulsar discovered, spins 642 times per second')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO pulsars 
            (name, catalog_designation, constellation, distance_ly, period_ms, period_derivative, 
             magnetic_field_gauss, age_million_years, right_ascension, declination, 
             discovery_date, discovered_by, notable_features, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', pulsars)
    
    def query_star_cluster(self, query: str) -> Dict[str, Any]:
        """Query star cluster information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM star_clusters 
                    WHERE LOWER(name) LIKE LOWER(?) 
                    OR LOWER(catalog_designation) LIKE LOWER(?)
                    OR LOWER(type) LIKE LOWER(?)
                    OR LOWER(constellation) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    clusters = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'cluster_info',
                        'clusters': clusters,
                        'count': len(clusters)
                    }
                
                return {'type': 'no_results', 'message': f'No star clusters found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Star cluster query failed: {e}")
            return {'type': 'error', 'message': 'Star cluster query failed'}
    
    def query_quasar(self, query: str) -> Dict[str, Any]:
        """Query quasar information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM quasars 
                    WHERE LOWER(name) LIKE LOWER(?) 
                    OR LOWER(catalog_designation) LIKE LOWER(?)
                    OR LOWER(constellation) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    quasars = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'quasar_info',
                        'quasars': quasars,
                        'count': len(quasars)
                    }
                
                return {'type': 'no_results', 'message': f'No quasars found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Quasar query failed: {e}")
            return {'type': 'error', 'message': 'Quasar query failed'}
    
    def query_pulsar(self, query: str) -> Dict[str, Any]:
        """Query pulsar information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM pulsars 
                    WHERE LOWER(name) LIKE LOWER(?) 
                    OR LOWER(catalog_designation) LIKE LOWER(?)
                    OR LOWER(constellation) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    pulsars = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'pulsar_info',
                        'pulsars': pulsars,
                        'count': len(pulsars)
                    }
                
                return {'type': 'no_results', 'message': f'No pulsars found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Pulsar query failed: {e}")
            return {'type': 'error', 'message': 'Pulsar query failed'}
    
    def format_deep_space_info(self, data: Dict[str, Any]) -> str:
        """Format deep space information for display."""
        if data['type'] == 'nebula_info':
            output = []
            for nebula in data['nebulae']:
                info = [f"**{nebula['name']} ({nebula['catalog_designation']}) - {nebula['type']} Nebula**"]
                
                if nebula['constellation']:
                    info.append(f"Constellation: {nebula['constellation']}")
                
                if nebula['distance_ly']:
                    info.append(f"Distance: {nebula['distance_ly']:,.0f} light-years")
                
                if nebula['size_ly']:
                    info.append(f"Size: {nebula['size_ly']:.1f} light-years")
                
                if nebula['apparent_magnitude']:
                    info.append(f"Apparent Magnitude: {nebula['apparent_magnitude']:.1f}")
                
                if nebula['central_star']:
                    info.append(f"Central Star: {nebula['central_star']}")
                
                if nebula['composition']:
                    info.append(f"Composition: {nebula['composition']}")
                
                if nebula['temperature_k']:
                    info.append(f"Temperature: {nebula['temperature_k']:,.0f} K")
                
                if nebula['discovery_date'] and nebula['discovered_by']:
                    info.append(f"Discovered: {nebula['discovery_date']} by {nebula['discovered_by']}")
                
                if nebula['notable_features']:
                    info.append(f"Notable Features: {nebula['notable_features']}")
                
                if nebula['description']:
                    info.append(f"Description: {nebula['description']}")
                
                output.append('\n'.join(info))
            
            return '\n\n'.join(output)
        
        elif data['type'] == 'cluster_info':
            output = []
            for cluster in data['clusters']:
                info = [f"**{cluster['name']} ({cluster['catalog_designation']}) - {cluster['type']} Cluster**"]
                
                if cluster['constellation']:
                    info.append(f"Constellation: {cluster['constellation']}")
                
                if cluster['distance_ly']:
                    info.append(f"Distance: {cluster['distance_ly']:,.0f} light-years")
                
                if cluster['diameter_ly']:
                    info.append(f"Diameter: {cluster['diameter_ly']:.1f} light-years")
                
                if cluster['age_million_years']:
                    info.append(f"Age: {cluster['age_million_years']:,.0f} million years")
                
                if cluster['star_count']:
                    info.append(f"Star Count: ~{cluster['star_count']:,}")
                
                if cluster['apparent_magnitude']:
                    info.append(f"Apparent Magnitude: {cluster['apparent_magnitude']:.1f}")
                
                if cluster['discovery_date'] and cluster['discovered_by']:
                    info.append(f"Discovered: {cluster['discovery_date']} by {cluster['discovered_by']}")
                
                if cluster['notable_features']:
                    info.append(f"Notable Features: {cluster['notable_features']}")
                
                if cluster['description']:
                    info.append(f"Description: {cluster['description']}")
                
                output.append('\n'.join(info))
            
            return '\n\n'.join(output)
        
        elif data['type'] == 'no_results':
            return data['message']
        
        elif data['type'] == 'error':
            return f"Error: {data['message']}"
        
        else:
            return "Unknown deep space data format"
