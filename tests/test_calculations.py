#!/usr/bin/env python3
"""
Test script for Advanced Calculator - Simple to Complex Calculations
Demonstrates rapid computation capabilities in minutes.
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.utils.config import Config
from src.core.ai_engine import SpaceAIEngine

def test_calculations():
    """Test various calculation types from simple to complex."""
    
    # Initialize AI Engine
    config_path = Path(__file__).parent / 'config' / 'sai_config.yaml'
    config = Config(str(config_path))
    ai_engine = SpaceAIEngine(config)
    
    print("🚀 **SPACE AI ADVANCED CALCULATOR TEST**")
    print("=" * 60)
    print("Testing calculations from simple to most complex...")
    print()
    
    # Test cases from simple to complex
    test_cases = [
        # Basic Arithmetic
        ("Basic Addition", "2 + 3"),
        ("Complex Arithmetic", "15 * 7 + 23 - 8 / 2"),
        ("Powers and Roots", "sqrt(144) + 2^8"),
        
        # Trigonometry
        ("Trigonometric", "sin(pi/4) + cos(pi/3)"),
        ("Advanced Trig", "tan(45 * pi/180) * cos(60 * pi/180)"),
        
        # Logarithms
        ("Logarithmic", "log(100) + ln(e^3)"),
        ("Complex Log", "log10(1000) * ln(exp(2))"),
        
        # Physics Calculations
        ("Kinetic Energy", "0.5 * 1000 * 25^2"),
        ("Force Calculation", "1500 * 9.81"),
        ("Wave Frequency", "c / 550e-9"),
        
        # Space Calculations
        ("Earth Escape Velocity", "sqrt(2 * G * M_earth / R_earth)"),
        ("Orbital Velocity", "sqrt(G * M_sun / au)"),
        ("Light Travel Time", "au / c"),
        ("Schwarzschild Radius", "2 * G * M_sun / c^2"),
        
        # Advanced Physics
        ("Relativistic Energy", "M_sun * c^2"),
        ("Planck Energy", "sqrt(h * c^5 / G)"),
        ("Stefan-Boltzmann", "sigma * 5778^4"),
        
        # Complex Mathematical
        ("Factorial", "factorial(10)"),
        ("Gamma Function", "gamma(5.5)"),
        ("Exponential Growth", "exp(ln(2) * 10)"),
        
        # Astronomical Distances
        ("Proxima Distance", "4.24 * ly"),
        ("Galactic Center", "26000 * ly"),
        ("Andromeda Distance", "2.537e6 * ly"),
        
        # Extreme Calculations
        ("Avogadro's Number", "N_A"),
        ("Planck Time", "sqrt(h * G / (2 * pi * c^5))"),
        ("Universe Age", "13.8e9 * 365.25 * 24 * 3600"),
    ]
    
    successful_calcs = 0
    total_time = 0
    
    for i, (name, expression) in enumerate(test_cases, 1):
        print(f"**Test {i:2d}: {name}**")
        print(f"Expression: `{expression}`")
        
        start_time = time.time()
        
        try:
            # Create mock NLU result for calculation
            nlu_result = {
                'intent': 'calculate',
                'processed_text': f"calculate {expression}",
                'entities': {},
                'confidence': 0.9
            }
            
            result = ai_engine._handle_calculation(nlu_result)
            calc_time = time.time() - start_time
            total_time += calc_time
            
            if result['success']:
                print(f"✅ **Result:** {result['data']['result']}")
                if result['data'].get('units'):
                    print(f"   Units: {result['data']['units']}")
                print(f"   Type: {result['data']['calculation_type'].replace('_', ' ').title()}")
                print(f"   Time: {calc_time:.4f}s")
                successful_calcs += 1
            else:
                print(f"❌ **Error:** {result.get('error', 'Unknown error')}")
                print(f"   Time: {calc_time:.4f}s")
        
        except Exception as e:
            calc_time = time.time() - start_time
            total_time += calc_time
            print(f"❌ **Exception:** {str(e)}")
            print(f"   Time: {calc_time:.4f}s")
        
        print("-" * 50)
        print()
    
    # Summary
    print("📊 **CALCULATION SUMMARY**")
    print("=" * 60)
    print(f"Total Tests: {len(test_cases)}")
    print(f"Successful: {successful_calcs}")
    print(f"Failed: {len(test_cases) - successful_calcs}")
    print(f"Success Rate: {successful_calcs/len(test_cases)*100:.1f}%")
    print(f"Total Time: {total_time:.3f}s")
    print(f"Average Time: {total_time/len(test_cases):.4f}s per calculation")
    print(f"Calculations per minute: {60/(total_time/len(test_cases)):.1f}")
    print()
    
    if successful_calcs == len(test_cases):
        print("🎉 **ALL CALCULATIONS COMPLETED SUCCESSFULLY!**")
        print("The AI can handle simple to complex calculations rapidly!")
    else:
        print("⚠️  Some calculations failed. Check error messages above.")

def test_interactive_mode():
    """Test interactive calculation mode."""
    print("\n🔬 **INTERACTIVE CALCULATION MODE**")
    print("=" * 60)
    print("Enter mathematical expressions (type 'quit' to exit):")
    print("Examples:")
    print("  - 2 + 3 * 4")
    print("  - sin(pi/2)")
    print("  - sqrt(G * M_sun / au)")
    print("  - factorial(5)")
    print()
    
    config_path = Path(__file__).parent / 'config' / 'sai_config.yaml'
    config = Config(str(config_path))
    ai_engine = SpaceAIEngine(config)
    
    while True:
        try:
            expression = input("Calculate: ").strip()
            
            if expression.lower() in ['quit', 'exit', 'q']:
                break
            
            if not expression:
                continue
            
            start_time = time.time()
            
            nlu_result = {
                'intent': 'calculate',
                'processed_text': f"calculate {expression}",
                'entities': {},
                'confidence': 0.9
            }
            
            result = ai_engine._handle_calculation(nlu_result)
            calc_time = time.time() - start_time
            
            if result['success']:
                print(f"✅ Result: {result['data']['result']}")
                if result['data'].get('units'):
                    print(f"   Units: {result['data']['units']}")
                print(f"   Time: {calc_time:.4f}s")
            else:
                print(f"❌ Error: {result.get('error', 'Unknown error')}")
            
            print()
            
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"❌ Exception: {str(e)}")
            print()

def test_batch_calculations():
    """Test batch calculation processing."""
    print("\n⚡ **BATCH CALCULATION TEST**")
    print("=" * 60)
    
    config_path = Path(__file__).parent / 'config' / 'sai_config.yaml'
    config = Config(str(config_path))
    ai_engine = SpaceAIEngine(config)
    
    # Large batch of calculations
    batch_expressions = [
        "2^10", "sqrt(256)", "log10(1000)", "sin(pi/6)",
        "factorial(7)", "exp(2)", "ln(10)", "cos(pi/4)",
        "tan(pi/3)", "sqrt(2)", "pi^2", "e^3",
        "G * M_sun", "c / 1000", "h * c", "k_b * 300",
        "sigma * 5778^4", "R_earth / 1000", "au / 1e6", "ly / 1e12"
    ]
    
    print(f"Processing {len(batch_expressions)} calculations...")
    
    start_time = time.time()
    results = []
    
    for expr in batch_expressions:
        nlu_result = {
            'intent': 'calculate',
            'processed_text': f"calculate {expr}",
            'entities': {},
            'confidence': 0.9
        }
        
        result = ai_engine._handle_calculation(nlu_result)
        results.append((expr, result))
    
    total_time = time.time() - start_time
    
    successful = sum(1 for _, r in results if r['success'])
    
    print(f"✅ Completed {successful}/{len(batch_expressions)} calculations")
    print(f"⏱️  Total time: {total_time:.3f}s")
    print(f"🚀 Rate: {len(batch_expressions)/total_time:.1f} calculations/second")
    print(f"📈 Rate: {len(batch_expressions)*60/total_time:.0f} calculations/minute")
    
    print("\nSample Results:")
    for i, (expr, result) in enumerate(results[:5]):
        if result['success']:
            print(f"  {expr} = {result['data']['result']}")
        else:
            print(f"  {expr} = ERROR")

if __name__ == "__main__":
    print("🧮 **SPACE AI ADVANCED CALCULATOR TESTING**")
    print("Testing rapid computation from simple to complex calculations")
    print("=" * 80)
    print()
    
    # Run comprehensive tests
    test_calculations()
    
    # Run batch test
    test_batch_calculations()
    
    # Optional interactive mode
    response = input("\nWould you like to try interactive mode? (y/n): ").strip().lower()
    if response in ['y', 'yes']:
        test_interactive_mode()
    
    print("\n🎯 **TESTING COMPLETE**")
    print("The Space AI can now perform rapid calculations from simple arithmetic")
    print("to the most complex space physics computations in minutes!")
