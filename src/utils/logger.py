"""
Logging utilities for Space AI Assistant.
"""

import logging
import logging.handlers
import os
from pathlib import Path
from datetime import datetime
from typing import Optional

def setup_logger(name: str, log_level: str = "INFO", log_dir: Optional[Path] = None) -> logging.Logger:
    """
    Set up a logger with both file and console handlers.
    
    Args:
        name: Logger name
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
    )
    simple_formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler
    if log_dir is None:
        log_dir = Path(__file__).parent.parent.parent / "data" / "logs"
    
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Create rotating file handler
    log_file = log_dir / f"{name.lower()}.log"
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(detailed_formatter)
    logger.addHandler(file_handler)
    
    # Mission critical log handler (separate file for important events)
    critical_log_file = log_dir / f"{name.lower()}_critical.log"
    critical_handler = logging.handlers.RotatingFileHandler(
        critical_log_file,
        maxBytes=5*1024*1024,  # 5MB
        backupCount=10
    )
    critical_handler.setLevel(logging.WARNING)
    critical_handler.setFormatter(detailed_formatter)
    logger.addHandler(critical_handler)
    
    return logger

class MissionLogger:
    """Specialized logger for mission-critical events and astronaut logs."""
    
    def __init__(self, log_dir: Optional[Path] = None):
        self.log_dir = log_dir or Path(__file__).parent.parent.parent / "data" / "logs"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.mission_log_file = self.log_dir / "mission_log.txt"
        
    def log_mission_event(self, event: str, category: str = "GENERAL", priority: str = "INFO"):
        """
        Log a mission event with timestamp.
        
        Args:
            event: Description of the event
            category: Event category (SYSTEM, ASTRONAUT, EMERGENCY, etc.)
            priority: Priority level (INFO, WARNING, CRITICAL)
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        log_entry = f"[{timestamp}] [{priority}] [{category}] {event}\n"
        
        try:
            with open(self.mission_log_file, 'a', encoding='utf-8') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Failed to write mission log: {e}")
    
    def log_astronaut_note(self, note: str, astronaut_id: str = "CREW"):
        """Log an astronaut's note or observation."""
        self.log_mission_event(
            f"{astronaut_id}: {note}",
            category="ASTRONAUT_LOG",
            priority="INFO"
        )
    
    def log_system_status(self, system: str, status: str, details: str = ""):
        """Log system status update."""
        event = f"{system} status: {status}"
        if details:
            event += f" - {details}"
        self.log_mission_event(event, category="SYSTEM", priority="INFO")
    
    def log_emergency(self, emergency_type: str, details: str, response_taken: str = ""):
        """Log emergency event."""
        event = f"EMERGENCY: {emergency_type} - {details}"
        if response_taken:
            event += f" - Response: {response_taken}"
        self.log_mission_event(event, category="EMERGENCY", priority="CRITICAL")
    
    def get_recent_logs(self, lines: int = 50) -> list:
        """Get recent mission log entries."""
        try:
            with open(self.mission_log_file, 'r', encoding='utf-8') as f:
                all_lines = f.readlines()
                return all_lines[-lines:] if len(all_lines) > lines else all_lines
        except FileNotFoundError:
            return []
        except Exception as e:
            print(f"Failed to read mission log: {e}")
            return []
