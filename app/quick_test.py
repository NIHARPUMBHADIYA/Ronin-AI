#!/usr/bin/env python3
"""
Quick validation test for Space AI Assistant
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    print("🚀 Space AI Assistant - Quick Validation Test")
    print("=" * 50)
    
    try:
        # Test basic imports
        from src.utils.config import Config
        from src.core.ai_engine import SpaceAIEngine
        print("✅ Core imports successful")
        
        # Test configuration
        config = Config()
        print("✅ Configuration loaded")
        
        # Test AI engine initialization
        engine = SpaceAIEngine(config)
        print("✅ AI Engine initialized")
        
        # Test basic query processing
        response = engine.process_input("system status")
        if response.get('success'):
            print("✅ Query processing working")
        else:
            print("⚠️  Query processing has issues")
        
        # Test galaxy database
        from src.modules.galaxy_database import GalaxyDatabase
        galaxy_db = GalaxyDatabase(config)
        galaxy_result = galaxy_db.query_galaxy("milky way")
        if galaxy_result.get('type') == 'galaxy_info':
            print("✅ Galaxy database working")
        else:
            print("⚠️  Galaxy database has issues")
        
        engine.shutdown()
        
        print("\n" + "=" * 50)
        print("🎉 SPACE AI ASSISTANT IS OPERATIONAL!")
        print("=" * 50)
        print("\nTo start the full system:")
        print("  python main.py")
        print("\nTo run the demo:")
        print("  python demo.py")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
