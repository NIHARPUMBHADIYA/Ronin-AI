#!/usr/bin/env python3
"""
Test script for Space AI Assistant system integration.
"""

import sys
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing module imports...")
    
    try:
        from src.utils.config import Config
        from src.utils.logger import setup_logger, MissionLogger
        from src.core.ai_engine import SpaceAIEngine
        from src.modules.nlu_engine import NLUEngine
        from src.modules.knowledge_base import SpaceKnowledgeBase
        from src.modules.calculator import SpaceCalculator
        from src.modules.mission_support import MissionSupport
        from src.modules.emergency_system import EmergencySystem
        from src.interface.text_interface import TextInterface
        from src.interface.voice_interface import VoiceInterface
        from src.interface.gui_interface import GUIInterface
        
        print("✅ All modules imported successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def test_configuration():
    """Test configuration loading."""
    print("Testing configuration...")
    
    try:
        from src.utils.config import Config
        
        config = Config()
        
        # Test basic config access
        assert config.enable_voice is not None
        assert config.enable_text is not None
        assert config.offline_mode is not None
        
        print("✅ Configuration loaded successfully")
        return True
        
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_nlu_engine():
    """Test Natural Language Understanding engine."""
    print("Testing NLU Engine...")
    
    try:
        from src.utils.config import Config
        from src.modules.nlu_engine import NLUEngine
        
        config = Config()
        nlu = NLUEngine(config)
        
        # Test basic parsing
        test_queries = [
            "Calculate escape velocity for Mars",
            "What is the orbital period of the ISS?",
            "Remind me to check oxygen levels in 30 minutes",
            "Show EVA checklist",
            "Emergency fire detected"
        ]
        
        for query in test_queries:
            result = nlu.parse(query)
            assert 'intent' in result
            assert 'confidence' in result
            print(f"  ✓ Parsed: '{query}' -> Intent: {result['intent']}")
        
        print("✅ NLU Engine working correctly")
        return True
        
    except Exception as e:
        print(f"❌ NLU Engine error: {e}")
        return False

def test_knowledge_base():
    """Test knowledge base functionality."""
    print("Testing Knowledge Base...")
    
    try:
        from src.utils.config import Config
        from src.modules.knowledge_base import SpaceKnowledgeBase
        from src.modules.nlu_engine import NLUEngine
        
        config = Config()
        kb = SpaceKnowledgeBase(config)
        nlu = NLUEngine(config)
        
        # Test knowledge queries
        test_queries = [
            "What is Mars?",
            "Tell me about the ISS",
            "What is the speed of light?"
        ]
        
        for query in test_queries:
            nlu_result = nlu.parse(query)
            kb_result = kb.query(nlu_result)
            assert 'answer' in kb_result
            print(f"  ✓ Query: '{query}' -> Answer found")
        
        print("✅ Knowledge Base working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Knowledge Base error: {e}")
        return False

def test_calculator():
    """Test space calculator functionality."""
    print("Testing Space Calculator...")
    
    try:
        from src.utils.config import Config
        from src.modules.calculator import SpaceCalculator
        from src.modules.nlu_engine import NLUEngine
        
        config = Config()
        calc = SpaceCalculator(config)
        nlu = NLUEngine(config)
        
        # Test calculations
        test_queries = [
            "Calculate escape velocity for Earth",
            "What is the orbital period of a satellite at 400 km?",
            "Convert 100 km to miles",
            "What is the surface gravity on Mars?"
        ]
        
        for query in test_queries:
            nlu_result = nlu.parse(query)
            calc_result = calc.calculate(nlu_result)
            assert 'explanation' in calc_result
            print(f"  ✓ Calculation: '{query}' -> Result computed")
        
        print("✅ Space Calculator working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Space Calculator error: {e}")
        return False

def test_ai_engine():
    """Test the main AI engine integration."""
    print("Testing AI Engine Integration...")
    
    try:
        from src.utils.config import Config
        from src.core.ai_engine import SpaceAIEngine
        
        config = Config()
        ai_engine = SpaceAIEngine(config)
        
        # Test various types of queries
        test_queries = [
            ("system status", "system_status"),
            ("what is mars", "knowledge"),
            ("calculate escape velocity for earth", "calculation"),
            ("remind me to check systems in 5 minutes", "reminder"),
            ("show eva checklist", "checklist"),
            ("log oxygen level is 98%", "logging")
        ]
        
        for query, expected_type in test_queries:
            response = ai_engine.process_input(query, input_type="test")
            assert response.get('success') is not None
            print(f"  ✓ Processed: '{query}' -> Type: {response.get('type', 'unknown')}")
        
        ai_engine.shutdown()
        print("✅ AI Engine integration working correctly")
        return True
        
    except Exception as e:
        print(f"❌ AI Engine error: {e}")
        return False

def test_interfaces():
    """Test interface components."""
    print("Testing Interfaces...")
    
    try:
        from src.utils.config import Config
        from src.core.ai_engine import SpaceAIEngine
        from src.interface.text_interface import TextInterface
        from src.interface.voice_interface import VoiceInterface
        from src.interface.gui_interface import GUIInterface
        
        config = Config()
        ai_engine = SpaceAIEngine(config)
        
        # Test text interface
        text_interface = TextInterface(ai_engine, config)
        print("  ✓ Text interface initialized")
        
        # Test voice interface
        voice_interface = VoiceInterface(ai_engine, config)
        voice_available = voice_interface.is_voice_available()
        print(f"  ✓ Voice interface initialized (Available: {voice_available})")
        
        # Test GUI interface
        gui_interface = GUIInterface(ai_engine, config)
        print("  ✓ GUI interface initialized")
        
        ai_engine.shutdown()
        print("✅ All interfaces working correctly")
        return True
        
    except Exception as e:
        print(f"❌ Interface error: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 SPACE AI ASSISTANT - SYSTEM INTEGRATION TEST")
    print("=" * 60)
    print()
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_configuration),
        ("NLU Engine", test_nlu_engine),
        ("Knowledge Base", test_knowledge_base),
        ("Space Calculator", test_calculator),
        ("AI Engine Integration", test_ai_engine),
        ("Interface Components", test_interfaces)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Running {test_name}...")
        try:
            if test_func():
                passed += 1
            else:
                print(f"❌ {test_name} failed")
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
        print()
    
    print("=" * 60)
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed! System is ready for use.")
        print("\nTo start the Space AI Assistant:")
        print("  python main.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
