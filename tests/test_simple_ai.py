#!/usr/bin/env python3
"""
Simple test to check AI understanding with clear output
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.core.ai_engine import SpaceAIEngine

class SimpleConfig:
    def __init__(self):
        self.data_dir = Path("data")
        self.knowledge_dir = self.data_dir / "knowledge"
        self.logs_dir = self.data_dir / "logs"
        
        self.data_dir.mkdir(exist_ok=True)
        self.knowledge_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
    
    def get(self, key, default=None):
        return default

def test_questions():
    """Test AI with simple questions"""
    
    print("🧠 TESTING AI UNDERSTANDING")
    print("=" * 40)
    
    config = SimpleConfig()
    ai_engine = SpaceAIEngine(config)
    
    questions = [
        "What is Mars?",
        "Calculate escape velocity of Earth",
        "Tell me about the Moon",
        "Convert 100 km to miles",
        "How far is Jupiter?",
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n{i}. Question: {question}")
        print("-" * 30)
        
        try:
            response = ai_engine.process_input(question, "text")
            success = response.get('success', False)
            text = response.get('text', 'No response')
            
            print(f"Success: {success}")
            print(f"Response: {text[:150]}...")
            
            if not success:
                print(f"Error: {response.get('error', 'Unknown error')}")
                
        except Exception as e:
            print(f"Exception: {e}")
    
    print("\n" + "=" * 40)
    print("Test completed!")

if __name__ == "__main__":
    test_questions()
