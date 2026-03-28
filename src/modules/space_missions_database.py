#!/usr/bin/env python3
"""
Space Missions Database Module for Space AI Assistant.
Handles historical and current space missions, spacecraft, and exploration programs.
"""

import sqlite3
import os
from typing import Dict, List, Any, Optional
from ..utils.logger import setup_logger

class SpaceMissionsDatabase:
    """Database for space missions, spacecraft, and exploration programs."""
    
    def __init__(self, config, logger=None):
        """Initialize the Space Missions Database."""
        self.config = config
        self.logger = logger or setup_logger()
        
        # Database path
        data_dir = config.get('data.knowledge_dir', 'data/knowledge')
        os.makedirs(data_dir, exist_ok=True)
        self.db_path = os.path.join(data_dir, 'space_missions_database.db')
        
        # Initialize database
        self._initialize_database()
        self.logger.info("Space Missions Database initialized successfully")
    
    def _initialize_database(self):
        """Create and populate the space missions database."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Create tables
            self._create_tables(cursor)
            
            # Populate with data
            self._populate_missions(cursor)
            self._populate_spacecraft(cursor)
            self._populate_astronauts(cursor)
            
            conn.commit()
    
    def _create_tables(self, cursor):
        """Create database tables for space missions."""
        
        # Missions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS missions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                agency TEXT,
                mission_type TEXT,
                launch_date TEXT,
                end_date TEXT,
                status TEXT,
                destination TEXT,
                spacecraft TEXT,
                crew_size INTEGER,
                duration_days REAL,
                cost_million_usd REAL,
                launch_vehicle TEXT,
                objectives TEXT,
                achievements TEXT,
                notable_events TEXT,
                description TEXT
            )
        ''')
        
        # Spacecraft table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS spacecraft (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                type TEXT,
                manufacturer TEXT,
                first_flight TEXT,
                status TEXT,
                crew_capacity INTEGER,
                mass_kg REAL,
                length_m REAL,
                diameter_m REAL,
                power_source TEXT,
                propulsion TEXT,
                missions_flown INTEGER,
                notable_features TEXT,
                description TEXT
            )
        ''')
        
        # Astronauts table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS astronauts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                nationality TEXT,
                agency TEXT,
                birth_date TEXT,
                selection_year INTEGER,
                total_flights INTEGER,
                total_eva_hours REAL,
                total_space_time_days REAL,
                missions TEXT,
                achievements TEXT,
                notable_records TEXT,
                description TEXT
            )
        ''')
    
    def _populate_missions(self, cursor):
        """Populate space missions data."""
        missions = [
            # name, agency, type, launch_date, end_date, status, destination, spacecraft, crew_size, duration_days, cost_million_usd, launch_vehicle, objectives, achievements, notable_events, description
            ('Apollo 11', 'NASA', 'Crewed Lunar Landing', '1969-07-16', '1969-07-24', 'Completed', 'Moon', 'Apollo Command/Service Module + Lunar Module', 3, 8.14, 25400, 'Saturn V', 'First crewed lunar landing', 'First humans on Moon, lunar samples returned', 'Neil Armstrong first words: "That\'s one small step for man, one giant leap for mankind"', 'Historic first crewed lunar landing mission that achieved Kennedy\'s goal of landing humans on Moon'),
            
            ('Voyager 1', 'NASA', 'Interplanetary Probe', '1977-09-05', 'Ongoing', 'Active', 'Interstellar Space', 'Voyager spacecraft', 0, 16800, 865, 'Titan IIIE', 'Outer planet exploration, interstellar mission', 'First spacecraft to reach interstellar space, Golden Record', 'Crossed heliopause in 2012, still transmitting data', 'Longest-operating spacecraft, first to enter interstellar space with Golden Record for potential alien contact'),
            
            ('International Space Station', 'NASA/Roscosmos/ESA/JAXA/CSA', 'Space Station', '1998-11-20', 'Ongoing', 'Active', 'Low Earth Orbit', 'Modular Space Station', 3-7, 9100, 150000, 'Multiple', 'Long-duration human spaceflight, scientific research', 'Longest continuously inhabited space station, 20+ years', 'Over 250 visitors from 19 countries, 3000+ experiments', 'Largest human-made object in space, international cooperation symbol, continuous human presence since 2000'),
            
            ('Mars Perseverance Rover', 'NASA', 'Mars Rover', '2020-07-30', 'Ongoing', 'Active', 'Mars', 'Perseverance Rover', 0, 1200, 2700, 'Atlas V 541', 'Search for ancient microbial life, collect samples', 'First helicopter flight on another planet (Ingenuity)', 'Ingenuity helicopter exceeded planned flights, sample collection ongoing', 'Most advanced Mars rover with helicopter companion, searching for signs of ancient life'),
            
            ('SpaceX Crew Dragon Demo-2', 'SpaceX/NASA', 'Crewed Test Flight', '2020-05-30', '2020-08-02', 'Completed', 'International Space Station', 'Crew Dragon', 2, 64, 3100, 'Falcon 9', 'First crewed commercial spaceflight', 'Restored US human spaceflight capability', 'First crewed launch from US soil since 2011', 'Historic first crewed commercial spaceflight, ending US dependence on Russian Soyuz'),
            
            ('Hubble Space Telescope', 'NASA/ESA', 'Space Observatory', '1990-04-24', 'Ongoing', 'Active', 'Low Earth Orbit', 'Hubble Space Telescope', 0, 12400, 16000, 'Space Shuttle Discovery', 'Deep space observations, astronomical research', 'Revolutionary astronomical discoveries, 1.5 million observations', 'Initial mirror flaw corrected by servicing mission, multiple upgrades', 'Most famous space telescope, revolutionized astronomy with stunning images and discoveries'),
            
            ('Cassini-Huygens', 'NASA/ESA/ASI', 'Saturn Orbiter', '1997-10-15', '2017-09-15', 'Completed', 'Saturn', 'Cassini Orbiter + Huygens Lander', 0, 7300, 3900, 'Titan IV', 'Saturn system exploration', 'Detailed study of Saturn, moons, and rings', 'Huygens landed on Titan, discovered water geysers on Enceladus', 'Most successful outer planet mission, revealed Saturn system complexity and potential for life'),
            
            ('James Webb Space Telescope', 'NASA/ESA/CSA', 'Space Observatory', '2021-12-25', 'Ongoing', 'Active', 'L2 Lagrange Point', 'James Webb Space Telescope', 0, 1200, 10000, 'Ariane 5', 'Infrared astronomy, early universe observations', 'Deepest infrared images of universe, exoplanet atmospheres', 'Perfect deployment, exceeding performance expectations', 'Most powerful space telescope ever built, successor to Hubble, observing first galaxies and exoplanet atmospheres'),
            
            ('Chang\'e 4', 'CNSA', 'Lunar Lander', '2018-12-07', '2022-04-30', 'Completed', 'Moon Far Side', 'Chang\'e 4 Lander + Yutu-2 Rover', 0, 1238, 180, 'Long March 3B', 'First far side lunar landing', 'First successful far side landing, radio astronomy', 'Relay satellite enabled communication, biological experiments', 'Historic first landing on Moon\'s far side, advancing lunar exploration and radio astronomy'),
            
            ('New Horizons', 'NASA', 'Interplanetary Probe', '2006-01-19', 'Ongoing', 'Active', 'Kuiper Belt', 'New Horizons spacecraft', 0, 6400, 720, 'Atlas V 551', 'Pluto flyby, Kuiper Belt exploration', 'First close-up images of Pluto, Kuiper Belt object flyby', 'Revealed Pluto\'s complexity, heart-shaped feature, active geology', 'Fastest spacecraft at launch, revealed Pluto as dynamic world, continuing Kuiper Belt exploration')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO missions 
            (name, agency, mission_type, launch_date, end_date, status, destination, spacecraft, 
             crew_size, duration_days, cost_million_usd, launch_vehicle, objectives, achievements, 
             notable_events, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', missions)
    
    def _populate_spacecraft(self, cursor):
        """Populate spacecraft data."""
        spacecraft = [
            # name, type, manufacturer, first_flight, status, crew_capacity, mass_kg, length_m, diameter_m, power_source, propulsion, missions_flown, notable_features, description
            ('Space Shuttle', 'Reusable Orbiter', 'NASA/Rockwell', '1981-04-12', 'Retired', 7, 78000, 37.2, 8.7, 'Fuel cells', 'Main engines + SRBs', 135, 'Reusable, cargo bay, robotic arm', 'Reusable spacecraft that enabled ISS construction and Hubble servicing'),
            
            ('Soyuz', 'Crew Vehicle', 'Roscosmos/RSC Energia', '1967-04-23', 'Active', 3, 7150, 7.5, 2.7, 'Solar panels + batteries', 'Hypergolic propellant', 140, 'Reliable, proven design, orbital module', 'Most reliable crewed spacecraft with over 140 flights and excellent safety record'),
            
            ('Crew Dragon', 'Commercial Crew Vehicle', 'SpaceX', '2020-05-30', 'Active', 7, 12055, 8.1, 4.0, 'Solar panels', 'SuperDraco thrusters', 8, 'Touchscreen controls, autonomous docking, reusable', 'First commercial crewed spacecraft with modern touchscreen interface and reusability'),
            
            ('Falcon 9', 'Launch Vehicle', 'SpaceX', '2010-06-04', 'Active', 0, 549000, 70, 3.7, 'RP-1/LOX', 'Merlin engines', 200, 'Reusable first stage, grid fins, landing legs', 'Revolutionary reusable rocket that dramatically reduced launch costs'),
            
            ('Saturn V', 'Heavy Launch Vehicle', 'NASA/Boeing', '1967-11-09', 'Retired', 0, 2970000, 110.6, 10.1, 'RP-1/LOX + LH2/LOX', 'F-1 and J-2 engines', 13, 'Most powerful successful rocket, Moon missions', 'Most powerful rocket ever successfully flown, enabled Apollo lunar missions'),
            
            ('Starship', 'Super Heavy Lift Vehicle', 'SpaceX', '2023-04-20', 'Development', 100, 5000000, 120, 9.0, 'Methane/LOX', 'Raptor engines', 2, 'Fully reusable, Mars-capable, largest rocket', 'Next-generation fully reusable super heavy-lift vehicle designed for Mars colonization')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO spacecraft 
            (name, type, manufacturer, first_flight, status, crew_capacity, mass_kg, length_m, 
             diameter_m, power_source, propulsion, missions_flown, notable_features, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', spacecraft)
    
    def _populate_astronauts(self, cursor):
        """Populate astronauts data."""
        astronauts = [
            # name, nationality, agency, birth_date, selection_year, total_flights, total_eva_hours, total_space_time_days, missions, achievements, notable_records, description
            ('Neil Armstrong', 'American', 'NASA', '1930-08-05', 1962, 2, 2.5, 8.14, 'Gemini 8, Apollo 11', 'First person to walk on Moon', 'First human to step on lunar surface', 'Commander of Apollo 11, first person to walk on Moon with famous words about giant leap for mankind'),
            
            ('Yuri Gagarin', 'Soviet', 'Roscosmos', '1934-03-09', 1959, 1, 0, 0.07, 'Vostok 1', 'First human in space', 'First human spaceflight, orbital flight', 'First human to journey into outer space and orbit Earth, opening space age for humanity'),
            
            ('Peggy Whitson', 'American', 'NASA', '1960-02-09', 1996, 3, 60.21, 665, 'Expedition 5, 16, 50/51', 'Most spacewalks by woman, oldest woman in space', 'Record holder for most EVA time by woman, most time in space by American', 'Record-breaking astronaut with most spacewalk time by any woman and most cumulative time in space by American'),
            
            ('Chris Hadfield', 'Canadian', 'CSA', '1959-08-29', 1992, 3, 14.85, 166, 'STS-74, STS-100, Expedition 34/35', 'ISS Commander, space educator, musician', 'First Canadian ISS Commander, viral space videos', 'Canadian astronaut who became ISS Commander and famous for educational space videos and music'),
            
            ('Valentina Tereshkova', 'Soviet', 'Roscosmos', '1937-03-06', 1962, 1, 0, 2.95, 'Vostok 6', 'First woman in space', 'First and youngest woman to fly in space', 'First woman to travel to space, orbiting Earth 48 times and inspiring generations of female astronauts'),
            
            ('Scott Kelly', 'American', 'NASA', '1964-02-21', 1996, 4, 18.02, 520, 'STS-103, STS-118, Expedition 25/26, 43-46', 'Year in Space mission, twin study', 'Longest single spaceflight by American, medical research subject', 'Participated in year-long ISS mission for medical research, part of twin study with brother Mark Kelly')
        ]
        
        cursor.executemany('''
            INSERT OR REPLACE INTO astronauts 
            (name, nationality, agency, birth_date, selection_year, total_flights, total_eva_hours, 
             total_space_time_days, missions, achievements, notable_records, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', astronauts)
    
    def query_mission(self, query: str) -> Dict[str, Any]:
        """Query mission information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM missions 
                    WHERE LOWER(name) LIKE LOWER(?) 
                    OR LOWER(agency) LIKE LOWER(?)
                    OR LOWER(mission_type) LIKE LOWER(?)
                    OR LOWER(destination) LIKE LOWER(?)
                    OR LOWER(spacecraft) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    missions = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'mission_info',
                        'missions': missions,
                        'count': len(missions)
                    }
                
                return {'type': 'no_results', 'message': f'No missions found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Mission query failed: {e}")
            return {'type': 'error', 'message': 'Mission query failed'}
    
    def query_spacecraft(self, query: str) -> Dict[str, Any]:
        """Query spacecraft information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM spacecraft 
                    WHERE LOWER(name) LIKE LOWER(?) 
                    OR LOWER(type) LIKE LOWER(?)
                    OR LOWER(manufacturer) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    spacecraft = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'spacecraft_info',
                        'spacecraft': spacecraft,
                        'count': len(spacecraft)
                    }
                
                return {'type': 'no_results', 'message': f'No spacecraft found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Spacecraft query failed: {e}")
            return {'type': 'error', 'message': 'Spacecraft query failed'}
    
    def query_astronaut(self, query: str) -> Dict[str, Any]:
        """Query astronaut information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT * FROM astronauts 
                    WHERE LOWER(name) LIKE LOWER(?) 
                    OR LOWER(nationality) LIKE LOWER(?)
                    OR LOWER(agency) LIKE LOWER(?)
                ''', (f'%{query}%', f'%{query}%', f'%{query}%'))
                
                results = cursor.fetchall()
                if results:
                    columns = [desc[0] for desc in cursor.description]
                    astronauts = [dict(zip(columns, row)) for row in results]
                    return {
                        'type': 'astronaut_info',
                        'astronauts': astronauts,
                        'count': len(astronauts)
                    }
                
                return {'type': 'no_results', 'message': f'No astronauts found matching "{query}"'}
                
        except Exception as e:
            self.logger.error(f"Astronaut query failed: {e}")
            return {'type': 'error', 'message': 'Astronaut query failed'}
    
    def query_space_missions(self, query: str) -> Dict[str, Any]:
        """General space missions query across all types."""
        try:
            # Try missions first
            mission_result = self.query_mission(query)
            if mission_result['type'] != 'no_results':
                return mission_result
            
            # Try spacecraft
            spacecraft_result = self.query_spacecraft(query)
            if spacecraft_result['type'] != 'no_results':
                return spacecraft_result
            
            # Try astronauts
            astronaut_result = self.query_astronaut(query)
            if astronaut_result['type'] != 'no_results':
                return astronaut_result
            
            return {'type': 'no_results', 'message': f'No space missions data found matching "{query}"'}
            
        except Exception as e:
            self.logger.error(f"Space missions query failed: {e}")
            return {'type': 'error', 'message': 'Space missions query failed'}
    
    def format_missions_info(self, data: Dict[str, Any]) -> str:
        """Format space missions information for display."""
        if data['type'] == 'mission_info':
            output = []
            for mission in data['missions']:
                info = [f"**{mission['name']} - {mission['mission_type']}**"]
                
                if mission['agency']:
                    info.append(f"Agency: {mission['agency']}")
                
                if mission['launch_date']:
                    info.append(f"Launch Date: {mission['launch_date']}")
                
                if mission['status']:
                    info.append(f"Status: {mission['status']}")
                
                if mission['destination']:
                    info.append(f"Destination: {mission['destination']}")
                
                if mission['spacecraft']:
                    info.append(f"Spacecraft: {mission['spacecraft']}")
                
                if mission['crew_size']:
                    info.append(f"Crew Size: {mission['crew_size']}")
                
                if mission['duration_days']:
                    info.append(f"Duration: {mission['duration_days']:.1f} days")
                
                if mission['cost_million_usd']:
                    info.append(f"Cost: ${mission['cost_million_usd']:,.0f} million USD")
                
                if mission['objectives']:
                    info.append(f"Objectives: {mission['objectives']}")
                
                if mission['achievements']:
                    info.append(f"Achievements: {mission['achievements']}")
                
                if mission['notable_events']:
                    info.append(f"Notable Events: {mission['notable_events']}")
                
                if mission['description']:
                    info.append(f"Description: {mission['description']}")
                
                output.append('\n'.join(info))
            
            return '\n\n'.join(output)
        
        elif data['type'] == 'spacecraft_info':
            output = []
            for craft in data['spacecraft']:
                info = [f"**{craft['name']} - {craft['type']}**"]
                
                if craft['manufacturer']:
                    info.append(f"Manufacturer: {craft['manufacturer']}")
                
                if craft['first_flight']:
                    info.append(f"First Flight: {craft['first_flight']}")
                
                if craft['status']:
                    info.append(f"Status: {craft['status']}")
                
                if craft['crew_capacity']:
                    info.append(f"Crew Capacity: {craft['crew_capacity']}")
                
                if craft['mass_kg']:
                    info.append(f"Mass: {craft['mass_kg']:,.0f} kg")
                
                if craft['length_m'] and craft['diameter_m']:
                    info.append(f"Dimensions: {craft['length_m']:.1f}m length × {craft['diameter_m']:.1f}m diameter")
                
                if craft['power_source']:
                    info.append(f"Power Source: {craft['power_source']}")
                
                if craft['propulsion']:
                    info.append(f"Propulsion: {craft['propulsion']}")
                
                if craft['missions_flown']:
                    info.append(f"Missions Flown: {craft['missions_flown']}")
                
                if craft['notable_features']:
                    info.append(f"Notable Features: {craft['notable_features']}")
                
                if craft['description']:
                    info.append(f"Description: {craft['description']}")
                
                output.append('\n'.join(info))
            
            return '\n\n'.join(output)
        
        elif data['type'] == 'astronaut_info':
            output = []
            for astronaut in data['astronauts']:
                info = [f"**{astronaut['name']} - {astronaut['nationality']} Astronaut**"]
                
                if astronaut['agency']:
                    info.append(f"Agency: {astronaut['agency']}")
                
                if astronaut['birth_date']:
                    info.append(f"Born: {astronaut['birth_date']}")
                
                if astronaut['selection_year']:
                    info.append(f"Selected: {astronaut['selection_year']}")
                
                if astronaut['total_flights']:
                    info.append(f"Total Flights: {astronaut['total_flights']}")
                
                if astronaut['total_space_time_days']:
                    info.append(f"Total Space Time: {astronaut['total_space_time_days']:.1f} days")
                
                if astronaut['total_eva_hours']:
                    info.append(f"Total EVA Time: {astronaut['total_eva_hours']:.1f} hours")
                
                if astronaut['missions']:
                    info.append(f"Missions: {astronaut['missions']}")
                
                if astronaut['achievements']:
                    info.append(f"Achievements: {astronaut['achievements']}")
                
                if astronaut['notable_records']:
                    info.append(f"Notable Records: {astronaut['notable_records']}")
                
                if astronaut['description']:
                    info.append(f"Description: {astronaut['description']}")
                
                output.append('\n'.join(info))
            
            return '\n\n'.join(output)
        
        elif data['type'] == 'no_results':
            return data['message']
        
        elif data['type'] == 'error':
            return f"Error: {data['message']}"
        
        else:
            return "Unknown space missions data format"
