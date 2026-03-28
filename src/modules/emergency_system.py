"""
Emergency System for Space AI Assistant.
Handles emergency procedures, alerts, and critical situation management.
"""

import logging
import threading
import time
import json
from typing import Dict, List, Any, Optional
from datetime import datetime
from pathlib import Path
import sqlite3

class EmergencySystem:
    """Emergency response and procedure management system."""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("Emergency_System")
        
        # Emergency state
        self.emergency_active = False
        self.current_emergency = None
        self.emergency_log = []
        
        # Database setup
        self.db_path = config.knowledge_dir / "emergency_system.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._initialize_database()
        
        # Load emergency procedures
        self.emergency_procedures = self._load_emergency_procedures()
        
        # Emergency contacts and protocols
        self.emergency_contacts = {
            'mission_control': 'Houston Mission Control',
            'medical': 'Flight Surgeon',
            'commander': 'ISS Commander',
            'ground_support': 'Ground Support Team'
        }
    
    def _initialize_database(self):
        """Initialize emergency system database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Emergency incidents table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS emergency_incidents (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        incident_type TEXT NOT NULL,
                        severity TEXT NOT NULL,
                        start_time TEXT NOT NULL,
                        end_time TEXT,
                        status TEXT DEFAULT 'active',
                        description TEXT,
                        actions_taken TEXT,
                        outcome TEXT
                    )
                ''')
                
                # Emergency actions log
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS emergency_actions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        incident_id INTEGER,
                        timestamp TEXT NOT NULL,
                        action_type TEXT NOT NULL,
                        description TEXT NOT NULL,
                        success BOOLEAN DEFAULT 1,
                        FOREIGN KEY (incident_id) REFERENCES emergency_incidents (id)
                    )
                ''')
                
                conn.commit()
                self.logger.info("Emergency system database initialized")
                
        except Exception as e:
            self.logger.error(f"Emergency database initialization failed: {e}")
            raise
    
    def _load_emergency_procedures(self) -> Dict[str, Dict]:
        """Load emergency procedures and protocols."""
        return {
            'fire': {
                'severity': 'critical',
                'immediate_actions': [
                    'Sound general alarm',
                    'Don breathing apparatus immediately',
                    'Isolate electrical power to affected area',
                    'Use appropriate fire extinguisher (CO2 for electrical)',
                    'Evacuate affected compartment if necessary'
                ],
                'detailed_procedure': {
                    'assessment': 'Identify fire type and location',
                    'suppression': 'Use CO2 extinguisher for electrical fires, water for combustibles',
                    'ventilation': 'Activate smoke evacuation if safe',
                    'monitoring': 'Watch for re-ignition, monitor air quality',
                    'communication': 'Maintain contact with all crew and ground'
                },
                'equipment_needed': ['Fire extinguisher', 'Breathing apparatus', 'Emergency lighting'],
                'time_critical': True,
                'max_response_time': 60  # seconds
            },
            
            'depressurization': {
                'severity': 'critical',
                'immediate_actions': [
                    'Don emergency oxygen masks immediately',
                    'Locate source of pressure loss',
                    'Apply emergency patch if breach is accessible',
                    'Isolate affected compartment',
                    'Monitor pressure levels continuously'
                ],
                'detailed_procedure': {
                    'detection': 'Confirm pressure drop rate and location',
                    'isolation': 'Close hatches to isolate breach',
                    'repair': 'Apply temporary patch or permanent repair',
                    'monitoring': 'Continuous pressure and leak monitoring',
                    'eva_prep': 'Prepare for EVA if external repair needed'
                },
                'equipment_needed': ['Emergency oxygen', 'Patch kit', 'Pressure suits', 'Leak detection equipment'],
                'time_critical': True,
                'max_response_time': 30  # seconds
            },
            
            'medical_emergency': {
                'severity': 'high',
                'immediate_actions': [
                    'Ensure scene safety',
                    'Check patient responsiveness and breathing',
                    'Call for medical assistance from ground',
                    'Begin appropriate first aid',
                    'Prepare medical equipment'
                ],
                'detailed_procedure': {
                    'assessment': 'Primary and secondary patient assessment',
                    'treatment': 'Administer appropriate medical care',
                    'monitoring': 'Continuous vital signs monitoring',
                    'communication': 'Maintain contact with flight surgeon',
                    'evacuation': 'Prepare for emergency return if necessary'
                },
                'equipment_needed': ['Medical kit', 'Defibrillator', 'Medications', 'Monitoring equipment'],
                'time_critical': True,
                'max_response_time': 120  # seconds
            },
            
            'power_failure': {
                'severity': 'high',
                'immediate_actions': [
                    'Switch to backup power systems',
                    'Check critical system status',
                    'Reduce non-essential power consumption',
                    'Diagnose main power failure cause',
                    'Implement power conservation measures'
                ],
                'detailed_procedure': {
                    'backup_activation': 'Ensure backup systems are operational',
                    'load_management': 'Prioritize critical systems',
                    'diagnosis': 'Identify and isolate fault',
                    'repair': 'Attempt repair if safe and possible',
                    'monitoring': 'Monitor battery levels and consumption'
                },
                'equipment_needed': ['Backup batteries', 'Diagnostic tools', 'Repair equipment'],
                'time_critical': False,
                'max_response_time': 300  # seconds
            },
            
            'communication_loss': {
                'severity': 'medium',
                'immediate_actions': [
                    'Check all communication equipment',
                    'Verify antenna positioning',
                    'Switch to backup communication systems',
                    'Try different frequencies',
                    'Implement communication schedule'
                ],
                'detailed_procedure': {
                    'equipment_check': 'Verify all connections and settings',
                    'antenna_adjustment': 'Reposition antennas if possible',
                    'frequency_scan': 'Try all available frequencies',
                    'backup_systems': 'Activate secondary communication',
                    'schedule': 'Implement predetermined communication windows'
                },
                'equipment_needed': ['Backup radio', 'Antenna controls', 'Frequency guides'],
                'time_critical': False,
                'max_response_time': 600  # seconds
            },
            
            'radiation_exposure': {
                'severity': 'high',
                'immediate_actions': [
                    'Move to most shielded area immediately',
                    'Monitor radiation levels continuously',
                    'Check personal dosimeters',
                    'Cancel all non-essential EVAs',
                    'Contact medical for guidance'
                ],
                'detailed_procedure': {
                    'shelter': 'Move to designated radiation shelter',
                    'monitoring': 'Continuous radiation level monitoring',
                    'exposure_tracking': 'Document all crew exposure levels',
                    'medical_consultation': 'Consult with radiation health officer',
                    'activity_restriction': 'Limit exposure activities'
                },
                'equipment_needed': ['Radiation detectors', 'Dosimeters', 'Shielding materials'],
                'time_critical': True,
                'max_response_time': 180  # seconds
            }
        }
    
    def handle_emergency(self, nlu_result: Dict, context: Dict = None) -> Dict[str, Any]:
        """Handle emergency situations and procedures."""
        try:
            query_text = nlu_result.get('processed_text', '')
            
            # Identify emergency type
            emergency_type = self._identify_emergency_type(query_text)
            
            if emergency_type == 'activate_emergency_mode':
                return self._activate_emergency_mode()
            elif emergency_type == 'deactivate_emergency_mode':
                return self._deactivate_emergency_mode()
            elif emergency_type in self.emergency_procedures:
                return self._handle_specific_emergency(emergency_type, query_text)
            elif emergency_type == 'status':
                return self._get_emergency_status()
            else:
                return self._provide_general_emergency_info(query_text)
                
        except Exception as e:
            self.logger.error(f"Emergency handling error: {e}")
            return {
                'message': f"Emergency system error: {str(e)}",
                'emergency_type': 'system_error',
                'success': False
            }
    
    def _identify_emergency_type(self, query_text: str) -> str:
        """Identify the type of emergency from query text."""
        query_lower = query_text.lower()
        
        # Check for emergency mode activation/deactivation
        if any(phrase in query_lower for phrase in ['emergency mode', 'activate emergency', 'emergency activated']):
            return 'activate_emergency_mode'
        elif any(phrase in query_lower for phrase in ['deactivate emergency', 'emergency off', 'cancel emergency']):
            return 'deactivate_emergency_mode'
        elif any(phrase in query_lower for phrase in ['emergency status', 'emergency state']):
            return 'status'
        
        # Check for specific emergency types
        emergency_keywords = {
            'fire': ['fire', 'smoke', 'burning', 'flames'],
            'depressurization': ['depressurization', 'pressure loss', 'leak', 'breach', 'hole'],
            'medical_emergency': ['medical', 'injury', 'sick', 'unconscious', 'heart attack', 'breathing'],
            'power_failure': ['power failure', 'power loss', 'electrical failure', 'blackout'],
            'communication_loss': ['communication loss', 'radio failure', 'contact lost', 'no signal'],
            'radiation_exposure': ['radiation', 'solar storm', 'cosmic rays', 'radiation alert']
        }
        
        for emergency_type, keywords in emergency_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                return emergency_type
        
        return 'general'
    
    def _activate_emergency_mode(self) -> Dict[str, Any]:
        """Activate emergency mode."""
        if self.emergency_active:
            return {
                'message': '🚨 Emergency mode is already active.',
                'emergency_type': 'mode_activation',
                'success': True
            }
        
        self.emergency_active = True
        self.current_emergency = {
            'start_time': datetime.now(),
            'type': 'general',
            'status': 'active'
        }
        
        # Log emergency activation
        self._log_emergency_action('emergency_mode_activated', 'Emergency mode activated by crew request')
        
        message = """🚨 EMERGENCY MODE ACTIVATED 🚨

