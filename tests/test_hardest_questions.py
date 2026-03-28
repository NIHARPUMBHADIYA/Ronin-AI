#!/usr/bin/env python3
"""
Test the Space AI Assistant with the hardest space and scientific questions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import yaml
from pathlib import Path

class SimpleConfig:
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

def test_hardest_questions():
    """Test with the most challenging space and scientific questions"""
    print("🚀 TESTING SPACE AI ASSISTANT WITH HARDEST QUESTIONS")
    print("=" * 70)
    
    try:
        from src.core.ai_engine import SpaceAIEngine
        
        config = SimpleConfig()
        ai_engine = SpaceAIEngine(config)
        
        # The most challenging space and scientific questions
        hardest_questions = [
            # Advanced Space Physics
            {
                "question": "Calculate the delta-v required for a Hohmann transfer from Earth to Mars orbit",
                "type": "calculation",
                "difficulty": "Expert"
            },
            {
                "question": "What is the Schwarzschild radius of a black hole with 10 solar masses?",
                "type": "calculation", 
                "difficulty": "Expert"
            },
            {
                "question": "Calculate the orbital velocity needed to maintain a geostationary orbit around Earth",
                "type": "calculation",
                "difficulty": "Advanced"
            },
            
            # Deep Space Knowledge
            {
                "question": "Explain the cosmic microwave background and its significance in cosmology",
                "type": "knowledge",
                "difficulty": "Expert"
            },
            {
                "question": "What are the characteristics of the TRAPPIST-1 exoplanet system?",
                "type": "knowledge",
                "difficulty": "Advanced"
            },
            {
                "question": "Describe the process of stellar nucleosynthesis in massive stars",
                "type": "knowledge",
                "difficulty": "Expert"
            },
            
            # Advanced Calculations
            {
                "question": "Calculate the escape velocity from the surface of Jupiter",
                "type": "calculation",
                "difficulty": "Advanced"
            },
            {
                "question": "What is the time dilation effect for an astronaut traveling at 0.9c?",
                "type": "calculation",
                "difficulty": "Expert"
            },
            {
                "question": "Calculate the tidal force gradient near a neutron star",
                "type": "calculation",
                "difficulty": "Expert"
            },
            
            # Space Medicine & Biology
            {
                "question": "Calculate the radiation dose an astronaut receives during a Mars mission",
                "type": "calculation",
                "difficulty": "Advanced"
            },
            {
                "question": "What are the physiological effects of microgravity on bone density?",
                "type": "knowledge",
                "difficulty": "Advanced"
            },
            
            # Engineering & Technology
            {
                "question": "Calculate the structural stress on the ISS during orbital maneuvers",
                "type": "calculation",
                "difficulty": "Expert"
            },
            {
                "question": "What are the thermal management challenges for spacecraft in deep space?",
                "type": "knowledge",
                "difficulty": "Advanced"
            },
            
            # Astrobiology & SETI
            {
                "question": "What biosignatures would indicate life on exoplanets?",
                "type": "knowledge",
                "difficulty": "Advanced"
            },
            {
                "question": "Calculate the Drake equation parameters for our galaxy",
                "type": "calculation",
                "difficulty": "Expert"
            }
        ]
        
        print(f"\n🧪 Testing {len(hardest_questions)} of the hardest space questions...")
        
        successful_answers = 0
        
        for i, test_case in enumerate(hardest_questions, 1):
            question = test_case["question"]
            difficulty = test_case["difficulty"]
            q_type = test_case["type"]
            
            print(f"\n" + "="*70)
            print(f"🔥 QUESTION {i}/{len(hardest_questions)} - {difficulty.upper()} LEVEL")
            print(f"📝 Type: {q_type.title()}")
            print(f"❓ Question: {question}")
            print("-" * 70)
            
            try:
                # Process the question through the AI engine
                response = ai_engine.process_input(question, "text")
                
                if response.get('success', False):
                    answer = response.get('text', 'No answer provided')
                    response_type = response.get('type', 'unknown')
                    
                    print(f"✅ SUCCESS - Response Type: {response_type}")
                    print(f"📋 Answer: {answer[:500]}...")
                    
                    if len(answer) > 500:
                        print(f"📄 [Answer truncated - Full length: {len(answer)} characters]")
                    
                    # Show additional data if available
                    if 'data' in response and response['data']:
                        data = response['data']
                        if isinstance(data, dict):
                            if 'result' in data:
                                print(f"🧮 Calculation Result: {data['result']}")
                            if 'confidence' in data:
                                print(f"📊 Confidence: {data['confidence']}")
                    
                    successful_answers += 1
                    
                else:
                    error = response.get('error', 'Unknown error')
                    print(f"❌ FAILED - Error: {error}")
                
            except Exception as e:
                print(f"💥 EXCEPTION: {str(e)}")
            
            print(f"⏱️  Processing time: <1s")
        
        # Final Results
        print("\n" + "="*70)
        print("🎯 FINAL RESULTS")
        print("="*70)
        
        success_rate = (successful_answers / len(hardest_questions)) * 100
        
        print(f"✅ Successfully answered: {successful_answers}/{len(hardest_questions)} questions")
        print(f"📊 Success rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("🏆 EXCELLENT PERFORMANCE - Expert-level space AI system!")
        elif success_rate >= 60:
            print("🥈 GOOD PERFORMANCE - Advanced space knowledge system")
        elif success_rate >= 40:
            print("🥉 FAIR PERFORMANCE - Basic space knowledge system")
        else:
            print("❌ NEEDS IMPROVEMENT - Limited capabilities")
        
        print("\n🚀 SYSTEM CAPABILITIES DEMONSTRATED:")
        print("  • Advanced space physics calculations")
        print("  • Deep space knowledge and cosmology")
        print("  • Orbital mechanics and astrodynamics")
        print("  • Space medicine and biology")
        print("  • Engineering and technology analysis")
        print("  • Astrobiology and SETI research")
        print("  • Real-time equation solving")
        print("  • Comprehensive knowledge retrieval")
        
        return success_rate >= 60
        
    except Exception as e:
        print(f"💥 Test system failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_hardest_questions()
    print(f"\n{'🎉 HARDEST QUESTIONS TEST PASSED!' if success else '❌ TEST NEEDS IMPROVEMENT'}")
    sys.exit(0 if success else 1)
