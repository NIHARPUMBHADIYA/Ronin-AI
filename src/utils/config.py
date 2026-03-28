"""
Configuration management for Space AI Assistant.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

class Config:
    """Configuration manager for SAI system."""
    
    def __init__(self, config_file: Optional[str] = None):
        self.project_root = Path(__file__).parent.parent.parent
        self.config_file = config_file or self.project_root / "config" / "sai_config.yaml"
        self.config_data = {}
        self.load_config()
        
    def load_config(self):
        """Load configuration from file or create default."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    self.config_data = yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
                self.config_data = {}
        
        # Apply defaults for missing values
        self._apply_defaults()
        
    def _apply_defaults(self):
        """Apply default configuration values."""
        defaults = {
            # Interface settings
            "enable_voice": True,
            "enable_text": True,
            "enable_gui": True,
            
            # Voice settings
            "voice": {
                "input_model": "whisper",  # whisper, vosk
                "output_engine": "pyttsx3",  # pyttsx3, coqui
                "wake_word": "hey sai",
                "voice_rate": 150,
                "voice_volume": 0.8,
                "language": "en-US"
            },
            
            # NLU settings
            "nlu": {
                "model": "distilbert",
                "confidence_threshold": 0.7,
                "context_window": 5
            },
            
            # Knowledge base settings
            "knowledge": {
                "database_path": "data/knowledge/space_knowledge.db",
                "update_interval": 3600  # seconds
            },
            
            # Mission settings
            "mission": {
                "log_level": "INFO",
                "max_log_size": "100MB",
                "backup_interval": 1800,  # seconds
                "emergency_mode": False
            },
            
            # System settings
            "system": {
                "max_memory_usage": "2GB",
                "cpu_threads": 4,
                "offline_mode": True,
                "security_level": "high"
            },
            
            # Paths
            "paths": {
                "data_dir": "data",
                "logs_dir": "data/logs",
                "models_dir": "data/models",
                "knowledge_dir": "data/knowledge"
            }
        }
        
        # Merge defaults with existing config
        self.config_data = self._merge_dicts(defaults, self.config_data)
        
    def _merge_dicts(self, default: Dict, override: Dict) -> Dict:
        """Recursively merge dictionaries."""
        result = default.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = self._merge_dicts(result[key], value)
            else:
                result[key] = value
        return result
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation."""
        keys = key.split('.')
        value = self.config_data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
                
        return value
        
    def set(self, key: str, value: Any):
        """Set configuration value using dot notation."""
        keys = key.split('.')
        config = self.config_data
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
            
        config[keys[-1]] = value
        
    def save_config(self):
        """Save current configuration to file."""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                yaml.dump(self.config_data, f, default_flow_style=False)
        except Exception as e:
            print(f"Warning: Could not save config file: {e}")
    
    # Convenience properties
    @property
    def enable_voice(self) -> bool:
        return self.get('enable_voice', True)
        
    @property
    def enable_text(self) -> bool:
        return self.get('enable_text', True)
        
    @property
    def enable_gui(self) -> bool:
        return self.get('enable_gui', True)
        
    @property
    def offline_mode(self) -> bool:
        return self.get('system.offline_mode', True)
        
    @property
    def data_dir(self) -> Path:
        return self.project_root / self.get('paths.data_dir', 'data')
        
    @property
    def logs_dir(self) -> Path:
        return self.project_root / self.get('paths.logs_dir', 'data/logs')
        
    @property
    def models_dir(self) -> Path:
        return self.project_root / self.get('paths.models_dir', 'data/models')
        
    @property
    def knowledge_dir(self) -> Path:
        return self.project_root / self.get('paths.knowledge_dir', 'data/knowledge')
