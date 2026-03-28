"""
Galaxy Database for Space AI Assistant.
Comprehensive database of galaxies, galaxy clusters, and cosmic structures.
"""

import sqlite3
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

class GalaxyDatabase:
    """Comprehensive database of galaxies and cosmic structures."""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("Galaxy_Database")
        
        # Database setup
        self.db_path = config.knowledge_dir / "galaxy_database.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize galaxy database
        self._initialize_galaxy_database()
        self._populate_galaxy_data()
        
    def _initialize_galaxy_database(self):
        """Initialize galaxy database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Major galaxies table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS galaxies (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        common_names TEXT,
                        catalog_designations TEXT,
                        galaxy_type TEXT,
                        constellation TEXT,
                        distance_mly REAL,
                        diameter_ly REAL,
                        mass_solar_masses REAL,
                        stars_estimated REAL,
                        apparent_magnitude REAL,
                        absolute_magnitude REAL,
                        redshift REAL,
                        coordinates_ra TEXT,
                        coordinates_dec TEXT,
                        central_black_hole_mass REAL,
                        active_nucleus BOOLEAN DEFAULT 0,
                        discovery_year INTEGER,
                        discovered_by TEXT,
                        notable_features TEXT,
                        description TEXT
                    )
                ''')
                
                # Galaxy clusters table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS galaxy_clusters (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        catalog_designations TEXT,
                        constellation TEXT,
                        distance_mly REAL,
                        diameter_mly REAL,
                        galaxy_count INTEGER,
                        mass_solar_masses REAL,
                        temperature_k REAL,
                        coordinates_ra TEXT,
                        coordinates_dec TEXT,
                        richness_class TEXT,
                        notable_members TEXT,
                        description TEXT
                    )
                ''')
                
                # Cosmic structures table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS cosmic_structures (
                        id INTEGER PRIMARY KEY,
                        name TEXT UNIQUE NOT NULL,
                        structure_type TEXT,
                        scale_mpc REAL,
                        mass_solar_masses REAL,
                        member_count INTEGER,
                        notable_features TEXT,
                        description TEXT
                    )
                ''')
                
                conn.commit()
                self.logger.info("Galaxy database initialized")
                
        except Exception as e:
            self.logger.error(f"Galaxy database initialization failed: {e}")
            raise
    
    def _populate_galaxy_data(self):
        """Populate galaxy database with comprehensive data."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if data exists
                cursor.execute("SELECT COUNT(*) FROM galaxies")
                if cursor.fetchone()[0] > 0:
                    return
                
                self._populate_major_galaxies(cursor)
                self._populate_galaxy_clusters(cursor)
                self._populate_cosmic_structures(cursor)
                
                conn.commit()
                self.logger.info("Galaxy data populated")
                
        except Exception as e:
            self.logger.error(f"Galaxy data population failed: {e}")
    
    def _populate_major_galaxies(self, cursor):
        """Populate major galaxies data."""
        galaxies = [
            # name, common_names, catalog_designations, galaxy_type, constellation, distance_mly, diameter_ly, mass_solar, stars_est, app_mag, abs_mag, redshift, ra, dec, bh_mass, active, discovery_year, discoverer, notable_features, description
            ('Milky Way', 'Our Galaxy, Via Lactea', 'MW', 'SBbc (Barred Spiral)', 'Sagittarius', 0, 105700, 1.5e12, 4e11, -6.5, -20.9, 0, '17h 45m 40s', '-29° 00\' 28"', 4.1e6, 0, 0, 'Ancient', 'Central bar, spiral arms, supermassive black hole Sagittarius A*', 'Our home galaxy, barred spiral containing our solar system'),
            
            ('Andromeda Galaxy', 'M31, Great Andromeda Nebula', 'NGC 224, M31', 'SA(s)b (Spiral)', 'Andromeda', 2.537, 220000, 1.5e12, 1e12, 3.44, -21.5, -0.001001, '00h 42m 44.3s', '+41° 16\' 09"', 1.4e8, 0, 964, 'Abd al-Rahman al-Sufi', 'Largest Local Group galaxy, approaching Milky Way', 'Nearest major galaxy, will collide with Milky Way in ~4.5 billion years'),
            
            ('Triangulum Galaxy', 'M33, Pinwheel Galaxy', 'NGC 598, M33', 'SA(s)cd (Spiral)', 'Triangulum', 2.73, 60000, 5e10, 4e10, 5.72, -18.87, -0.000597, '01h 33m 50.9s', '+30° 39\' 37"', 0, 0, 1764, 'Charles Messier', 'Third largest Local Group galaxy, face-on spiral', 'Third largest galaxy in Local Group, beautiful face-on spiral structure'),
            
            ('Large Magellanic Cloud', 'LMC, Nubecula Major', 'ESO 56-115', 'SB(s)m (Irregular)', 'Dorado/Mensa', 0.163, 14000, 2e10, 2e10, 0.13, -18.1, 0.000293, '05h 23m 34s', '-69° 45\' 22"', 0, 0, 0, 'Ancient Southern Hemisphere', 'Satellite galaxy, Tarantula Nebula, site of SN 1987A', 'Satellite galaxy of Milky Way, contains the bright Tarantula Nebula'),
            
            ('Small Magellanic Cloud', 'SMC, Nubecula Minor', 'NGC 292', 'SB(s)m pec (Irregular)', 'Tucana', 0.197, 7000, 7e9, 3e9, 2.7, -16.8, 0.000527, '00h 52m 38s', '-72° 48\' 01"', 0, 0, 0, 'Ancient Southern Hemisphere', 'Satellite galaxy, interacting with LMC', 'Smaller satellite galaxy, gravitationally interacting with LMC'),
            
            ('Centaurus A', 'NGC 5128, Caldwell 77', 'NGC 5128, PKS 1322-427', 'S0 pec (Peculiar Elliptical)', 'Centaurus', 13.7, 60000, 1e12, 1e11, 6.84, -22.4, 0.001825, '13h 25m 27.6s', '-43° 01\' 09"', 5.5e7, 1, 1826, 'James Dunlop', 'Active galactic nucleus, prominent dust lane, radio galaxy', 'Peculiar elliptical galaxy with prominent dust lane and active nucleus'),
            
            ('Whirlpool Galaxy', 'M51a, Question Mark Galaxy', 'NGC 5194, M51', 'SA(s)bc pec (Spiral)', 'Canes Venatici', 23.16, 76000, 1.6e11, 1e11, 8.4, -21.8, 0.001544, '13h 29m 52.7s', '+47° 11\' 43"', 3.8e6, 0, 1773, 'Charles Messier', 'Grand design spiral, interacting with M51b companion', 'Classic grand design spiral galaxy interacting with smaller companion'),
            
            ('Sombrero Galaxy', 'M104, Hat Galaxy', 'NGC 4594, M104', 'SA(s)a (Spiral)', 'Virgo', 31.1, 50000, 8e11, 1e11, 8.98, -22.7, 0.003416, '12h 39m 59.4s', '-11° 37\' 23"', 1e9, 0, 1781, 'Pierre Méchain', 'Prominent dust lane, large central bulge', 'Spiral galaxy with prominent dust lane resembling a sombrero hat'),
            
            ('Pinwheel Galaxy', 'M101, Fireworks Galaxy', 'NGC 5457, M101', 'SAB(rs)cd (Spiral)', 'Ursa Major', 20.9, 170000, 1e12, 1e12, 7.86, -21.6, 0.000804, '14h 03m 12.6s', '+54° 20\' 57"', 0, 0, 1781, 'Pierre Méchain', 'Face-on spiral, asymmetric structure, active star formation', 'Large face-on spiral galaxy with prominent star-forming regions'),
            
            ('Sculptor Galaxy', 'NGC 253, Silver Coin Galaxy', 'NGC 253, Caldwell 65', 'SAB(s)c (Spiral)', 'Sculptor', 11.4, 90000, 1e11, 1e11, 7.1, -20.5, 0.000811, '00h 47m 33.1s', '-25° 17\' 18"', 5e6, 0, 1783, 'Caroline Herschel', 'Starburst galaxy, high star formation rate', 'Bright spiral galaxy with intense star formation activity'),
            
            ('Black Eye Galaxy', 'M64, Evil Eye Galaxy', 'NGC 4826, M64', 'SA(rs)ab (Spiral)', 'Coma Berenices', 24.0, 54000, 1e11, 1e11, 8.52, -21.6, 0.001361, '12h 56m 43.7s', '+21° 40\' 58"', 0, 0, 1779, 'Edward Pigott', 'Prominent dark dust lane, counter-rotating gas', 'Spiral galaxy with distinctive dark dust lane across bright nucleus'),
            
            ('Cigar Galaxy', 'M82, Starburst Galaxy', 'NGC 3034, M82', 'I0 (Irregular)', 'Ursa Major', 11.4, 37000, 3e10, 3e10, 8.41, -19.7, 0.000677, '09h 55m 52.2s', '+69° 40\' 47"', 3e7, 0, 1774, 'Johann Bode', 'Starburst galaxy, galactic superwind, interacting with M81', 'Irregular starburst galaxy with intense star formation and galactic winds'),
            
            ('Bode\'s Galaxy', 'M81, Ursa Major Galaxy', 'NGC 3031, M81', 'SA(s)ab (Spiral)', 'Ursa Major', 11.6, 90000, 7e10, 2.5e11, 6.94, -21.0, -0.000034, '09h 55m 33.2s', '+69° 03\' 55"', 7e7, 0, 1774, 'Johann Bode', 'Grand design spiral, interacting with M82', 'Beautiful grand design spiral galaxy, gravitationally interacting with M82'),
            
            ('Southern Pinwheel Galaxy', 'M83, Thousand-Ruby Galaxy', 'NGC 5236, M83', 'SAB(s)c (Barred Spiral)', 'Hydra', 15.2, 55000, 3e10, 3e10, 7.54, -20.5, 0.001712, '13h 37m 00.9s', '-29° 51\' 57"', 0, 0, 1752, 'Nicolas-Louis de Lacaille', 'Face-on barred spiral, prominent star formation', 'Face-on barred spiral galaxy with active star formation regions'),
            
            ('Leo Triplet - M65', 'NGC 3623, M65', 'NGC 3623, M65', 'SAB(rs)a (Spiral)', 'Leo', 35.0, 60000, 2e11, 1e11, 9.3, -21.7, 0.002425, '11h 18m 55.9s', '+13° 05\' 32"', 0, 0, 1780, 'Charles Messier', 'Member of Leo Triplet, dust lanes', 'Spiral galaxy in the Leo Triplet group with prominent dust lanes'),
            
            ('Leo Triplet - M66', 'NGC 3627, M66', 'NGC 3627, M66', 'SAB(s)b (Barred Spiral)', 'Leo', 35.0, 95000, 2e11, 1e11, 8.9, -21.6, 0.002267, '11h 20m 15.0s', '+12° 59\' 30"', 0, 0, 1780, 'Charles Messier', 'Member of Leo Triplet, asymmetric spiral arms', 'Barred spiral galaxy in Leo Triplet with distorted spiral structure'),
            
            ('Sunflower Galaxy', 'M63, Flower Galaxy', 'NGC 5055, M63', 'SA(rs)bc (Spiral)', 'Canes Venatici', 37.0, 98000, 1e11, 4e10, 8.6, -22.0, 0.001605, '13h 15m 49.3s', '+42° 01\' 45"', 0, 0, 1779, 'Pierre Méchain', 'Flocculent spiral arms, yellow nucleus', 'Spiral galaxy with flocculent spiral pattern resembling sunflower petals')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO galaxies 
            (name, common_names, catalog_designations, galaxy_type, constellation, distance_mly, 
             diameter_ly, mass_solar_masses, stars_estimated, apparent_magnitude, absolute_magnitude, 
             redshift, coordinates_ra, coordinates_dec, central_black_hole_mass, active_nucleus, 
             discovery_year, discovered_by, notable_features, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', galaxies)
    
    def _populate_galaxy_clusters(self, cursor):
        """Populate galaxy clusters data."""
        clusters = [
            # name, catalog_designations, constellation, distance_mly, diameter_mly, galaxy_count, mass_solar, temp_k, ra, dec, richness_class, notable_members, description
            ('Local Group', 'LG', 'Multiple', 0, 10, 80, 2e12, 0, 'Various', 'Various', 'Poor', 'Milky Way, Andromeda, Triangulum', 'Our local galaxy group containing Milky Way and nearby galaxies'),
            ('Virgo Cluster', 'Abell 1656', 'Virgo', 53.8, 15, 1300, 1.2e15, 2.2e7, '12h 27m', '+12° 43\'', 'Rich', 'M87, M49, M58, M60', 'Nearest major galaxy cluster, contains giant elliptical M87'),
            ('Coma Cluster', 'Abell 1656', 'Coma Berenices', 321, 20, 1000, 4.6e14, 8.2e7, '12h 59m 48s', '+27° 58\' 50"', 'Rich', 'NGC 4874, NGC 4889', 'Dense, spherical cluster with no dominant central galaxy'),
            ('Perseus Cluster', 'Abell 426', 'Perseus', 240, 15, 1000, 6.6e14, 6.5e7, '02h 20m 00s', '+57° 08\' 00"', 'Rich', 'NGC 1275 (Perseus A)', 'X-ray bright cluster with central radio galaxy NGC 1275'),
            ('Fornax Cluster', 'Abell S373', 'Fornax', 62, 8, 58, 7e13, 3.5e6, '03h 38m', '-35° 27\'', 'Poor', 'NGC 1316, NGC 1365', 'Second nearest galaxy cluster, dominated by elliptical galaxies'),
            ('Hydra Cluster', 'Abell 1060', 'Hydra', 158, 10, 157, 8.2e13, 3.7e7, '10h 36m 43s', '-27° 31\' 47"', 'Medium', 'NGC 3311', 'X-ray luminous cluster with central cD galaxy'),
            ('Centaurus Cluster', 'Abell 3526', 'Centaurus', 170, 8, 100, 3.8e14, 3.8e7, '12h 48m 49s', '-41° 18\' 40"', 'Rich', 'NGC 4696', 'Nearby rich cluster with cooling flow'),
            ('Norma Cluster', 'Abell 3627', 'Norma', 220, 8, 100, 1e15, 5e7, '16h 15m 32s', '-60° 54\' 30"', 'Rich', 'ESO 137-001', 'Massive cluster behind Galactic plane, Great Attractor region')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO galaxy_clusters 
            (name, catalog_designations, constellation, distance_mly, diameter_mly, galaxy_count, 
             mass_solar_masses, temperature_k, coordinates_ra, coordinates_dec, richness_class, 
             notable_members, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', clusters)
    
    def _populate_cosmic_structures(self, cursor):
        """Populate cosmic structures data."""
        structures = [
            # name, structure_type, scale_mpc, mass_solar, member_count, notable_features, description
            ('Local Supercluster', 'Galaxy Supercluster', 110, 1e15, 100, 'Contains Local Group and Virgo Cluster', 'Our local supercluster centered on Virgo Cluster'),
            ('Great Wall', 'Galaxy Filament', 200, 1e16, 10000, 'One of largest known structures', 'Massive wall of galaxies discovered in 1989'),
            ('Sloan Great Wall', 'Galaxy Filament', 423, 1e16, 10000, 'Largest known cosmic structure', 'Enormous filament of galaxies spanning 1.37 billion light-years'),
            ('Boötes Void', 'Cosmic Void', 330, 0, 60, 'Nearly empty region of space', 'Enormous void containing very few galaxies'),
            ('Perseus-Pisces Supercluster', 'Galaxy Supercluster', 300, 1e16, 1000, 'Chain of galaxy clusters', 'Large supercluster containing Perseus and Pisces clusters'),
            ('Shapley Supercluster', 'Galaxy Supercluster', 650, 1e16, 8000, 'Most massive known supercluster', 'Concentration of galaxy clusters 650 million light-years away'),
            ('Laniakea Supercluster', 'Galaxy Supercluster', 520, 1e17, 100000, 'Contains Local Supercluster', 'Immense supercluster containing our Local Supercluster'),
            ('Cosmic Web', 'Large Scale Structure', 1000, 1e18, 1000000, 'Filamentary structure of matter', 'Largest scale structure of the universe')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO cosmic_structures 
            (name, structure_type, scale_mpc, mass_solar_masses, member_count, notable_features, description)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', structures)
    
    def query_galaxy(self, query: str) -> Dict[str, Any]:
        """Query galaxy information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Search galaxies by name or common names
                cursor.execute('''
                    SELECT * FROM galaxies 
                    WHERE LOWER(name) LIKE LOWER(?) 
                    OR LOWER(common_names) LIKE LOWER(?)
                    OR LOWER(catalog_designations) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    galaxies = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'galaxy_info',
                        'galaxies': galaxies,
                        'count': len(galaxies)
                    }
                
                return {'type': 'no_results', 'message': f'No galaxies found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Galaxy query failed: {e}")
            return {'type': 'error', 'message': 'Galaxy query failed'}
    
    def query_galaxy_cluster(self, query: str) -> Dict[str, Any]:
        """Query galaxy cluster information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM galaxy_clusters 
                    WHERE LOWER(name) LIKE LOWER(?) 
                    OR LOWER(catalog_designations) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    clusters = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'cluster_info',
                        'clusters': clusters,
                        'count': len(clusters)
                    }
                
                return {'type': 'no_results', 'message': f'No galaxy clusters found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Galaxy cluster query failed: {e}")
            return {'type': 'error', 'message': 'Galaxy cluster query failed'}
    
    def query_cosmic_structure(self, query: str) -> Dict[str, Any]:
        """Query cosmic structure information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM cosmic_structures 
                    WHERE LOWER(name) LIKE LOWER(?) 
                    OR LOWER(structure_type) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    structures = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'structure_info',
                        'structures': structures,
                        'count': len(structures)
                    }
                
                return {'type': 'no_results', 'message': f'No cosmic structures found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Cosmic structure query failed: {e}")
            return {'type': 'error', 'message': 'Cosmic structure query failed'}
    
    def get_galaxy_by_type(self, galaxy_type: str) -> Dict[str, Any]:
        """Get galaxies by morphological type."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM galaxies 
                    WHERE LOWER(galaxy_type) LIKE LOWER(?)
                    ORDER BY distance_mly
                ''', (f'%{galaxy_type}%',))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    galaxies = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'galaxy_type_results',
                        'galaxies': galaxies,
                        'galaxy_type': galaxy_type,
                        'count': len(galaxies)
                    }
                
                return {'type': 'no_results', 'message': f'No galaxies found of type "{galaxy_type}"'}
                
        except Exception as e:
            self.logger.error(f"Galaxy type query failed: {e}")
            return {'type': 'error', 'message': 'Galaxy type query failed'}
    
    def get_nearest_galaxies(self, limit: int = 10) -> Dict[str, Any]:
        """Get nearest galaxies to Earth."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM galaxies 
                    WHERE distance_mly > 0
                    ORDER BY distance_mly 
                    LIMIT ?
                ''', (limit,))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    galaxies = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'nearest_galaxies',
                        'galaxies': galaxies,
                        'count': len(galaxies)
                    }
                
                return {'type': 'no_results', 'message': 'No galaxy distance data available'}
                
        except Exception as e:
            self.logger.error(f"Nearest galaxies query failed: {e}")
            return {'type': 'error', 'message': 'Nearest galaxies query failed'}
    
    def get_local_group_members(self) -> Dict[str, Any]:
        """Get Local Group galaxy members."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM galaxies 
                    WHERE distance_mly <= 3.0 OR name IN ('Milky Way', 'Andromeda Galaxy', 'Triangulum Galaxy')
                    ORDER BY distance_mly
                ''')
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    galaxies = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'local_group',
                        'galaxies': galaxies,
                        'count': len(galaxies)
                    }
                
                return {'type': 'no_results', 'message': 'No Local Group data available'}
                
        except Exception as e:
            self.logger.error(f"Local Group query failed: {e}")
            return {'type': 'error', 'message': 'Local Group query failed'}
    
    def format_galaxy_info(self, galaxy_data: Dict[str, Any]) -> str:
        """Format galaxy information for display."""
        if galaxy_data['type'] == 'galaxy_info':
            output = []
            for galaxy in galaxy_data['galaxies']:
                info = [f"**{galaxy['name']}**"]
                
                if galaxy['common_names']:
                    info.append(f"Also known as: {galaxy['common_names']}")
                
                if galaxy['catalog_designations']:
                    info.append(f"Catalog: {galaxy['catalog_designations']}")
                
                info.append(f"Type: {galaxy['galaxy_type']}")
                info.append(f"Constellation: {galaxy['constellation']}")
                
                if galaxy['distance_mly'] and galaxy['distance_mly'] > 0:
                    info.append(f"Distance: {galaxy['distance_mly']:,.1f} million light-years")
                
                if galaxy['diameter_ly']:
                    info.append(f"Diameter: {galaxy['diameter_ly']:,.0f} light-years")
                
                if galaxy['mass_solar_masses']:
                    info.append(f"Mass: {galaxy['mass_solar_masses']:.1e} solar masses")
                
                if galaxy['stars_estimated']:
                    info.append(f"Estimated stars: {galaxy['stars_estimated']:.1e}")
                
                if galaxy['apparent_magnitude']:
                    info.append(f"Apparent magnitude: {galaxy['apparent_magnitude']}")
                
                if galaxy['central_black_hole_mass'] and galaxy['central_black_hole_mass'] > 0:
                    info.append(f"Central black hole: {galaxy['central_black_hole_mass']:.1e} solar masses")
                
                if galaxy['notable_features']:
                    info.append(f"Notable features: {galaxy['notable_features']}")
                
                if galaxy['description']:
                    info.append(f"Description: {galaxy['description']}")
                
                output.append('\n'.join(info))
            
            return '\n\n'.join(output)
        
        elif galaxy_data['type'] == 'cluster_info':
            output = []
            for cluster in galaxy_data['clusters']:
                info = [f"**{cluster['name']} Galaxy Cluster**"]
                
                if cluster['catalog_designations']:
                    info.append(f"Catalog: {cluster['catalog_designations']}")
                
                info.append(f"Constellation: {cluster['constellation']}")
                
                if cluster['distance_mly']:
                    info.append(f"Distance: {cluster['distance_mly']:,.1f} million light-years")
                
                if cluster['diameter_mly']:
                    info.append(f"Diameter: {cluster['diameter_mly']:,.1f} million light-years")
                
                if cluster['galaxy_count']:
                    info.append(f"Galaxy count: {cluster['galaxy_count']:,}")
                
                if cluster['mass_solar_masses']:
                    info.append(f"Mass: {cluster['mass_solar_masses']:.1e} solar masses")
                
                if cluster['temperature_k']:
                    info.append(f"Temperature: {cluster['temperature_k']:.1e} K")
                
                if cluster['richness_class']:
                    info.append(f"Richness class: {cluster['richness_class']}")
                
                if cluster['notable_members']:
                    info.append(f"Notable members: {cluster['notable_members']}")
                
                if cluster['description']:
                    info.append(f"Description: {cluster['description']}")
                
                output.append('\n'.join(info))
            
            return '\n\n'.join(output)
        
        elif galaxy_data['type'] == 'structure_info':
            output = []
            for structure in galaxy_data['structures']:
                info = [f"**{structure['name']}**"]
                info.append(f"Type: {structure['structure_type']}")
                
                if structure['scale_mpc']:
                    info.append(f"Scale: {structure['scale_mpc']:,.0f} megaparsecs")
                
                if structure['mass_solar_masses']:
                    info.append(f"Mass: {structure['mass_solar_masses']:.1e} solar masses")
                
                if structure['member_count']:
                    info.append(f"Members: {structure['member_count']:,}")
                
                if structure['notable_features']:
                    info.append(f"Notable features: {structure['notable_features']}")
                
                if structure['description']:
                    info.append(f"Description: {structure['description']}")
                
                output.append('\n'.join(info))
            
            return '\n\n'.join(output)
        
        elif galaxy_data['type'] == 'no_results':
            return galaxy_data['message']
        
        elif galaxy_data['type'] == 'error':
            return f"Error: {galaxy_data['message']}"
        
        else:
            return "Unknown galaxy data format"
