#!/usr/bin/env python3
"""
RONIN - Robotic Operations & Navigation Intelligence Network
Command-line interface for the space AI assistant system
"""

import sys
import logging
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.utils.config import Config
from src.core.ai_engine import SpaceAIEngine

def setup_logging(config):
    """Setup logging configuration"""
    log_level = getattr(logging, config.get('log_level', 'INFO').upper())
    log_format = config.get('log_format', '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.FileHandler(config.get('log_file', 'data/logs/ai_engine.log')),
        ]
    )

def print_banner():
    """Print RONIN banner"""
    print("\n" + "="*60)
    print("🚀 RONIN - Robotic Operations & Navigation Intelligence Network")
    print("   Advanced Space AI Assistant - Command Line Interface")
    print("="*60)
    print("Commands:")
    print("  • Type your questions naturally")
    print("  • 'help' - Show available commands")
    print("  • 'exit' or 'quit' - Exit the program")
    print("  • 'clear' - Clear screen")
    print("="*60 + "\n")

def print_help():
    """Print help information"""
    print("\n🔍 RONIN HELP - What I can do:")
    print("-" * 40)
    print("🌌 SPACE KNOWLEDGE:")
    print("  • 'What is Mars?' - Planet information")
    print("  • 'Tell me about Jupiter' - Celestial body details")
    print("  • 'Explain black holes' - Space phenomena")
    print()
    print("🧮 CALCULATIONS:")
    print("  • 'Calculate escape velocity of Earth'")
    print("  • 'Convert 100 km to miles'")
    print("  • 'Find orbital period of ISS'")
    print()
    print("⚛️ EQUATIONS & FORMULAS:")
    print("  • 'Show me Newton's laws'")
    print("  • 'What is E=mc²?'")
    print("  • 'Kinetic energy equation'")
    print()
    print("🚀 SPACE MISSIONS:")
    print("  • 'Tell me about Apollo 11'")
    print("  • 'Voyager mission details'")
    print("  • 'ISS information'")
    print("-" * 40 + "\n")

def main():
    """Main command-line interface"""
    try:
        # Load configuration
        config = Config()
        
        # Setup logging (file only, no console output)
        setup_logging(config)
        logger = logging.getLogger(__name__)
        
        logger.info("Starting RONIN Space AI Assistant (CLI mode)...")
        
        # Initialize AI engine
        print("🔧 Initializing RONIN AI Engine...")
        ai_engine = SpaceAIEngine(config)
        print("✅ RONIN AI Engine ready!")
        
        # Print banner
        print_banner()
        
        # Main interaction loop
        while True:
            try:
                # Get user input
                user_input = input("🚀 RONIN> ").strip()
                
                # Handle special commands
                if user_input.lower() in ['exit', 'quit', 'q']:
                    print("\n👋 Goodbye! Safe travels, astronaut!")
                    break
                elif user_input.lower() == 'help':
                    print_help()
                    continue
                elif user_input.lower() == 'clear':
                    import os
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print_banner()
                    continue
                elif not user_input:
                    continue
                
                # Process query with AI engine
                print("\n🤖 Processing...")
                response = ai_engine.process_input(user_input, "text")
                
                # Display response
                print("\n" + "="*50)
                if response.get('success', False):
                    print("📡 RONIN RESPONSE:")
                    print("-" * 20)
                    print(response.get('text', 'No response available'))
                    
                    # Show additional info if available
                    response_type = response.get('type', '')
                    if response_type:
                        print(f"\n📊 Response Type: {response_type}")
                else:
                    print("❌ ERROR:")
                    print("-" * 10)
                    print(response.get('error', 'Unknown error occurred'))
                
                print("="*50 + "\n")
                
            except KeyboardInterrupt:
                print("\n\n👋 Goodbye! Safe travels, astronaut!")
                break
            except Exception as e:
                print(f"\n❌ Error: {e}")
                logger.error(f"CLI error: {e}")
        
    except Exception as e:
        print(f"Fatal error starting RONIN: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