All systems are now in emergency configuration:
• Priority given to life support systems
• Non-essential systems may be powered down
• Enhanced monitoring active
• Direct communication with mission control established

Available emergency procedures:
• Fire suppression
• Depressurization response
• Medical emergency
• Power failure response
• Communication backup
• Radiation protection

Say "emergency [type]" for specific procedures or "emergency status" for current state."""
        
        return {
            'message': message,
            'emergency_type': 'mode_activation',
            'success': True,
            'priority': 'high'
        }
    
    def _deactivate_emergency_mode(self) -> Dict[str, Any]:
        """Deactivate emergency mode."""
        if not self.emergency_active:
            return {
                'message': 'Emergency mode is not currently active.',
                'emergency_type': 'mode_deactivation',
                'success': True
            }
        
        self.emergency_active = False
        
        # Log emergency deactivation
        self._log_emergency_action('emergency_mode_deactivated', 'Emergency mode deactivated - situation resolved')
        
        if self.current_emergency:
            self.current_emergency['end_time'] = datetime.now()
            self.current_emergency['status'] = 'resolved'
        
        message = """✅ Emergency mode deactivated.

All systems returning to normal operation:
• Standard system priorities restored
• Normal power management resumed
• Routine monitoring active
• Standard communication protocols

Emergency systems remain on standby. Say "emergency" to reactivate if needed."""
        
        return {
            'message': message,
            'emergency_type': 'mode_deactivation',
            'success': True
        }
    
    def _handle_specific_emergency(self, emergency_type: str, query_text: str) -> Dict[str, Any]:
        """Handle a specific type of emergency."""
        procedure = self.emergency_procedures[emergency_type]
        
        # Activate emergency mode if not already active
        if not self.emergency_active:
            self.emergency_active = True
        
        # Create emergency incident record
        incident_id = self._create_emergency_incident(emergency_type, procedure['severity'])
        
        # Format emergency response
        message = f"🚨 {emergency_type.upper().replace('_', ' ')} EMERGENCY PROTOCOL\n"
        message += f"Severity: {procedure['severity'].upper()}\n\n"
        
        if procedure['time_critical']:
            message += f"⚠️ TIME CRITICAL - Maximum response time: {procedure['max_response_time']} seconds\n\n"
        
        message += "IMMEDIATE ACTIONS:\n"
        for i, action in enumerate(procedure['immediate_actions'], 1):
            message += f"{i}. {action}\n"
        
        message += f"\nEQUIPMENT NEEDED: {', '.join(procedure['equipment_needed'])}\n"
        
        message += "\nSay 'emergency details' for detailed procedure or 'emergency complete' when resolved."
        
        # Log emergency start
        self._log_emergency_action('emergency_started', f'{emergency_type} emergency protocol initiated', incident_id)
        
        return {
            'message': message,
            'emergency_type': emergency_type,
            'success': True,
            'priority': 'high',
            'incident_id': incident_id,
            'time_critical': procedure['time_critical']
        }
    
    def _get_emergency_status(self) -> Dict[str, Any]:
        """Get current emergency system status."""
        if not self.emergency_active:
            message = "✅ No active emergencies. All systems normal.\n"
            message += "Emergency systems on standby."
        else:
            message = "🚨 EMERGENCY MODE ACTIVE\n"
            if self.current_emergency:
                start_time = self.current_emergency['start_time']
                duration = datetime.now() - start_time
                message += f"Duration: {duration.total_seconds():.0f} seconds\n"
                message += f"Type: {self.current_emergency.get('type', 'General')}\n"
            
            message += "\nAvailable emergency procedures:\n"
            for emergency_type in self.emergency_procedures.keys():
                message += f"• {emergency_type.replace('_', ' ').title()}\n"
        
        return {
            'message': message,
            'emergency_type': 'status',
            'success': True,
            'emergency_active': self.emergency_active
        }
    
    def _provide_general_emergency_info(self, query_text: str) -> Dict[str, Any]:
        """Provide general emergency information."""
        message = """🚨 EMERGENCY ASSISTANCE AVAILABLE

