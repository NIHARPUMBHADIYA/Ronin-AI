#!/usr/bin/env python3
"""
Advanced Calculator Module for Space AI Assistant.
Handles simple to complex calculations with rapid computation capabilities.
"""

import math
import numpy as np
import sympy as sp
from scipy import optimize, integrate, special
from typing import Dict, List, Any, Optional, Union
import re
import ast
import operator
from ..utils.logger import setup_logger

class AdvancedCalculator:
    """Advanced calculation engine for simple to complex computations."""
    
    def __init__(self, config, logger=None):
        """Initialize the Advanced Calculator."""
        self.config = config
        self.logger = logger or setup_logger()
        
        # Mathematical constants
        self.constants = {
            'pi': math.pi,
            'e': math.e,
            'c': 299792458,  # Speed of light (m/s)
            'G': 6.67430e-11,  # Gravitational constant
            'h': 6.62607015e-34,  # Planck constant
            'k_b': 1.380649e-23,  # Boltzmann constant
            'sigma': 5.670374419e-8,  # Stefan-Boltzmann constant
            'R': 8.314462618,  # Gas constant
            'N_A': 6.02214076e23,  # Avogadro's number
            'mu_0': 4*math.pi*1e-7,  # Permeability of free space
            'epsilon_0': 8.8541878128e-12,  # Permittivity of free space
            'au': 149597870700,  # Astronomical unit (m)
            'ly': 9.4607304725808e15,  # Light year (m)
            'pc': 3.0857e16,  # Parsec (m)
            'M_sun': 1.98847e30,  # Solar mass (kg)
            'R_sun': 6.96e8,  # Solar radius (m)
            'M_earth': 5.9722e24,  # Earth mass (kg)
            'R_earth': 6.371e6,  # Earth radius (m)
        }
        
        # Mathematical operators
        self.operators = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
            '//': operator.floordiv,
            '%': operator.mod,
            '**': operator.pow,
            '^': operator.pow,
        }
        
        self.logger.info("Advanced Calculator initialized successfully")
    
    def calculate(self, expression: str, variables: Dict[str, float] = None) -> Dict[str, Any]:
        """Main calculation method that handles various types of expressions."""
        try:
            # Clean and prepare expression
            expr = self._clean_expression(expression)
            
            # Detect calculation type
            calc_type = self._detect_calculation_type(expr)
            
            # Route to appropriate calculation method
            if calc_type == 'basic_arithmetic':
                result = self._basic_arithmetic(expr)
            elif calc_type == 'algebraic':
                result = self._algebraic_calculation(expr, variables)
            elif calc_type == 'trigonometric':
                result = self._trigonometric_calculation(expr)
            elif calc_type == 'logarithmic':
                result = self._logarithmic_calculation(expr)
            elif calc_type == 'calculus':
                result = self._calculus_calculation(expr)
            elif calc_type == 'physics':
                result = self._physics_calculation(expr, variables)
            elif calc_type == 'space_calculation':
                result = self._space_calculation(expr, variables)
            elif calc_type == 'statistical':
                result = self._statistical_calculation(expr)
            elif calc_type == 'matrix':
                result = self._matrix_calculation(expr)
            else:
                result = self._general_calculation(expr, variables)
            
            return {
                'result': result,
                'expression': expression,
                'calculation_type': calc_type,
                'success': True,
                'units': self._detect_units(expression)
            }
            
        except Exception as e:
            self.logger.error(f"Calculation failed: {e}")
            return {
                'error': str(e),
                'expression': expression,
                'success': False
            }
    
    def _clean_expression(self, expr: str) -> str:
        """Clean and standardize mathematical expression."""
        # Replace common symbols
        expr = expr.replace('×', '*').replace('÷', '/')
        expr = expr.replace('²', '**2').replace('³', '**3')
        expr = expr.replace('√', 'sqrt')
        
        # Replace constants
        for const, value in self.constants.items():
            expr = re.sub(r'\b' + const + r'\b', str(value), expr)
        
        return expr.strip()
    
    def _detect_calculation_type(self, expr: str) -> str:
        """Detect the type of calculation based on expression content."""
        expr_lower = expr.lower()
        
        # Space calculations
        if any(word in expr_lower for word in ['orbital', 'escape', 'velocity', 'gravity', 'mass', 'distance', 'light']):
            return 'space_calculation'
        
        # Physics calculations
        if any(word in expr_lower for word in ['force', 'energy', 'momentum', 'acceleration', 'frequency']):
            return 'physics'
        
        # Calculus
        if any(word in expr_lower for word in ['integral', 'derivative', 'limit', 'diff', 'integrate']):
            return 'calculus'
        
        # Trigonometric
        if any(func in expr_lower for func in ['sin', 'cos', 'tan', 'asin', 'acos', 'atan']):
            return 'trigonometric'
        
        # Logarithmic
        if any(func in expr_lower for func in ['log', 'ln', 'exp']):
            return 'logarithmic'
        
        # Matrix operations
        if any(word in expr_lower for word in ['matrix', 'det', 'inverse', 'eigenvalue']):
            return 'matrix'
        
        # Statistical
        if any(word in expr_lower for word in ['mean', 'std', 'variance', 'correlation']):
            return 'statistical'
        
        # Algebraic (contains variables)
        if re.search(r'[a-zA-Z]', expr) and not any(func in expr_lower for func in ['sin', 'cos', 'tan', 'log', 'exp']):
            return 'algebraic'
        
        # Basic arithmetic
        return 'basic_arithmetic'
    
    def _basic_arithmetic(self, expr: str) -> float:
        """Handle basic arithmetic calculations."""
        try:
            # Safe evaluation using ast
            node = ast.parse(expr, mode='eval')
            return self._eval_node(node.body)
        except:
            # Fallback to sympy
            return float(sp.sympify(expr).evalf())
    
    def _eval_node(self, node):
        """Safely evaluate AST node."""
        if isinstance(node, ast.Constant):
            return node.value
        elif isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)
            op = type(node.op)
            if op == ast.Add:
                return left + right
            elif op == ast.Sub:
                return left - right
            elif op == ast.Mult:
                return left * right
            elif op == ast.Div:
                return left / right
            elif op == ast.Pow:
                return left ** right
        elif isinstance(node, ast.UnaryOp):
            operand = self._eval_node(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +operand
            elif isinstance(node.op, ast.USub):
                return -operand
        elif isinstance(node, ast.Call):
            func_name = node.func.id
            args = [self._eval_node(arg) for arg in node.args]
            return self._call_function(func_name, args)
        
        raise ValueError(f"Unsupported node type: {type(node)}")
    
    def _call_function(self, func_name: str, args: List[float]) -> float:
        """Call mathematical functions."""
        func_map = {
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'asin': math.asin, 'acos': math.acos, 'atan': math.atan,
            'sinh': math.sinh, 'cosh': math.cosh, 'tanh': math.tanh,
            'log': math.log, 'log10': math.log10, 'ln': math.log,
            'exp': math.exp, 'sqrt': math.sqrt, 'abs': abs,
            'ceil': math.ceil, 'floor': math.floor, 'round': round,
            'factorial': math.factorial, 'gamma': math.gamma,
        }
        
        if func_name in func_map:
            return func_map[func_name](*args)
        else:
            raise ValueError(f"Unknown function: {func_name}")
    
    def _algebraic_calculation(self, expr: str, variables: Dict[str, float] = None) -> Any:
        """Handle algebraic calculations and equation solving."""
        try:
            # Parse expression with sympy
            sym_expr = sp.sympify(expr)
            
            # If variables provided, substitute them
            if variables:
                for var, val in variables.items():
                    sym_expr = sym_expr.subs(var, val)
            
            # Try to evaluate numerically
            try:
                return float(sym_expr.evalf())
            except:
                # Return symbolic result if can't evaluate numerically
                return str(sym_expr)
                
        except Exception as e:
            raise ValueError(f"Algebraic calculation failed: {e}")
    
    def _trigonometric_calculation(self, expr: str) -> float:
        """Handle trigonometric calculations."""
        # Convert degrees to radians if needed
        if 'deg' in expr.lower():
            expr = expr.replace('deg', '').strip()
            expr = f"({expr}) * pi / 180"
        
        return float(sp.sympify(expr).evalf())
    
    def _logarithmic_calculation(self, expr: str) -> float:
        """Handle logarithmic calculations."""
        return float(sp.sympify(expr).evalf())
    
    def _calculus_calculation(self, expr: str) -> Any:
        """Handle calculus operations (derivatives, integrals)."""
        try:
            if 'derivative' in expr.lower() or 'diff' in expr.lower():
                # Extract function and variable
                match = re.search(r'diff\((.*?),\s*(\w+)\)', expr)
                if match:
                    func_str, var_str = match.groups()
                    func = sp.sympify(func_str)
                    var = sp.Symbol(var_str)
                    result = sp.diff(func, var)
                    return str(result)
            
            elif 'integral' in expr.lower() or 'integrate' in expr.lower():
                # Extract function and variable
                match = re.search(r'integrate\((.*?),\s*(\w+)\)', expr)
                if match:
                    func_str, var_str = match.groups()
                    func = sp.sympify(func_str)
                    var = sp.Symbol(var_str)
                    result = sp.integrate(func, var)
                    return str(result)
            
            return "Calculus operation not recognized"
            
        except Exception as e:
            raise ValueError(f"Calculus calculation failed: {e}")
    
    def _physics_calculation(self, expr: str, variables: Dict[str, float] = None) -> float:
        """Handle physics calculations."""
        expr_lower = expr.lower()
        
        # Force calculations
        if 'force' in expr_lower and 'mass' in expr_lower and 'acceleration' in expr_lower:
            if variables and 'mass' in variables and 'acceleration' in variables:
                return variables['mass'] * variables['acceleration']
        
        # Energy calculations
        if 'kinetic' in expr_lower and 'energy' in expr_lower:
            if variables and 'mass' in variables and 'velocity' in variables:
                return 0.5 * variables['mass'] * variables['velocity']**2
        
        # General physics expression
        return float(sp.sympify(expr).evalf())
    
    def _space_calculation(self, expr: str, variables: Dict[str, float] = None) -> float:
        """Handle space-related calculations."""
        expr_lower = expr.lower()
        
        # Orbital velocity
        if 'orbital' in expr_lower and 'velocity' in expr_lower:
            if variables and 'mass' in variables and 'radius' in variables:
                G = self.constants['G']
                return math.sqrt(G * variables['mass'] / variables['radius'])
        
        # Escape velocity
        if 'escape' in expr_lower and 'velocity' in expr_lower:
            if variables and 'mass' in variables and 'radius' in variables:
                G = self.constants['G']
                return math.sqrt(2 * G * variables['mass'] / variables['radius'])
        
        # Distance calculations
        if 'distance' in expr_lower and 'light' in expr_lower:
            if variables and 'time' in variables:
                c = self.constants['c']
                return c * variables['time']
        
        # General space expression
        return float(sp.sympify(expr).evalf())
    
    def _statistical_calculation(self, expr: str) -> float:
        """Handle statistical calculations."""
        # This would handle statistical functions
        return float(sp.sympify(expr).evalf())
    
    def _matrix_calculation(self, expr: str) -> Any:
        """Handle matrix calculations."""
        # This would handle matrix operations
        return "Matrix calculations not yet implemented"
    
    def _general_calculation(self, expr: str, variables: Dict[str, float] = None) -> float:
        """Handle general calculations."""
        sym_expr = sp.sympify(expr)
        
        if variables:
            for var, val in variables.items():
                sym_expr = sym_expr.subs(var, val)
        
        return float(sym_expr.evalf())
    
    def _detect_units(self, expr: str) -> Optional[str]:
        """Detect units in the expression."""
        unit_patterns = {
            r'\bm\b': 'meters',
            r'\bkm\b': 'kilometers',
            r'\bs\b': 'seconds',
            r'\bkg\b': 'kilograms',
            r'\bN\b': 'Newtons',
            r'\bJ\b': 'Joules',
            r'\bW\b': 'Watts',
            r'\bm/s\b': 'meters per second',
            r'\bm/s²\b': 'meters per second squared',
        }
        
        for pattern, unit in unit_patterns.items():
            if re.search(pattern, expr):
                return unit
        
        return None
    
    def solve_equation(self, equation: str, variable: str = 'x') -> List[float]:
        """Solve equations for a given variable."""
        try:
            eq = sp.Eq(*[sp.sympify(side) for side in equation.split('=')])
            var = sp.Symbol(variable)
            solutions = sp.solve(eq, var)
            return [float(sol.evalf()) for sol in solutions if sol.is_real]
        except Exception as e:
            self.logger.error(f"Equation solving failed: {e}")
            return []
    
    def evaluate_function(self, func_str: str, x_values: List[float]) -> List[float]:
        """Evaluate a function at multiple points."""
        try:
            func = sp.sympify(func_str)
            x = sp.Symbol('x')
            return [float(func.subs(x, val).evalf()) for val in x_values]
        except Exception as e:
            self.logger.error(f"Function evaluation failed: {e}")
            return []
    
    def quick_calculate(self, expression: str) -> str:
        """Quick calculation with formatted result."""
        result = self.calculate(expression)
        
        if result['success']:
            if isinstance(result['result'], float):
                if result['result'] > 1e6 or result['result'] < 1e-3:
                    formatted_result = f"{result['result']:.3e}"
                else:
                    formatted_result = f"{result['result']:.6g}"
            else:
                formatted_result = str(result['result'])
            
            units = result.get('units', '')
            unit_str = f" {units}" if units else ""
            
            return f"**{expression}** = **{formatted_result}{unit_str}**"
        else:
            return f"**Error:** {result['error']}"
    
    def batch_calculate(self, expressions: List[str]) -> List[Dict[str, Any]]:
        """Perform batch calculations."""
        results = []
        for expr in expressions:
            results.append(self.calculate(expr))
        return results
    
    def get_calculation_help(self) -> str:
        """Get help information for calculations."""
        return """**Advanced Calculator Help**

**Supported Operations:**
• Basic arithmetic: +, -, *, /, **, ^, sqrt(), abs()
• Trigonometric: sin(), cos(), tan(), asin(), acos(), atan()
• Logarithmic: log(), ln(), log10(), exp()
• Physics: Force, energy, momentum calculations
• Space: Orbital velocity, escape velocity, distances
• Algebraic: Equation solving, symbolic math
• Calculus: diff(f,x), integrate(f,x)

**Constants Available:**
• pi, e, c (speed of light), G (gravitational constant)
• h (Planck), k_b (Boltzmann), sigma (Stefan-Boltzmann)
• au (astronomical unit), ly (light year), pc (parsec)
• M_sun, R_sun, M_earth, R_earth

**Examples:**
• `2 + 3 * 4`
• `sin(pi/4)`
• `sqrt(G * M_sun / au)`
• `orbital velocity: mass=M_sun, radius=au`
• `solve: x^2 - 5*x + 6 = 0`
"""
