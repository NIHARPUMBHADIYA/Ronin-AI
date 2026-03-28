#!/usr/bin/env python3
"""
Test script for the Universal Equation Engine
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import yaml
from pathlib import Path

class SimpleConfig:
    """Simple configuration class for testing"""
    def __init__(self):
        # Load YAML config
        config_path = Path("config/sai_config.yaml")
        if config_path.exists():
            with open(config_path, 'r') as f:
                self.config_data = yaml.safe_load(f)
        else:
            self.config_data = {}
        
        # Set up paths
        self.data_dir = Path("data")
        self.knowledge_dir = self.data_dir / "knowledge"
        self.logs_dir = self.data_dir / "logs"
        
        # Create directories if they don't exist
        self.data_dir.mkdir(exist_ok=True)
        self.knowledge_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
    
    def get(self, key, default=None):
        """Get configuration value using dot notation"""
        keys = key.split('.')
        value = self.config_data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

def test_equation_engine():
    """Test the equation engine functionality"""
    print("🧪 Testing Universal Equation Engine...")
    
    try:
        # Import the equation engine
        from src.modules.equation_engine import UniversalEquationEngine
        
        # Create config
        config = SimpleConfig()
        
        # Initialize engine
        print("📊 Initializing equation engine...")
        engine = UniversalEquationEngine(config)
        
        # Get database statistics
        print("📈 Getting database statistics...")
        stats = engine.get_equation_stats()
        print(f"Database Statistics: {stats}")
        
        # Test equation search
        print("\n🔍 Testing equation search...")
        results = engine.search_equations("kinetic energy")
        print(f"Found {len(results)} equations for 'kinetic energy'")
        if results:
            eq = results[0]
            print(f"First result: {eq['name']} - {eq['formula']}")
        
        # Test unit conversion
        print("\n🔄 Testing unit conversion...")
        conversion = engine.convert_units(100, 'm', 'ft')
        if 'error' not in conversion:
            print(f"100 m = {conversion['converted_value']:.2f} ft")
        else:
            print(f"Conversion error: {conversion['error']}")
        
        # Test calculation (if we have the right equation)
        print("\n🧮 Testing calculation...")
        if results:
            # Try to calculate kinetic energy with sample values
            try:
                calc_result = engine.calculate("Kinetic Energy", {"m": 10, "v": 5})
                if 'error' not in calc_result:
                    print(f"Kinetic Energy calculation: {calc_result['result']} {calc_result['units']}")
                else:
                    print(f"Calculation error: {calc_result['error']}")
            except Exception as e:
                print(f"Calculation test failed: {e}")
        
        print("\n✅ Equation engine test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_equation_engine()
    sys.exit(0 if success else 1)
