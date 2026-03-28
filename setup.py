#!/usr/bin/env python3
"""
Setup script for Space AI Assistant (SAI)
"""

import os
import sys
import subprocess
from pathlib import Path

def create_directories():
    """Create necessary directories."""
    directories = [
        'data',
        'data/logs',
        'data/models',
        'data/knowledge',
        'data/backups',
        'data/temp',
        'config'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def install_dependencies():
    """Install required Python packages."""
    print("Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✓ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to install dependencies: {e}")
        return False
    
    return True

def download_models():
    """Download required AI models."""
    print("Downloading AI models...")
    
    try:
        # Download Whisper model for speech recognition
        import whisper
        model = whisper.load_model("base")
        print("✓ Whisper model downloaded")
    except ImportError:
        print("⚠ Whisper not available - voice input will be limited")
    except Exception as e:
        print(f"⚠ Could not download Whisper model: {e}")
    
    return True

def setup_database():
    """Initialize databases."""
    print("Setting up databases...")
    
    try:
        # Import and initialize components to create databases
        from src.utils.config import Config
        from src.modules.knowledge_base import SpaceKnowledgeBase
        from src.modules.mission_support import MissionSupport
        from src.modules.emergency_system import EmergencySystem
        
        config = Config()
        
        # Initialize knowledge base
        kb = SpaceKnowledgeBase(config)
        print("✓ Knowledge base initialized")
        
        # Initialize mission support
        ms = MissionSupport(config)
        print("✓ Mission support database initialized")
        
        # Initialize emergency system
        es = EmergencySystem(config)
        print("✓ Emergency system database initialized")
        
        return True
        
    except Exception as e:
        print(f"✗ Database setup failed: {e}")
        return False

def test_system():
    """Test basic system functionality."""
    print("Testing system components...")
    
    try:
        from src.core.ai_engine import SpaceAIEngine
        from src.utils.config import Config
        
        config = Config()
        ai_engine = SpaceAIEngine(config)
        
        # Test basic query
        test_response = ai_engine.process_input("system status", input_type="test")
        
        if test_response.get('success'):
            print("✓ AI Engine test passed")
        else:
            print("⚠ AI Engine test failed")
        
        ai_engine.shutdown()
        return True
        
    except Exception as e:
        print(f"✗ System test failed: {e}")
        return False

def main():
    """Main setup function."""
    print("=" * 60)
    print("🚀 SPACE AI ASSISTANT (SAI) - SETUP")
    print("=" * 60)
    print()
    
    success = True
    
    # Step 1: Create directories
    print("Step 1: Creating directories...")
    create_directories()
    print()
    
    # Step 2: Install dependencies
    print("Step 2: Installing dependencies...")
    if not install_dependencies():
        success = False
    print()
    
    # Step 3: Download models
    print("Step 3: Downloading AI models...")
    download_models()
    print()
    
    # Step 4: Setup databases
    print("Step 4: Setting up databases...")
    if not setup_database():
        success = False
    print()
    
    # Step 5: Test system
    print("Step 5: Testing system...")
    if not test_system():
        success = False
    print()
    
    # Final status
    if success:
        print("✅ Setup completed successfully!")
        print()
        print("To start the Space AI Assistant, run:")
        print("  python main.py")
        print()
        print("For help and documentation, see README.md")
    else:
        print("❌ Setup completed with errors.")
        print("Please check the error messages above and try again.")
        sys.exit(1)

if __name__ == "__main__":
    main()
