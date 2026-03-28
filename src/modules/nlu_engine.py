"""
Natural Language Understanding Engine for Space AI Assistant.
Handles intent recognition, entity extraction, and context understanding.
"""

import re
import json
import logging
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

class NLUEngine:
    """Offline Natural Language Understanding engine optimized for space operations."""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("NLU_Engine")
        
        # Intent patterns and keywords
        self.intent_patterns = self._load_intent_patterns()
        self.entity_patterns = self._load_entity_patterns()
        self.space_vocabulary = self._load_space_vocabulary()
        
        # Context tracking
        self.conversation_history = []
        
    def _load_intent_patterns(self) -> Dict[str, List[str]]:
        """Load intent recognition patterns."""
        return {
            'calculate': [
                # Physics and space calculations
                r'\b(calculate|compute|find|determine|what\s+is|how\s+much|how\s+fast|how\s+far)\b.*\b(velocity|speed|distance|mass|force|energy|orbit|delta-v|fuel|acceleration|momentum|trajectory)\b',
                r'\b(escape\s+velocity|orbital\s+period|rocket\s+equation|hohmann\s+transfer|schwarzschild\s+radius|time\s+dilation)\b',
                r'\b(gravity|gravitational|centripetal|kinetic\s+energy|potential\s+energy|angular\s+momentum)\b',
                r'\b(radiation\s+dose|structural\s+stress|thermal|heat\s+transfer|fluid\s+dynamics)\b',
                r'\b(bmi|body\s+mass\s+index|cardiac\s+output|blood\s+pressure|metabolic\s+rate)\b',
            ],
            'equation': [
                r'\b(equation|formula|law|theorem)\b',
                r'\b(einstein|newton|kepler|planck|boltzmann|stefan)\b',
                r'\b(E\s*=\s*mc|F\s*=\s*ma|a\s*=\s*GM/r)\b',
                r'\b(show\s+me.*?(formula|equation))\b'
            ],
            'knowledge': [
                # Basic question patterns
                r'\b(what\s+is|what\s+are|what\'s)\b',
                r'\b(tell\s+me\s+about|tell\s+me)\b',
                r'\b(explain|describe|define)\b',
                r'\b(how\s+does|how\s+do|how\s+can|how\s+is)\b',
                r'\b(why\s+does|why\s+do|why\s+is|why\s+are)\b',
                r'\b(where\s+is|where\s+are|where\s+can)\b',
                r'\b(when\s+did|when\s+does|when\s+will)\b',
                r'\b(who\s+is|who\s+are|who\s+discovered)\b',
                r'\b(which\s+is|which\s+are|which\s+planet)\b',
                
                # Information request patterns
                r'\b(information\s+about|facts\s+about|details\s+about)\b',
                r'\b(can\s+you\s+tell|do\s+you\s+know)\b',
                r'\b(i\s+want\s+to\s+know|i\s+need\s+to\s+know)\b',
                
                # Space-specific terms
                r'\b(planet|star|galaxy|nebula|asteroid|comet|meteor)\b',
                r'\b(mission|spacecraft|satellite|ISS|space\s+station|rocket|probe)\b',
                r'\b(atmosphere|radiation|temperature|pressure|magnetic\s+field|gravity)\b',
                r'\b(exoplanet|black\s+hole|neutron\s+star|supernova|quasar|pulsar)\b',
                r'\b(constellation|nebula|cluster|void|dark\s+matter|dark\s+energy)\b',
                r'\b(apollo|artemis|voyager|cassini|hubble|james\s+webb|kepler|tess)\b',
                r'\b(mars|venus|jupiter|saturn|earth|mercury|uranus|neptune|pluto)\b',
                r'\b(astrobiology|seti|biosignature|extremophile|habitable\s+zone)\b',
                r'\b(cosmology|big\s+bang|cosmic\s+microwave|inflation|multiverse)\b',
                
                # Common question formats
                r'\b(what.*?(mars|jupiter|saturn|earth|moon|sun|space|universe))\b',
                r'\b(how.*?(big|large|small|hot|cold|far|fast|old))\b',
                r'\b(why.*?(is|are|does|do))\b',
                r'\b(where.*?(is|are|located))\b'
            ],
            'reminder': [
                r'\b(remind\s+me|set\s+reminder|alert\s+me|schedule)\b',
                r'\b(in\s+\d+\s+(minutes?|hours?|days?))\b',
                r'\b(at\s+\d{1,2}:\d{2})\b',
                r'\b(don\'t\s+forget|remember\s+to)\b'
            ],
            'checklist': [
                r'\b(checklist|procedure|steps|protocol|sequence)\b',
                r'\b(next\s+step|what\'s\s+next|continue\s+with)\b',
                r'\b(EVA|spacewalk|docking|launch|landing)\b',
                r'\b(mark\s+complete|check\s+off|finished\s+with)\b'
            ],
            'log': [
                r'\b(log|record|note|write\s+down|save)\b',
                r'\b(observation|reading|measurement|status)\b',
                r'\b(oxygen|pressure|temperature|fuel|battery)\b'
            ],
            'emergency': [
                r'\b(emergency|urgent|help|mayday|alert)\b',
                r'\b(fire|leak|depressurization|radiation|medical)\b',
                r'\b(abort|evacuate|seal|isolate)\b',
                r'\b(life\s+support|oxygen|pressure\s+loss)\b'
            ],
            'status': [
                r'\b(status|health|check|diagnostic|report)\b',
                r'\b(system|component|module|subsystem)\b',
                r'\b(operational|online|offline|fault|error)\b'
            ],
            'unit_conversion': [
                r'\b(convert|change|transform)\b.*\b(to|into|in)\b',
                r'\b(km|miles|AU|light-years|meters|feet)\b',
                r'\b(kg|pounds|tons|grams)\b',
                r'\b(celsius|fahrenheit|kelvin)\b'
            ]
        }
    
    def _load_entity_patterns(self) -> Dict[str, List[str]]:
        """Load entity extraction patterns."""
        return {
            'celestial_body': [
                r'\b(Earth|Mars|Venus|Jupiter|Saturn|Uranus|Neptune|Mercury|Pluto)\b',
                r'\b(Moon|Europa|Titan|Io|Ganymede|Callisto|Enceladus|Phobos|Deimos|Triton)\b',
                r'\b(Sun|Alpha\s+Centauri|Proxima\s+Centauri|Sirius|Betelgeuse|Vega|Polaris)\b',
                r'\b(Andromeda|Milky\s+Way|Orion\s+Nebula|Crab\s+Nebula|Eagle\s+Nebula)\b',
                r'\b(Sagittarius\s+A|Cygnus\s+X-1|Vela\s+Pulsar)\b'
            ],
            'spacecraft': [
                r'\b(ISS|International\s+Space\s+Station)\b',
                r'\b(Hubble|James\s+Webb|Kepler|Voyager|Cassini|New\s+Horizons|Juno)\b',
                r'\b(Dragon|Falcon|Soyuz|Artemis|Orion|Apollo|Shuttle)\b',
                r'\b(Perseverance|Curiosity|Opportunity|Spirit|InSight)\b',
                r'\b(JWST|HST|Spitzer|Chandra|TESS)\b'
            ],
            'physics_concept': [
                r'\b(escape\s+velocity|orbital\s+velocity|delta-v|hohmann\s+transfer)\b',
                r'\b(schwarzschild\s+radius|event\s+horizon|time\s+dilation|redshift)\b',
                r'\b(kinetic\s+energy|potential\s+energy|angular\s+momentum|conservation)\b',
                r'\b(gravity|gravitational|centripetal|centrifugal|tidal\s+force)\b',
                r'\b(radiation|electromagnetic|thermal|nuclear|fusion|fission)\b'
            ],
            'measurement': [
                r'\b(\d+(?:\.\d+)?)\s*(km|miles|meters|feet|AU|light-years|parsecs)\b',
                r'\b(\d+(?:\.\d+)?)\s*(kg|pounds|tons|grams|solar\s+masses)\b',
                r'\b(\d+(?:\.\d+)?)\s*(°C|°F|K|celsius|fahrenheit|kelvin)\b',
                r'\b(\d+(?:\.\d+)?)\s*(m/s|km/h|mph|knots|c)\b',
                r'\b(\d+(?:\.\d+)?)\s*(years?|days?|hours?|minutes?|seconds?)\b',
                r'\b(\d+(?:\.\d+)?)\s*(Pa|psi|atm|bar|torr)\b',
                r'\b(\d+(?:\.\d+)?)\s*(J|eV|cal|BTU|kWh)\b'
            ],
            'mathematical_variable': [
                r'\b(mass|m)\s*=\s*(\d+(?:\.\d+)?)\b',
                r'\b(velocity|v)\s*=\s*(\d+(?:\.\d+)?)\b',
                r'\b(distance|d|r)\s*=\s*(\d+(?:\.\d+)?)\b',
                r'\b(time|t)\s*=\s*(\d+(?:\.\d+)?)\b',
                r'\b(force|F)\s*=\s*(\d+(?:\.\d+)?)\b',
                r'\b(energy|E)\s*=\s*(\d+(?:\.\d+)?)\b',
                r'\b(acceleration|a)\s*=\s*(\d+(?:\.\d+)?)\b',
                r'\b(radius|R)\s*=\s*(\d+(?:\.\d+)?)\b'
            ],
            'time': [
                r'\b(\d{1,2}:\d{2}(?::\d{2})?)\b',
                r'\b(\d+)\s+(seconds?|minutes?|hours?|days?|weeks?|months?|years?)\b',
                r'\b(in|after|at)\s+(\d+)\s+(minutes?|hours?|days?)\b'
            ],
            'system_component': [
                r'\b(life\s+support|oxygen|CO2|pressure|temperature)\b',
                r'\b(fuel|battery|power|solar\s+panels|radiator)\b',
                r'\b(navigation|guidance|communication|radar)\b',
                r'\b(airlock|hatch|docking\s+port|robotic\s+arm)\b'
            ]
        }
    
    def _load_space_vocabulary(self) -> Dict[str, str]:
        """Load space-specific vocabulary and abbreviations."""
        return {
            'EVA': 'Extra-Vehicular Activity',
            'ISS': 'International Space Station',
            'LEO': 'Low Earth Orbit',
            'GEO': 'Geostationary Earth Orbit',
            'AU': 'Astronomical Unit',
            'ESA': 'European Space Agency',
            'NASA': 'National Aeronautics and Space Administration',
            'JAXA': 'Japan Aerospace Exploration Agency',
            'CSA': 'Canadian Space Agency',
            'EMU': 'Extravehicular Mobility Unit',
            'ECLSS': 'Environmental Control and Life Support System',
            'RCS': 'Reaction Control System',
            'OMS': 'Orbital Maneuvering System',
            'SSRMS': 'Space Station Remote Manipulator System'
        }
    
    def parse(self, text: str, context: Dict = None) -> Dict[str, Any]:
        """
        Parse input text to extract intent, entities, and context.
        
        Args:
            text: Input text to parse
            context: Additional context information
            
        Returns:
            Dictionary containing intent, entities, confidence, and metadata
        """
        try:
            # Preprocess text
            processed_text = self._preprocess_text(text)
            
            # Extract intent
            intent, intent_confidence = self._extract_intent(processed_text)
            
            # Extract entities
            entities = self._extract_entities(processed_text)
            
            # Calculate overall confidence
            confidence = self._calculate_confidence(intent_confidence, entities, processed_text)
            
            # Build result
            result = {
                'original_text': text,
                'processed_text': processed_text,
                'intent': intent,
                'entities': entities,
                'confidence': confidence,
                'intent_confidence': intent_confidence,
                'context': context or {}
            }
            
            # Update conversation history
            self._update_history(result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error parsing text: {e}")
            return {
                'original_text': text,
                'intent': 'unknown',
                'entities': {},
                'confidence': 0.0,
                'error': str(e)
            }
    
    def _preprocess_text(self, text: str) -> str:
        """Preprocess input text."""
        # Convert to lowercase
        text = text.lower().strip()
        
        # Expand abbreviations
        for abbrev, full_form in self.space_vocabulary.items():
            text = re.sub(rf'\b{re.escape(abbrev.lower())}\b', full_form.lower(), text)
        
        # Normalize whitespace
        text = re.sub(r'\s+', ' ', text)
        
        return text
    
    def _extract_intent(self, text: str) -> Tuple[str, float]:
        """Extract intent from text using pattern matching."""
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0.0
            matches = 0
            
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    matches += 1
                    # Weight by pattern specificity
                    pattern_weight = len(pattern.split('|')) / 10.0
                    score += pattern_weight
            
            if matches > 0:
                # Normalize score by number of patterns
                intent_scores[intent] = score / len(patterns)
        
        if not intent_scores:
            return 'unknown', 0.0
        
        # Get highest scoring intent
        best_intent = max(intent_scores.items(), key=lambda x: x[1])
        return best_intent[0], min(best_intent[1], 1.0)
    
    def _extract_entities(self, text: str) -> Dict[str, List[Dict]]:
        """Extract entities from text."""
        entities = {}
        
        for entity_type, patterns in self.entity_patterns.items():
            entity_matches = []
            
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    entity_matches.append({
                        'value': match.group(),
                        'start': match.start(),
                        'end': match.end(),
                        'confidence': 0.9  # High confidence for pattern matches
                    })
            
            if entity_matches:
                entities[entity_type] = entity_matches
        
        return entities
    
    def _calculate_confidence(self, intent_confidence: float, entities: Dict, text: str) -> float:
        """Calculate overall confidence score."""
        # Base confidence from intent (more generous)
        confidence = intent_confidence * 0.8
        
        # Boost confidence if entities are found
        if entities:
            entity_boost = min(len(entities) * 0.15, 0.4)
            confidence += entity_boost
        
        # Boost confidence for common question words
        question_words = ['what', 'how', 'why', 'where', 'when', 'who', 'which', 'tell', 'explain', 'describe']
        if any(word in text.lower() for word in question_words):
            confidence += 0.2
        
        # Boost confidence for space-related terms
        space_terms = ['mars', 'jupiter', 'earth', 'moon', 'sun', 'planet', 'star', 'galaxy', 'space', 'universe', 'orbit', 'rocket']
        if any(term in text.lower() for term in space_terms):
            confidence += 0.15
        
        # Boost confidence for longer, more specific queries
        text_length_boost = min(len(text.split()) * 0.02, 0.15)
        confidence += text_length_boost
        
        # Less penalty for short queries if they contain question words
        if len(text.split()) < 3:
            if any(word in text.lower() for word in question_words):
                confidence *= 0.9  # Less penalty
            else:
                confidence *= 0.7
        
        return min(confidence, 1.0)
    
    def _update_history(self, result: Dict):
        """Update conversation history."""
        self.conversation_history.append({
            'timestamp': self._get_timestamp(),
            'intent': result['intent'],
            'entities': result['entities'],
            'confidence': result['confidence']
        })
        
        # Keep only recent history
        max_history = self.config.get('nlu.context_window', 5)
        if len(self.conversation_history) > max_history:
            self.conversation_history = self.conversation_history[-max_history:]
    
    def _get_timestamp(self) -> float:
        """Get current timestamp."""
        import time
        return time.time()
    
    def get_context_summary(self) -> Dict[str, Any]:
        """Get summary of recent conversation context."""
        if not self.conversation_history:
            return {}
        
        recent_intents = [item['intent'] for item in self.conversation_history[-3:]]
        avg_confidence = sum(item['confidence'] for item in self.conversation_history[-3:]) / len(self.conversation_history[-3:])
        
        return {
            'recent_intents': recent_intents,
            'average_confidence': avg_confidence,
            'conversation_length': len(self.conversation_history)
        }
    
    def reset_context(self):
        """Reset conversation context."""
        self.conversation_history = []
        self.logger.info("NLU context reset")
    
    def shutdown(self):
        """Shutdown the NLU engine."""
        self.logger.info("NLU Engine shutting down")
        self.conversation_history = []
