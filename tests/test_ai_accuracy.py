#!/usr/bin/env python3
"""
Test script to diagnose and improve AI text understanding accuracy
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from src.core.ai_engine import SpaceAIEngine
import yaml

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

def test_ai_understanding():
    """Test AI understanding with various question types"""
    
    print("🧠 TESTING AI UNDERSTANDING & ACCURACY")
    print("=" * 50)
    
    # Initialize AI engine
    config = SimpleConfig()
    ai_engine = SpaceAIEngine(config)
    
    # Test questions that should work well
    test_questions = [
        # Simple space knowledge
        "What is Mars?",
        "Tell me about the Moon",
        "How far is Jupiter?",
        
        # Calculations
        "Calculate the escape velocity of Earth",
        "What is the orbital period of the ISS?",
        "Convert 100 km to miles",
        
        # Complex questions
        "What's the distance between Earth and Mars right now?",
        "How do black holes form?",
        "Explain orbital mechanics",
        
        # Conversational style
        "Hey, can you help me understand gravity?",
        "I'm curious about space missions",
        "What makes rockets work?",
        
        # Edge cases
        "asdf random text",
        "Calculate something",
        "Tell me",
    ]
    
    results = []
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n{i}. Testing: '{question}'")
        print("-" * 40)
        
        try:
            response = ai_engine.process_input(question, "text")
            
            success = response.get('success', False)
            response_text = response.get('text', 'No response')
            response_type = response.get('type', 'unknown')
            
            print(f"✅ Success: {success}")
            print(f"📝 Type: {response_type}")
            print(f"💬 Response: {response_text[:200]}...")
            
            results.append({
                'question': question,
                'success': success,
                'type': response_type,
                'response_length': len(response_text),
                'has_meaningful_response': len(response_text) > 50 and 'error' not in response_text.lower()
            })
            
        except Exception as e:
            print(f"❌ Error: {e}")
            results.append({
                'question': question,
                'success': False,
                'error': str(e)
            })
    
    # Analyze results
    print("\n" + "=" * 50)
    print("📊 ANALYSIS RESULTS")
    print("=" * 50)
    
    total_questions = len(results)
    successful_responses = sum(1 for r in results if r.get('success', False))
    meaningful_responses = sum(1 for r in results if r.get('has_meaningful_response', False))
    
    print(f"Total Questions: {total_questions}")
    print(f"Successful Responses: {successful_responses} ({successful_responses/total_questions*100:.1f}%)")
    print(f"Meaningful Responses: {meaningful_responses} ({meaningful_responses/total_questions*100:.1f}%)")
    
    # Identify issues
    print("\n🔍 IDENTIFIED ISSUES:")
    failed_questions = [r for r in results if not r.get('success', False)]
    if failed_questions:
        for fail in failed_questions:
            print(f"❌ '{fail['question']}' - {fail.get('error', 'Unknown error')}")
    
    poor_responses = [r for r in results if r.get('success', False) and not r.get('has_meaningful_response', False)]
    if poor_responses:
        print("\n⚠️ POOR QUALITY RESPONSES:")
        for poor in poor_responses:
            print(f"⚠️ '{poor['question']}' - Response too short or generic")
    
    return results

def test_nlu_accuracy():
    """Test NLU engine specifically"""
    print("\n🎯 TESTING NLU ENGINE ACCURACY")
    print("=" * 50)
    
    from src.modules.nlu_engine import NLUEngine
    
    config = SimpleConfig()
    nlu = NLUEngine(config)
    
    test_cases = [
        ("What is the distance to Mars?", "knowledge"),
        ("Calculate escape velocity", "calculate"),
        ("Show me Newton's laws", "equation"),
        ("Convert 100 km to miles", "unit_conversion"),
        ("Emergency life support failure", "emergency"),
        ("Set reminder for EVA", "reminder"),
        ("System status check", "status"),
    ]
    
    correct_predictions = 0
    
    for text, expected_intent in test_cases:
        result = nlu.parse(text)
        predicted_intent = result.get('intent', 'unknown')
        confidence = result.get('confidence', 0.0)
        
        is_correct = predicted_intent == expected_intent
        if is_correct:
            correct_predictions += 1
        
        print(f"Text: '{text}'")
        print(f"Expected: {expected_intent} | Predicted: {predicted_intent} | Confidence: {confidence:.2f}")
        print(f"✅ Correct" if is_correct else "❌ Wrong")
        print("-" * 40)
    
    accuracy = correct_predictions / len(test_cases) * 100
    print(f"\n🎯 NLU Accuracy: {accuracy:.1f}% ({correct_predictions}/{len(test_cases)})")
    
    return accuracy

if __name__ == "__main__":
    print("🚀 RONIN AI ACCURACY DIAGNOSTIC")
    print("=" * 60)
    
    # Test overall AI understanding
    ai_results = test_ai_understanding()
    
    # Test NLU specifically
    nlu_accuracy = test_nlu_accuracy()
    
    print("\n" + "=" * 60)
    print("🎯 RECOMMENDATIONS FOR IMPROVEMENT")
    print("=" * 60)
    
    if nlu_accuracy < 80:
        print("❌ NLU accuracy is below 80% - needs improvement")
        print("🔧 Recommendations:")
        print("   • Add more intent patterns")
        print("   • Improve entity extraction")
        print("   • Enhance preprocessing")
    
    meaningful_rate = sum(1 for r in ai_results if r.get('has_meaningful_response', False)) / len(ai_results) * 100
    
    if meaningful_rate < 70:
        print("❌ Response quality is below 70% - needs improvement")
        print("🔧 Recommendations:")
        print("   • Enhance knowledge base responses")
        print("   • Improve fallback mechanisms")
        print("   • Add more contextual understanding")
    
    print("\n✨ To achieve ChatGPT-level accuracy:")
    print("   1. Expand intent patterns with more variations")
    print("   2. Add semantic similarity matching")
    print("   3. Implement context-aware responses")
    print("   4. Add conversation memory")
    print("   5. Enhance entity recognition")
