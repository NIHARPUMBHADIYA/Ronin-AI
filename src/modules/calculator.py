"""
Space Calculator for Space AI Assistant.
Handles astronomical calculations, orbital mechanics, and physics computations.
"""

import math
import logging
from typing import Dict, List, Any, Optional, Tuple, Union
import re

class SpaceCalculator:
    """Calculator for space-related physics and astronomical computations."""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("Space_Calculator")
        
        # Physical constants
        self.constants = {
            'G': 6.67430e-11,  # Gravitational constant (m³/kg⋅s²)
            'c': 299792458,    # Speed of light (m/s)
            'g_earth': 9.80665,  # Standard gravity (m/s²)
            'AU': 149597870.7e3,  # Astronomical unit (m)
            'ly': 9.4607304725808e15,  # Light year (m)
            'pc': 3.0857e16,   # Parsec (m)
            'M_sun': 1.98847e30,  # Solar mass (kg)
            'M_earth': 5.9722e24,  # Earth mass (kg)
            'R_earth': 6.371e6,   # Earth radius (m)
            'R_sun': 6.96340e8,   # Solar radius (m)
        }
        
        # Planetary data for calculations
        self.planetary_data = {
            'mercury': {'mass': 3.301e23, 'radius': 2.4397e6, 'distance': 0.387*self.constants['AU']},
            'venus': {'mass': 4.867e24, 'radius': 6.0518e6, 'distance': 0.723*self.constants['AU']},
            'earth': {'mass': 5.972e24, 'radius': 6.371e6, 'distance': 1.0*self.constants['AU']},
            'mars': {'mass': 6.417e23, 'radius': 3.3895e6, 'distance': 1.524*self.constants['AU']},
            'jupiter': {'mass': 1.898e27, 'radius': 6.9911e7, 'distance': 5.204*self.constants['AU']},
            'saturn': {'mass': 5.683e26, 'radius': 5.8232e7, 'distance': 9.573*self.constants['AU']},
            'uranus': {'mass': 8.681e25, 'radius': 2.5362e7, 'distance': 19.165*self.constants['AU']},
            'neptune': {'mass': 1.024e26, 'radius': 2.4622e7, 'distance': 30.178*self.constants['AU']},
            'moon': {'mass': 7.342e22, 'radius': 1.737e6, 'distance': 384400e3},
            'sun': {'mass': 1.98847e30, 'radius': 6.96340e8, 'distance': 0}
        }
    
    def calculate(self, nlu_result: Dict, context: Dict = None) -> Dict[str, Any]:
        """Main calculation dispatcher based on NLU results."""
        try:
            query_text = nlu_result.get('processed_text', '')
            entities = nlu_result.get('entities', {})
            
            # Determine calculation type
            if any(word in query_text for word in ['escape', 'velocity']):
                return self._calculate_escape_velocity(query_text, entities)
            elif any(word in query_text for word in ['orbital', 'period']):
                return self._calculate_orbital_period(query_text, entities)
            elif any(word in query_text for word in ['delta-v', 'delta', 'change', 'velocity']):
                return self._calculate_delta_v(query_text, entities)
            elif any(word in query_text for word in ['rocket', 'equation', 'tsiolkovsky']):
                return self._calculate_rocket_equation(query_text, entities)
            elif any(word in query_text for word in ['gravity', 'weight', 'force']):
                return self._calculate_gravity(query_text, entities)
            elif any(word in query_text for word in ['distance', 'light', 'travel', 'time']):
                return self._calculate_light_travel_time(query_text, entities)
            elif any(word in query_text for word in ['convert', 'conversion']):
                return self._unit_conversion(query_text, entities)
            elif any(word in query_text for word in ['energy', 'kinetic', 'potential']):
                return self._calculate_energy(query_text, entities)
            else:
                return self._general_calculation(query_text, entities)
                
        except Exception as e:
            self.logger.error(f"Calculation error: {e}")
            return {
                'result': None,
                'explanation': f"Calculation error: {str(e)}",
                'units': '',
                'confidence': 0.0
            }
    
    def _calculate_escape_velocity(self, query_text: str, entities: Dict) -> Dict[str, Any]:
        """Calculate escape velocity for a celestial body."""
        try:
            # Extract celestial body
            body_name = self._extract_celestial_body(query_text, entities)
            
            if body_name in self.planetary_data:
                body_data = self.planetary_data[body_name]
                mass = body_data['mass']
                radius = body_data['radius']
                
                # Escape velocity formula: v = sqrt(2GM/r)
                escape_velocity = math.sqrt(2 * self.constants['G'] * mass / radius)
                
                explanation = f"The escape velocity for {body_name.title()} is {escape_velocity:.0f} m/s ({escape_velocity/1000:.2f} km/s). "
                explanation += f"This is the minimum velocity needed to escape {body_name.title()}'s gravitational field."
                
                return {
                    'result': escape_velocity,
                    'explanation': explanation,
                    'units': 'm/s',
                    'confidence': 0.9,
                    'calculation_type': 'escape_velocity',
                    'body': body_name
                }
            else:
                return {
                    'result': None,
                    'explanation': f"I don't have data for {body_name}. Available bodies: {', '.join(self.planetary_data.keys())}",
                    'units': '',
                    'confidence': 0.1
                }
                
        except Exception as e:
            return {
                'result': None,
                'explanation': f"Error calculating escape velocity: {str(e)}",
                'units': '',
                'confidence': 0.0
            }
    
    def _calculate_orbital_period(self, query_text: str, entities: Dict) -> Dict[str, Any]:
        """Calculate orbital period using Kepler's third law."""
        try:
            # Extract orbital radius or celestial body
            body_name = self._extract_celestial_body(query_text, entities)
            
            if body_name in self.planetary_data:
                # For planets, calculate around the Sun
                if body_name != 'sun':
                    distance = self.planetary_data[body_name]['distance']
                    central_mass = self.constants['M_sun']
                    central_body = "Sun"
                else:
                    return {
                        'result': None,
                        'explanation': "The Sun doesn't orbit around another body in our solar system.",
                        'units': '',
                        'confidence': 0.1
                    }
                
                # Kepler's third law: T = 2π * sqrt(r³/GM)
                period_seconds = 2 * math.pi * math.sqrt(distance**3 / (self.constants['G'] * central_mass))
                period_days = period_seconds / (24 * 3600)
                period_years = period_days / 365.25
                
                explanation = f"The orbital period of {body_name.title()} around the {central_body} is "
                
                if period_days < 1:
                    explanation += f"{period_seconds/3600:.1f} hours."
                elif period_days < 365:
                    explanation += f"{period_days:.1f} days."
                else:
                    explanation += f"{period_years:.2f} years ({period_days:.0f} days)."
                
                return {
                    'result': period_seconds,
                    'explanation': explanation,
                    'units': 'seconds',
                    'confidence': 0.9,
                    'calculation_type': 'orbital_period',
                    'period_days': period_days,
                    'period_years': period_years
                }
            else:
                # Try to extract orbital altitude for satellites
                altitude_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:km|kilometers?)', query_text)
                if altitude_match:
                    altitude_km = float(altitude_match.group(1))
                    return self._calculate_satellite_period(altitude_km)
                
                return {
                    'result': None,
                    'explanation': f"I need either a celestial body name or orbital altitude to calculate orbital period.",
                    'units': '',
                    'confidence': 0.1
                }
                
        except Exception as e:
            return {
                'result': None,
                'explanation': f"Error calculating orbital period: {str(e)}",
                'units': '',
                'confidence': 0.0
            }
    
    def _calculate_satellite_period(self, altitude_km: float) -> Dict[str, Any]:
        """Calculate orbital period for Earth satellite at given altitude."""
        try:
            altitude_m = altitude_km * 1000
            orbital_radius = self.constants['R_earth'] + altitude_m
            
            # Orbital period: T = 2π * sqrt(r³/GM)
            period_seconds = 2 * math.pi * math.sqrt(orbital_radius**3 / (self.constants['G'] * self.constants['M_earth']))
            period_minutes = period_seconds / 60
            period_hours = period_minutes / 60
            
            explanation = f"A satellite at {altitude_km} km altitude above Earth has an orbital period of "
            
            if period_hours < 1:
                explanation += f"{period_minutes:.1f} minutes."
            else:
                explanation += f"{period_hours:.2f} hours ({period_minutes:.0f} minutes)."
            
            # Add orbital velocity
            orbital_velocity = 2 * math.pi * orbital_radius / period_seconds
            explanation += f" The orbital velocity is {orbital_velocity/1000:.2f} km/s."
            
            return {
                'result': period_seconds,
                'explanation': explanation,
                'units': 'seconds',
                'confidence': 0.9,
                'calculation_type': 'satellite_period',
                'altitude_km': altitude_km,
                'orbital_velocity_ms': orbital_velocity
            }
            
        except Exception as e:
            return {
                'result': None,
                'explanation': f"Error calculating satellite period: {str(e)}",
                'units': '',
                'confidence': 0.0
            }
    
    def _calculate_delta_v(self, query_text: str, entities: Dict) -> Dict[str, Any]:
        """Calculate delta-v for orbital maneuvers."""
        try:
            # This is a simplified delta-v calculation
            # In practice, delta-v depends on specific maneuver type
            
            explanation = "Delta-v calculations depend on the specific maneuver. Here are some common values:\n"
            explanation += "• Low Earth Orbit to escape: ~3.2 km/s\n"
            explanation += "• LEO to Mars transfer: ~3.6 km/s\n"
            explanation += "• LEO to Moon transfer: ~3.1 km/s\n"
            explanation += "• Geostationary orbit insertion: ~1.5 km/s\n"
            explanation += "For specific calculations, please provide orbital parameters."
            
            return {
                'result': None,
                'explanation': explanation,
                'units': 'km/s',
                'confidence': 0.7,
                'calculation_type': 'delta_v_reference'
            }
            
        except Exception as e:
            return {
                'result': None,
                'explanation': f"Error with delta-v calculation: {str(e)}",
                'units': '',
                'confidence': 0.0
            }
    
    def _calculate_rocket_equation(self, query_text: str, entities: Dict) -> Dict[str, Any]:
        """Calculate using Tsiolkovsky rocket equation."""
        try:
            # Extract parameters if available
            # Δv = ve * ln(m0/mf)
            # where ve = exhaust velocity, m0 = initial mass, mf = final mass
            
            explanation = "The Tsiolkovsky rocket equation is: Δv = ve × ln(m₀/mf)\n"
            explanation += "Where:\n"
            explanation += "• Δv = change in velocity\n"
            explanation += "• ve = exhaust velocity\n"
            explanation += "• m₀ = initial mass (with fuel)\n"
            explanation += "• mf = final mass (without fuel)\n\n"
            explanation += "For specific calculations, please provide the exhaust velocity and mass ratio."
            
            return {
                'result': None,
                'explanation': explanation,
                'units': 'm/s',
                'confidence': 0.8,
                'calculation_type': 'rocket_equation_info'
            }
            
        except Exception as e:
            return {
                'result': None,
                'explanation': f"Error with rocket equation: {str(e)}",
                'units': '',
                'confidence': 0.0
            }
    
    def _calculate_gravity(self, query_text: str, entities: Dict) -> Dict[str, Any]:
        """Calculate gravitational force or surface gravity."""
        try:
            body_name = self._extract_celestial_body(query_text, entities)
            
            if body_name in self.planetary_data:
                body_data = self.planetary_data[body_name]
                mass = body_data['mass']
                radius = body_data['radius']
                
                # Surface gravity: g = GM/r²
                surface_gravity = self.constants['G'] * mass / (radius**2)
                earth_ratio = surface_gravity / self.constants['g_earth']
                
                explanation = f"The surface gravity on {body_name.title()} is {surface_gravity:.2f} m/s² "
                explanation += f"({earth_ratio:.2f}× Earth's gravity). "
                
                if earth_ratio > 1:
                    explanation += f"You would weigh {earth_ratio:.1f} times more on {body_name.title()} than on Earth."
                else:
                    explanation += f"You would weigh {1/earth_ratio:.1f} times less on {body_name.title()} than on Earth."
                
                return {
                    'result': surface_gravity,
                    'explanation': explanation,
                    'units': 'm/s²',
                    'confidence': 0.9,
                    'calculation_type': 'surface_gravity',
                    'earth_ratio': earth_ratio
                }
            else:
                return {
                    'result': None,
                    'explanation': f"I don't have gravitational data for {body_name}.",
                    'units': '',
                    'confidence': 0.1
                }
                
        except Exception as e:
            return {
                'result': None,
                'explanation': f"Error calculating gravity: {str(e)}",
                'units': '',
                'confidence': 0.0
            }
    
    def _calculate_light_travel_time(self, query_text: str, entities: Dict) -> Dict[str, Any]:
        """Calculate light travel time between celestial bodies."""
        try:
            # Extract distance or celestial bodies
            distance_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:km|kilometers?|AU|light-years?|ly)', query_text)
            
            if distance_match:
                distance_str = distance_match.group(0)
                distance_value = float(distance_match.group(1))
                
                # Convert to meters
                if 'AU' in distance_str:
                    distance_m = distance_value * self.constants['AU']
                elif 'ly' in distance_str or 'light-year' in distance_str:
                    distance_m = distance_value * self.constants['ly']
                else:  # km
                    distance_m = distance_value * 1000
                
                # Calculate travel time
                travel_time_seconds = distance_m / self.constants['c']
                
                # Format time appropriately
                if travel_time_seconds < 1:
                    time_str = f"{travel_time_seconds*1000:.1f} milliseconds"
                elif travel_time_seconds < 60:
                    time_str = f"{travel_time_seconds:.2f} seconds"
                elif travel_time_seconds < 3600:
                    time_str = f"{travel_time_seconds/60:.1f} minutes"
                elif travel_time_seconds < 86400:
                    time_str = f"{travel_time_seconds/3600:.1f} hours"
                else:
                    time_str = f"{travel_time_seconds/86400:.1f} days"
                
                explanation = f"Light travels {distance_str} in {time_str}."
                
                return {
                    'result': travel_time_seconds,
                    'explanation': explanation,
                    'units': 'seconds',
                    'confidence': 0.9,
                    'calculation_type': 'light_travel_time',
                    'distance_m': distance_m
                }
            else:
                # Try to find celestial bodies for distance calculation
                body_name = self._extract_celestial_body(query_text, entities)
                if body_name in self.planetary_data and body_name != 'sun':
                    distance_m = self.planetary_data[body_name]['distance']
                    travel_time_seconds = distance_m / self.constants['c']
                    
                    if travel_time_seconds < 60:
                        time_str = f"{travel_time_seconds:.1f} seconds"
                    else:
                        time_str = f"{travel_time_seconds/60:.1f} minutes"
                    
                    explanation = f"Light from the Sun takes {time_str} to reach {body_name.title()}."
                    
                    return {
                        'result': travel_time_seconds,
                        'explanation': explanation,
                        'units': 'seconds',
                        'confidence': 0.9,
                        'calculation_type': 'light_travel_time'
                    }
                
                return {
                    'result': None,
                    'explanation': "Please specify a distance or celestial body for light travel time calculation.",
                    'units': '',
                    'confidence': 0.1
                }
                
        except Exception as e:
            return {
                'result': None,
                'explanation': f"Error calculating light travel time: {str(e)}",
                'units': '',
                'confidence': 0.0
            }
    
    def _unit_conversion(self, query_text: str, entities: Dict) -> Dict[str, Any]:
        """Handle unit conversions."""
        try:
            # Extract conversion request
            conversion_patterns = [
                r'(\d+(?:\.\d+)?)\s*(km|kilometers?)\s+(?:to|in)\s*(miles?|mi)',
                r'(\d+(?:\.\d+)?)\s*(miles?|mi)\s+(?:to|in)\s*(km|kilometers?)',
                r'(\d+(?:\.\d+)?)\s*(AU)\s+(?:to|in)\s*(km|kilometers?)',
                r'(\d+(?:\.\d+)?)\s*(km|kilometers?)\s+(?:to|in)\s*(AU)',
                r'(\d+(?:\.\d+)?)\s*(kg|kilograms?)\s+(?:to|in)\s*(pounds?|lbs?)',
                r'(\d+(?:\.\d+)?)\s*(pounds?|lbs?)\s+(?:to|in)\s*(kg|kilograms?)',
                r'(\d+(?:\.\d+)?)\s*°?([CF]|celsius|fahrenheit)\s+(?:to|in)\s*°?([CF]|celsius|fahrenheit)',
            ]
            
            for pattern in conversion_patterns:
                match = re.search(pattern, query_text, re.IGNORECASE)
                if match:
                    value = float(match.group(1))
                    from_unit = match.group(2).lower()
                    to_unit = match.group(3).lower()
                    
                    result = self._perform_conversion(value, from_unit, to_unit)
                    if result:
                        return result
            
            return {
                'result': None,
                'explanation': "I couldn't understand the conversion request. Please specify the value and units clearly (e.g., '100 km to miles').",
                'units': '',
                'confidence': 0.1
            }
            
        except Exception as e:
            return {
                'result': None,
                'explanation': f"Error with unit conversion: {str(e)}",
                'units': '',
                'confidence': 0.0
            }
    
    def _perform_conversion(self, value: float, from_unit: str, to_unit: str) -> Optional[Dict[str, Any]]:
        """Perform the actual unit conversion."""
        conversions = {
            ('km', 'mi'): 0.621371,
            ('km', 'miles'): 0.621371,
            ('mi', 'km'): 1.60934,
            ('miles', 'km'): 1.60934,
            ('au', 'km'): 149597870.7,
            ('km', 'au'): 1/149597870.7,
            ('kg', 'lbs'): 2.20462,
            ('kg', 'pounds'): 2.20462,
            ('lbs', 'kg'): 0.453592,
            ('pounds', 'kg'): 0.453592,
        }
        
        # Temperature conversions
        if from_unit in ['c', 'celsius'] and to_unit in ['f', 'fahrenheit']:
            result_value = (value * 9/5) + 32
            explanation = f"{value}°C equals {result_value:.1f}°F"
            return {
                'result': result_value,
                'explanation': explanation,
                'units': '°F',
                'confidence': 0.9,
                'calculation_type': 'temperature_conversion'
            }
        elif from_unit in ['f', 'fahrenheit'] and to_unit in ['c', 'celsius']:
            result_value = (value - 32) * 5/9
            explanation = f"{value}°F equals {result_value:.1f}°C"
            return {
                'result': result_value,
                'explanation': explanation,
                'units': '°C',
                'confidence': 0.9,
                'calculation_type': 'temperature_conversion'
            }
        
        # Standard conversions
        conversion_key = (from_unit, to_unit)
        if conversion_key in conversions:
            result_value = value * conversions[conversion_key]
            explanation = f"{value} {from_unit} equals {result_value:.6g} {to_unit}"
            
            return {
                'result': result_value,
                'explanation': explanation,
                'units': to_unit,
                'confidence': 0.9,
                'calculation_type': 'unit_conversion'
            }
        
        return None
    
    def _calculate_energy(self, query_text: str, entities: Dict) -> Dict[str, Any]:
        """Calculate kinetic or potential energy."""
        try:
            explanation = "Energy calculations require specific parameters:\n"
            explanation += "• Kinetic Energy: KE = ½mv² (mass and velocity needed)\n"
            explanation += "• Gravitational Potential Energy: PE = mgh (mass, gravity, height needed)\n"
            explanation += "• Orbital Energy: E = -GMm/2r (for circular orbits)\n"
            explanation += "Please provide the necessary values for calculation."
            
            return {
                'result': None,
                'explanation': explanation,
                'units': 'J',
                'confidence': 0.7,
                'calculation_type': 'energy_info'
            }
            
        except Exception as e:
            return {
                'result': None,
                'explanation': f"Error with energy calculation: {str(e)}",
                'units': '',
                'confidence': 0.0
            }
    
    def _general_calculation(self, query_text: str, entities: Dict) -> Dict[str, Any]:
        """Handle general mathematical calculations."""
        try:
            # Try to extract mathematical expressions
            math_match = re.search(r'(\d+(?:\.\d+)?)\s*([+\-*/])\s*(\d+(?:\.\d+)?)', query_text)
            
            if math_match:
                num1 = float(math_match.group(1))
                operator = math_match.group(2)
                num2 = float(math_match.group(3))
                
                if operator == '+':
                    result = num1 + num2
                elif operator == '-':
                    result = num1 - num2
                elif operator == '*':
                    result = num1 * num2
                elif operator == '/':
                    if num2 != 0:
                        result = num1 / num2
                    else:
                        return {
                            'result': None,
                            'explanation': "Cannot divide by zero.",
                            'units': '',
                            'confidence': 0.0
                        }
                
                explanation = f"{num1} {operator} {num2} = {result}"
                
                return {
                    'result': result,
                    'explanation': explanation,
                    'units': '',
                    'confidence': 0.8,
                    'calculation_type': 'basic_math'
                }
            
            return {
                'result': None,
                'explanation': "I couldn't identify a specific calculation. Please be more specific about what you'd like me to calculate.",
                'units': '',
                'confidence': 0.1
            }
            
        except Exception as e:
            return {
                'result': None,
                'explanation': f"Error with calculation: {str(e)}",
                'units': '',
                'confidence': 0.0
            }
    
    def _extract_celestial_body(self, query_text: str, entities: Dict) -> str:
        """Extract celestial body name from query."""
        # Check entities first
        if 'celestial_body' in entities and entities['celestial_body']:
            return entities['celestial_body'][0]['value'].lower()
        
        # Check for body names in query text
        for body_name in self.planetary_data.keys():
            if body_name in query_text.lower():
                return body_name
        
        # Default to Earth if no body specified
        return 'earth'
    
    def get_available_calculations(self) -> List[str]:
        """Get list of available calculation types."""
        return [
            'Escape velocity',
            'Orbital period',
            'Delta-v',
            'Rocket equation',
            'Surface gravity',
            'Light travel time',
            'Unit conversions',
            'Energy calculations'
        ]
    
    def shutdown(self):
        """Shutdown the calculator."""
        self.logger.info("Space calculator shutting down")
