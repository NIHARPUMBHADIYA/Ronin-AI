"""
Mission Support module for Space AI Assistant.
Handles reminders, checklists, logging, and mission management features.
"""

import json
import logging
import threading
import time
try:
    import schedule
    SCHEDULE_AVAILABLE = True
except ImportError:
    SCHEDULE_AVAILABLE = False
from typing import Dict, List, Any, Optional
from pathlib import Path
from datetime import datetime, timedelta
import sqlite3

class MissionSupport:
    """Mission support system for astronaut assistance."""
    
    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger("Mission_Support")
        
        # Database setup
        self.db_path = config.knowledge_dir / "mission_support.db"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Initialize database
        self._initialize_database()
        
        # Scheduler for reminders
        self.scheduler_thread = None
        self.scheduler_running = False
        
        # Load checklists
        self.checklists = self._load_checklists()
        
        # Start reminder scheduler if available
        if SCHEDULE_AVAILABLE:
            self._start_reminder_scheduler()
        
    def _start_reminder_scheduler(self):
        """Start the reminder scheduler thread."""
        if not SCHEDULE_AVAILABLE:
            return
            
        self.scheduler_running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        self.logger.info("Reminder scheduler started")
    
    def _initialize_database(self):
        """Initialize SQLite database for mission support."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Reminders table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS reminders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        description TEXT,
                        due_time TEXT NOT NULL,
                        priority TEXT DEFAULT 'medium',
                        status TEXT DEFAULT 'pending',
                        created_time TEXT NOT NULL,
                        completed_time TEXT
                    )
                ''')
                
                # Mission logs table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS mission_logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        timestamp TEXT NOT NULL,
                        category TEXT NOT NULL,
                        content TEXT NOT NULL,
                        priority TEXT DEFAULT 'info',
                        astronaut_id TEXT DEFAULT 'CREW'
                    )
                ''')
                
                # Checklist progress table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS checklist_progress (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        checklist_name TEXT NOT NULL,
                        step_id TEXT NOT NULL,
                        status TEXT DEFAULT 'pending',
                        completed_time TEXT,
                        notes TEXT
                    )
                ''')
                
                conn.commit()
                self.logger.info("Mission support database initialized")
                
        except Exception as e:
            self.logger.error(f"Database initialization failed: {e}")
            raise
    
    def _load_checklists(self) -> Dict[str, Dict]:
        """Load mission checklists from configuration."""
        return {
            'eva_preparation': {
                'name': 'EVA Preparation Checklist',
                'description': 'Pre-EVA preparation procedures',
                'steps': [
                    {'id': 'eva_001', 'title': 'Review EVA timeline and objectives', 'critical': True},
                    {'id': 'eva_002', 'title': 'Check weather conditions and debris forecast', 'critical': True},
                    {'id': 'eva_003', 'title': 'Verify EMU suit integrity and functionality', 'critical': True},
                    {'id': 'eva_004', 'title': 'Test communication systems', 'critical': True},
                    {'id': 'eva_005', 'title': 'Pre-breathe pure oxygen for 2 hours', 'critical': True},
                    {'id': 'eva_006', 'title': 'Final suit leak check', 'critical': True},
                    {'id': 'eva_007', 'title': 'Tool and equipment verification', 'critical': False},
                    {'id': 'eva_008', 'title': 'Coordinate with mission control', 'critical': True}
                ]
            },
            'docking_procedure': {
                'name': 'Spacecraft Docking Checklist',
                'description': 'Automated and manual docking procedures',
                'steps': [
                    {'id': 'dock_001', 'title': 'Verify approach trajectory and velocity', 'critical': True},
                    {'id': 'dock_002', 'title': 'Activate docking sensors and cameras', 'critical': True},
                    {'id': 'dock_003', 'title': 'Confirm docking port alignment', 'critical': True},
                    {'id': 'dock_004', 'title': 'Monitor relative velocity (<0.1 m/s)', 'critical': True},
                    {'id': 'dock_005', 'title': 'Engage soft capture mechanisms', 'critical': True},
                    {'id': 'dock_006', 'title': 'Verify hard mate completion', 'critical': True},
                    {'id': 'dock_007', 'title': 'Pressurize vestibule', 'critical': False},
                    {'id': 'dock_008', 'title': 'Leak check docking interface', 'critical': True}
                ]
            },
            'life_support_check': {
                'name': 'Life Support Systems Check',
                'description': 'Daily life support systems verification',
                'steps': [
                    {'id': 'ls_001', 'title': 'Check oxygen levels (>21%)', 'critical': True},
                    {'id': 'ls_002', 'title': 'Verify CO2 scrubber functionality', 'critical': True},
                    {'id': 'ls_003', 'title': 'Monitor cabin pressure (14.7 psi)', 'critical': True},
                    {'id': 'ls_004', 'title': 'Check temperature control (18-24°C)', 'critical': False},
                    {'id': 'ls_005', 'title': 'Verify water recovery system', 'critical': False},
                    {'id': 'ls_006', 'title': 'Test emergency oxygen supply', 'critical': True},
                    {'id': 'ls_007', 'title': 'Check air circulation fans', 'critical': False}
                ]
            },
            'emergency_evacuation': {
                'name': 'Emergency Evacuation Procedure',
                'description': 'Emergency evacuation from ISS to Soyuz',
                'steps': [
                    {'id': 'evac_001', 'title': 'Sound general alarm', 'critical': True},
                    {'id': 'evac_002', 'title': 'Don emergency breathing apparatus', 'critical': True},
                    {'id': 'evac_003', 'title': 'Secure critical systems', 'critical': True},
                    {'id': 'evac_004', 'title': 'Gather emergency supplies', 'critical': False},
                    {'id': 'evac_005', 'title': 'Proceed to Soyuz spacecraft', 'critical': True},
                    {'id': 'evac_006', 'title': 'Seal hatches behind crew', 'critical': True},
                    {'id': 'evac_007', 'title': 'Prepare Soyuz for undocking', 'critical': True},
                    {'id': 'evac_008', 'title': 'Contact mission control', 'critical': True}
                ]
            }
        }
    
    def handle_reminder(self, nlu_result: Dict, context: Dict = None) -> Dict[str, Any]:
        """Handle reminder creation and management."""
        try:
            query_text = nlu_result.get('processed_text', '')
            entities = nlu_result.get('entities', {})
            
            # Extract reminder details
            reminder_text = self._extract_reminder_text(query_text)
            due_time = self._extract_time(query_text, entities)
            priority = self._extract_priority(query_text)
            
            if not reminder_text:
                return {
                    'message': "Please specify what you'd like me to remind you about.",
                    'success': False
                }
            
            if not due_time:
                return {
                    'message': "Please specify when you'd like to be reminded (e.g., 'in 30 minutes', 'at 14:30').",
                    'success': False
                }
            
            # Create reminder
            reminder_id = self._create_reminder(reminder_text, due_time, priority)
            
            # Format response
            time_str = self._format_time(due_time)
            message = f"✅ Reminder set: '{reminder_text}' for {time_str}"
            
            return {
                'message': message,
                'success': True,
                'reminder_id': reminder_id,
                'due_time': due_time
            }
            
        except Exception as e:
            self.logger.error(f"Reminder handling error: {e}")
            return {
                'message': f"Error setting reminder: {str(e)}",
                'success': False
            }
    
    def handle_checklist(self, nlu_result: Dict, context: Dict = None) -> Dict[str, Any]:
        """Handle checklist operations."""
        try:
            query_text = nlu_result.get('processed_text', '')
            
            # Determine operation type
            if any(word in query_text for word in ['show', 'display', 'what', 'list']):
                return self._show_checklist(query_text)
            elif any(word in query_text for word in ['complete', 'done', 'finished', 'check off']):
                return self._complete_checklist_step(query_text)
            elif any(word in query_text for word in ['next', 'continue']):
                return self._get_next_step(query_text)
            elif any(word in query_text for word in ['reset', 'restart']):
                return self._reset_checklist(query_text)
            else:
                return self._list_available_checklists()
                
        except Exception as e:
            self.logger.error(f"Checklist handling error: {e}")
            return {
                'message': f"Error with checklist: {str(e)}",
                'success': False
            }
    
    def handle_logging(self, nlu_result: Dict, context: Dict = None) -> Dict[str, Any]:
        """Handle mission logging operations."""
        try:
            query_text = nlu_result.get('processed_text', '')
            
            # Extract log content
            log_content = self._extract_log_content(query_text)
            category = self._extract_log_category(query_text)
            priority = self._extract_priority(query_text)
            
            if not log_content:
                return {
                    'message': "Please specify what you'd like to log.",
                    'success': False
                }
            
            # Create log entry
            log_id = self._create_log_entry(log_content, category, priority)
            
            message = f"📝 Logged: {log_content}"
            
            return {
                'message': message,
                'success': True,
                'log_id': log_id,
                'logged_text': log_content
            }
            
        except Exception as e:
            self.logger.error(f"Logging error: {e}")
            return {
                'message': f"Error logging entry: {str(e)}",
                'success': False
            }
    
    def _extract_reminder_text(self, query_text: str) -> str:
        """Extract reminder text from query."""
        # Remove common reminder phrases
        text = query_text
        for phrase in ['remind me to', 'remind me', 'set reminder', 'alert me']:
            text = text.replace(phrase, '').strip()
        
        # Remove time expressions
        import re
        text = re.sub(r'\b(in|at|after)\s+\d+\s+(minutes?|hours?|days?)', '', text)
        text = re.sub(r'\b(at\s+)?\d{1,2}:\d{2}', '', text)
        
        return text.strip()
    
    def _extract_time(self, query_text: str, entities: Dict) -> Optional[datetime]:
        """Extract time from query text."""
        import re
        
        # Check entities first
        if 'time' in entities:
            time_entity = entities['time'][0]['value']
            return self._parse_time_entity(time_entity)
        
        # Look for relative time expressions
        relative_match = re.search(r'\b(in|after)\s+(\d+)\s+(minutes?|hours?|days?)', query_text)
        if relative_match:
            amount = int(relative_match.group(2))
            unit = relative_match.group(3).rstrip('s')  # Remove plural 's'
            
            now = datetime.now()
            if unit == 'minute':
                return now + timedelta(minutes=amount)
            elif unit == 'hour':
                return now + timedelta(hours=amount)
            elif unit == 'day':
                return now + timedelta(days=amount)
        
        # Look for absolute time expressions
        time_match = re.search(r'\b(\d{1,2}):(\d{2})', query_text)
        if time_match:
            hour = int(time_match.group(1))
            minute = int(time_match.group(2))
            
            now = datetime.now()
            target_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            
            # If time has passed today, schedule for tomorrow
            if target_time <= now:
                target_time += timedelta(days=1)
            
            return target_time
        
        return None
    
    def _extract_priority(self, query_text: str) -> str:
        """Extract priority from query text."""
        if any(word in query_text for word in ['urgent', 'critical', 'important', 'high']):
            return 'high'
        elif any(word in query_text for word in ['low', 'minor']):
            return 'low'
        else:
            return 'medium'
    
    def _extract_log_content(self, query_text: str) -> str:
        """Extract log content from query."""
        # Remove log command phrases
        text = query_text
        for phrase in ['log', 'record', 'note', 'write down']:
            if text.startswith(phrase):
                text = text[len(phrase):].strip()
                if text.startswith(':'):
                    text = text[1:].strip()
                break
        
        return text
    
    def _extract_log_category(self, query_text: str) -> str:
        """Extract log category from query."""
        if any(word in query_text for word in ['oxygen', 'pressure', 'temperature', 'life support']):
            return 'LIFE_SUPPORT'
        elif any(word in query_text for word in ['fuel', 'power', 'battery', 'energy']):
            return 'POWER_SYSTEMS'
        elif any(word in query_text for word in ['navigation', 'position', 'orbit']):
            return 'NAVIGATION'
        elif any(word in query_text for word in ['communication', 'radio', 'contact']):
            return 'COMMUNICATION'
        elif any(word in query_text for word in ['experiment', 'research', 'science']):
            return 'SCIENCE'
        else:
            return 'GENERAL'
    
    def _create_reminder(self, text: str, due_time: datetime, priority: str) -> int:
        """Create a new reminder in the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO reminders (title, due_time, priority, created_time)
                    VALUES (?, ?, ?, ?)
                ''', (text, due_time.isoformat(), priority, datetime.now().isoformat()))
                
                reminder_id = cursor.lastrowid
                conn.commit()
                
                self.logger.info(f"Reminder created: {text} at {due_time}")
                return reminder_id
                
        except Exception as e:
            self.logger.error(f"Error creating reminder: {e}")
            raise
    
    def _create_log_entry(self, content: str, category: str, priority: str) -> int:
        """Create a new log entry in the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO mission_logs (timestamp, category, content, priority)
                    VALUES (?, ?, ?, ?)
                ''', (datetime.now().isoformat(), category, content, priority))
                
                log_id = cursor.lastrowid
                conn.commit()
                
                self.logger.info(f"Log entry created: {content}")
                return log_id
                
        except Exception as e:
            self.logger.error(f"Error creating log entry: {e}")
            raise
    
    def _show_checklist(self, query_text: str) -> Dict[str, Any]:
        """Show a specific checklist."""
        checklist_name = self._identify_checklist(query_text)
        
        if checklist_name not in self.checklists:
            return {
                'message': f"Checklist '{checklist_name}' not found. Available checklists: {', '.join(self.checklists.keys())}",
                'success': False
            }
        
        checklist = self.checklists[checklist_name]
        progress = self._get_checklist_progress(checklist_name)
        
        message = f"📋 {checklist['name']}\n"
        message += f"Description: {checklist['description']}\n\n"
        
        for step in checklist['steps']:
            step_id = step['id']
            status = progress.get(step_id, 'pending')
            
            if status == 'completed':
                icon = "✅"
            elif step['critical']:
                icon = "🔴"
            else:
                icon = "⚪"
            
            message += f"{icon} {step['title']}\n"
        
        return {
            'message': message,
            'success': True,
            'checklist_name': checklist_name,
            'progress': progress
        }
    
    def _complete_checklist_step(self, query_text: str) -> Dict[str, Any]:
        """Mark a checklist step as complete."""
        checklist_name = self._identify_checklist(query_text)
        
        if checklist_name not in self.checklists:
            return {
                'message': "Please specify which checklist you're working on.",
                'success': False
            }
        
        # For now, mark the next pending step as complete
        next_step = self._get_next_pending_step(checklist_name)
        
        if not next_step:
            return {
                'message': f"All steps in {checklist_name} checklist are already complete!",
                'success': True
            }
        
        self._mark_step_complete(checklist_name, next_step['id'])
        
        message = f"✅ Completed: {next_step['title']}"
        
        # Check if checklist is now complete
        if self._is_checklist_complete(checklist_name):
            message += f"\n🎉 {checklist_name} checklist is now complete!"
        
        return {
            'message': message,
            'success': True,
            'completed_step': next_step
        }
    
    def _get_next_step(self, query_text: str) -> Dict[str, Any]:
        """Get the next step in a checklist."""
        checklist_name = self._identify_checklist(query_text)
        
        if checklist_name not in self.checklists:
            return {
                'message': "Please specify which checklist you're working on.",
                'success': False
            }
        
        next_step = self._get_next_pending_step(checklist_name)
        
        if not next_step:
            return {
                'message': f"All steps in {checklist_name} checklist are complete!",
                'success': True
            }
        
        critical_indicator = " (CRITICAL)" if next_step['critical'] else ""
        message = f"📋 Next step: {next_step['title']}{critical_indicator}"
        
        return {
            'message': message,
            'success': True,
            'next_step': next_step
        }
    
    def _list_available_checklists(self) -> Dict[str, Any]:
        """List all available checklists."""
        message = "📋 Available Checklists:\n"
        
        for name, checklist in self.checklists.items():
            progress = self._get_checklist_progress(name)
            total_steps = len(checklist['steps'])
            completed_steps = len([s for s in progress.values() if s == 'completed'])
            
            message += f"• {checklist['name']} ({completed_steps}/{total_steps} complete)\n"
        
        return {
            'message': message,
            'success': True,
            'checklists': list(self.checklists.keys())
        }
    
    def _identify_checklist(self, query_text: str) -> str:
        """Identify which checklist is being referenced."""
        for name, checklist in self.checklists.items():
            if name.replace('_', ' ') in query_text.lower():
                return name
            if any(word in query_text.lower() for word in name.split('_')):
                return name
        
        # Default to EVA if no specific checklist identified
        return 'eva_preparation'
    
    def _get_checklist_progress(self, checklist_name: str) -> Dict[str, str]:
        """Get progress for a specific checklist."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT step_id, status FROM checklist_progress
                    WHERE checklist_name = ?
                ''', (checklist_name,))
                
                return {row[0]: row[1] for row in cursor.fetchall()}
                
        except Exception as e:
            self.logger.error(f"Error getting checklist progress: {e}")
            return {}
    
    def _get_next_pending_step(self, checklist_name: str) -> Optional[Dict]:
        """Get the next pending step in a checklist."""
        if checklist_name not in self.checklists:
            return None
        
        progress = self._get_checklist_progress(checklist_name)
        
        for step in self.checklists[checklist_name]['steps']:
            if progress.get(step['id'], 'pending') == 'pending':
                return step
        
        return None
    
    def _mark_step_complete(self, checklist_name: str, step_id: str):
        """Mark a checklist step as complete."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR REPLACE INTO checklist_progress
                    (checklist_name, step_id, status, completed_time)
                    VALUES (?, ?, 'completed', ?)
                ''', (checklist_name, step_id, datetime.now().isoformat()))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Error marking step complete: {e}")
    
    def _is_checklist_complete(self, checklist_name: str) -> bool:
        """Check if a checklist is complete."""
        if checklist_name not in self.checklists:
            return False
        
        progress = self._get_checklist_progress(checklist_name)
        total_steps = len(self.checklists[checklist_name]['steps'])
        completed_steps = len([s for s in progress.values() if s == 'completed'])
        
        return completed_steps == total_steps
    
    def _format_time(self, dt: datetime) -> str:
        """Format datetime for display."""
        now = datetime.now()
        diff = dt - now
        
        if diff.total_seconds() < 3600:  # Less than 1 hour
            minutes = int(diff.total_seconds() / 60)
            return f"in {minutes} minutes"
        elif diff.total_seconds() < 86400:  # Less than 1 day
            hours = int(diff.total_seconds() / 3600)
            return f"in {hours} hours"
        else:
            return dt.strftime("%Y-%m-%d %H:%M")
    
    def _parse_time_entity(self, time_str: str) -> Optional[datetime]:
        """Parse time entity string."""
        # This would need more sophisticated parsing
        # For now, return None to fall back to regex parsing
        return None
    
    def _start_scheduler(self):
        """Start the reminder scheduler."""
        self.scheduler_running = True
        self.scheduler_thread = threading.Thread(target=self._scheduler_loop, daemon=True)
        self.scheduler_thread.start()
        self.logger.info("Reminder scheduler started")
    
    def _scheduler_loop(self):
        """Main scheduler loop."""
        while self.scheduler_running:
            try:
                self._check_due_reminders()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                self.logger.error(f"Scheduler error: {e}")
                time.sleep(60)  # Wait longer on error
    
    def _check_due_reminders(self):
        """Check for due reminders and trigger them."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                now = datetime.now().isoformat()
                
                cursor.execute('''
                    SELECT id, title, due_time, priority FROM reminders
                    WHERE status = 'pending' AND due_time <= ?
                ''', (now,))
                
                due_reminders = cursor.fetchall()
                
                for reminder in due_reminders:
                    reminder_id, title, due_time, priority = reminder
                    self._trigger_reminder(reminder_id, title, priority)
                    
                    # Mark as completed
                    cursor.execute('''
                        UPDATE reminders SET status = 'completed', completed_time = ?
                        WHERE id = ?
                    ''', (now, reminder_id))
                
                conn.commit()
                
        except Exception as e:
            self.logger.error(f"Error checking due reminders: {e}")
    
    def _trigger_reminder(self, reminder_id: int, title: str, priority: str):
        """Trigger a reminder notification."""
        self.logger.info(f"Reminder triggered: {title}")
        # In a full implementation, this would trigger audio/visual alerts
        # For now, just log it
    
    def get_recent_logs(self, limit: int = 10) -> List[Dict]:
        """Get recent mission logs."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT timestamp, category, content, priority FROM mission_logs
                    ORDER BY timestamp DESC LIMIT ?
                ''', (limit,))
                
                columns = ['timestamp', 'category', 'content', 'priority']
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
                
        except Exception as e:
            self.logger.error(f"Error getting recent logs: {e}")
            return []
    
    def shutdown(self):
        """Shutdown mission support system."""
        self.scheduler_running = False
        if self.scheduler_thread and self.scheduler_thread.is_alive():
            self.scheduler_thread.join(timeout=2)
        self.logger.info("Mission support system shutdown")
