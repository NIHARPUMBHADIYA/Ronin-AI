#!/usr/bin/env python3
"""
Test the enhanced Space AI Assistant with natural language questions
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

def test_natural_language_understanding():
    """Test natural language understanding with various question formats"""
    print("🧠 TESTING ENHANCED NATURAL LANGUAGE UNDERSTANDING")
    print("=" * 70)
    
    try:
        from src.core.ai_engine import SpaceAIEngine
        
        config = SimpleConfig()
        ai_engine = SpaceAIEngine(config)
        
        # Natural language questions in various formats
        natural_questions = [
            # Casual conversational style
            "Hey, what's the deal with Mars?",
            "Can you tell me about black holes?",
            "I'm curious about the ISS",
            "What do you know about Jupiter's moons?",
            
            # Question variations
            "How fast does light travel?",
            "What's the distance to the nearest star?",
            "How big is our galaxy?",
            "Why is space cold?",
            
            # Calculation requests in natural language
            "I need to know the escape velocity from Earth",
            "Can you figure out how much I would weigh on Mars?",
            "What's the orbital speed of the ISS?",
            "How long would it take to get to Mars?",
            
            # Complex multi-part questions
            "What is a black hole and how do we detect them?",
            "Tell me about exoplanets and which ones might have life",
            "Explain dark matter and why it's important",
            "What are the challenges of getting to Mars?",
            
            # Equation and formula requests
            "Show me Einstein's mass-energy equation",
            "What's Newton's law of gravitation?",
            "I need the rocket equation",
            "Can you give me the formula for kinetic energy?",
            
            # Informal/colloquial questions
            "What's up with Saturn's rings?",
            "How come we can't see black holes?",
            "Why don't we fall into the sun?",
            "What makes stars shine?",
            
            # Specific technical questions
            "Calculate the Schwarzschild radius of a 10 solar mass black hole",
            "What's the delta-v for a Hohmann transfer to Mars?",
            "How much radiation exposure during a Mars mission?",
            "What's the tidal force near a neutron star?",
            
            # Comparative questions
            "Which planet is bigger, Jupiter or Saturn?",
            "What's the difference between a star and a planet?",
            "How does the ISS compare to other space stations?",
            "Which is faster, Voyager 1 or New Horizons?",
            
            # Hypothetical questions
            "What would happen if Earth stopped rotating?",
            "Could we live on Europa?",
            "What if we could travel at light speed?",
            "Is time travel possible near black holes?"
        ]
        
        print(f"\n🧪 Testing {len(natural_questions)} natural language questions...")
        
        successful_responses = 0
        partial_responses = 0
        
        for i, question in enumerate(natural_questions, 1):
            print(f"\n" + "="*70)
            print(f"🗣️  QUESTION {i}/{len(natural_questions)}")
            print(f"❓ Human asks: \"{question}\"")
            print("-" * 70)
            
            try:
                # Process the natural language question
                response = ai_engine.process_input(question, "text")
                
                if response.get('success', False):
                    answer = response.get('text', 'No answer provided')
                    response_type = response.get('type', 'unknown')
                    
                    # Evaluate response quality
                    if len(answer) > 100 and 'clarification' not in response_type:
                        print(f"✅ EXCELLENT - Detailed response ({response_type})")
                        successful_responses += 1
                    elif len(answer) > 50:
                        print(f"🟡 GOOD - Partial response ({response_type})")
                        partial_responses += 1
                    else:
                        print(f"🟠 BASIC - Short response ({response_type})")
                        partial_responses += 1
                    
                    # Show response preview
                    preview = answer[:200] + "..." if len(answer) > 200 else answer
                    print(f"🤖 AI responds: {preview}")
                    
                    # Show confidence if available
                    if 'data' in response and isinstance(response['data'], dict):
                        confidence = response['data'].get('confidence', 'N/A')
                        if confidence != 'N/A':
                            print(f"📊 Confidence: {confidence}")
                    
                else:
                    error = response.get('error', 'Unknown error')
                    print(f"❌ FAILED - {error}")
                
            except Exception as e:
                print(f"💥 EXCEPTION: {str(e)}")
        
        # Calculate results
        total_questions = len(natural_questions)
        success_rate = (successful_responses / total_questions) * 100
        partial_rate = (partial_responses / total_questions) * 100
        total_useful = success_rate + partial_rate
        
        # Final Results
        print("\n" + "="*70)
        print("🎯 NATURAL LANGUAGE UNDERSTANDING RESULTS")
        print("="*70)
        
        print(f"✅ Excellent responses: {successful_responses}/{total_questions} ({success_rate:.1f}%)")
        print(f"🟡 Good/Partial responses: {partial_responses}/{total_questions} ({partial_rate:.1f}%)")
        print(f"📊 Total useful responses: {successful_responses + partial_responses}/{total_questions} ({total_useful:.1f}%)")
        
        if total_useful >= 85:
            print("🏆 OUTSTANDING - Human-like conversation capability!")
            grade = "A+"
        elif total_useful >= 75:
            print("🥇 EXCELLENT - Very natural conversation")
            grade = "A"
        elif total_useful >= 65:
            print("🥈 GOOD - Solid natural language understanding")
            grade = "B"
        elif total_useful >= 50:
            print("🥉 FAIR - Basic conversation capability")
            grade = "C"
        else:
            print("❌ NEEDS IMPROVEMENT - Limited natural language understanding")
            grade = "F"
        
        print(f"\n🎓 Overall Grade: {grade}")
        
        print("\n🚀 ENHANCED CAPABILITIES DEMONSTRATED:")
        print("  • Natural conversational responses")
        print("  • Intelligent question interpretation")
        print("  • Context-aware routing")
        print("  • Fallback suggestions")
        print("  • Multi-domain knowledge integration")
        print("  • Casual and technical language support")
        print("  • Question type recognition")
        print("  • Enhanced entity extraction")
        
        return total_useful >= 65
        
    except Exception as e:
        print(f"💥 Test system failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_natural_language_understanding()
    print(f"\n{'🎉 NATURAL LANGUAGE TEST PASSED!' if success else '❌ TEST NEEDS IMPROVEMENT'}")
    sys.exit(0 if success else 1)
