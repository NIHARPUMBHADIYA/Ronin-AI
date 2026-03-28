#!/usr/bin/env python3
"""
RONIN - Simple Terminal Search Interface
Simplified command-line search for space knowledge
"""

import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent / "src"))

from src.modules.knowledge_base import SpaceKnowledgeBase
from src.modules.nlu_engine import NLUEngine
from src.modules.calculator import SpaceCalculator
from src.modules.equation_engine import EquationEngine

class SimpleSearchEngine:
    def __init__(self):
        """Initialize simple search engine"""
        # Create data directories
        self.data_dir = Path("data")
        self.knowledge_dir = self.data_dir / "knowledge"
        self.logs_dir = self.data_dir / "logs"
        
        self.data_dir.mkdir(exist_ok=True)
        self.knowledge_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        
        # Initialize components
        self.knowledge_base = SpaceKnowledgeBase(str(self.knowledge_dir))
        self.nlu_engine = NLUEngine()
        self.calculator = SpaceCalculator(None)
        self.equation_engine = EquationEngine()
    
    def search(self, query):
        """Process search query and return response"""
        try:
            # Parse query with NLU
            nlu_result = self.nlu_engine.parse(query)
            intent = nlu_result.get('intent', 'unknown')
            
            # Route based on intent
            if intent == 'calculate':
                return self._handle_calculation(query, nlu_result)
            elif intent == 'equation':
                return self._handle_equation(query, nlu_result)
            elif intent == 'knowledge':
                return self._handle_knowledge(query, nlu_result)
            else:
                return self._handle_general(query, nlu_result)
                
        except Exception as e:
            return f"Error processing query: {str(e)}"
    
    def _handle_calculation(self, query, nlu_result):
        """Handle calculation queries"""
        try:
            result = self.calculator.calculate(nlu_result)
            if result.get('success'):
                return f"**Calculation Result:**\n{result['result']}\n\n{result.get('explanation', '')}"
            else:
                return f"Calculation error: {result.get('error', 'Unknown error')}"
        except Exception as e:
            return f"Calculation failed: {str(e)}"
    
    def _handle_equation(self, query, nlu_result):
        """Handle equation queries"""
        try:
            result = self.equation_engine.find_equation(nlu_result)
            if result.get('success'):
                equations = result.get('equations', [])
                if equations:
                    response = "**Equations Found:**\n\n"
                    for eq in equations[:3]:  # Show top 3
                        response += f"**{eq['name']}**\n"
                        response += f"Formula: {eq['formula']}\n"
                        response += f"Description: {eq['description']}\n\n"
                    return response
                else:
                    return "No equations found for your query."
            else:
                return f"Equation search error: {result.get('error', 'Unknown error')}"
        except Exception as e:
            return f"Equation search failed: {str(e)}"
    
    def _handle_knowledge(self, query, nlu_result):
        """Handle knowledge queries"""
        try:
            result = self.knowledge_base.query(nlu_result)
            if result.get('answer'):
                return result['answer']
            else:
                return "I don't have information about that topic in my knowledge base."
        except Exception as e:
            return f"Knowledge search failed: {str(e)}"
    
    def _handle_general(self, query, nlu_result):
        """Handle general queries"""
        # Try knowledge base first
        try:
            kb_result = self.knowledge_base.query(nlu_result)
            if kb_result.get('confidence', 0) > 0.3:
                return kb_result['answer']
        except:
            pass
        
        # Fallback response
        return f"I understand you're asking about '{query}'. I can help with:\n\n" \
               "🌌 **Space Knowledge**: planets, stars, missions, spacecraft\n" \
               "🧮 **Calculations**: orbital mechanics, physics, unit conversions\n" \
               "⚛️ **Equations**: scientific formulas and laws\n\n" \
               "Try being more specific about what you'd like to know!"

def print_banner():
    """Print search interface banner"""
    print("\n" + "="*60)
    print("🚀 RONIN - Space Knowledge Search Terminal")
    print("   Type your questions and get instant answers!")
    print("="*60)
    print("Commands:")
    print("  • Type any space/science question")
    print("  • 'help' - Show examples")
    print("  • 'exit' or 'quit' - Exit")
    print("  • 'clear' - Clear screen")
    print("="*60 + "\n")

def print_help():
    """Print help examples"""
    print("\n🔍 SEARCH EXAMPLES:")
    print("-" * 30)
    print("🌌 **Knowledge Queries:**")
    print("  • What is Mars?")
    print("  • Tell me about Jupiter")
    print("  • Explain black holes")
    print()
    print("🧮 **Calculations:**")
    print("  • Calculate escape velocity of Earth")
    print("  • Convert 100 km to miles")
    print("  • Find orbital period of ISS")
    print()
    print("⚛️ **Equations:**")
    print("  • Show me Newton's laws")
    print("  • What is E=mc²?")
    print("  • Kinetic energy equation")
    print("-" * 30 + "\n")

def main():
    """Main search interface"""
    try:
        print("🔧 Initializing RONIN Search Engine...")
        search_engine = SimpleSearchEngine()
        print("✅ RONIN Search Engine ready!")
        
        print_banner()
        
        while True:
            try:
                # Get user input
                query = input("🔍 Search> ").strip()
                
                # Handle commands
                if query.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye! Happy exploring!")
                    break
                elif query.lower() == 'help':
                    print_help()
                    continue
                elif query.lower() == 'clear':
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_banner()
                    continue
                elif not query:
                    continue
                
                # Process search
                print("\n🤖 Searching...")
                response = search_engine.search(query)
                
                # Display results
                print("\n" + "="*50)
                print("📡 SEARCH RESULTS:")
                print("-" * 20)
                print(response)
                print("="*50 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Happy exploring!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
    
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