Available emergency procedures:
• Fire suppression and smoke evacuation
• Depressurization and breach response
• Medical emergency and first aid
• Power failure and backup systems
• Communication loss recovery
• Radiation exposure protection

To activate specific emergency procedure, say:
"Emergency [type]" (e.g., "Emergency fire", "Emergency medical")

For immediate emergency mode activation, say:
"Activate emergency mode"

⚠️ In case of immediate life-threatening emergency:
1. Ensure personal safety first
2. Alert all crew members
3. Contact mission control immediately
4. Follow trained emergency procedures

Remember: Stay calm, follow procedures, communicate clearly."""
        
        return {
            'message': message,
            'emergency_type': 'general_info',
            'success': True
        }
    
    def _create_emergency_incident(self, emergency_type: str, severity: str) -> int:
        """Create a new emergency incident record."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO emergency_incidents 
                    (incident_type, severity, start_time, description)
                    VALUES (?, ?, ?, ?)
                ''', (
                    emergency_type,
                    severity,
                    datetime.now().isoformat(),
                    f'{emergency_type} emergency initiated'
                ))
                
                incident_id = cursor.lastrowid
                conn.commit()
                
                self.logger.critical(f"Emergency incident created: {emergency_type} (ID: {incident_id})")
                return incident_id
                
        except Exception as e:
            self.logger.error(f"Error creating emergency incident: {e}")
            return 0
    
    def _log_emergency_action(self, action_type: str, description: str, incident_id: int = None):
        """Log an emergency action."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO emergency_actions
                    (incident_id, timestamp, action_type, description)
                    VALUES (?, ?, ?, ?)
                ''', (
                    incident_id,
                    datetime.now().isoformat(),
                    action_type,
                    description
                ))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Error logging emergency action: {e}")
    
    def get_emergency_history(self, limit: int = 10) -> List[Dict]:
        """Get recent emergency incident history."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT incident_type, severity, start_time, end_time, status, description
                    FROM emergency_incidents
                    ORDER BY start_time DESC LIMIT ?
                ''', (limit,))
                
                columns = ['incident_type', 'severity', 'start_time', 'end_time', 'status', 'description']
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
                
        except Exception as e:
            self.logger.error(f"Error getting emergency history: {e}")
            return []
    
    def is_emergency_active(self) -> bool:
        """Check if emergency mode is currently active."""
        return self.emergency_active
    
    def get_emergency_contacts(self) -> Dict[str, str]:
        """Get emergency contact information."""
        return self.emergency_contacts.copy()
    
    def shutdown(self):
        """Shutdown emergency system."""
        if self.emergency_active:
            self.logger.warning("Emergency system shutting down while emergency mode active")
            self._log_emergency_action('system_shutdown', 'Emergency system shutdown during active emergency')
        
        self.logger.info("Emergency system shutdown")
