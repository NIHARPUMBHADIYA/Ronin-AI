"""
Core AI Engine for Space AI Assistant.
Coordinates all AI components and manages the main intelligence loop.
"""

import logging
import threading
import time
from typing import Dict, Any, Optional, List
from pathlib import Path

from ..utils.logger import setup_logger, MissionLogger
from ..modules.nlu_engine import NLUEngine
from ..modules.knowledge_base import SpaceKnowledgeBase
from ..modules.calculator import SpaceCalculator
from ..modules.advanced_calculator import AdvancedCalculator
from ..modules.equation_engine import UniversalEquationEngine
from ..modules.mission_support import MissionSupport
from ..modules.emergency_system import EmergencySystem

class SpaceAIEngine:
    """Main AI engine coordinating all intelligence components."""
    
    def __init__(self, config):
        self.config = config
        self.logger = setup_logger("AI_Engine", config.get('mission.log_level', 'INFO'))
        self.mission_logger = MissionLogger(config.logs_dir)
        
        # Core components
        self.nlu_engine = None
        self.knowledge_base = None
        self.calculator = None
        self.advanced_calculator = None
        self.equation_engine = None
        self.mission_support = None
        self.emergency_system = None
        
        # State management
        self.conversation_context = []
        self.current_session = {}
        self.is_initialized = False
        self.is_running = False
        
        # Thread safety
        self.lock = threading.RLock()
        
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize all AI components."""
        try:
            self.logger.info("Initializing AI Engine components...")
            
            # Initialize NLU Engine
            self.nlu_engine = NLUEngine(self.config)
            
            # Initialize Knowledge Base
            self.knowledge_base = SpaceKnowledgeBase(self.config)
            
            # Initialize knowledge modules
            try:
                from ..modules.galaxy_database import GalaxyDatabase
                from ..modules.exoplanet_database import ExoplanetDatabase
                from ..modules.stellar_catalog import StellarCatalog
                from ..modules.solar_system_database import SolarSystemDatabase
                from ..modules.deep_space_database import DeepSpaceDatabase
                from ..modules.space_missions_database import SpaceMissionsDatabase
                
                self.galaxy_db = GalaxyDatabase(self.config, self.logger)
                self.exoplanet_db = ExoplanetDatabase(self.config, self.logger)
                self.stellar_catalog = StellarCatalog(self.config, self.logger)
                self.solar_system_db = SolarSystemDatabase(self.config, self.logger)
                self.deep_space_db = DeepSpaceDatabase(self.config, self.logger)
                self.space_missions_db = SpaceMissionsDatabase(self.config, self.logger)
                
                self.logger.info("Enhanced knowledge modules initialized successfully")
            except Exception as e:
                self.logger.error(f"Failed to initialize enhanced knowledge modules: {e}")
                self.galaxy_db = None
                self.exoplanet_db = None
                self.stellar_catalog = None
                self.solar_system_db = None
                self.deep_space_db = None
                self.space_missions_db = None
            
            # Initialize Calculator
            self.calculator = SpaceCalculator(self.config)
            
            # Initialize Advanced Calculator
            self.advanced_calculator = AdvancedCalculator(self.config, self.logger)
            
            # Initialize Equation Engine
            self.equation_engine = UniversalEquationEngine(self.config)
            
            # Initialize Mission Support
            self.mission_support = MissionSupport(self.config)
            
            # Initialize Emergency System
            self.emergency_system = EmergencySystem(self.config)
            
            self.is_initialized = True
            self.logger.info("AI Engine components initialized successfully")
            self.mission_logger.log_system_status("AI_ENGINE", "INITIALIZED", "All components ready")
            
        except Exception as e:
            self.logger.error(f"Failed to initialize AI Engine: {e}")
            self.mission_logger.log_system_status("AI_ENGINE", "FAILED", f"Initialization error: {e}")
            raise
    
    def process_input(self, input_text: str, input_type: str = "text", context: Dict = None) -> Dict[str, Any]:
        """
        Process user input and generate appropriate response.
        
        Args:
            input_text: User's input text
            input_type: Type of input (text, voice)
            context: Additional context information
            
        Returns:
            Response dictionary with text, audio, and metadata
        """
        if not self.is_initialized:
            return self._error_response("AI Engine not initialized")
        
        with self.lock:
            try:
                self.logger.debug(f"Processing {input_type} input: {input_text[:100]}...")
                
                # Parse input using NLU
                nlu_result = self.nlu_engine.parse(input_text, context)
                
                # Update conversation context
                self._update_context(input_text, nlu_result)
                
                # Route to appropriate handler based on intent
                response = self._route_intent(nlu_result, context)
                
                # Log the interaction
                self.mission_logger.log_mission_event(
                    f"Query: {input_text[:50]}... | Intent: {nlu_result.get('intent', 'unknown')}",
                    category="AI_INTERACTION"
                )
                
                return response
                
            except Exception as e:
                self.logger.error(f"Error processing input: {e}")
                return self._error_response(f"Processing error: {str(e)}")
    
    def _route_intent(self, nlu_result: Dict, context: Dict = None) -> Dict[str, Any]:
        """Route parsed intent to appropriate handler."""
        intent = nlu_result.get('intent', 'unknown')
        entities = nlu_result.get('entities', {})
        confidence = nlu_result.get('confidence', 0.0)
        
        # Low confidence fallback
        if confidence < self.config.get('nlu.confidence_threshold', 0.7):
            return self._clarification_response(nlu_result)
        
        # Route to handlers
        if intent in ['calculate', 'compute', 'math']:
            return self._handle_calculation(nlu_result, context)
        elif intent in ['equation', 'formula', 'solve']:
            return self._handle_equation(nlu_result, context)
        elif intent in ['knowledge', 'info', 'what_is', 'explain']:
            return self._handle_knowledge_query(nlu_result, context)
        elif intent in ['reminder', 'schedule', 'alert']:
            return self._handle_reminder(nlu_result, context)
        elif intent in ['checklist', 'procedure', 'steps']:
            return self._handle_checklist(nlu_result, context)
        elif intent in ['log', 'note', 'record']:
            return self._handle_logging(nlu_result, context)
        elif intent in ['emergency', 'help', 'urgent']:
            return self._handle_emergency(nlu_result, context)
        elif intent in ['status', 'system', 'health']:
            return self._handle_system_status(nlu_result, context)
        else:
            return self._handle_general_query(nlu_result, context)
    
    def _handle_calculation(self, nlu_result: Dict, context: Dict = None) -> Dict[str, Any]:
        """Handle calculation requests with advanced calculator."""
        try:
            # Extract calculation expression from the input
            query_text = nlu_result.get('processed_text', '')
            entities = nlu_result.get('entities', {})
            
            # Try to extract mathematical expression
            expression = self._extract_calculation_expression(query_text, entities)
            
            if expression:
                # Use advanced calculator for rapid computation
                result = self.advanced_calculator.calculate(expression, entities.get('variables', {}))
                
                if result['success']:
                    response_text = f"**Calculation Result:**\n\n"
                    response_text += f"Expression: `{result['expression']}`\n"
                    response_text += f"Result: **{result['result']}**"
                    
                    if result.get('units'):
                        response_text += f" {result['units']}"
                    
                    response_text += f"\nCalculation Type: {result['calculation_type'].replace('_', ' ').title()}\n"
                    
                    # Add quick calculation format for simple results
                    if isinstance(result['result'], (int, float)):
                        response_text += f"\n{self.advanced_calculator.quick_calculate(expression)}"
                    
                    return {
                        'text': response_text,
                        'data': result,
                        'type': 'advanced_calculation',
                        'success': True
                    }
                else:
                    return self._error_response(f"Calculation failed: {result['error']}")
            
            # Fallback to original calculator if no expression found
            result = self.calculator.calculate(nlu_result, context)
            return {
                'text': result['explanation'],
                'data': result,
                'type': 'calculation',
                'success': True
            }
            
        except Exception as e:
            return self._error_response(f"Calculation error: {str(e)}")
    
    def _extract_calculation_expression(self, query_text: str, entities: Dict) -> str:
        """Extract mathematical expression from query text."""
        import re
        
        # Common calculation patterns
        calc_patterns = [
            r'calculate\s+(.+)',
            r'compute\s+(.+)',
            r'solve\s+(.+)',
            r'what\s+is\s+(.+)',
            r'find\s+(.+)',
            r'evaluate\s+(.+)',
        ]
        
        query_lower = query_text.lower().strip()
        
        # Try to match calculation patterns
        for pattern in calc_patterns:
            match = re.search(pattern, query_lower)
            if match:
                expression = match.group(1).strip()
                # Clean up common words
                expression = re.sub(r'\b(the|value|of|for|equals?|equal\s+to)\b', '', expression)
                expression = expression.strip()
                if expression:
                    return expression
        
        # If no pattern matches, check if the entire query looks like a math expression
        math_chars = set('0123456789+-*/^().,=<>sincostandlogexpqrtabsfloorceil')
        if len(set(query_lower.replace(' ', '')) & math_chars) > len(query_lower.replace(' ', '')) * 0.5:
            return query_text.strip()
        
        return ""
    
    def _handle_equation(self, nlu_result: Dict, context: Dict = None) -> Dict[str, Any]:
        """Handle equation and formula requests."""
        try:
            query_text = nlu_result.get('processed_text', '')
            entities = nlu_result.get('entities', {})
            
            # Check if it's a calculation request
            if any(word in query_text.lower() for word in ['calculate', 'solve', 'compute']):
                # Extract equation name and variables
                equation_name = entities.get('equation_name', '')
                variables = entities.get('variables', {})
                
                if equation_name and variables:
                    result = self.equation_engine.calculate(equation_name, variables)
                    if 'error' in result:
                        return self._error_response(result['error'])
                    
                    response_text = f"**{result['equation']}**\n\n"
                    response_text += f"Formula: {result['formula']}\n"
                    response_text += f"Variables: {', '.join([f'{k}={v}' for k, v in result['variables'].items()])}\n"
                    response_text += f"Result: {result['result']} {result['units']}\n\n"
                    response_text += f"Description: {result['description']}"
                    
                    return {
                        'text': response_text,
                        'data': result,
                        'type': 'equation_calculation',
                        'success': True
                    }
            
            # Search for equations
            elif any(word in query_text.lower() for word in ['find', 'search', 'show', 'list']):
                search_query = query_text.lower()
                results = self.equation_engine.search_equations(search_query)
                
                if not results:
                    return {
                        'text': f"No equations found matching '{query_text}'. Try searching for physics, math, engineering, or chemistry formulas.",
                        'type': 'equation_search',
                        'success': True
                    }
                
                response_text = f"**Found {len(results)} equation(s) matching '{query_text}':**\n\n"
                for i, eq in enumerate(results[:5], 1):  # Limit to top 5 results
                    response_text += f"{i}. **{eq['name']}**\n"
                    response_text += f"   Formula: {eq['formula']}\n"
                    response_text += f"   Category: {eq.get('category', 'Unknown')}\n"
                    response_text += f"   Description: {eq.get('description', 'No description')}\n\n"
                
                if len(results) > 5:
                    response_text += f"... and {len(results) - 5} more results. Be more specific to narrow down the search."
                
                return {
                    'text': response_text,
                    'data': {'results': results, 'count': len(results)},
                    'type': 'equation_search',
                    'success': True
                }
            
            # Unit conversion request
            elif any(word in query_text.lower() for word in ['convert', 'conversion']):
                # Try to extract conversion parameters from entities
                value = entities.get('value', 0)
                from_unit = entities.get('from_unit', '')
                to_unit = entities.get('to_unit', '')
                
                if value and from_unit and to_unit:
                    result = self.equation_engine.convert_units(value, from_unit, to_unit)
                    if 'error' in result:
                        return self._error_response(result['error'])
                    
                    response_text = f"**Unit Conversion**\n\n"
                    response_text += f"{result['original_value']} {result['original_unit']} = "
                    response_text += f"{result['converted_value']:.6f} {result['converted_unit']}\n\n"
                    response_text += f"Conversion factor: {result['conversion_factor']}"
                    
                    return {
                        'text': response_text,
                        'data': result,
                        'type': 'unit_conversion',
                        'success': True
                    }
                else:
                    return {
                        'text': "For unit conversion, please specify: value, from unit, and to unit. Example: 'Convert 10 meters to feet'",
                        'type': 'clarification',
                        'success': True
                    }
            
            # General equation information
            else:
                # Try to find specific equation by name
                results = self.equation_engine.search_equations(query_text)
                if results:
                    eq = results[0]  # Take the best match
                    response_text = f"**{eq['name']}**\n\n"
                    response_text += f"Formula: {eq['formula']}\n"
                    response_text += f"Variables: {eq.get('variables', 'Not specified')}\n"
                    response_text += f"Units: {eq.get('units', 'Not specified')}\n"
                    response_text += f"Category: {eq.get('category', 'Unknown')}\n\n"
                    response_text += f"Description: {eq.get('description', 'No description available')}\n\n"
                    if eq.get('applications'):
                        response_text += f"Applications: {eq['applications']}\n"
                    if eq.get('derivation'):
                        response_text += f"Derivation: {eq['derivation']}"
                    
                    return {
                        'text': response_text,
                        'data': eq,
                        'type': 'equation_info',
                        'success': True
                    }
                else:
                    return {
                        'text': f"I couldn't find information about '{query_text}'. Try searching for specific equation names, physics formulas, or mathematical concepts.",
                        'type': 'equation_info',
                        'success': True
                    }
                    
        except Exception as e:
            return self._error_response(f"Equation engine error: {str(e)}")
    
    def _handle_knowledge_query(self, nlu_result: Dict, context: Dict = None) -> Dict[str, Any]:
        """Handle knowledge base queries."""
        try:
            result = self.knowledge_base.query(nlu_result, context)
            return {
                'text': result['answer'],
                'data': result,
                'type': 'knowledge',
                'success': True
            }
        except Exception as e:
            return self._error_response(f"Knowledge query error: {str(e)}")
    
    def _handle_reminder(self, nlu_result: Dict, context: Dict = None) -> Dict[str, Any]:
        """Handle reminder and scheduling requests."""
        try:
            result = self.mission_support.handle_reminder(nlu_result, context)
            return {
                'text': result['message'],
                'data': result,
                'type': 'reminder',
                'success': True
            }
        except Exception as e:
            return self._error_response(f"Reminder error: {str(e)}")
    
    def _handle_checklist(self, nlu_result: Dict, context: Dict = None) -> Dict[str, Any]:
        """Handle checklist and procedure requests."""
        try:
            result = self.mission_support.handle_checklist(nlu_result, context)
            return {
                'text': result['message'],
                'data': result,
                'type': 'checklist',
                'success': True
            }
        except Exception as e:
            return self._error_response(f"Checklist error: {str(e)}")
    
    def _handle_logging(self, nlu_result: Dict, context: Dict = None) -> Dict[str, Any]:
        """Handle logging and note-taking requests."""
        try:
            result = self.mission_support.handle_logging(nlu_result, context)
            # Also log to mission logger
            self.mission_logger.log_astronaut_note(result.get('logged_text', ''))
            return {
                'text': result['message'],
                'data': result,
                'type': 'logging',
                'success': True
            }
        except Exception as e:
            return self._error_response(f"Logging error: {str(e)}")
    
    def _handle_emergency(self, nlu_result: Dict, context: Dict = None) -> Dict[str, Any]:
        """Handle emergency situations."""
        try:
            result = self.emergency_system.handle_emergency(nlu_result, context)
            # Log emergency
            self.mission_logger.log_emergency(
                result.get('emergency_type', 'UNKNOWN'),
                result.get('details', ''),
                result.get('response', '')
            )
            return {
                'text': result['message'],
                'data': result,
                'type': 'emergency',
                'success': True,
                'priority': 'high'
            }
        except Exception as e:
            return self._error_response(f"Emergency system error: {str(e)}")
    
    def _handle_system_status(self, nlu_result: Dict, context: Dict = None) -> Dict[str, Any]:
        """Handle system status queries."""
        try:
            status = self._get_system_status()
            return {
                'text': self._format_system_status(status),
                'data': status,
                'type': 'system_status',
                'success': True
            }
        except Exception as e:
            return self._error_response(f"System status error: {str(e)}")
    
    def _handle_general_query(self, nlu_result: Dict, context: Dict = None) -> Dict[str, Any]:
        """Handle general queries with enhanced ChatGPT-level understanding."""
        try:
            query_text = nlu_result.get('processed_text', '').lower()
            original_text = nlu_result.get('original_text', '')
            
            # Enhanced intelligent routing with better pattern matching
            # Check for calculation-related keywords (expanded)
            calc_keywords = ['calculate', 'compute', 'find', 'determine', 'what is the', 'how much', 'how fast', 'how far', 
                           'velocity', 'speed', 'distance', 'mass', 'energy', 'force', 'acceleration', 'orbit', 'delta-v',
                           'escape velocity', 'schwarzschild', 'time dilation', 'hohmann', 'radiation dose', 'bmi',
                           'convert', 'transformation', 'units', 'km', 'miles', 'meters', 'feet', 'celsius', 'fahrenheit']
            
            # Enhanced calculation detection
            calc_patterns = [
                r'\b(calculate|compute|find|determine)\b',
                r'\b(what\s+is\s+the.*?(speed|velocity|distance|mass|energy|force))\b',
                r'\b(how\s+(fast|far|much|long|heavy))\b',
                r'\b(convert.*?to)\b',
                r'\b\d+.*?(km|miles|meters|feet|celsius|fahrenheit)\b'
            ]
            
            if any(keyword in query_text for keyword in calc_keywords) or any(re.search(pattern, query_text) for pattern in calc_patterns):
                return self._handle_calculation(nlu_result, context)
            
            # Enhanced equation detection
            eq_keywords = ['equation', 'formula', 'law', 'principle', 'theorem', 'newton', 'einstein', 'kepler', 'planck']
            eq_patterns = [
                r'\b(show\s+me.*?(equation|formula))\b',
                r'\b(what.*?(equation|formula))\b',
                r'\b(newton|einstein|kepler)\b'
            ]
            
            if any(keyword in query_text for keyword in eq_keywords) or any(re.search(pattern, query_text) for pattern in eq_patterns):
                return self._handle_equation(nlu_result, context)
            
            # Enhanced space knowledge detection
            space_keywords = ['mars', 'jupiter', 'saturn', 'earth', 'moon', 'sun', 'planet', 'star', 'galaxy', 'universe',
                            'spacecraft', 'iss', 'hubble', 'voyager', 'apollo', 'artemis', 'mission', 'orbit', 'space',
                            'constellation', 'exoplanet', 'black hole', 'neutron star', 'supernova', 'nebula', 'cosmos',
                            'astrobiology', 'seti', 'dark matter', 'dark energy', 'big bang', 'cosmic microwave']
            
            knowledge_patterns = [
                r'\b(what\s+is|tell\s+me\s+about|explain|describe)\b',
                r'\b(mars|jupiter|saturn|earth|moon|sun)\b',
                r'\b(black\s+hole|neutron\s+star)\b'
            ]
            
            if any(keyword in query_text for keyword in space_keywords) or any(re.search(pattern, query_text) for pattern in knowledge_patterns):
                return self._handle_knowledge_query(nlu_result, context)
            
            # Try enhanced knowledge modules first
            enhanced_result = self._query_enhanced_knowledge(query_text, entities)
            if enhanced_result:
                return enhanced_result
            
            # Try knowledge base with enhanced search
            kb_result = self.knowledge_base.query(nlu_result, context)
            if kb_result.get('confidence', 0) > 0.3:  # Lower threshold for better coverage
                return {
                    'text': kb_result['answer'],
                    'data': kb_result,
                    'type': 'general',
                    'success': True
                }
            
            # Try equation engine search as fallback
            try:
                eq_results = self.equation_engine.search_equations(query_text)
                if eq_results:
                    eq = eq_results[0]
                    response_text = f"I found this related equation: **{eq['name']}**\n\n"
                    response_text += f"Formula: {eq['formula']}\n"
                    response_text += f"Description: {eq.get('description', 'No description available')}\n\n"
                    response_text += "Would you like me to calculate something with this equation or provide more information?"
                    
                    return {
                        'text': response_text,
                        'data': {'equation': eq},
                        'type': 'equation_suggestion',
                        'success': True
                    }
            except:
                pass
            
            # ChatGPT-level intelligent fallback with context understanding
            # Analyze the query for intent clues
            query_words = query_text.split()
            
            # Generate contextual response based on query content
            if len(query_words) == 1 and query_words[0] in ['mars', 'jupiter', 'earth', 'moon', 'sun', 'space', 'universe']:
                # Single word planet/celestial body query
                topic = query_words[0].title()
                enhanced_result = self._query_enhanced_knowledge(topic, {})
                if enhanced_result:
                    return enhanced_result
                
                fallback_text = f"I'd be happy to tell you about {topic}! Here's what I know:\n\n"
                # Try to get basic info from knowledge base
                planet_result = self.knowledge_base.query({'processed_text': f'what is {topic}'}, context)
                if planet_result.get('answer'):
                    fallback_text += planet_result['answer']
                else:
                    fallback_text += f"{topic} is a fascinating subject. Would you like to know about its characteristics, distance from Earth, or any specific details?"
                
                return {
                    'text': fallback_text,
                    'data': {'inferred_topic': topic},
                    'type': 'contextual_knowledge',
                    'success': True
                }
            
            # Handle incomplete calculation requests
            if any(word in query_text for word in ['calculate', 'compute', 'find']) and len(query_words) < 4:
                fallback_text = "I can help you calculate many things! Here are some examples:\n\n"
                fallback_text += "• **Orbital mechanics**: 'Calculate escape velocity of Mars'\n"
                fallback_text += "• **Physics**: 'Find the kinetic energy of a 1000kg object at 50 m/s'\n"
                fallback_text += "• **Unit conversion**: 'Convert 100 km to miles'\n"
                fallback_text += "• **Space distances**: 'What is the distance to Jupiter?'\n\n"
                fallback_text += "What would you like me to calculate?"
                
                return {
                    'text': fallback_text,
                    'data': {'suggested_action': 'calculation'},
                    'type': 'calculation_help',
                    'success': True
                }
            
            # Handle vague knowledge requests
            if any(word in query_text for word in ['what', 'tell', 'explain']) and len(query_words) < 3:
                fallback_text = "I'm here to help with space and science questions! You can ask me about:\n\n"
                fallback_text += "🌌 **Space objects**: planets, stars, galaxies, black holes\n"
                fallback_text += "🚀 **Space missions**: Apollo, Artemis, Voyager, Hubble\n"
                fallback_text += "⚛️ **Physics concepts**: gravity, relativity, quantum mechanics\n"
                fallback_text += "🧮 **Calculations**: orbital mechanics, energy, forces\n"
                fallback_text += "🔬 **Scientific phenomena**: supernovas, dark matter, time dilation\n\n"
                fallback_text += "What specific topic interests you?"
                
                return {
                    'text': fallback_text,
                    'data': {'suggested_action': 'knowledge'},
                    'type': 'knowledge_help',
                    'success': True
                }
            
            # Smart suggestions based on partial matches
            suggestions = []
            if any(word in query_text for word in ['calculate', 'compute', 'find', 'determine']):
                suggestions.append("🧮 **Calculations**: 'Calculate escape velocity of Earth' or 'Find orbital period of ISS'")
            if any(word in query_text for word in ['mars', 'jupiter', 'planet', 'space']):
                suggestions.append("🌌 **Space Knowledge**: 'Tell me about Mars' or 'Explain black holes'")
            if any(word in query_text for word in ['equation', 'formula', 'law']):
                suggestions.append("⚛️ **Equations**: 'Show me Newton's laws' or 'What is E=mc²?'")
            
            # Generate intelligent response
            fallback_text = f"I understand you're asking about '{original_text}'. "
            
            if suggestions:
                fallback_text += "Based on your question, you might be interested in:\n\n" + "\n".join(suggestions)
                fallback_text += "\n\nCould you provide more details about what you'd like to know?"
            else:
                fallback_text += "I can help with space knowledge, physics calculations, scientific equations, and more. "
                fallback_text += "Could you rephrase your question or provide more specific details?"
                fallback_text += "Please try rephrasing your question or be more specific about what you'd like to know."
            
            return {
                'text': fallback_text,
                'type': 'clarification',
                'success': True
            }
        except Exception as e:
            return self._error_response(f"General query error: {str(e)}")
    
    def _update_context(self, input_text: str, nlu_result: Dict):
        """Update conversation context."""
        context_entry = {
            'timestamp': time.time(),
            'input': input_text,
            'intent': nlu_result.get('intent'),
            'entities': nlu_result.get('entities', {})
        }
        
        self.conversation_context.append(context_entry)
        
        # Keep only recent context
        max_context = self.config.get('nlu.context_window', 5)
        if len(self.conversation_context) > max_context:
            self.conversation_context = self.conversation_context[-max_context:]
    
    def _get_system_status(self) -> Dict[str, Any]:
        """Get current system status."""
        return {
            'ai_engine': 'operational' if self.is_initialized else 'offline',
            'nlu_engine': 'operational' if self.nlu_engine else 'offline',
            'knowledge_base': 'operational' if self.knowledge_base else 'offline',
            'calculator': 'operational' if self.calculator else 'offline',
            'equation_engine': 'operational' if self.equation_engine else 'offline',
            'mission_support': 'operational' if self.mission_support else 'offline',
            'emergency_system': 'operational' if self.emergency_system else 'offline',
            'context_size': len(self.conversation_context),
            'uptime': time.time() - getattr(self, 'start_time', time.time())
        }
    
    def _format_system_status(self, status: Dict) -> str:
        """Format system status for display."""
        lines = ["🚀 Space AI Assistant System Status:"]
        for component, state in status.items():
            if component == 'uptime':
                hours = int(state // 3600)
                minutes = int((state % 3600) // 60)
                lines.append(f"  ⏱️  Uptime: {hours}h {minutes}m")
            elif component == 'context_size':
                lines.append(f"  🧠 Context: {state} recent interactions")
            else:
                emoji = "✅" if state == "operational" else "❌"
                lines.append(f"  {emoji} {component.replace('_', ' ').title()}: {state}")
        return "\n".join(lines)
    
    def _error_response(self, error_msg: str) -> Dict[str, Any]:
        """Generate error response."""
        return {
            'text': f"I encountered an issue: {error_msg}. Please try again or contact mission control if the problem persists.",
            'type': 'error',
            'success': False,
            'error': error_msg
        }
    
    def _clarification_response(self, nlu_result: Dict) -> Dict[str, Any]:
        """Generate clarification request."""
        return {
            'text': "I'm not sure what you're asking about. Could you please rephrase your question or provide more specific details?",
            'type': 'clarification',
            'success': True,
            'confidence': nlu_result.get('confidence', 0.0)
        }
    
    def _query_enhanced_knowledge(self, query: str, entities: Dict) -> Optional[Dict[str, Any]]:
        """Query enhanced knowledge modules for comprehensive responses."""
        try:
            # Check if enhanced modules are available
            if not all([self.galaxy_db, self.exoplanet_db, self.stellar_catalog, self.solar_system_db, self.deep_space_db, self.space_missions_db]):
                return None
            
            # Check for galaxy-related queries
            galaxy_keywords = ['galaxy', 'galaxies', 'milky way', 'andromeda', 'spiral', 'elliptical', 'cluster', 'supercluster', 'local group', 'virgo']
            if any(keyword in query.lower() for keyword in galaxy_keywords):
                result = self.galaxy_db.query_galaxy(query)
                if result['type'] != 'no_results':
                    return {
                        'text': self.galaxy_db.format_galaxy_info(result),
                        'data': result,
                        'type': 'enhanced_knowledge',
                        'success': True
                    }
                
                # Try cluster search
                result = self.galaxy_db.query_galaxy_cluster(query)
                if result['type'] != 'no_results':
                    return {
                        'text': self.galaxy_db.format_galaxy_info(result),
                        'data': result,
                        'type': 'enhanced_knowledge',
                        'success': True
                    }
            
            # Check for exoplanet-related queries
            exoplanet_keywords = ['exoplanet', 'planet', 'proxima', 'kepler', 'trappist', 'habitable', 'host star', 'planetary system']
            if any(keyword in query.lower() for keyword in exoplanet_keywords):
                result = self.exoplanet_db.query_exoplanet(query)
                if result['type'] != 'no_results':
                    return {
                        'text': self.exoplanet_db.format_exoplanet_info(result),
                        'data': result,
                        'type': 'enhanced_knowledge',
                        'success': True
                    }
                
                # Try host star search
                result = self.exoplanet_db.query_host_star(query)
                if result['type'] != 'no_results':
                    return {
                        'text': self.exoplanet_db.format_exoplanet_info(result),
                        'data': result,
                        'type': 'enhanced_knowledge',
                        'success': True
                    }
            
            # Check for stellar queries
            stellar_keywords = ['star', 'stellar', 'constellation', 'sirius', 'betelgeuse', 'vega', 'polaris', 'sun']
            if any(keyword in query.lower() for keyword in stellar_keywords):
                result = self.stellar_catalog.query_star(query)
                if result['type'] != 'no_results':
                    return {
                        'text': self.stellar_catalog.format_star_info(result),
                        'data': result,
                        'type': 'enhanced_knowledge',
                        'success': True
                    }
            
            # Check for solar system queries
            solar_system_keywords = ['mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto', 
                                   'moon', 'europa', 'titan', 'enceladus', 'io', 'ganymede', 'callisto', 'phobos', 'deimos',
                                   'asteroid', 'ceres', 'vesta', 'pallas', 'hygiea', 'eros', 'itokawa',
                                   'comet', 'halley', 'hale-bopp', 'hyakutake', 'neowise', 'encke',
                                   'dwarf planet', 'eris', 'makemake', 'haumea', 'planet', 'solar system']
            if any(keyword in query.lower() for keyword in solar_system_keywords):
                result = self.solar_system_db.query_solar_system(query)
                if result['type'] != 'no_results':
                    return {
                        'text': self.solar_system_db.format_solar_system_info(result),
                        'data': result,
                        'type': 'enhanced_knowledge',
                        'success': True
                    }
            
            # Check for deep space queries
            deep_space_keywords = ['nebula', 'nebulae', 'orion nebula', 'crab nebula', 'eagle nebula', 'horsehead', 'ring nebula',
                                 'cluster', 'pleiades', 'hyades', 'beehive', 'globular', 'open cluster',
                                 'quasar', '3c 273', '3c 48', 'ton 618', 'quasi-stellar',
                                 'pulsar', 'crab pulsar', 'vela pulsar', 'neutron star', 'millisecond pulsar']
            if any(keyword in query.lower() for keyword in deep_space_keywords):
                result = self.deep_space_db.query_deep_space(query)
                if result['type'] != 'no_results':
                    return {
                        'text': self.deep_space_db.format_deep_space_info(result),
                        'data': result,
                        'type': 'enhanced_knowledge',
                        'success': True
                    }
            
            # Check for space missions queries
            missions_keywords = ['mission', 'apollo', 'voyager', 'cassini', 'hubble', 'james webb', 'perseverance', 'curiosity',
                               'spacecraft', 'shuttle', 'soyuz', 'dragon', 'falcon', 'saturn v', 'starship',
                               'astronaut', 'armstrong', 'gagarin', 'aldrin', 'glenn', 'ride', 'hadfield',
                               'iss', 'space station', 'mir', 'skylab', 'launch', 'landing', 'eva', 'spacewalk']
            if any(keyword in query.lower() for keyword in missions_keywords):
                result = self.space_missions_db.query_space_missions(query)
                if result['type'] != 'no_results':
                    return {
                        'text': self.space_missions_db.format_missions_info(result),
                        'data': result,
                        'type': 'enhanced_knowledge',
                        'success': True
                    }
            
            # Handle general space queries
            space_keywords = ['space', 'universe', 'cosmos', 'astronomy', 'astrophysics']
            if any(keyword in query.lower() for keyword in space_keywords):
                if 'space' in query.lower():
                    return {
                        'text': self._get_space_overview(),
                        'data': {'topic': 'space_overview'},
                        'type': 'enhanced_knowledge',
                        'success': True
                    }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Enhanced knowledge query failed: {e}")
            return None
    
    def _get_space_overview(self) -> str:
        """Provide comprehensive overview of space."""
        return """**Space: The Final Frontier**

