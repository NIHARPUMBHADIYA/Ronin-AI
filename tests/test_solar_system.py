#!/usr/bin/env python3
"""
Test script for Solar System Database functionality.
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.utils.config import Config
from src.utils.logger import setup_logger
from src.modules.solar_system_database import SolarSystemDatabase

def test_solar_system_database():
    """Test the Solar System Database functionality."""
    print("🚀 Testing Solar System Database...")
    
    # Initialize components
    config = Config('config/sai_config.yaml')
    logger = setup_logger(config.get('logging.level', 'INFO'))
    
    # Initialize Solar System Database
    solar_db = SolarSystemDatabase(config, logger)
    
    # Test queries
    test_queries = [
        "Mars",
        "Jupiter",
        "Europa",
        "Titan", 
        "Ceres",
        "Halley's Comet",
        "Pluto",
        "asteroid belt",
        "dwarf planet"
    ]
    
    print("\n" + "="*60)
    print("SOLAR SYSTEM DATABASE TEST RESULTS")
    print("="*60)
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        print("-" * 40)
        
        try:
            result = solar_db.query_solar_system(query)
            if result['type'] != 'no_results':
                formatted_response = solar_db.format_solar_system_info(result)
                print(formatted_response)
            else:
                print(f"No results found for '{query}'")
        except Exception as e:
            print(f"Error querying '{query}': {e}")
        
        print()

if __name__ == "__main__":
    test_solar_system_database()
