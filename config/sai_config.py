#!/usr/bin/env python3
"""
Simple configuration loader for RONIN
"""

import yaml
from pathlib import Path

class SimpleConfig:
    def __init__(self):
        self.data_dir = Path("data")
        self.knowledge_dir = self.data_dir / "knowledge"
        self.logs_dir = self.data_dir / "logs"
        
        # Create directories if they don't exist
        self.data_dir.mkdir(exist_ok=True)
        self.knowledge_dir.mkdir(exist_ok=True)
        self.logs_dir.mkdir(exist_ok=True)
        
        # Default configuration
        self.config = {
            'log_level': 'INFO',
            'log_format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            'log_file': str(self.logs_dir / 'ai_engine.log'),
            'data_directory': str(self.data_dir),
            'knowledge_directory': str(self.knowledge_dir),
            'logs_directory': str(self.logs_dir)
        }
    
    def get(self, key, default=None):
        return self.config.get(key, default)

def load_config():
    """Load configuration - simplified version"""
    return SimpleConfig()