Space, also known as outer space, is the vast expanse that exists beyond Earth's atmosphere. Here's what makes it fascinating:

**🌌 Scale and Structure:**
• The observable universe is about 93 billion light-years in diameter
• Contains over 2 trillion galaxies, each with billions of stars
• Organized in a cosmic web of filaments, clusters, and voids

**🪐 Our Solar System:**
• 8 planets orbiting our Sun (a G-type main-sequence star)
• Hundreds of moons, asteroids, comets, and other objects
• Located in the Milky Way's Orion Arm, ~26,000 light-years from center

**🔭 Key Discoveries:**
• **Exoplanets**: Over 5,000 confirmed planets around other stars
• **Dark Matter & Energy**: Make up ~95% of the universe
• **Cosmic Microwave Background**: Afterglow of the Big Bang

**🚀 Human Exploration:**
• International Space Station orbits Earth every 90 minutes
• 12 humans have walked on the Moon (Apollo missions)
• Robotic missions have visited every planet in our solar system

**🌟 Current Frontiers:**
• Search for extraterrestrial life and biosignatures
• Understanding black holes and gravitational waves
• Planning missions to Mars and beyond

Would you like to explore any specific aspect of space in more detail?"""

    def shutdown(self):
        """Shutdown the AI engine and all components."""
        self.logger.info("Shutting down AI Engine...")
        self.is_running = False
        
        # Shutdown components
        components = [
            self.nlu_engine,
            self.knowledge_base,
            self.calculator,
            self.equation_engine,
            self.mission_support,
            self.emergency_system
        ]
        
        for component in components:
            if component and hasattr(component, 'shutdown'):
                try:
                    component.shutdown()
                except Exception as e:
                    self.logger.error(f"Error shutting down component: {e}")
        
        self.mission_logger.log_system_status("AI_ENGINE", "SHUTDOWN", "Clean shutdown completed")
        self.logger.info("AI Engine shutdown complete")
