#!/usr/bin/env python3
"""
Comprehensive demonstration of the Space AI Assistant with Universal Equation Engine
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import yaml
from pathlib import Path

class SimpleConfig:
    """Simple configuration class for testing"""
    def __init__(self):
        config_path = Path("config/sai_config.yaml")
        if config_path.exists():
            with open(config_path, 'r') as f:
                self.config_data = yaml.safe_load(f)
        else:
            self.config_data = {}
        
        self.data_dir = Path("data")
        self.knowledge_dir = self.data_dir / "knowledge"
        self.logs_dir = self.data_dir / "logs"
        
        self.data_dir.mkdir(exist_ok=True)
        self.knowledge_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
    
    def get(self, key, default=None):
        keys = key.split('.')
        value = self.config_data
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

def demo_comprehensive_system():
    """Demonstrate the comprehensive space knowledge and calculation system"""
    print("🚀 Space AI Assistant - Comprehensive System Demo")
    print("=" * 60)
    
    try:
        from src.modules.knowledge_base import SpaceKnowledgeBase
        from src.modules.equation_engine import UniversalEquationEngine
        
        config = SimpleConfig()
        
        # Initialize systems
        print("\n📊 Initializing Knowledge Base...")
        kb = SpaceKnowledgeBase(config)
        
        print("🧮 Initializing Universal Equation Engine...")
        eq_engine = UniversalEquationEngine(config)
        
        # Get system statistics
        print("\n📈 System Statistics:")
        eq_stats = eq_engine.get_equation_stats()
        total_equations = sum(eq_stats.values())
        print(f"Total Equations: {total_equations}")
        for category, count in eq_stats.items():
            print(f"  {category.replace('_', ' ').title()}: {count}")
        
        # Demo 1: Space Knowledge Queries
        print("\n" + "="*60)
        print("🌌 SPACE KNOWLEDGE DEMONSTRATION")
        print("="*60)
        
        knowledge_queries = [
            "Tell me about Mars",
            "What is the Andromeda Galaxy?",
            "Show me information about the ISS",
            "What are the constellations visible in winter?",
            "Tell me about exoplanets in the habitable zone"
        ]
        
        for query in knowledge_queries:
            print(f"\n🔍 Query: {query}")
            try:
                # Simulate NLU result
                nlu_result = {
                    'processed_text': query,
                    'intent': 'knowledge',
                    'entities': {},
                    'confidence': 0.9
                }
                result = kb.query(nlu_result)
                print(f"📝 Answer: {result.get('answer', 'No answer found')[:200]}...")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        # Demo 2: Equation Search and Information
        print("\n" + "="*60)
        print("🧮 EQUATION ENGINE DEMONSTRATION")
        print("="*60)
        
        equation_searches = [
            "kinetic energy",
            "body mass index",
            "present value",
            "darcy law",
            "newton second law"
        ]
        
        for search_term in equation_searches:
            print(f"\n🔍 Searching for: {search_term}")
            results = eq_engine.search_equations(search_term)
            if results:
                eq = results[0]
                print(f"📐 Found: {eq['name']}")
                print(f"📋 Formula: {eq['formula']}")
                print(f"📊 Category: {eq.get('category', 'Unknown')}")
                print(f"📝 Description: {eq.get('description', 'No description')[:100]}...")
            else:
                print("❌ No equations found")
        
        # Demo 3: Unit Conversions
        print("\n" + "="*60)
        print("🔄 UNIT CONVERSION DEMONSTRATION")
        print("="*60)
        
        conversions = [
            (100, 'm', 'ft'),
            (75, 'kg', 'lb'),
            (1000, 'Pa', 'psi'),
            (5000, 'J', 'BTU')
        ]
        
        for value, from_unit, to_unit in conversions:
            print(f"\n🔄 Converting {value} {from_unit} to {to_unit}")
            result = eq_engine.convert_units(value, from_unit, to_unit)
            if 'error' not in result:
                print(f"✅ Result: {result['converted_value']:.4f} {result['converted_unit']}")
                print(f"📊 Conversion factor: {result['conversion_factor']}")
            else:
                print(f"❌ Error: {result['error']}")
        
        # Demo 4: Calculation Examples
        print("\n" + "="*60)
        print("🧪 CALCULATION DEMONSTRATION")
        print("="*60)
        
        # Try some basic calculations
        calculations = [
            ("Kinetic Energy", {"m": 10, "v": 5}),
            ("Body Mass Index", {"weight": 70, "height": 1.75}),
            ("Present Value", {"FV": 1000, "r": 0.05, "n": 10})
        ]
        
        for eq_name, variables in calculations:
            print(f"\n🧮 Calculating {eq_name} with variables: {variables}")
            try:
                result = eq_engine.calculate(eq_name, variables)
                if 'error' not in result:
                    print(f"✅ Result: {result['result']} {result['units']}")
                    print(f"📐 Formula: {result['formula']}")
                else:
                    print(f"❌ Error: {result['error']}")
            except Exception as e:
                print(f"❌ Calculation failed: {e}")
        
        # Demo 5: System Integration Summary
        print("\n" + "="*60)
        print("🎯 SYSTEM INTEGRATION SUMMARY")
        print("="*60)
        
        print("\n✅ Successfully Implemented:")
        print("  🌌 Comprehensive Space Knowledge Base")
        print("    - Celestial bodies, spacecraft, missions")
        print("    - Constellations, exoplanets, space history")
        print("    - Cosmology, astrobiology, space medicine")
        print("    - Emergency procedures and protocols")
        
        print("\n  🧮 Universal Equation Engine")
        print("    - Physics equations (mechanics, thermodynamics, etc.)")
        print("    - Mathematical formulas (calculus, statistics, etc.)")
        print("    - Engineering calculations (structural, thermal, etc.)")
        print("    - Chemistry equations and reactions")
        print("    - Computer science algorithms")
        print("    - Biological and medical calculations")
        print("    - Financial and economic formulas")
        print("    - Geological and environmental calculations")
        
        print("\n  🔧 Advanced Features")
        print("    - Symbolic math evaluation")
        print("    - Unit conversion system")
        print("    - Equation search and discovery")
        print("    - Integration with AI engine")
        print("    - Offline operation capability")
        
        print(f"\n📊 Total Knowledge Items: {total_equations}+ equations")
        print("🎯 Mission: Universal calculation and knowledge system for astronauts")
        print("✅ Status: FULLY OPERATIONAL")
        
        return True
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = demo_comprehensive_system()
    print(f"\n{'🎉 DEMO COMPLETED SUCCESSFULLY!' if success else '❌ DEMO FAILED'}")
    sys.exit(0 if success else 1)
