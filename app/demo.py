#!/usr/bin/env python3
"""
Demo script for Space AI Assistant - Shows key functionality
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def demo_basic_functionality():
    """Demonstrate basic SAI functionality."""
    print("🚀 SPACE AI ASSISTANT - DEMO")
    print("=" * 50)
    print()
    
    try:
        # Import core components
        from src.utils.config import Config
        from src.modules.nlu_engine import NLUEngine
        from src.modules.calculator import SpaceCalculator
        from src.modules.knowledge_base import SpaceKnowledgeBase
        
        print("✅ Core modules imported successfully")
        
        # Initialize configuration
        config = Config()
        print("✅ Configuration loaded")
        
        # Initialize NLU engine
        nlu = NLUEngine(config)
        print("✅ NLU Engine initialized")
        
        # Initialize calculator
        calculator = SpaceCalculator(config)
        print("✅ Space Calculator initialized")
        
        # Initialize knowledge base
        knowledge_base = SpaceKnowledgeBase(config)
        print("✅ Knowledge Base initialized")
        
        print("\n" + "=" * 50)
        print("DEMONSTRATION QUERIES")
        print("=" * 50)
        
        # Demo queries
        demo_queries = [
            "Calculate escape velocity for Mars",
            "What is the orbital period of the ISS?",
            "Tell me about Jupiter",
            "Convert 100 kilometers to miles"
        ]
        
        for query in demo_queries:
            print(f"\n🤖 Query: {query}")
            
            # Parse with NLU
            nlu_result = nlu.parse(query)
            intent = nlu_result.get('intent', 'unknown')
            confidence = nlu_result.get('confidence', 0.0)
            
            print(f"   Intent: {intent} (confidence: {confidence:.2f})")
            
            # Route to appropriate handler
            if intent in ['calculate', 'compute']:
                result = calculator.calculate(nlu_result)
                print(f"   Result: {result.get('explanation', 'No explanation')}")
            elif intent in ['knowledge', 'info', 'what_is']:
                result = knowledge_base.query(nlu_result)
                answer = result.get('answer', 'No answer found')
                print(f"   Answer: {answer[:100]}{'...' if len(answer) > 100 else ''}")
            else:
                print(f"   Handler: Would route to {intent} handler")
        
        print("\n" + "=" * 50)
        print("✅ DEMO COMPLETED SUCCESSFULLY")
        print("The Space AI Assistant is ready for astronaut use!")
        print("\nTo start the full system:")
        print("  python main.py")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("Please run setup.py first to initialize the system.")

if __name__ == "__main__":
    demo_basic_functionality()
