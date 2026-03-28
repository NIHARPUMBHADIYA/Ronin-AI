#!/usr/bin/env python3
"""
Test script to verify AI assistant responses and debug confidence issues.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.core.ai_engine import SpaceAIEngine
from src.utils.config import Config
from src.utils.logger import setup_logger
import logging

def test_ai_responses():
    """Test various types of questions to ensure proper responses."""
    
    # Setup logging
    logger = setup_logger("Test_AI_Responses")
    
    try:
        # Initialize configuration
        config = Config()
        
        # Initialize AI Engine
        logger.info("Initializing AI Engine...")
        ai_engine = SpaceAIEngine(config)
        
        # Test questions
        test_questions = [
            "What is Mars?",
            "Tell me about Jupiter",
            "How big is the sun?",
            "What is the distance to Mars?",
            "Explain black holes",
            "What is gravity?",
            "How does a rocket work?",
            "What is the ISS?",
            "Tell me about the moon",
            "What are exoplanets?",
            "How far is Andromeda galaxy?",
            "What is dark matter?",
            "Explain the Big Bang",
            "What is a neutron star?",
            "How hot is Venus?"
        ]
        
        print("=" * 60)
        print("TESTING AI ASSISTANT RESPONSES")
        print("=" * 60)
        
        for i, question in enumerate(test_questions, 1):
            print(f"\n[TEST {i}] Question: {question}")
            print("-" * 40)
            
            try:
                # Process the question
                response = ai_engine.process_input(question)
                
                # Display results
                print(f"Response Type: {response.get('type', 'unknown')}")
                print(f"Success: {response.get('success', False)}")
                
                if 'confidence' in response:
                    print(f"Confidence: {response['confidence']:.2f}")
                
                response_text = response.get('text', 'No response text')
                print(f"Response: {response_text[:200]}...")
                
                # Check if it's the generic fallback response
                if "I'm not entirely sure what you're asking about" in response_text:
                    print("⚠️  WARNING: Generic fallback response detected!")
                else:
                    print("✅ Proper response generated")
                
            except Exception as e:
                print(f"❌ ERROR: {e}")
            
            print("-" * 40)
        
        print(f"\n{'=' * 60}")
        print("TEST COMPLETED")
        print(f"{'=' * 60}")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        print(f"❌ Test initialization failed: {e}")

if __name__ == "__main__":
    test_ai_responses()
