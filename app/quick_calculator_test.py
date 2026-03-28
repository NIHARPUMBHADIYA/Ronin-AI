#!/usr/bin/env python3
"""
Quick test for Advanced Calculator - Direct testing without full AI engine.
Demonstrates rapid computation capabilities from simple to complex calculations.
"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / 'src'))

from src.modules.advanced_calculator import AdvancedCalculator
import logging

class MockConfig:
    """Mock configuration for testing."""
    def get(self, key, default=None):
        return default

def test_direct_calculations():
    """Test advanced calculator directly."""
    
    print("🚀 **ADVANCED CALCULATOR DIRECT TEST**")
    print("=" * 60)
    print("Testing rapid calculations from simple to most complex...")
    print()
    
    # Initialize calculator directly
    config = MockConfig()
    logger = logging.getLogger("test")
    logger.setLevel(logging.INFO)
    calculator = AdvancedCalculator(config, logger)
    
    # Test cases from simple to extremely complex
    test_cases = [
        # Basic Arithmetic
        ("Basic Addition", "2 + 3"),
        ("Complex Arithmetic", "15 * 7 + 23 - 8 / 2"),
        ("Powers and Roots", "sqrt(144) + 2**8"),
        ("Large Numbers", "123456789 * 987654321"),
        
        # Trigonometry
        ("Sine Function", "sin(pi/4)"),
        ("Cosine Function", "cos(pi/3)"),
        ("Tangent Function", "tan(pi/6)"),
        ("Advanced Trig", "sin(pi/4) + cos(pi/3) - tan(pi/6)"),
        
        # Logarithms and Exponentials
        ("Natural Log", "ln(e**3)"),
        ("Base 10 Log", "log10(1000)"),
        ("Exponential", "exp(2)"),
        ("Complex Log", "log10(1000) + ln(e**2)"),
        
        # Mathematical Functions
        ("Square Root", "sqrt(256)"),
        ("Factorial", "factorial(10)"),
        ("Absolute Value", "abs(-42)"),
        ("Floor Function", "floor(3.7)"),
        
        # Physics Constants and Calculations
        ("Speed of Light", "c"),
        ("Gravitational Constant", "G"),
        ("Planck Constant", "h"),
        ("Boltzmann Constant", "k_b"),
        
        # Space Physics Calculations
        ("Earth Mass", "M_earth"),
        ("Solar Mass", "M_sun"),
        ("Astronomical Unit", "au"),
        ("Light Year", "ly"),
        ("Earth Escape Velocity", "sqrt(2 * G * M_earth / R_earth)"),
        ("Solar System Escape", "sqrt(2 * G * M_sun / au)"),
        
        # Advanced Physics
        ("Einstein Mass-Energy", "M_sun * c**2"),
        ("Planck Energy", "sqrt(h * c**5 / G)"),
        ("Stefan-Boltzmann Law", "sigma * 5778**4"),
        ("Schwarzschild Radius", "2 * G * M_sun / c**2"),
        
        # Extreme Calculations
        ("Avogadro's Number", "N_A"),
        ("Planck Time", "sqrt(h * G / (2 * pi * c**5))"),
        ("Planck Length", "sqrt(h * G / (2 * pi * c**3))"),
        ("Universe Age Seconds", "13.8e9 * 365.25 * 24 * 3600"),
        
        # Complex Mathematical Expressions
        ("Euler's Identity", "exp(1j * pi) + 1"),
        ("Golden Ratio", "(1 + sqrt(5)) / 2"),
        ("Gamma Function", "gamma(5.5)"),
        ("Large Factorial", "factorial(20)"),
    ]
    
    successful_calcs = 0
    total_time = 0
    results = []
    
    for i, (name, expression) in enumerate(test_cases, 1):
        print(f"**Test {i:2d}: {name}**")
        print(f"Expression: `{expression}`")
        
        start_time = time.time()
        
        try:
            result = calculator.calculate(expression)
            calc_time = time.time() - start_time
            total_time += calc_time
            
            if result['success']:
                # Format result for display
                res_value = result['result']
                if isinstance(res_value, (int, float)):
                    if abs(res_value) > 1e6 or (abs(res_value) < 1e-3 and res_value != 0):
                        formatted_result = f"{res_value:.3e}"
                    else:
                        formatted_result = f"{res_value:.6g}"
                else:
                    formatted_result = str(res_value)
                
                print(f"✅ **Result:** {formatted_result}")
                if result.get('units'):
                    print(f"   Units: {result['units']}")
                print(f"   Type: {result['calculation_type'].replace('_', ' ').title()}")
                print(f"   Time: {calc_time:.4f}s")
                successful_calcs += 1
                results.append((name, formatted_result, calc_time))
            else:
                print(f"❌ **Error:** {result.get('error', 'Unknown error')}")
                print(f"   Time: {calc_time:.4f}s")
                results.append((name, "ERROR", calc_time))
        
        except Exception as e:
            calc_time = time.time() - start_time
            total_time += calc_time
            print(f"❌ **Exception:** {str(e)}")
            print(f"   Time: {calc_time:.4f}s")
            results.append((name, "EXCEPTION", calc_time))
        
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
    
    # Show fastest and slowest calculations
    if results:
        fastest = min(results, key=lambda x: x[2])
        slowest = max(results, key=lambda x: x[2])
        print(f"⚡ Fastest: {fastest[0]} ({fastest[2]:.4f}s)")
        print(f"🐌 Slowest: {slowest[0]} ({slowest[2]:.4f}s)")
        print()
    
    if successful_calcs == len(test_cases):
        print("🎉 **ALL CALCULATIONS COMPLETED SUCCESSFULLY!**")
        print("The AI can handle simple to complex calculations rapidly!")
    else:
        print("⚠️  Some calculations failed. Check error messages above.")
    
    return successful_calcs, len(test_cases), total_time

def test_batch_performance():
    """Test batch calculation performance."""
    print("\n⚡ **BATCH PERFORMANCE TEST**")
    print("=" * 60)
    
    config = MockConfig()
    logger = logging.getLogger("test")
    logger.setLevel(logging.INFO)
    calculator = AdvancedCalculator(config, logger)
    
    # Create a large batch of varied calculations
    batch_expressions = [
        # Basic arithmetic
        "2 + 3", "10 - 4", "7 * 8", "15 / 3", "2**10",
        # Trigonometry
        "sin(pi/2)", "cos(0)", "tan(pi/4)", "sin(pi/6)", "cos(pi/3)",
        # Logarithms
        "log10(100)", "ln(e)", "exp(1)", "log10(1000)", "ln(10)",
        # Square roots
        "sqrt(4)", "sqrt(16)", "sqrt(64)", "sqrt(100)", "sqrt(144)",
        # Constants
        "pi", "e", "c", "G", "h",
        # Physics calculations
        "G * M_earth", "c / 1000", "h * c", "sigma * 300**4", "k_b * 273",
        # Space calculations
        "au / 1000", "ly / 1e12", "M_sun / 1e30", "R_earth / 1000", "c * 3600",
        # Complex expressions
        "sqrt(G * M_sun / au)", "2 * G * M_earth / R_earth", "h * c / 500e-9",
        "factorial(5)", "factorial(7)", "gamma(3)", "abs(-100)", "floor(9.9)",
        # Large numbers
        "1e6 * 1e6", "2**20", "factorial(10)", "N_A / 1e20", "c**2 / 1e16"
    ]
    
    print(f"Processing {len(batch_expressions)} calculations...")
    
    start_time = time.time()
    successful = 0
    
    for i, expr in enumerate(batch_expressions):
        try:
            result = calculator.calculate(expr)
            if result['success']:
                successful += 1
            if (i + 1) % 10 == 0:
                print(f"  Completed {i + 1}/{len(batch_expressions)} calculations...")
        except:
            pass
    
    total_time = time.time() - start_time
    
    print(f"✅ Completed {successful}/{len(batch_expressions)} calculations")
    print(f"⏱️  Total time: {total_time:.3f}s")
    print(f"🚀 Rate: {len(batch_expressions)/total_time:.1f} calculations/second")
    print(f"📈 Rate: {len(batch_expressions)*60/total_time:.0f} calculations/minute")
    
    return successful, len(batch_expressions), total_time

def test_interactive_calculator():
    """Interactive calculator test."""
    print("\n🔬 **INTERACTIVE CALCULATOR**")
    print("=" * 60)
    print("Enter mathematical expressions (type 'quit' to exit):")
    print("Examples:")
    print("  - 2 + 3 * 4")
    print("  - sin(pi/2)")
    print("  - sqrt(G * M_sun / au)")
    print("  - factorial(5)")
    print("  - help (for calculator help)")
    print()
    
    config = MockConfig()
    logger = logging.getLogger("test")
    logger.setLevel(logging.INFO)
    calculator = AdvancedCalculator(config, logger)
    
    while True:
        try:
            expression = input("Calculate: ").strip()
            
            if expression.lower() in ['quit', 'exit', 'q']:
                break
            
            if expression.lower() == 'help':
                print(calculator.get_calculation_help())
                continue
            
            if not expression:
                continue
            
            start_time = time.time()
            result = calculator.calculate(expression)
            calc_time = time.time() - start_time
            
            if result['success']:
                res_value = result['result']
                if isinstance(res_value, (int, float)):
                    if abs(res_value) > 1e6 or (abs(res_value) < 1e-3 and res_value != 0):
                        formatted_result = f"{res_value:.3e}"
                    else:
                        formatted_result = f"{res_value:.6g}"
                else:
                    formatted_result = str(res_value)
                
                print(f"✅ Result: {formatted_result}")
                if result.get('units'):
                    print(f"   Units: {result['units']}")
                print(f"   Type: {result['calculation_type'].replace('_', ' ').title()}")
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

if __name__ == "__main__":
    print("🧮 **SPACE AI ADVANCED CALCULATOR TESTING**")
    print("Testing rapid computation from simple to complex calculations")
    print("=" * 80)
    print()
    
    # Run comprehensive tests
    success1, total1, time1 = test_direct_calculations()
    
    # Run batch performance test
    success2, total2, time2 = test_batch_performance()
    
    # Overall summary
    print("\n🎯 **OVERALL PERFORMANCE SUMMARY**")
    print("=" * 60)
    print(f"Total calculations performed: {total1 + total2}")
    print(f"Total successful: {success1 + success2}")
    print(f"Overall success rate: {(success1 + success2)/(total1 + total2)*100:.1f}%")
    print(f"Total computation time: {time1 + time2:.3f}s")
    print(f"Average time per calculation: {(time1 + time2)/(total1 + total2):.4f}s")
    print(f"Overall calculation rate: {(total1 + total2)*60/(time1 + time2):.0f} calculations/minute")
    print()
    
    if (success1 + success2) == (total1 + total2):
        print("🎉 **PERFECT PERFORMANCE!**")
        print("The Space AI can perform rapid calculations from simple arithmetic")
        print("to the most complex space physics computations in minutes!")
    
    # Optional interactive mode
    response = input("\nWould you like to try interactive mode? (y/n): ").strip().lower()
    if response in ['y', 'yes']:
        test_interactive_calculator()
    
    print("\n✨ **TESTING COMPLETE**")
    print("Advanced Calculator is ready for rapid computations!")
